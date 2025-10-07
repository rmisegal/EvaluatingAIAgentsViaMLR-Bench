"""Idea evaluator using Google ADK."""

from typing import List
from google.adk.agents import Agent
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.evaluation import EvaluationResult
from mlr_bench.config.prompts import IDEA_EVALUATION_PROMPT
from mlr_bench.judge.evaluators.base_evaluator import BaseEvaluator


class IdeaEvaluator(BaseEvaluator):
    """Evaluator for research ideas."""
    
    def _create_agent(self) -> Agent:
        """Create ADK agent for idea evaluation."""
        return Agent(
            name=f"idea_evaluator_{self.evaluator_name}",
            model=self.model_name,
            description="Expert reviewer evaluating research ideas",
            instruction=(
                "You are an expert reviewer at a top ML conference. "
                "Evaluate research ideas rigorously on consistency, clarity, "
                "novelty, feasibility, and significance. "
                "Provide scores from 0-10 and detailed feedback. "
                "Use extract_scores_from_text to parse scores and "
                "calculate_average_score to compute averages."
            ),
            tools=self.common_tools  # Add evaluation tools
        )
    
    async def evaluate(
        self, 
        idea: ResearchIdea, 
        task: Task
    ) -> List[EvaluationResult]:
        """Evaluate research idea.
        
        Args:
            idea: Research idea to evaluate
            task: Original task
            
        Returns:
            List with single evaluation result
        """
        logger.info(f"Evaluating idea: {idea.title} with {self.evaluator_name}")
        
        # Format prompt
        prompt = IDEA_EVALUATION_PROMPT.format(
            idea_title=idea.title,
            motivation=idea.motivation,
            main_idea=idea.main_idea
        )
        
        # Get evaluation from agent
        response = await self.agent.run(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
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
                scores.get('consistency', 0),
                scores.get('clarity', 0),
                scores.get('novelty', 0),
                scores.get('feasibility', 0),
                scores.get('significance', 0)
            ]
            overall_score = sum(s for s in relevant_scores if s > 0) / max(1, sum(1 for s in relevant_scores if s > 0))
        
        result = EvaluationResult(
            evaluator_name=self.evaluator_name,
            overall_score=overall_score or 5.0,
            consistency_score=scores.get('consistency'),
            clarity_score=scores.get('clarity'),
            novelty_score=scores.get('novelty'),
            feasibility_score=scores.get('feasibility'),
            significance_score=scores.get('significance'),
            feedback=feedback,
            strengths=strengths,
            weaknesses=weaknesses
        )
        
        logger.info(f"Evaluation complete: {result.overall_score:.1f}/10")
        return [result]
