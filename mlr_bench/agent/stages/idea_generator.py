"""Idea generation agent using Google ADK."""

import uuid
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.config.prompts import IDEA_GENERATION_PROMPT
from mlr_bench.utils.retry import async_retry_on_503


class IdeaGenerator:
    """Agent for generating research ideas."""

    def __init__(self, model_name: str = "gemini-2.0-flash", temperature: float = 0.7):
        """Initialize idea generator.

        Args:
            model_name: LLM model name
            temperature: Generation temperature
        """
        self.model_name = model_name
        self.temperature = temperature
        self.app_name = "mlr_bench_idea_generator"
        self.agent = self._create_agent()
        self.runner = InMemoryRunner(agent=self.agent, app_name=self.app_name)

    def _create_agent(self) -> Agent:
        """Create ADK agent for idea generation."""
        return Agent(
            name="idea_generator",
            model=self.model_name,
            description="Agent specialized in generating novel research ideas",
            instruction=(
                "You are a creative AI research scientist. "
                "Generate novel, feasible, and impactful research ideas. "
                "Be specific about methodology and expected outcomes."
            )
        )
    
    @async_retry_on_503(max_retries=5, base_delay=2.0)
    async def generate_idea(self, task: Task) -> ResearchIdea:
        """Generate research idea for a task.

        Args:
            task: Research task

        Returns:
            Generated research idea
        """
        logger.info(f"Generating idea for task: {task.task_id}")

        # Format prompt
        prompt = IDEA_GENERATION_PROMPT.format(
            task_title=task.title,
            task_description=task.description,
            task_category=task.category
        )

        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=prompt)]
        )

        # Generate idea using agent via runner
        # Use unique session ID to avoid conflicts
        session_id = f'idea_{task.task_id}_{uuid.uuid4().hex[:8]}'
        user_id = 'mlr_bench'

        # Create session first
        await self.runner.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id
        )

        idea_text = ""
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        idea_text += part.text

        idea = self._parse_idea_response(idea_text, task)

        logger.info(f"Generated idea: {idea.title}")
        return idea
    
    def _parse_idea_response(self, response_text: str, task: Task) -> ResearchIdea:
        """Parse LLM response into ResearchIdea.
        
        Args:
            response_text: LLM response text
            task: Original task
            
        Returns:
            ResearchIdea object
        """
        # Simple parsing - extract sections
        lines = response_text.split('\n')
        
        title = ""
        motivation = ""
        main_idea = ""
        methodology = ""
        expected_outcomes = ""
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if "title:" in line.lower() or line.startswith("1."):
                current_section = "title"
                title = line.split(":", 1)[-1].strip() if ":" in line else line
            elif "motivation:" in line.lower() or line.startswith("2."):
                current_section = "motivation"
            elif "main idea:" in line.lower() or line.startswith("3."):
                current_section = "main_idea"
            elif "methodology:" in line.lower() or line.startswith("4."):
                current_section = "methodology"
            elif "expected outcomes:" in line.lower() or line.startswith("5."):
                current_section = "expected_outcomes"
            else:
                # Append to current section
                if current_section == "motivation":
                    motivation += line + " "
                elif current_section == "main_idea":
                    main_idea += line + " "
                elif current_section == "methodology":
                    methodology += line + " "
                elif current_section == "expected_outcomes":
                    expected_outcomes += line + " "
        
        # Fallback if parsing fails
        if not title:
            title = f"Research Idea for {task.title}"
        if not main_idea:
            main_idea = response_text[:500]
        
        return ResearchIdea(
            task_id=task.task_id,
            title=title.strip(),
            motivation=motivation.strip() or "Generated motivation",
            main_idea=main_idea.strip(),
            methodology=methodology.strip() or None,
            expected_outcomes=expected_outcomes.strip() or None,
            model_name=self.model_name
        )
