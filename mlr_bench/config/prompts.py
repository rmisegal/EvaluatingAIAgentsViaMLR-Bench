"""Prompt templates for different research stages."""


# Idea Generation Prompts
IDEA_GENERATION_PROMPT = """You are a creative AI research scientist. Generate a novel research idea for the following task:

Task: {task_title}
Description: {task_description}
Category: {task_category}

Generate a research idea that includes:
1. A clear and concise title
2. Motivation: Why is this research important?
3. Main idea: What is the core concept?
4. Methodology: How would you approach this?
5. Expected outcomes: What results do you anticipate?

Be creative, novel, and feasible. The idea should be implementable within a research project."""


# Literature Review Prompts
LITERATURE_REVIEW_PROMPT = """You are an expert research assistant conducting a literature review.

Research Idea: {idea_title}
Main Concept: {main_idea}

Conduct a literature review that includes:
1. Key findings from related work
2. Identification of the research gap
3. Summary of how existing work relates to this idea

Provide a comprehensive review that situates this research idea in the current state of the field."""


# Proposal Writing Prompts
PROPOSAL_WRITING_PROMPT = """You are an experienced research scientist writing a detailed research proposal.

Task: {task_title}
Research Idea: {idea_title}
Literature Review Summary: {literature_summary}

Write a complete research proposal with the following sections:
1. Abstract (150-200 words)
2. Introduction (explaining the problem and motivation)
3. Related Work (building on the literature review)
4. Methodology (detailed approach and techniques)
5. Expected Results (anticipated outcomes)
6. Experimental Plan (how to validate the approach)

Write in a clear, academic style suitable for a top-tier ML conference."""


# Experiment Coding Prompts
EXPERIMENT_CODING_PROMPT = """You are an expert ML engineer implementing research experiments.

Research Proposal: {proposal_title}
Methodology: {methodology}
Experimental Plan: {experimental_plan}

Generate Python code to implement the proposed experiments. Include:
1. Data loading and preprocessing
2. Model implementation
3. Training loop
4. Evaluation metrics
5. Result logging

Use PyTorch or TensorFlow. Keep code modular and well-documented.
For this educational version, create a simplified implementation that demonstrates the concept."""


# Paper Writing Prompts
PAPER_WRITING_PROMPT = """You are an accomplished research scientist writing a conference paper.

Task: {task_title}
Proposal: {proposal_abstract}
Experimental Results: {experiment_results}

Write a complete research paper with these sections:
1. Abstract
2. Introduction
3. Related Work
4. Methodology
5. Experiments
6. Results
7. Discussion
8. Conclusion
9. References

Write in the style of a top-tier ML conference paper (ICLR, NeurIPS, ICML).
Be rigorous, clear, and thorough."""


# Evaluation Prompts
IDEA_EVALUATION_PROMPT = """You are an expert reviewer evaluating a research idea.

Research Idea:
Title: {idea_title}
Motivation: {motivation}
Main Idea: {main_idea}

Evaluate this idea on the following criteria (score 0-10 for each):
1. Consistency: Is the idea logically coherent?
2. Clarity: Is the idea clearly explained?
3. Novelty: Is this a novel contribution?
4. Feasibility: Can this be realistically implemented?
5. Significance: Would this have impact on the field?

Provide:
- Scores for each criterion
- Overall score (average)
- Detailed feedback
- Strengths and weaknesses"""


PAPER_EVALUATION_PROMPT = """You are an expert reviewer evaluating a research paper.

Paper Title: {paper_title}
Abstract: {abstract}

Evaluate this paper on the following criteria (score 0-10 for each):
1. Clarity: Is the paper well-written and clear?
2. Novelty: Does it present novel contributions?
3. Soundness: Is the methodology sound?
4. Significance: Is this work significant?

Also check for:
- Hallucinated results (unrealistic claims)
- Code quality (if provided)

Provide:
- Scores for each criterion
- Overall score
- Detailed feedback
- Strengths and weaknesses"""
