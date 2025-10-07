"""Literature review data models."""

from typing import List
from pydantic import BaseModel, Field


class Paper(BaseModel):
    """Individual paper reference."""
    
    title: str = Field(..., description="Paper title")
    authors: str = Field(..., description="Paper authors")
    year: int = Field(..., description="Publication year")
    summary: str = Field(..., description="Brief summary")
    relevance: str = Field(..., description="Why this paper is relevant")


class LiteratureReview(BaseModel):
    """Literature review results."""
    
    task_id: str = Field(..., description="Associated task ID")
    idea_title: str = Field(..., description="Research idea being reviewed")
    papers: List[Paper] = Field(default_factory=list, description="Reviewed papers")
    key_findings: str = Field(..., description="Key findings from literature")
    research_gap: str = Field(..., description="Identified research gap")
    related_work_summary: str = Field(..., description="Summary of related work")
    model_name: str = Field(..., description="LLM model used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "iclr2025_task_001",
                "idea_title": "Efficient Attention Mechanisms",
                "papers": [],
                "key_findings": "Most work focuses on sparse attention",
                "research_gap": "Limited work on hierarchical approaches",
                "model_name": "gemini-2.0-flash"
            }
        }
