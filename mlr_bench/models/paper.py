"""Research paper data models."""

from pydantic import BaseModel, Field


class ResearchPaper(BaseModel):
    """Complete research paper."""
    
    task_id: str = Field(..., description="Associated task ID")
    title: str = Field(..., description="Paper title")
    abstract: str = Field(..., description="Abstract")
    introduction: str = Field(..., description="Introduction section")
    related_work: str = Field(..., description="Related work section")
    methodology: str = Field(..., description="Methodology section")
    experiments: str = Field(..., description="Experiments section")
    results: str = Field(..., description="Results section")
    discussion: str = Field(..., description="Discussion section")
    conclusion: str = Field(..., description="Conclusion section")
    references: str = Field(..., description="References section")
    model_name: str = Field(..., description="LLM model used")
    
    def to_markdown(self) -> str:
        """Convert paper to markdown format."""
        return f"""# {self.title}

## Abstract
{self.abstract}

## 1. Introduction
{self.introduction}

## 2. Related Work
{self.related_work}

## 3. Methodology
{self.methodology}

## 4. Experiments
{self.experiments}

## 5. Results
{self.results}

## 6. Discussion
{self.discussion}

## 7. Conclusion
{self.conclusion}

## References
{self.references}
"""
