"""Base evaluator interface."""

from abc import ABC, abstractmethod
from typing import List
from google.adk.agents import Agent

from mlr_bench.models.evaluation import EvaluationResult
from mlr_bench.agent.tools import calculate_average_score, extract_scores_from_text


class BaseEvaluator(ABC):
    """Base class for evaluators."""
    
    def __init__(self, model_name: str, evaluator_name: str):
        """Initialize evaluator.
        
        Args:
            model_name: LLM model name
            evaluator_name: Name of this evaluator
        """
        self.model_name = model_name
        self.evaluator_name = evaluator_name
        
        # Tools available to all evaluators - MUST be defined before _create_agent()
        self.common_tools = [calculate_average_score, extract_scores_from_text]
        
        # Create agent after tools are defined
        self.agent = self._create_agent()
    
    @abstractmethod
    def _create_agent(self) -> Agent:
        """Create ADK agent for evaluation.
        
        Returns:
            Configured Agent
        """
        pass
    
    @abstractmethod
    async def evaluate(self, *args, **kwargs) -> List[EvaluationResult]:
        """Evaluate research output.
        
        Returns:
            List of evaluation results
        """
        pass
    
    def _parse_scores(self, response_text: str) -> dict:
        """Parse scores from LLM response.
        
        Args:
            response_text: LLM response
            
        Returns:
            Dictionary of scores
        """
        scores = {}
        lines = response_text.lower().split('\n')
        
        score_keywords = [
            'consistency', 'clarity', 'novelty', 
            'feasibility', 'significance', 'soundness',
            'overall'
        ]
        
        for line in lines:
            for keyword in score_keywords:
                if keyword in line and ':' in line:
                    try:
                        # Extract number after colon
                        parts = line.split(':')
                        if len(parts) >= 2:
                            score_str = parts[1].strip().split()[0]
                            # Remove non-numeric characters except decimal point
                            score_str = ''.join(c for c in score_str if c.isdigit() or c == '.')
                            if score_str:
                                score = float(score_str)
                                if 0 <= score <= 10:
                                    scores[keyword] = score
                    except (ValueError, IndexError):
                        continue
        
        return scores
