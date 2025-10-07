"""Experiment result data models."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ExperimentResult(BaseModel):
    """Results from running experiments."""
    
    task_id: str = Field(..., description="Associated task ID")
    code_files: List[str] = Field(default_factory=list, description="Generated code file paths")
    execution_log: str = Field(..., description="Execution log")
    results: Dict[str, Any] = Field(default_factory=dict, description="Experimental results")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    success: bool = Field(..., description="Whether experiments succeeded")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    model_name: str = Field(..., description="LLM model used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "iclr2025_task_001",
                "code_files": ["experiment.py", "model.py"],
                "execution_log": "Running experiments...",
                "results": {"accuracy": 0.95},
                "metrics": {"accuracy": 0.95, "f1": 0.93},
                "success": True,
                "model_name": "gemini-2.0-flash"
            }
        }
