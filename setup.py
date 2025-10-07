from setuptools import setup, find_packages

setup(
    name="mlr-bench",
    version="0.1.0",
    description="MLR-Bench: Evaluating AI Agents on Open-Ended Machine Learning Research",
    author="MLR-Bench Team",
    python_requires=">=3.11",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "loguru>=0.7.0",
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "aiofiles>=23.0.0",
        "python-dotenv>=1.0.0",
        "ollama>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "mlr-bench=mlr_bench.cli.main:main",
        ],
    },
)
