# MLR-Bench: Multi-Agent Research Orchestration System with Real-Time GUI

**Educational Implementation for Teaching Multi-Agent Orchestration**

---

## Abstract

MLR-Bench is an educational implementation of a multi-agent AI system for conducting open-ended machine learning research. This project demonstrates agent orchestration, inter-agent communication, tool usage, and real-time visualization through a complete research pipeline: Idea Generation → Literature Review → Proposal Writing → Experimentation → Paper Writing. Built with Google AI Agent Development Kit (ADK), it features 10 Trustworthy AI research tasks from the original paper, a web-based real-time GUI for monitoring agent activities, and comprehensive installation scripts for both Linux and Windows. The focus is on teaching orchestration mechanics and agent communication protocols rather than achieving high-quality research outputs.

---

## Table of Contents

1. [Credits and Attribution](#credits-and-attribution)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Linux/WSL Installation](#linuxwsl-installation)
   - [Windows PowerShell Installation](#windows-powershell-installation)
4. [Running MLR-Bench](#running-mlr-bench)
   - [Starting the Visualization UI](#starting-the-visualization-ui)
   - [Running a Single Task](#running-a-single-task)
   - [Running All Tasks](#running-all-tasks)
5. [Uninstallation](#uninstallation)
   - [Linux/WSL Uninstallation](#linuxwsl-uninstallation)
   - [Windows PowerShell Uninstallation](#windows-powershell-uninstallation)
6. [Real-Time Visualization UI](#real-time-visualization-ui)
7. [Architecture and Components](#architecture-and-components)
8. [Available Research Tasks](#available-research-tasks)
9. [Project Structure](#project-structure)
10. [Testing](#testing)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)
13. [License](#license)

---

## Credits and Attribution

### Original Research Paper

This implementation is based on the research paper:

**"Evaluating AI Agents on Open-Ended Machine Learning Research"**

- **Paper Link:** https://arxiv.org/abs/2505.19955
- **Original Authors:** Chenhui Zhang (Lead Author) and colleagues
- **Original Repository:** https://github.com/chchenhui/mlrbench

### Educational Implementation

**All rights reserved to Dr. Yoram Segal**

This code is developed for **educational purposes only** to teach:
- Multi-agent orchestration
- Agent communication protocols
- Agent instruction design
- Tool usage in agent systems
- Real-time monitoring and visualization

The focus is on learning the orchestration mechanics rather than achieving high-quality research outputs.

---

## Quick Start

### Download the Project

```bash
# Clone the repository
git clone https://github.com/rmisegal/EvaluatingAIAgentsViaMLR-Bench.git
cd EvaluatingAIAgentsViaMLR-Bench
```

### Install and Run (Linux/WSL)

```bash
# Run installation script
./install_linux.sh

# The script will:
# 1. Check Python and Node.js
# 2. Create virtual environment
# 3. Install all dependencies
# 4. Ask for your Google AI API Key
# 5. Configure environment

# After installation, start the UI (Terminal 1)
source .venv/bin/activate
python -m mlr_bench.cli.ui_server

# Run a task (Terminal 2)
source .venv/bin/activate
mlr-bench --task-id iclr2025_bi_align

# Open browser: http://localhost:5000
```

### Install and Run (Windows PowerShell)

```powershell
# Run installation script
.\install_windows.ps1

# The script will:
# 1. Check Python and Node.js
# 2. Create virtual environment
# 3. Install all dependencies
# 4. Ask for your Google AI API Key
# 5. Configure PATH and environment

# Restart PowerShell, then start the UI (Terminal 1)
.\.venv\Scripts\Activate.ps1
python -m mlr_bench.cli.ui_server

# Run a task (Terminal 2)
.\.venv\Scripts\Activate.ps1
mlr-bench --task-id iclr2025_bi_align

# Open browser: http://localhost:5000
```

---

## Installation

### Prerequisites

Before installation, ensure you have:

1. **Python 3.11 or higher**
   - Linux: `sudo apt install python3.11 python3.11-venv`
   - Windows: Download from https://www.python.org/downloads/
   - Verify: `python --version` or `python3 --version`

2. **Node.js** (optional, for future extensions)
   - Linux: `sudo apt install nodejs npm`
   - Windows: Download from https://nodejs.org/
   - Verify: `node --version`

3. **Google AI API Key** (required)
   - Get your free API key from: https://aistudio.google.com/
   - The installation script will ask for this key
   - **Security:** Your key is stored locally only in `.env` file and will NOT be uploaded to GitHub

4. **Git** (for cloning the repository)
   - Linux: `sudo apt install git`
   - Windows: Download from https://git-scm.com/

---

### Linux/WSL Installation

**Step 1: Download the Project**

```bash
# Clone the repository
git clone https://github.com/rmisegal/EvaluatingAIAgentsViaMLR-Bench.git
cd EvaluatingAIAgentsViaMLR-Bench
```

**Step 2: Run Installation Script**

```bash
# Make the script executable (if needed)
chmod +x install_linux.sh

# Run the installation
./install_linux.sh
```

**What the script does:**

1. ✅ Backs up your current environment to `.backup/environment_backup.txt`
2. ✅ Checks Python 3.11+ is installed
3. ✅ Checks Node.js (optional)
4. ✅ Creates Python virtual environment in `.venv/`
5. ✅ Installs all required packages:
   - MLR-Bench package
   - Google ADK
   - Flask + SocketIO (for UI)
   - All dependencies
6. ✅ Asks for your **Google AI API Key**
   - **Security Notice:** Your key will be stored ONLY in the local `.env` file
   - The `.env` file is in `.gitignore` and will NOT be uploaded to GitHub
   - Your API key will NOT leave your local machine
7. ✅ Asks for **Brave API Key** (optional, for enhanced search)
8. ✅ Configures PATH and PYTHONPATH in your shell RC file
9. ✅ Creates directories: `results/`, `workspaces/`, `logs/`
10. ✅ Runs environment check to verify everything works

**Step 3: Activate Virtual Environment**

```bash
# Activate the virtual environment
source .venv/bin/activate

# Or use the alias (if you reloaded your shell)
mlr-bench-activate
```

**Step 4: Verify Installation**

```bash
# Run environment check
python test_environment.py

# You should see:
# ✅ PASS: Python Version
# ✅ PASS: Node.js
# ✅ PASS: Python Packages
# ✅ PASS: Flask + SocketIO
# ✅ PASS: API Keys
# ✅ PASS: Project Structure
# ✅ PASS: Data Files
# Total: 7/7 checks passed
```

---

### Windows PowerShell Installation

**Step 1: Enable Script Execution**

Open PowerShell as Administrator and run:

```powershell
# Allow running scripts (required once)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Step 2: Download the Project**

```powershell
# Clone the repository
git clone https://github.com/rmisegal/EvaluatingAIAgentsViaMLR-Bench.git
cd EvaluatingAIAgentsViaMLR-Bench
```

**Step 3: Run Installation Script**

```powershell
# Run the installation script
.\install_windows.ps1
```

**What the script does:**

1. ✅ Backs up your current environment to `.backup\environment_backup.txt`
2. ✅ Checks Python 3.11+ is installed
3. ✅ Checks Node.js (optional)
4. ✅ Creates Python virtual environment in `.venv\`
5. ✅ Installs all required packages:
   - MLR-Bench package
   - Google ADK
   - Flask + SocketIO (for UI)
   - All dependencies
6. ✅ Asks for your **Google AI API Key**
   - **Security Notice:** Your key will be stored ONLY in the local `.env` file
   - The `.env` file is in `.gitignore` and will NOT be uploaded to GitHub
   - Your API key will NOT leave your local machine
   - The key is also set as a User environment variable for convenience
7. ✅ Asks for **Brave API Key** (optional, for enhanced search)
8. ✅ Configures PATH and PYTHONPATH as User environment variables
9. ✅ Creates directories: `results\`, `workspaces\`, `logs\`
10. ✅ Runs environment check to verify everything works

**Step 4: Restart PowerShell**

Close and reopen PowerShell to load the new PATH settings.

**Step 5: Activate Virtual Environment**

```powershell
# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

**Step 6: Verify Installation**

```powershell
# Run environment check
python test_environment.py

# You should see:
# ✅ PASS: Python Version
# ✅ PASS: Node.js
# ✅ PASS: Python Packages
# ✅ PASS: Flask + SocketIO
# ✅ PASS: API Keys
# ✅ PASS: Project Structure
# ✅ PASS: Data Files
# Total: 7/7 checks passed
```

---

## Running MLR-Bench

MLR-Bench consists of two components that run simultaneously:

1. **Visualization UI Server** - Web interface for real-time monitoring
2. **MLR-Bench Agent System** - The actual research pipeline

### Starting the Visualization UI

The visualization UI provides real-time monitoring of agent activities, data flow, and pipeline status.

**Linux/WSL:**

```bash
# Terminal 1: Start UI Server
source .venv/bin/activate
python -m mlr_bench.cli.ui_server

# Server will start on http://localhost:5000
# Keep this terminal running
```

**Windows PowerShell:**

```powershell
# Terminal 1: Start UI Server
.\.venv\Scripts\Activate.ps1
python -m mlr_bench.cli.ui_server

# Server will start on http://localhost:5000
# Keep this terminal running
```

**Custom Port:**

```bash
# If port 5000 is busy, use a different port
python -m mlr_bench.cli.ui_server --port 5001
```

**Open the UI:**

Open your web browser and navigate to:
```
http://localhost:5000
```

You should see the MLR-Bench Agent Orchestration interface with 5 pipeline stages.

---

### Running a Single Task

**Linux/WSL:**

```bash
# Terminal 2: Run MLR-Bench
source .venv/bin/activate
mlr-bench --task-id iclr2025_bi_align

# Watch the UI in your browser for real-time updates!
```

**Windows PowerShell:**

```powershell
# Terminal 2: Run MLR-Bench
.\.venv\Scripts\Activate.ps1
mlr-bench --task-id iclr2025_bi_align

# Watch the UI in your browser for real-time updates!
```

**What happens:**

1. The agent system loads the task
2. Each stage executes sequentially:
   - 💡 Idea Generation
   - 📚 Literature Review
   - 📝 Proposal Writing
   - 🧪 Experimentation
   - 📄 Paper Writing
3. The UI updates in real-time showing:
   - Active stage (green border)
   - Input/output data
   - Event log
   - Statistics
4. Results are saved to `results/<task_id>/`

---

### Running All Tasks

To run all 10 research tasks sequentially:

```bash
mlr-bench --all
```

**Note:** This will take a long time (hours) as each task goes through the complete pipeline.

---

### Available Command-Line Options

```bash
# Run specific task
mlr-bench --task-id <task_id>

# Run all tasks
mlr-bench --all

# List available tasks
mlr-bench --list-tasks

# Specify output directory
mlr-bench --task-id <task_id> --output-dir ./my_results

# Enable debug logging
mlr-bench --task-id <task_id> --log-level DEBUG

# Run with custom model
mlr-bench --task-id <task_id> --model gemini-2.0-flash
```

---

## Uninstallation

### Linux/WSL Uninstallation

```bash
# Run uninstallation script
./uninstall_linux.sh
```

**What the script does:**

1. ❓ Asks for confirmation
2. 🗑️ Removes virtual environment (`.venv/`)
3. 🔧 Cleans shell configuration (`.bashrc` or `.zshrc`)
   - Removes MLR-Bench PATH entries
   - Creates backup of RC file
4. ❓ Asks if you want to remove results and workspaces
5. ❓ Asks if you want to remove `.env` file (contains API keys)
   - Creates backup before removal
   - Removes API keys from environment
6. 📋 Shows environment restoration information
7. ✅ Preserves backup files in `.backup/`

**To restore your original environment:**

Check the backup file:
```bash
cat .backup/environment_backup.txt
```

---

### Windows PowerShell Uninstallation

```powershell
# Run uninstallation script
.\uninstall_windows.ps1
```

**What the script does:**

1. ❓ Asks for confirmation
2. 🗑️ Removes virtual environment (`.venv\`)
3. 🔧 Cleans environment variables
   - Removes MLR-Bench from PATH
   - Removes PYTHONPATH entries
4. ❓ Asks if you want to remove results and workspaces
5. ❓ Asks if you want to remove `.env` file (contains API keys)
   - Creates backup before removal
   - Removes API keys from User environment variables
6. 📋 Shows environment restoration information
7. ✅ Preserves backup files in `.backup\`

**Important:** Restart PowerShell after uninstallation for changes to take effect.

**To restore your original environment:**

Check the backup file:
```powershell
Get-Content .backup\environment_backup.txt
```

---

## Real-Time Visualization UI

MLR-Bench includes a **real-time web-based visualization** that shows the agent orchestration in action.

![MLR-Bench UI](docs/images/ui_screenshot.webp)

### UI Components

#### 1. Pipeline Visualization (Top Section)

Five connected stages showing the research pipeline:

- **💡 Idea Generation** - Generates novel research ideas
- **📚 Literature Review** - Reviews related academic papers  
- **📝 Proposal Writing** - Writes detailed research proposals
- **🧪 Experimentation** - Implements and runs experiments
- **📄 Paper Writing** - Writes the final research paper

**Stage Colors:**
- **White background** - Waiting (not started yet)
- **Green border + scale effect** - Currently active/running
- **Light green background** - Completed successfully
- **Light red background** - Error occurred

#### 2. Stage Status Indicators

Each stage shows:
- **🟢 Running...** - Agent is currently processing (green text)
- **✅ Completed** - Stage finished successfully (green text)
- **❌ Error** - Stage encountered an error (red text)
- **Waiting...** - Stage hasn't started yet (gray text)

#### 3. Input/Output Display

Below each stage status, you'll see:
- **Input:** What data the agent received (truncated to 100 chars)
- **Output:** What the agent produced (truncated to 100 chars)

This shows the **data flow between agents** in real-time.

#### 4. Event Log (Middle Section)

A chronological log of all agent activities:
- **Blue border** - Agent started
- **Green border** - Agent completed
- **Red border** - Error occurred

Each entry shows:
- Timestamp
- Agent name
- Stage name
- Event type

The log auto-scrolls and keeps the last 50 events.

#### 5. Statistics (Bottom Section)

Three key metrics:

- **Total Events** - Number of events since start
- **Active Stage** - Which stage is currently running
- **Status** - Overall system status (Connected/Idle/Running)

### UI Features

✅ **Real-time Updates** - WebSocket connection for instant updates  
✅ **Color-Coded Status** - Easy visual identification of agent states  
✅ **Data Flow Visualization** - See inputs/outputs between agents  
✅ **Event History** - Complete log of all activities  
✅ **Clear Button** - Reset the visualization  
✅ **Responsive Design** - Works on desktop and mobile  

### Understanding the Orchestration

The UI helps you understand:

1. **Sequential Flow** - Agents execute in order (Idea → Literature → Proposal → Experiment → Paper)
2. **Data Passing** - Each agent receives output from previous agents
3. **Real-time Processing** - See exactly when each agent starts/stops
4. **Error Handling** - Immediately see if any stage fails
5. **Timing** - Understand how long each stage takes

### Troubleshooting UI

**Port 5000 already in use:**
```bash
python -m mlr_bench.cli.ui_server --port 5001
```

**UI not updating:**
- Check that WebSocket connection shows "Connected" in statistics
- Refresh the browser page
- Check browser console for errors (F12)

**Server not starting:**
```bash
pip install flask flask-socketio aiohttp
```

---

## Architecture and Components

> **📐 For detailed system architecture, data flow, and communication protocols, see [ARCHITECTURE.md](ARCHITECTURE.md)**

The document includes:
- Complete system block diagram with all components
- Detailed explanation of each module (with language tags: [PY], [JS], [HTML], [MCP], etc.)
- Communication protocols (HTTP, WebSocket, MCP)
- Data flow examples
- 100-word summary of the architecture

### Quick Overview

**Agent System:**

```
MLRAgent (Orchestrator) [PY]
├── IdeaGenerator [PY]
├── LiteratureReviewer [PY]
├── ProposalWriter [PY]
├── Experimenter [PY]
└── PaperWriter [PY]
```

**Communication:**
- Client → Server: HTTP POST (port 5000) [HTTP/JSON]
- Server → Browser: WebSocket [WS]
- Agents → Gemini: HTTP API [HTTP/JSON]
- Tools → External Services: MCP [MCP]

**Judge System:**

```
MLRJudge [PY]
├── IdeaEvaluator [PY]
└── PaperEvaluator [PY]
```

**Tools Available to Agents [PY]:**

1. **search_papers(query)** - Search academic papers via Semantic Scholar API [MCP/HTTP]
2. **execute_python_code(code)** - Execute Python code in sandbox [MCP]
3. **save_to_file(path, content)** - Save files to workspace [PY]
4. **format_paper_section(section, content)** - Format paper sections [PY]
5. **calculate_average_score(scores)** - Calculate evaluation scores [PY]
6. **extract_scores_from_text(text)** - Parse scores from text [PY]

**Data Models [PY/JSON]:**

- **Task** - Research task definition [JSON]
- **ResearchIdea** - Generated idea with novelty and feasibility [JSON]
- **LiteratureReview** - Related work and references [JSON]
- **ResearchProposal** - Detailed proposal with methodology [JSON]
- **ExperimentResult** - Code, results, and analysis [JSON]
- **ResearchPaper** - Complete paper with all sections [TXT/JSON]
- **EvaluationResult** - Multi-dimensional scores and feedback [JSON]

---

## Available Research Tasks

The system includes **10 Trustworthy AI research tasks** from Table 7 of the original paper:

| Task ID | Topic | Category |
|---------|-------|----------|
| `iclr2025_bi_align` | Bidirectional Human-AI Alignment | Trustworthy AI |
| `iclr2025_buildingtrust` | Building Trust in Language Models | Trustworthy AI |
| `iclr2025_data_problems` | Data Problems for Foundation Models | Trustworthy AI |
| `iclr2025_dl4c` | Deep Learning for Code | LLM/VLM |
| `iclr2025_mldpr` | ML Data Practices and Repositories | Trustworthy AI |
| `iclr2025_question` | Uncertainty and Hallucination | LLM/VLM |
| `iclr2025_scope` | Scalable Optimization | Trustworthy AI |
| `iclr2025_scsl` | Spurious Correlation | Trustworthy AI |
| `iclr2025_verifai` | AI Verification | Trustworthy AI |
| `iclr2025_wsl` | Neural Network Weights | ML Theory |

**Note:** The full dataset of 201 tasks is available in the original repository: https://github.com/chchenhui/mlrbench

---

## Project Structure

```
EvaluatingAIAgentsViaMLR-Bench/
├── mlr_bench/                  # Main package
│   ├── agent/                  # Agent implementations
│   │   ├── stages/            # Stage-specific agents
│   │   │   ├── idea_generator.py
│   │   │   ├── literature_reviewer.py
│   │   │   ├── proposal_writer.py
│   │   │   ├── experimenter.py
│   │   │   └── paper_writer.py
│   │   ├── mlr_agent.py       # Main orchestrator
│   │   ├── agent_wrapper.py   # Event broadcasting wrapper
│   │   └── tools.py           # Agent tools
│   ├── judge/                  # Evaluation system
│   │   ├── evaluators/        # Stage-specific evaluators
│   │   └── mlr_judge.py       # Main judge
│   ├── models/                 # Data models
│   ├── mcp/                    # MCP integration (future)
│   ├── ui/                     # Visualization UI
│   │   ├── templates/         # HTML templates
│   │   ├── static/            # CSS and JavaScript
│   │   ├── event_bus.py       # Event broadcasting
│   │   └── server.py          # Flask server
│   ├── config/                 # Configuration
│   ├── tasks/                  # Task management
│   ├── utils/                  # Utilities
│   └── cli/                    # Command-line interface
├── data/                       # Task definitions
│   └── tasks/
│       └── tasks.json         # 10 research tasks
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── docs/                       # Documentation
│   └── images/                # Screenshots
├── results/                    # Output directory (created on first run)
├── workspaces/                 # Agent workspaces (created on first run)
├── logs/                       # Log files (created on first run)
├── install_linux.sh           # Linux installation script
├── install_windows.ps1        # Windows installation script
├── uninstall_linux.sh         # Linux uninstallation script
├── uninstall_windows.ps1      # Windows uninstallation script
├── test_environment.py        # Environment check script
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── QUICKSTART.md              # Quick start guide
├── CONTRIBUTING.md            # Contribution guidelines
└── LICENSE                    # MIT License
```

---

## Testing

### Run All Tests

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/WSL
# or
.\.venv\Scripts\Activate.ps1  # Windows

# Run all tests
pytest tests/ -v
```

### Run Specific Tests

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_models.py -v
```

### Environment Check

```bash
# Check if everything is configured correctly
python test_environment.py
```

**Checks:**
- ✅ Python 3.11+
- ✅ Node.js
- ✅ All Python packages
- ✅ Flask + SocketIO
- ✅ API keys
- ✅ Project structure
- ✅ Data files

### Client-Server Communication Test

```bash
# Test communication between client and UI server
# (Start UI server first in another terminal)
python test_client_server_communication.py
```

**Tests:**
- ✅ UI server running (port 5000)
- ✅ HTTP POST /api/event
- ✅ HTTP GET /api/events
- ✅ Event Bus → HTTP → Server
- ✅ WebSocket endpoint

### Internet and API Check

```bash
# Test Semantic Scholar API connection
python test_internet.py

# Test tool functionality
python test_tools.py
```

### Run All Tests

```bash
# Run everything
pytest tests/unit/ -v
python test_environment.py
python test_client_server_communication.py
```

---

## Troubleshooting

### Common Issues

**1. Python version error**
```
Error: Python 3.11+ required
```
Solution: Install Python 3.11 or higher from https://www.python.org/

**2. API Key not set**
```
Error: GOOGLE_API_KEY not found
```
Solution: 
- Edit `.env` file and add your key
- Or re-run installation script
- Get key from: https://aistudio.google.com/

**3. Port 5000 already in use**
```
Error: Address already in use
```
Solution: Use a different port
```bash
python -m mlr_bench.cli.ui_server --port 5001
```

**4. Module not found**
```
ModuleNotFoundError: No module named 'mlr_bench'
```
Solution: Activate virtual environment
```bash
source .venv/bin/activate  # Linux/WSL
.\.venv\Scripts\Activate.ps1  # Windows
```

**5. Permission denied (Linux)**
```
Permission denied: ./install_linux.sh
```
Solution: Make script executable
```bash
chmod +x install_linux.sh
```

**6. Execution policy error (Windows)**
```
cannot be loaded because running scripts is disabled
```
Solution: Enable script execution (as Administrator)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**7. UI not updating**
- Check WebSocket connection status in UI (should show "Connected")
- Refresh browser page
- Check browser console for errors (F12)
- Restart UI server

**8. Agent errors during execution**
- Check logs in `logs/` directory
- Verify API key is valid
- Check internet connection
- Try with `--log-level DEBUG` for detailed output

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/rmisegal/EvaluatingAIAgentsViaMLR-Bench.git
cd EvaluatingAIAgentsViaMLR-Bench

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/ -v

# Format code
black mlr_bench/

# Lint code
flake8 mlr_bench/
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Educational Use

**All rights reserved to Dr. Yoram Segal**

This code is provided for **educational purposes only**. It is designed to teach:
- Multi-agent orchestration
- Agent communication protocols
- Agent instruction design
- Tool usage in agent systems
- Real-time monitoring and visualization

The focus is on learning the orchestration mechanics rather than achieving high-quality research outputs.

### Original Research

This implementation is based on the research paper:
- **"Evaluating AI Agents on Open-Ended Machine Learning Research"**
- **Paper:** https://arxiv.org/abs/2505.19955
- **Authors:** Chenhui Zhang and colleagues
- **Original Repository:** https://github.com/chchenhui/mlrbench

---

## Support

For questions, issues, or suggestions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [QUICKSTART.md](QUICKSTART.md) for quick reference
3. Open an issue on GitHub: https://github.com/rmisegal/EvaluatingAIAgentsViaMLR-Bench/issues
4. Contact: Dr. Yoram Segal

---

## Acknowledgments

- Original MLR-Bench research team for the groundbreaking work
- Google AI for the Agent Development Kit (ADK)
- Semantic Scholar for the free academic search API
- All contributors and students using this educational tool

---

**Happy Learning! 🎓🤖**
