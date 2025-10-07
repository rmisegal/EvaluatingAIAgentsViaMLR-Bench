"""MLR Judge - Multi-LLM evaluation system."""

from typing import List, Dict
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.paper import ResearchPaper
from mlr_bench.models.evaluation import EvaluationResult, AggregatedEvaluation
from mlr_bench.config.config import Config
from mlr_bench.judge.evaluators.idea_evaluator import IdeaEvaluator
from mlr_bench.judge.evaluators.paper_evaluator import PaperEvaluator


class MLRJudge:
    """Multi-LLM judge for evaluating research outputs."""
    
    def __init__(self, config: Config, judge_models: List[str] = None):
        """Initialize MLR Judge.
        
        Args:
            config: Configuration object
            judge_models: List of model names to use as judges
        """
        self.config = config
        
        # Default judge models if not specified
        if judge_models is None:
            judge_models = [config.model_name]
        
        self.judge_models = judge_models
        
        # Initialize evaluators for each judge model
        self.idea_evaluators = [
            IdeaEvaluator(model_name=model, evaluator_name=f"judge_{i+1}")
            for i, model in enumerate(judge_models)
        ]
        
        self.paper_evaluators = [
            PaperEvaluator(model_name=model, evaluator_name=f"judge_{i+1}")
            for i, model in enumerate(judge_models)
        ]
        
        logger.info(f"MLRJudge initialized with {len(judge_models)} judges")
    
    async def evaluate_idea(
        self, 
        idea: ResearchIdea, 
        task: Task
    ) -> AggregatedEvaluation:
        """Evaluate research idea with multiple judges.
        
        Args:
            idea: Research idea to evaluate
            task: Original task
            
        Returns:
            Aggregated evaluation results
        """
        logger.info(f"Evaluating idea with {len(self.idea_evaluators)} judges")
        
        # Collect evaluations from all judges
        all_evaluations = []
        for evaluator in self.idea_evaluators:
            evaluations = await evaluator.evaluate(idea, task)
            all_evaluations.extend(evaluations)
        
        # Aggregate results
        aggregated = self._aggregate_evaluations(
            task_id=task.task_id,
            stage="idea",
            evaluations=all_evaluations
        )
        
        logger.info(f"Idea evaluation complete: {aggregated.average_score:.2f}/10")
        return aggregated
    
    async def evaluate_paper(
        self,
        paper: ResearchPaper,
        task: Task,
        code_files: List[str] = None
    ) -> AggregatedEvaluation:
        """Evaluate research paper with multiple judges.
        
        Args:
            paper: Research paper to evaluate
            task: Original task
            code_files: List of code file paths
            
        Returns:
            Aggregated evaluation results
        """
        logger.info(f"Evaluating paper with {len(self.paper_evaluators)} judges")
        
        # Collect evaluations from all judges
        all_evaluations = []
        for evaluator in self.paper_evaluators:
            evaluations = await evaluator.evaluate(paper, task, code_files)
            all_evaluations.extend(evaluations)
        
        # Aggregate results
        aggregated = self._aggregate_evaluations(
            task_id=task.task_id,
            stage="paper",
            evaluations=all_evaluations
        )
        
        logger.info(f"Paper evaluation complete: {aggregated.average_score:.2f}/10")
        return aggregated
    
    def _aggregate_evaluations(
        self,
        task_id: str,
        stage: str,
        evaluations: List[EvaluationResult]
    ) -> AggregatedEvaluation:
        """Aggregate multiple evaluation results.
        
        Args:
            task_id: Task identifier
            stage: Research stage
            evaluations: List of evaluation results
            
        Returns:
            Aggregated evaluation
        """
        if not evaluations:
            raise ValueError("No evaluations to aggregate")
        
        # Calculate average overall score
        average_score = sum(e.overall_score for e in evaluations) / len(evaluations)
        
        # Calculate average scores for each rubric
        score_breakdown = {}
        
        rubric_fields = [
            'consistency_score', 'clarity_score', 'novelty_score',
            'feasibility_score', 'significance_score', 'soundness_score'
        ]
        
        for field in rubric_fields:
            scores = [
                getattr(e, field) for e in evaluations 
                if getattr(e, field) is not None
            ]
            if scores:
                score_breakdown[field.replace('_score', '')] = sum(scores) / len(scores)
        
        return AggregatedEvaluation(
            task_id=task_id,
            stage=stage,
            evaluations=evaluations,
            average_score=average_score,
            score_breakdown=score_breakdown
        )
