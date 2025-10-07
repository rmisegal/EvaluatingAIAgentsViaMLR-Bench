"""Paper writing agent using Google ADK."""

import uuid
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.literature import LiteratureReview
from mlr_bench.models.proposal import ResearchProposal
from mlr_bench.models.experiment import ExperimentResult
from mlr_bench.models.paper import ResearchPaper
from mlr_bench.config.prompts import PAPER_WRITING_PROMPT
from mlr_bench.agent.tools import format_paper_section


class PaperWriter:
    """Agent for writing research papers."""

    def __init__(self, model_name: str = "gemini-2.0-flash", temperature: float = 0.7):
        """Initialize paper writer.

        Args:
            model_name: LLM model name
            temperature: Generation temperature
        """
        self.model_name = model_name
        self.temperature = temperature
        self.app_name = "mlr_bench_paper_writer"
        self.agent = self._create_agent()
        self.runner = InMemoryRunner(agent=self.agent, app_name=self.app_name)

    def _create_agent(self) -> Agent:
        """Create ADK agent for paper writing."""
        return Agent(
            name="paper_writer",
            model=self.model_name,
            description="Agent specialized in writing research papers",
            instruction=(
                "You are an accomplished research scientist. "
                "Write clear, rigorous, and well-structured research papers "
                "in the style of top-tier ML conferences (ICLR, NeurIPS, ICML). "
                "Use the format_paper_section tool to structure sections properly."
            ),
            tools=[format_paper_section]  # Add formatting tool
        )
    
    async def write_paper(
        self,
        task: Task,
        idea: ResearchIdea,
        literature: LiteratureReview,
        proposal: ResearchProposal,
        experiment: ExperimentResult
    ) -> ResearchPaper:
        """Write complete research paper.
        
        Args:
            task: Research task
            idea: Research idea
            literature: Literature review
            proposal: Research proposal
            experiment: Experiment results
            
        Returns:
            Research paper
        """
        logger.info(f"Writing paper for: {idea.title}")

        # Format prompt
        prompt = PAPER_WRITING_PROMPT.format(
            task_title=task.title,
            proposal_abstract=proposal.abstract,
            experiment_results=str(experiment.results)
        )

        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=prompt)]
        )

        # Generate paper using agent via runner
        session_id = f'paper_{task.task_id}_{uuid.uuid4().hex[:8]}'
        user_id = 'mlr_bench'

        # Create session first
        await self.runner.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id
        )

        paper_text = ""
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        paper_text += part.text
        
        paper = self._parse_paper_response(paper_text, task, idea, proposal)
        
        logger.info(f"Completed paper: {paper.title}")
        return paper
    
    def _parse_paper_response(
        self,
        response_text: str,
        task: Task,
        idea: ResearchIdea,
        proposal: ResearchProposal
    ) -> ResearchPaper:
        """Parse LLM response into ResearchPaper.
        
        Args:
            response_text: LLM response text
            task: Research task
            idea: Research idea
            proposal: Research proposal
            
        Returns:
            ResearchPaper object
        """
        sections = {
            "abstract": "",
            "introduction": "",
            "related_work": "",
            "methodology": "",
            "experiments": "",
            "results": "",
            "discussion": "",
            "conclusion": "",
            "references": ""
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
            elif "experiments" in line_lower and len(line) < 50:
                current_section = "experiments"
                continue
            elif "results" in line_lower and len(line) < 50:
                current_section = "results"
                continue
            elif "discussion" in line_lower and len(line) < 50:
                current_section = "discussion"
                continue
            elif "conclusion" in line_lower and len(line) < 50:
                current_section = "conclusion"
                continue
            elif "references" in line_lower and len(line) < 50:
                current_section = "references"
                continue
            
            # Append to current section
            if current_section:
                sections[current_section] += line + "\n"
        
        # Use proposal content as fallback
        if not sections["abstract"]:
            sections["abstract"] = proposal.abstract
        if not sections["introduction"]:
            sections["introduction"] = proposal.introduction
        if not sections["related_work"]:
            sections["related_work"] = proposal.related_work
        if not sections["methodology"]:
            sections["methodology"] = proposal.methodology
        
        return ResearchPaper(
            task_id=task.task_id,
            title=idea.title,
            abstract=sections["abstract"].strip(),
            introduction=sections["introduction"].strip(),
            related_work=sections["related_work"].strip(),
            methodology=sections["methodology"].strip(),
            experiments=sections["experiments"].strip() or "Experiments section",
            results=sections["results"].strip() or "Results section",
            discussion=sections["discussion"].strip() or "Discussion section",
            conclusion=sections["conclusion"].strip() or "Conclusion section",
            references=sections["references"].strip() or "References section",
            model_name=self.model_name
        )
