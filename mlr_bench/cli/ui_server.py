"""CLI for starting visualization UI server."""

import argparse
from loguru import logger

from mlr_bench.ui.server import start_server


def main():
    """Main entry point for UI server."""
    parser = argparse.ArgumentParser(
        description="MLR-Bench Visualization Server"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Server port (default: 5000)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("MLR-Bench Visualization Server")
    logger.info("=" * 60)
    logger.info(f"Open your browser at: http://localhost:{args.port}")
    logger.info("=" * 60)
    
    start_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
