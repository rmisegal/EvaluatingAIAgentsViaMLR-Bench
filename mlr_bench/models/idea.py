"""Research idea data models."""

from typing import Optional
from pydantic import BaseModel, Field


class ResearchIdea(BaseModel):
    """Generated research idea."""
    
    task_id: str = Field(..., description="Associated task ID")
    title: str = Field(..., description="Research idea title")
    motivation: str = Field(..., description="Why this research is important")
    main_idea: str = Field(..., description="Core research idea")
    methodology: Optional[str] = Field(None, description="Proposed methodology")
    expected_outcomes: Optional[str] = Field(None, description="Expected results")
    model_name: str = Field(..., description="LLM model used for generation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "iclr2025_task_001",
                "title": "Efficient Attention Mechanisms for Long Sequences",
                "motivation": "Current transformers struggle with long sequences",
                "main_idea": "Use hierarchical attention to reduce complexity",
                "model_name": "gemini-2.0-flash"
            }
        }
