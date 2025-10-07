"""Research proposal data models."""

from pydantic import BaseModel, Field


class ResearchProposal(BaseModel):
    """Detailed research proposal."""
    
    task_id: str = Field(..., description="Associated task ID")
    title: str = Field(..., description="Proposal title")
    abstract: str = Field(..., description="Research abstract")
    introduction: str = Field(..., description="Introduction section")
    related_work: str = Field(..., description="Related work section")
    methodology: str = Field(..., description="Proposed methodology")
    expected_results: str = Field(..., description="Expected results")
    experimental_plan: str = Field(..., description="Experimental plan")
    model_name: str = Field(..., description="LLM model used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "iclr2025_task_001",
                "title": "Hierarchical Attention for Long Sequences",
                "abstract": "We propose a novel hierarchical attention mechanism...",
                "introduction": "Transformers have revolutionized NLP...",
                "model_name": "gemini-2.0-flash"
            }
        }
