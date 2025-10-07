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
