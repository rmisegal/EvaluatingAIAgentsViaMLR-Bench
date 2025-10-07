"""Literature review agent using Google ADK."""

from google.adk.agents import Agent
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.literature import LiteratureReview
from mlr_bench.config.prompts import LITERATURE_REVIEW_PROMPT
from mlr_bench.mcp.mcp_tools import search_papers_sync


class LiteratureReviewer:
    """Agent for conducting literature reviews."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash", temperature: float = 0.7):
        """Initialize literature reviewer.
        
        Args:
            model_name: LLM model name
            temperature: Generation temperature
        """
        self.model_name = model_name
        self.temperature = temperature
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create ADK agent for literature review."""
        return Agent(
            name="literature_reviewer",
            model=self.model_name,
            description="Agent specialized in conducting literature reviews",
            instruction=(
                "You are an expert research assistant. "
                "Conduct thorough literature reviews to identify key findings, "
                "research gaps, and situate new ideas in existing work. "
                "Use the search_papers tool to find relevant research."
            ),
            tools=[search_papers_sync]  # Add MCP search tool
        )
    
    async def review_literature(
        self, 
        idea: ResearchIdea, 
        task: Task
    ) -> LiteratureReview:
        """Conduct literature review for a research idea.
        
        Args:
            idea: Research idea to review
            task: Original task
            
        Returns:
            Literature review results
        """
        logger.info(f"Reviewing literature for idea: {idea.title}")
        
        # Format prompt
        prompt = LITERATURE_REVIEW_PROMPT.format(
            idea_title=idea.title,
            main_idea=idea.main_idea
        )
        
        # Generate review using agent
        response = await self.agent.run(prompt)
        
        # Parse response
        review_text = response.text if hasattr(response, 'text') else str(response)
        
        review = self._parse_review_response(review_text, idea, task)
        
        logger.info(f"Completed literature review for: {idea.title}")
        return review
    
    def _parse_review_response(
        self, 
        response_text: str, 
        idea: ResearchIdea,
        task: Task
    ) -> LiteratureReview:
        """Parse LLM response into LiteratureReview.
        
        Args:
            response_text: LLM response text
            idea: Research idea
            task: Original task
            
        Returns:
            LiteratureReview object
        """
        lines = response_text.split('\n')
        
        key_findings = ""
        research_gap = ""
        related_work_summary = ""
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if "key findings:" in line.lower() or "findings:" in line.lower():
                current_section = "key_findings"
            elif "research gap:" in line.lower() or "gap:" in line.lower():
                current_section = "research_gap"
            elif "related work:" in line.lower() or "summary:" in line.lower():
                current_section = "related_work"
            else:
                # Append to current section
                if current_section == "key_findings":
                    key_findings += line + " "
                elif current_section == "research_gap":
                    research_gap += line + " "
                elif current_section == "related_work":
                    related_work_summary += line + " "
        
        # Fallback
        if not key_findings:
            key_findings = response_text[:300]
        if not research_gap:
            research_gap = "Identified research gap in the literature"
        if not related_work_summary:
            related_work_summary = response_text[:300]
        
        return LiteratureReview(
            task_id=task.task_id,
            idea_title=idea.title,
            papers=[],  # Simplified - no actual paper search
            key_findings=key_findings.strip(),
            research_gap=research_gap.strip(),
            related_work_summary=related_work_summary.strip(),
            model_name=self.model_name
        )
