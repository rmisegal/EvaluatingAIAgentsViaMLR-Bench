"""Proposal writing agent using Google ADK."""

import uuid
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.literature import LiteratureReview
from mlr_bench.models.proposal import ResearchProposal
from mlr_bench.config.prompts import PROPOSAL_WRITING_PROMPT


class ProposalWriter:
    """Agent for writing research proposals."""

    def __init__(self, model_name: str = "gemini-2.0-flash", temperature: float = 0.7):
        """Initialize proposal writer.

        Args:
            model_name: LLM model name
            temperature: Generation temperature
        """
        self.model_name = model_name
        self.temperature = temperature
        self.app_name = "mlr_bench_proposal_writer"
        self.agent = self._create_agent()
        self.runner = InMemoryRunner(agent=self.agent, app_name=self.app_name)

    def _create_agent(self) -> Agent:
        """Create ADK agent for proposal writing."""
        return Agent(
            name="proposal_writer",
            model=self.model_name,
            description="Agent specialized in writing detailed research proposals",
            instruction=(
                "You are an experienced research scientist. "
                "Write clear, detailed, and rigorous research proposals "
                "suitable for top-tier ML conferences."
            )
        )
    
    async def write_proposal(
        self,
        task: Task,
        idea: ResearchIdea,
        literature: LiteratureReview
    ) -> ResearchProposal:
        """Write research proposal.
        
        Args:
            task: Research task
            idea: Research idea
            literature: Literature review
            
        Returns:
            Research proposal
        """
        logger.info(f"Writing proposal for: {idea.title}")

        # Format prompt
        prompt = PROPOSAL_WRITING_PROMPT.format(
            task_title=task.title,
            idea_title=idea.title,
            literature_summary=literature.related_work_summary
        )

        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=prompt)]
        )

        # Generate proposal using agent via runner
        session_id = f'proposal_{task.task_id}_{uuid.uuid4().hex[:8]}'
        user_id = 'mlr_bench'

        # Create session first
        await self.runner.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id
        )

        proposal_text = ""
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        proposal_text += part.text
        
        proposal = self._parse_proposal_response(proposal_text, task, idea)
        
        logger.info(f"Completed proposal: {proposal.title}")
        return proposal
    
    def _parse_proposal_response(
        self,
        response_text: str,
        task: Task,
        idea: ResearchIdea
    ) -> ResearchProposal:
        """Parse LLM response into ResearchProposal.
        
        Args:
            response_text: LLM response text
            task: Research task
            idea: Research idea
            
        Returns:
            ResearchProposal object
        """
        sections = {
            "abstract": "",
            "introduction": "",
            "related_work": "",
            "methodology": "",
            "expected_results": "",
            "experimental_plan": ""
        }
        
        current_section = None
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect section headers
            line_lower = line.lower()
            if "abstract" in line_lower and len(line) < 50:
                current_section = "abstract"
                continue
            elif "introduction" in line_lower and len(line) < 50:
                current_section = "introduction"
                continue
            elif "related work" in line_lower and len(line) < 50:
                current_section = "related_work"
                continue
            elif "methodology" in line_lower and len(line) < 50:
                current_section = "methodology"
                continue
            elif "expected results" in line_lower and len(line) < 50:
                current_section = "expected_results"
                continue
            elif "experimental plan" in line_lower and len(line) < 50:
                current_section = "experimental_plan"
                continue
            
            # Append to current section
            if current_section:
                sections[current_section] += line + "\n"
        
        # Fallback if parsing fails
        if not sections["abstract"]:
            sections["abstract"] = response_text[:200]
        if not sections["methodology"]:
            sections["methodology"] = idea.methodology or "Proposed methodology"
        
        return ResearchProposal(
            task_id=task.task_id,
            title=idea.title,
            abstract=sections["abstract"].strip(),
            introduction=sections["introduction"].strip() or "Introduction section",
            related_work=sections["related_work"].strip() or "Related work section",
            methodology=sections["methodology"].strip(),
            expected_results=sections["expected_results"].strip() or "Expected results",
            experimental_plan=sections["experimental_plan"].strip() or "Experimental plan",
            model_name=self.model_name
        )
