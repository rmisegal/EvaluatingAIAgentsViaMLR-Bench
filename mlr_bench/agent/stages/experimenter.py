"""Experimenter agent using Google ADK."""

import uuid
from pathlib import Path
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.proposal import ResearchProposal
from mlr_bench.models.literature import LiteratureReview
from mlr_bench.models.experiment import ExperimentResult
from mlr_bench.config.prompts import EXPERIMENT_CODING_PROMPT
from mlr_bench.agent.tools import execute_python_code, save_to_file


class Experimenter:
    """Agent for running experiments (simplified for educational purposes)."""

    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        temperature: float = 0.7,
        timeout: int = 3600
    ):
        """Initialize experimenter.

        Args:
            model_name: LLM model name
            temperature: Generation temperature
            timeout: Execution timeout in seconds
        """
        self.model_name = model_name
        self.temperature = temperature
        self.timeout = timeout
        self.app_name = "mlr_bench_experimenter"
        self.agent = self._create_agent()
        self.runner = InMemoryRunner(agent=self.agent, app_name=self.app_name)

    def _create_agent(self) -> Agent:
        """Create ADK agent for experimentation."""
        return Agent(
            name="experimenter",
            model=self.model_name,
            description="Agent specialized in implementing and running ML experiments",
            instruction=(
                "You are an expert ML engineer. "
                "Generate clean, modular, well-documented Python code "
                "to implement research experiments. "
                "Use execute_python_code to run code and save_to_file to save results. "
                "For educational purposes, create simplified implementations."
            ),
            tools=[execute_python_code, save_to_file]  # Add execution tools
        )
    
    async def run_experiments(
        self,
        task: Task,
        idea: ResearchIdea,
        proposal: ResearchProposal,
        literature: LiteratureReview,
        workspace: Path
    ) -> ExperimentResult:
        """Run experiments (simplified version).
        
        Args:
            task: Research task
            idea: Research idea
            proposal: Research proposal
            literature: Literature review
            workspace: Workspace directory
            
        Returns:
            Experiment results
        """
        logger.info(f"Running experiments for: {idea.title}")

        # For educational purposes, we'll generate code but not execute it
        # In a full implementation, this would use a coding agent to write and run code

        # Format prompt
        prompt = EXPERIMENT_CODING_PROMPT.format(
            proposal_title=proposal.title,
            methodology=proposal.methodology,
            experimental_plan=proposal.experimental_plan
        )

        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=prompt)]
        )

        # Generate code using agent via runner
        session_id = f'experiment_{task.task_id}_{uuid.uuid4().hex[:8]}'
        user_id = 'mlr_bench'

        # Create session first
        await self.runner.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id
        )

        code_text = ""
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        code_text += part.text
        
        # Save code to workspace
        code_file = workspace / "experiment.py"
        code_file.write_text(code_text, encoding='utf-8')
        
        # Create mock results (in real implementation, would execute code)
        result = ExperimentResult(
            task_id=task.task_id,
            code_files=[str(code_file)],
            execution_log="Mock execution log - code generated but not executed for safety",
            results={
                "status": "generated",
                "note": "Code generated successfully. In production, this would execute."
            },
            metrics={
                "code_length": len(code_text),
                "lines_of_code": len(code_text.split('\n'))
            },
            success=True,
            error_message=None,
            model_name=self.model_name
        )
        
        logger.info(f"Completed experiments for: {idea.title}")
        return result
