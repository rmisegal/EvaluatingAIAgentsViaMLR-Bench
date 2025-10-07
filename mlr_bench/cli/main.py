"""Main CLI entry point for MLR-Bench."""

import sys
import asyncio
import argparse
from pathlib import Path
from loguru import logger

from mlr_bench.config.config import load_config
from mlr_bench.utils.logging_utils import setup_logging
from mlr_bench.tasks.task_manager import TaskManager
from mlr_bench.agent.mlr_agent import MLRAgent
from mlr_bench.judge.mlr_judge import MLRJudge
from mlr_bench.utils.file_utils import save_json


async def run_single_task(task_id: str, config):
    """Run MLR-Bench on a single task.
    
    Args:
        task_id: Task identifier
        config: Configuration object
    """
    logger.info(f"Running MLR-Bench on task: {task_id}")
    
    # Load tasks
    tasks_file = config.data_dir / "tasks" / "tasks.json"
    task_manager = TaskManager(tasks_file)
    
    task = task_manager.get_task(task_id)
    if not task:
        logger.error(f"Task not found: {task_id}")
        return
    
    # Initialize agent and judge
    agent = MLRAgent(config)
    judge = MLRJudge(config)
    
    try:
        # Run full pipeline
        paper = await agent.run_full_pipeline(task)
        
        # Evaluate results
        logger.info("Evaluating results...")
        idea_eval = await judge.evaluate_idea(
            await agent.generate_idea(task),
            task
        )
        paper_eval = await judge.evaluate_paper(paper, task)
        
        # Save evaluation results
        results_dir = config.results_dir / task_id
        await save_json(idea_eval.model_dump(), results_dir / "idea_evaluation.json")
        await save_json(paper_eval.model_dump(), results_dir / "paper_evaluation.json")
        
        logger.info(f"Task completed successfully: {task_id}")
        logger.info(f"Idea score: {idea_eval.average_score:.2f}/10")
        logger.info(f"Paper score: {paper_eval.average_score:.2f}/10")
        
    except Exception as e:
        logger.error(f"Error running task {task_id}: {e}")
        raise


async def run_all_tasks(config):
    """Run MLR-Bench on all tasks.
    
    Args:
        config: Configuration object
    """
    logger.info("Running MLR-Bench on all tasks")
    
    # Load tasks
    tasks_file = config.data_dir / "tasks" / "tasks.json"
    task_manager = TaskManager(tasks_file)
    
    all_tasks = task_manager.get_all_tasks()
    logger.info(f"Found {len(all_tasks)} tasks")
    
    for task in all_tasks:
        try:
            await run_single_task(task.task_id, config)
        except Exception as e:
            logger.error(f"Failed to run task {task.task_id}: {e}")
            continue


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MLR-Bench: Evaluating AI Agents on Open-Ended ML Research"
    )
    
    parser.add_argument(
        "--task-id",
        type=str,
        help="Specific task ID to run (e.g., iclr2025_bi_align)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run on all tasks"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    # Setup logging
    setup_logging(level=args.log_level, log_file=config.log_file)
    
    logger.info("=" * 60)
    logger.info("MLR-Bench: Machine Learning Research Benchmark")
    logger.info("=" * 60)
    
    # Run tasks
    try:
        if args.task_id:
            asyncio.run(run_single_task(args.task_id, config))
        elif args.all:
            asyncio.run(run_all_tasks(config))
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
