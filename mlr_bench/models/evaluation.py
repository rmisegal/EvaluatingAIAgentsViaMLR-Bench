"""Evaluation result data models."""

from typing import Dict, Optional
from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    """Evaluation result from a judge."""
    
    evaluator_name: str = Field(..., description="Name of the evaluator/judge")
    overall_score: float = Field(..., ge=0, le=10, description="Overall score (0-10)")
    
    # Rubric scores
    consistency_score: Optional[float] = Field(None, ge=0, le=10, description="Consistency score")
    clarity_score: Optional[float] = Field(None, ge=0, le=10, description="Clarity score")
    novelty_score: Optional[float] = Field(None, ge=0, le=10, description="Novelty score")
    feasibility_score: Optional[float] = Field(None, ge=0, le=10, description="Feasibility score")
    significance_score: Optional[float] = Field(None, ge=0, le=10, description="Significance score")
    soundness_score: Optional[float] = Field(None, ge=0, le=10, description="Soundness score")
    
    feedback: str = Field(..., description="Detailed feedback")
    strengths: str = Field(default="", description="Identified strengths")
    weaknesses: str = Field(default="", description="Identified weaknesses")
    
    class Config:
        json_schema_extra = {
            "example": {
                "evaluator_name": "gemini-judge",
                "overall_score": 7.5,
                "consistency_score": 8.0,
                "clarity_score": 7.0,
                "novelty_score": 7.5,
                "feedback": "The idea is novel and well-presented..."
            }
        }


class AggregatedEvaluation(BaseModel):
    """Aggregated evaluation from multiple judges."""
    
    task_id: str = Field(..., description="Associated task ID")
    stage: str = Field(..., description="Research stage (idea, proposal, paper)")
    evaluations: list[EvaluationResult] = Field(..., description="Individual evaluations")
    average_score: float = Field(..., description="Average overall score")
    score_breakdown: Dict[str, float] = Field(default_factory=dict, description="Average scores by rubric")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "iclr2025_task_001",
                "stage": "idea",
                "evaluations": [],
                "average_score": 7.5,
                "score_breakdown": {"consistency": 8.0, "clarity": 7.0}
            }
        }
