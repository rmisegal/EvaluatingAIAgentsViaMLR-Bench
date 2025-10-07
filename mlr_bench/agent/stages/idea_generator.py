"""Idea generation agent using Google ADK."""

from google.adk.agents import Agent
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.config.prompts import IDEA_GENERATION_PROMPT


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
        self.agent = self._create_agent()
    
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
        
        # Generate idea using agent
        response = await self.agent.run(prompt)
        
        # Parse response into ResearchIdea
        # For simplicity, we'll extract from the text response
        idea_text = response.text if hasattr(response, 'text') else str(response)
        
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
