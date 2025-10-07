// Connect to WebSocket
const socket = io();

let eventCount = 0;
let currentStage = 'None';

// Stage mapping
const stageMap = {
    'idea': 'idea',
    'literature': 'literature',
    'proposal': 'proposal',
    'experiment': 'experiment',
    'paper': 'paper',
    'evaluation': 'evaluation'
};

// Connection handlers
socket.on('connect', () => {
    console.log('WebSocket connected');
    updateStatus('Connected');
    showConnectionIndicator(true);
});

socket.on('disconnect', () => {
    console.log('WebSocket disconnected');
    updateStatus('Disconnected');
    showConnectionIndicator(false);
});

socket.on('connected', (data) => {
    console.log('Connected to server:', data);
    updateStatus('Connected');
    showConnectionIndicator(true);
});

// Handle agent events
socket.on('agent_event', (event) => {
    console.log('Agent event:', event);
    handleAgentEvent(event);
});

function handleAgentEvent(event) {
    eventCount++;
    updateStats();
    
    const stage = event.stage;
    const eventType = event.event_type;
    
    // Update client status (client is active)
    updateClientStatus(true);
    
    // Store agent data for modal
    storeAgentData(stage, eventType, event.data);
    
    // Update stage status
    if (stageMap[stage]) {
        updateStageStatus(stage, eventType, event.data);
    }
    
    // Add to event log
    addLogEntry(event);
    
    // Update current stage
    if (eventType === 'started') {
        currentStage = stage;
        document.getElementById('stat-stage').textContent = stage;
    }
}

function updateStageStatus(stage, eventType, data) {
    const stageEl = document.getElementById(`stage-${stage}`);
    const statusEl = document.getElementById(`status-${stage}`);
    const dataEl = document.getElementById(`data-${stage}`);
    
    // Remove all status classes
    stageEl.classList.remove('active', 'completed', 'error');
    
    // Update based on event type
    switch(eventType) {
        case 'started':
            stageEl.classList.add('active');
            statusEl.textContent = '🟢 Running...';
            statusEl.style.color = '#4CAF50';
            break;
        case 'completed':
            stageEl.classList.add('completed');
            statusEl.textContent = '✅ Completed';
            statusEl.style.color = '#4CAF50';
            
            // Show evaluation scores if this is evaluation stage
            if (stage === 'evaluation' && data && data.scores) {
                updateEvaluationScores(data.scores);
            }
            break;
        case 'error':
            stageEl.classList.add('error');
            statusEl.textContent = '❌ Error';
            statusEl.style.color = '#f44336';
            break;
        case 'input':
            dataEl.innerHTML = `<strong>Input:</strong> ${formatData(data)}`;
            break;
        case 'output':
            dataEl.innerHTML = `<strong>Output:</strong> ${formatData(data)}`;
            
            // Show evaluation scores if this is evaluation stage
            if (stage === 'evaluation' && data && data.scores) {
                updateEvaluationScores(data.scores);
            }
            break;
    }
}

function updateEvaluationScores(scores) {
    const scoresDiv = document.getElementById('scores-evaluation');
    if (scoresDiv && scores) {
        scoresDiv.style.display = 'block';
        
        // Update individual scores
        if (scores.idea_score !== undefined) {
            document.getElementById('score-idea-judge').textContent = scores.idea_score.toFixed(1);
        }
        if (scores.paper_score !== undefined) {
            document.getElementById('score-paper-judge').textContent = scores.paper_score.toFixed(1);
        }
        if (scores.average !== undefined) {
            document.getElementById('score-average').textContent = scores.average.toFixed(1);
        }
    }
}

function formatData(data) {
    if (!data) return 'N/A';
    
    if (typeof data === 'string') {
        return data.substring(0, 100) + (data.length > 100 ? '...' : '');
    }
    
    if (typeof data === 'object') {
        const str = JSON.stringify(data, null, 2);
        return str.substring(0, 100) + (str.length > 100 ? '...' : '');
    }
    
    return String(data);
}

function addLogEntry(event) {
    const logContent = document.getElementById('event-log');
    const entry = document.createElement('div');
    entry.className = `log-entry ${event.event_type}`;
    
    const timestamp = new Date(event.timestamp).toLocaleTimeString();
    
    entry.innerHTML = `
        <span class="log-timestamp">[${timestamp}]</span>
        <strong>${event.agent_name}</strong> - ${event.stage} - ${event.event_type}
    `;
    
    logContent.insertBefore(entry, logContent.firstChild);
    
    // Keep only last 50 entries
    while (logContent.children.length > 50) {
        logContent.removeChild(logContent.lastChild);
    }
}

function updateStats() {
    document.getElementById('stat-events').textContent = eventCount;
}

function updateStatus(status) {
    document.getElementById('stat-status').textContent = status;
}

function clearEvents() {
    fetch('/api/clear')
        .then(response => response.json())
        .then(data => {
            document.getElementById('event-log').innerHTML = '';
            eventCount = 0;
            updateStats();
            
            // Reset all stages
            const stages = ['idea', 'literature', 'proposal', 'experiment', 'paper'];
            stages.forEach(stage => {
                const stageEl = document.getElementById(`stage-${stage}`);
                const statusEl = document.getElementById(`status-${stage}`);
                const dataEl = document.getElementById(`data-${stage}`);
                
                stageEl.classList.remove('active', 'completed', 'error');
                statusEl.textContent = 'Waiting...';
                statusEl.style.color = '#666';
                dataEl.innerHTML = '';
            });
            
            currentStage = 'None';
            document.getElementById('stat-stage').textContent = 'None';
        });
}

// Load initial events on page load
window.addEventListener('load', () => {
    fetch('/api/events')
        .then(response => response.json())
        .then(events => {
            events.forEach(event => handleAgentEvent(event));
        });
});


// Show/hide connection indicator
function showConnectionIndicator(connected) {
    const serverEl = document.getElementById('stat-server');
    if (connected) {
        serverEl.textContent = '🟢 Connected';
        serverEl.style.color = '#10b981';
    } else {
        serverEl.textContent = '🔴 Disconnected';
        serverEl.style.color = '#ef4444';
    }
}

// Track client activity
let clientActivityTimeout = null;
let clientActive = false;

function updateClientStatus(active) {
    const clientEl = document.getElementById('stat-client');
    if (active) {
        clientEl.textContent = '🟢 Running';
        clientEl.style.color = '#10b981';
        clientActive = true;
        
        // Reset timeout
        if (clientActivityTimeout) {
            clearTimeout(clientActivityTimeout);
        }
        
        // Set client to idle after 10 seconds of no activity
        clientActivityTimeout = setTimeout(() => {
            clientEl.textContent = '⚪ Idle';
            clientEl.style.color = '#666';
            clientActive = false;
        }, 10000);
    } else {
        clientEl.textContent = '⚪ Idle';
        clientEl.style.color = '#666';
        clientActive = false;
    }
}

// Agent data storage
const agentData = {
    idea: { systemPrompt: '', input: '', output: '' },
    literature: { systemPrompt: '', input: '', output: '' },
    proposal: { systemPrompt: '', input: '', output: '' },
    experiment: { systemPrompt: '', input: '', output: '' },
    paper: { systemPrompt: '', input: '', output: '' },
    evaluation: { systemPrompt: '', input: '', output: '' }
};

// System prompts for each agent
const systemPrompts = {
    idea: `You are a creative AI research scientist. Generate a novel research idea.

Generate a research idea that includes:
1. A clear and concise title
2. Motivation: Why is this research important?
3. Main idea: What is the core concept?
4. Methodology: How would you approach this?
5. Expected outcomes: What results do you anticipate?

Be creative, novel, and feasible.`,
    
    literature: `You are an expert research assistant conducting a literature review.

Conduct a literature review that includes:
1. Key findings from related work
2. Identification of the research gap
3. Summary of how existing work relates to this idea

Provide a comprehensive review that situates this research idea in the current state of the field.`,
    
    proposal: `You are an experienced research scientist writing a detailed research proposal.

Write a complete research proposal with the following sections:
1. Abstract (150-200 words)
2. Introduction (explaining the problem and motivation)
3. Related Work (building on the literature review)
4. Methodology (detailed approach and techniques)
5. Expected Results (anticipated outcomes)
6. Experimental Plan (how to validate the approach)

Write in a clear, academic style suitable for a top-tier ML conference.`,
    
    experiment: `You are an expert ML engineer implementing research experiments.

Generate Python code to implement the proposed experiments. Include:
1. Data loading and preprocessing
2. Model implementation
3. Training loop
4. Evaluation metrics
5. Result logging

Use PyTorch or TensorFlow. Keep code modular and well-documented.`,
    
    paper: `You are an accomplished research scientist writing a conference paper.

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

Write in the style of a top-tier ML conference paper (ICLR, NeurIPS, ICML).`,
    
    evaluation: `You are an expert reviewer evaluating research work.

Evaluate the research on multiple criteria:
1. Novelty and originality
2. Technical soundness
3. Clarity and presentation
4. Experimental validation
5. Significance and impact

Provide scores (1-10) and detailed feedback for each criterion.`
};

// Store agent data when events arrive
function storeAgentData(stage, eventType, data) {
    if (!agentData[stage]) return;
    
    agentData[stage].systemPrompt = systemPrompts[stage] || 'No system prompt available';
    
    if (eventType === 'input') {
        agentData[stage].input = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    } else if (eventType === 'output') {
        agentData[stage].output = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Open agent modal
function openAgentModal(stage) {
    const modal = document.getElementById('agent-modal');
    const data = agentData[stage];
    
    if (!data) return;
    
    // Update modal title
    const stageNames = {
        idea: 'Idea Generator',
        literature: 'Literature Reviewer',
        proposal: 'Proposal Writer',
        experiment: 'Experimenter',
        paper: 'Paper Writer',
        evaluation: 'Evaluator (Judge)'
    };
    
    document.getElementById('modal-title').textContent = stageNames[stage] || 'Agent Details';
    
    // Update content
    document.getElementById('modal-system-prompt').textContent = data.systemPrompt || 'No system prompt available';
    document.getElementById('modal-input').textContent = data.input || 'No input data yet';
    document.getElementById('modal-output').textContent = data.output || 'No output data yet';
    
    // Show modal
    modal.style.display = 'block';
}

// Close agent modal
function closeAgentModal() {
    document.getElementById('agent-modal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('agent-modal');
    if (event.target === modal) {
        closeAgentModal();
    }
}

// Add click handlers to stages
document.addEventListener('DOMContentLoaded', () => {
    const stages = ['idea', 'literature', 'proposal', 'experiment', 'paper', 'evaluation'];
    stages.forEach(stage => {
        const stageEl = document.getElementById(`stage-${stage}`);
        if (stageEl) {
            stageEl.addEventListener('click', () => openAgentModal(stage));
        }
    });
});
