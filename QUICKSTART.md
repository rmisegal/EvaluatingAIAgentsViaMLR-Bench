# MLR-Bench Quick Start Guide

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd mlr-bench
```

### 2. Run Installation Script

```bash
./install.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Install Google ADK
- Install Flask and SocketIO

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Google AI API Key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

**Get your API key:** https://aistudio.google.com/

---

## Running MLR-Bench

### Option 1: With Visualization (Recommended)

**Terminal 1 - Start Visualization Server:**
```bash
source .venv/bin/activate
python -m mlr_bench.cli.ui_server
```

Open browser at: http://localhost:5000

**Terminal 2 - Run MLR-Bench:**
```bash
source .venv/bin/activate
mlr-bench --task-id iclr2025_bi_align
```

You'll see real-time agent orchestration in your browser! 🎉

### Option 2: Without Visualization

```bash
source .venv/bin/activate
mlr-bench --task-id iclr2025_bi_align
```

---

## Available Tasks

Run any of the 10 tasks from Table 7:

```bash
mlr-bench --task-id iclr2025_bi_align          # Bidirectional Human-AI Alignment
mlr-bench --task-id iclr2025_buildingtrust     # Building Trust in LLMs
mlr-bench --task-id iclr2025_data_problems     # Data Problems for Foundation Models
mlr-bench --task-id iclr2025_dl4c              # Deep Learning for Code
mlr-bench --task-id iclr2025_mldpr             # ML Data Practices
mlr-bench --task-id iclr2025_question          # Uncertainty and Hallucination
mlr-bench --task-id iclr2025_scope             # Scalable Optimization
mlr-bench --task-id iclr2025_scsl              # Spurious Correlation
mlr-bench --task-id iclr2025_verifai           # AI Verification
mlr-bench --task-id iclr2025_wsl               # Neural Network Weights
```

Or run all tasks:

```bash
mlr-bench --all
```

---

## Understanding the Visualization

The web UI shows:

1. **Pipeline Stages** (5 boxes):
   - 💡 Idea Generation
   - 📚 Literature Review
   - 📝 Proposal Writing
   - 🧪 Experimentation
   - 📄 Paper Writing

2. **Real-time Status**:
   - 🟢 Green = Currently running
   - ✅ Green background = Completed
   - ❌ Red = Error

3. **Input/Output**:
   - Each stage shows what it receives and produces

4. **Event Log**:
   - Chronological list of all agent activities

5. **Statistics**:
   - Total events
   - Current stage
   - Overall status

---

## Results

Results are saved to `results/<task_id>/`:

- `idea.json` - Generated research idea
- `literature.json` - Literature review
- `proposal.json` - Research proposal
- `experiment.json` - Experiment results
- `paper.json` - Final paper (JSON)
- `paper.md` - Final paper (Markdown)
- `idea_evaluation.json` - Idea evaluation scores
- `paper_evaluation.json` - Paper evaluation scores

---

## Troubleshooting

### "No module named 'google.adk'"

```bash
pip install google-adk
```

### "GOOGLE_API_KEY not found"

Make sure you:
1. Created `.env` file
2. Added `GOOGLE_API_KEY=your_key`
3. Got your key from https://aistudio.google.com/

### "Port 5000 already in use"

```bash
python -m mlr_bench.cli.ui_server --port 5001
```

### Tests failing

```bash
pytest tests/unit/ -v
```

---

## Next Steps

1. **Read the full README.md** for architecture details
2. **Explore the code** in `mlr_bench/`
3. **Modify prompts** in `mlr_bench/config/prompts.py`
4. **Add new tasks** in `data/tasks/tasks.json`
5. **Contribute** - see CONTRIBUTING.md

---

## Educational Goals

This implementation teaches:

✅ **Multi-agent orchestration** - How agents work together  
✅ **Event-driven architecture** - Real-time communication  
✅ **MCP integration** - External tool usage  
✅ **Pipeline design** - Sequential workflow  
✅ **Evaluation systems** - Multi-judge consensus  

---

## Support

- **Issues:** Open a GitHub issue
- **Original Research:** https://github.com/chchenhui/mlrbench
- **Google ADK Docs:** https://google.github.io/adk-docs/

---

**All rights reserved to Dr. Yoram Segal - Educational use only**
