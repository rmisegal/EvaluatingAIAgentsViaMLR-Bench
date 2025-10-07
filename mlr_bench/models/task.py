"""Task data models for MLR-Bench."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class TaskCategory(str, Enum):
    """Categories of research tasks."""
    TRUSTWORTHY_AI = "Trustworthy AI"
    LLM_VLM = "LLM/VLM"
    ML_THEORY = "ML Theory"
    AI_FOR_SCIENCE = "AI for Science"
    MULTIMODAL = "Multimodal"
    REINFORCEMENT_LEARNING = "Reinforcement Learning"
    COMPUTER_VISION = "Computer Vision"
    NLP = "NLP"
    OTHER = "Other"


class Task(BaseModel):
    """Research task definition."""
    
    task_id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    category: TaskCategory = Field(..., description="Task category")
    description: str = Field(..., description="Detailed task description")
    workshop_name: Optional[str] = Field(None, description="Workshop name if applicable")
    conference: Optional[str] = Field(None, description="Conference name (ICLR, NeurIPS, etc.)")
    year: Optional[int] = Field(None, description="Year of the task")
    topics: List[str] = Field(default_factory=list, description="Related topics")
    
    class Config:
        use_enum_values = True
