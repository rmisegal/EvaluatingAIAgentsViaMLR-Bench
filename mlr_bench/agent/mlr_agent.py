"""Main MLR Agent orchestrator."""

from pathlib import Path
from loguru import logger

from mlr_bench.models.task import Task
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.literature import LiteratureReview
from mlr_bench.models.proposal import ResearchProposal
from mlr_bench.models.experiment import ExperimentResult
from mlr_bench.models.paper import ResearchPaper
from mlr_bench.config.config import Config
from mlr_bench.utils.sandbox import SandboxManager
from mlr_bench.utils.file_utils import save_json, save_text

from mlr_bench.agent.stages.idea_generator import IdeaGenerator
from mlr_bench.agent.stages.literature_reviewer import LiteratureReviewer
from mlr_bench.agent.stages.proposal_writer import ProposalWriter
from mlr_bench.agent.stages.experimenter import Experimenter
from mlr_bench.agent.stages.paper_writer import PaperWriter
from mlr_bench.agent.agent_wrapper import track_agent_execution


class MLRAgent:
    """Main research agent orchestrating the full pipeline."""
    
    def __init__(self, config: Config):
        """Initialize MLR Agent.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.sandbox = SandboxManager(config.workspaces_dir)
        
        # Initialize stage agents
        self.idea_generator = IdeaGenerator(
            model_name=config.model_name,
            temperature=config.temperature
        )
        self.literature_reviewer = LiteratureReviewer(
            model_name=config.model_name,
            temperature=config.temperature
        )
        self.proposal_writer = ProposalWriter(
            model_name=config.model_name,
            temperature=config.temperature
        )
        self.experimenter = Experimenter(
            model_name=config.model_name,
            temperature=config.temperature,
            timeout=config.timeout
        )
        self.paper_writer = PaperWriter(
            model_name=config.model_name,
            temperature=config.temperature
        )
        
        logger.info("MLRAgent initialized with all stage agents")
    
    async def run_full_pipeline(self, task: Task) -> ResearchPaper:
        """Run the complete research pipeline.
        
        Args:
            task: Research task
            
        Returns:
            Final research paper
        """
        logger.info(f"Starting full pipeline for task: {task.task_id}")
        
        # Create workspace
        workspace = await self.sandbox.create_workspace(task.task_id)
        results_dir = self.config.results_dir / task.task_id
        results_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Stage 1: Generate Idea
            logger.info("Stage 1/5: Generating research idea...")
            idea = await self.generate_idea(task)
            await save_json(idea.model_dump(), results_dir / "idea.json")
            
            # Stage 2: Literature Review
            logger.info("Stage 2/5: Conducting literature review...")
            literature = await self.review_literature(idea, task)
            await save_json(literature.model_dump(), results_dir / "literature.json")
            
            # Stage 3: Write Proposal
            logger.info("Stage 3/5: Writing research proposal...")
            proposal = await self.generate_proposal(task, idea, literature)
            await save_json(proposal.model_dump(), results_dir / "proposal.json")
            
            # Stage 4: Run Experiments
            logger.info("Stage 4/5: Running experiments...")
            experiment = await self.run_experiments(
                task, idea, proposal, literature, workspace
            )
            await save_json(experiment.model_dump(), results_dir / "experiment.json")
            
            # Stage 5: Write Paper
            logger.info("Stage 5/6: Writing research paper...")
            paper = await self.write_paper(
                task, idea, literature, proposal, experiment
            )
            await save_json(paper.model_dump(), results_dir / "paper.json")
            await save_text(paper.to_markdown(), results_dir / "paper.md")
            
            # Stage 6: Evaluate (Judge)
            logger.info("Stage 6/6: Evaluating research...")
            from mlr_bench.judge.mlr_judge import MLRJudge
            from mlr_bench.agent.agent_wrapper import emit_agent_event
            
            judge = MLRJudge(self.config)
            
            # Emit started event
            emit_agent_event("MLRJudge", "evaluation", "started")
            
            # Evaluate
            evaluation = await judge.evaluate(idea, paper)
            await save_json(evaluation.model_dump(), results_dir / "evaluation.json")
            
            # Emit output event with scores
            # Note: idea_score is stored in consistency_score, paper_score in clarity_score, average in overall_score
            scores_data = {
                "idea_score": evaluation.consistency_score,
                "paper_score": evaluation.clarity_score,
                "average": evaluation.overall_score,
                "scores": {
                    "idea_score": evaluation.consistency_score,
                    "paper_score": evaluation.clarity_score,
                    "average": evaluation.overall_score
                }
            }
            emit_agent_event("MLRJudge", "evaluation", "output", scores_data)

            # Emit completed event
            emit_agent_event("MLRJudge", "evaluation", "completed", scores_data)

            logger.info(f"Pipeline completed successfully for: {task.task_id}")
            logger.info(f"Evaluation scores - Idea: {evaluation.consistency_score:.1f}, Paper: {evaluation.clarity_score:.1f}, Average: {evaluation.overall_score:.1f}")
            
            return paper
            
        except Exception as e:
            logger.error(f"Pipeline failed for {task.task_id}: {e}")
            raise
    
    @track_agent_execution("IdeaGenerator", "idea")
    async def generate_idea(self, task: Task) -> ResearchIdea:
        """Generate research idea."""
        return await self.idea_generator.generate_idea(task)
    
    @track_agent_execution("LiteratureReviewer", "literature")
    async def review_literature(
        self, 
        idea: ResearchIdea, 
        task: Task
    ) -> LiteratureReview:
        """Conduct literature review."""
        return await self.literature_reviewer.review_literature(idea, task)
    
    @track_agent_execution("ProposalWriter", "proposal")
    async def generate_proposal(
        self,
        task: Task,
        idea: ResearchIdea,
        literature: LiteratureReview
    ) -> ResearchProposal:
        """Generate research proposal."""
        return await self.proposal_writer.write_proposal(task, idea, literature)
    
    @track_agent_execution("Experimenter", "experiment")
    async def run_experiments(
        self,
        task: Task,
        idea: ResearchIdea,
        proposal: ResearchProposal,
        literature: LiteratureReview,
        workspace: Path
    ) -> ExperimentResult:
        """Run experiments."""
        return await self.experimenter.run_experiments(
            task, idea, proposal, literature, workspace
        )
    
    @track_agent_execution("PaperWriter", "paper")
    async def write_paper(
        self,
        task: Task,
        idea: ResearchIdea,
        literature: LiteratureReview,
        proposal: ResearchProposal,
        experiment: ExperimentResult
    ) -> ResearchPaper:
        """Write research paper."""
        return await self.paper_writer.write_paper(
            task, idea, literature, proposal, experiment
        )
