"""Configuration management for MLR-Bench."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config(BaseModel):
    """MLR-Bench configuration."""
    
    # Model settings
    model_name: str = Field(
        default=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
        description="Default LLM model name"
    )
    temperature: float = Field(
        default=float(os.getenv("TEMPERATURE", "0.7")),
        ge=0.0,
        le=2.0,
        description="LLM temperature"
    )
    max_tokens: int = Field(
        default=int(os.getenv("MAX_TOKENS", "4000")),
        description="Maximum tokens for generation"
    )
    
    # API Keys
    google_api_key: Optional[str] = Field(
        default=os.getenv("GOOGLE_API_KEY"),
        description="Google AI API key"
    )
    use_vertex_ai: bool = Field(
        default=os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE",
        description="Use Vertex AI instead of AI Studio"
    )
    
    # Paths
    data_dir: Path = Field(
        default=Path(os.getenv("DATA_DIR", "data")),
        description="Data directory"
    )
    results_dir: Path = Field(
        default=Path(os.getenv("RESULTS_DIR", "results")),
        description="Results directory"
    )
    workspaces_dir: Path = Field(
        default=Path(os.getenv("WORKSPACES_DIR", "workspaces")),
        description="Workspaces directory for experiments"
    )
    
    # Logging
    log_level: str = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level"
    )
    log_file: Path = Field(
        default=Path(os.getenv("LOG_FILE", "logs/mlr_bench.log")),
        description="Log file path"
    )
    
    # Execution settings
    timeout: int = Field(
        default=int(os.getenv("TIMEOUT", "3600")),
        description="Execution timeout in seconds"
    )
    
    class Config:
        validate_assignment = True
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.workspaces_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)


def load_config() -> Config:
    """Load configuration.
    
    Returns:
        Config object
    """
    config = Config()
    config.ensure_directories()
    return config
