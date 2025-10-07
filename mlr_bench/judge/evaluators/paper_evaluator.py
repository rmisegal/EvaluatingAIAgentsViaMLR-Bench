"""Paper evaluator using Google ADK."""

import uuid
from typing import List
from google.adk.agents import Agent
from google.genai import types
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.paper import ResearchPaper
from mlr_bench.models.evaluation import EvaluationResult
from mlr_bench.config.prompts import PAPER_EVALUATION_PROMPT
from mlr_bench.judge.evaluators.base_evaluator import BaseEvaluator


class PaperEvaluator(BaseEvaluator):
    """Evaluator for research papers."""
    
    def _create_agent(self) -> Agent:
        """Create ADK agent for paper evaluation."""
        return Agent(
            name=f"paper_evaluator_{self.evaluator_name}",
            model=self.model_name,
            description="Expert reviewer evaluating research papers",
            instruction=(
                "You are an expert reviewer at a top ML conference. "
                "Evaluate research papers rigorously on clarity, novelty, "
                "soundness, and significance. "
                "Check for hallucinated results and code quality. "
                "Provide scores from 0-10 and detailed feedback. "
                "Use extract_scores_from_text to parse scores and "
                "calculate_average_score to compute averages."
            ),
            tools=self.common_tools  # Add evaluation tools
        )
    
    async def evaluate(
        self,
        paper: ResearchPaper,
        task: Task,
        code_files: List[str] = None
    ) -> List[EvaluationResult]:
        """Evaluate research paper.
        
        Args:
            paper: Research paper to evaluate
            task: Original task
            code_files: List of code file paths (optional)
            
        Returns:
            List with single evaluation result
        """
        logger.info(f"Evaluating paper: {paper.title} with {self.evaluator_name}")

        # Format prompt
        prompt = PAPER_EVALUATION_PROMPT.format(
            paper_title=paper.title,
            abstract=paper.abstract
        )

        # Add code context if available
        if code_files:
            prompt += f"\n\nCode files provided: {len(code_files)}"

        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=prompt)]
        )

        # Get evaluation from agent via runner
        session_id = f'eval_paper_{task.task_id}_{self.evaluator_name}_{uuid.uuid4().hex[:8]}'
        user_id = 'mlr_bench'

        # Create session first
        await self.runner.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id
        )

        response_text = ""
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
        
        # Parse scores
        scores = self._parse_scores(response_text)
        
        # Extract feedback sections
        feedback_lines = []
        strengths_lines = []
        weaknesses_lines = []
        
        current_section = "feedback"
        for line in response_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if "strengths:" in line.lower():
                current_section = "strengths"
                continue
            elif "weaknesses:" in line.lower():
                current_section = "weaknesses"
                continue
            elif "feedback:" in line.lower():
                current_section = "feedback"
                continue
            
            if current_section == "feedback":
                feedback_lines.append(line)
            elif current_section == "strengths":
                strengths_lines.append(line)
            elif current_section == "weaknesses":
                weaknesses_lines.append(line)
        
        feedback = "\n".join(feedback_lines) or response_text[:500]
        strengths = "\n".join(strengths_lines) or "Strengths identified"
        weaknesses = "\n".join(weaknesses_lines) or "Weaknesses identified"
        
        # Calculate overall score
        overall_score = scores.get('overall', 0)
        if overall_score == 0 and scores:
            # Average of other scores
            relevant_scores = [
                scores.get('clarity', 0),
                scores.get('novelty', 0),
                scores.get('soundness', 0),
                scores.get('significance', 0)
            ]
            overall_score = sum(s for s in relevant_scores if s > 0) / max(1, sum(1 for s in relevant_scores if s > 0))
        
        result = EvaluationResult(
            evaluator_name=self.evaluator_name,
            overall_score=overall_score or 5.0,
            clarity_score=scores.get('clarity'),
            novelty_score=scores.get('novelty'),
            soundness_score=scores.get('soundness'),
            significance_score=scores.get('significance'),
            feedback=feedback,
            strengths=strengths,
            weaknesses=weaknesses
        )
        
        logger.info(f"Evaluation complete: {result.overall_score:.1f}/10")
        return [result]
