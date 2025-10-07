"""Flask server for visualization UI."""

import json
from pathlib import Path
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from loguru import logger

from mlr_bench.ui.event_bus import event_bus, AgentEvent


app = Flask(__name__, 
            template_folder=str(Path(__file__).parent / "templates"),
            static_folder=str(Path(__file__).parent / "static"))
app.config['SECRET_KEY'] = 'mlr-bench-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/events')
def get_events():
    """Get recent events."""
    limit = 100
    events = event_bus.get_events(limit=limit)
    return jsonify(events)


@app.route('/api/clear')
def clear_events():
    """Clear all events."""
    event_bus.clear()
    return jsonify({"status": "success"})


@app.route('/api/event', methods=['POST'])
def receive_event():
    """Receive event from client and broadcast to UI.
    
    This endpoint allows the mlr-bench client (running in a separate process)
    to send events to the UI server.
    """
    from flask import request
    
    try:
        event_data = request.get_json()
        
        # Create AgentEvent from received data
        event = AgentEvent(
            agent_name=event_data['agent_name'],
            stage=event_data['stage'],
            event_type=event_data['event_type'],
            data=event_data.get('data', {})
        )
        event.timestamp = event_data.get('timestamp', event.timestamp)
        
        # Add to event bus
        event_bus.events.append(event)
        
        # Broadcast to all connected WebSocket clients
        socketio.emit('agent_event', event.to_dict())
        
        logger.debug(f"Received and broadcasted event: {event.agent_name} - {event.event_type}")
        
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error receiving event: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info("Client connected to WebSocket")
    emit('connected', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info("Client disconnected from WebSocket")


def broadcast_event(event: AgentEvent):
    """Broadcast event to all connected clients.
    
    Args:
        event: Agent event
    """
    socketio.emit('agent_event', event.to_dict())


def start_server(host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
    """Start Flask server.
    
    Args:
        host: Server host
        port: Server port
        debug: Debug mode
    """
    # Subscribe to event bus
    event_bus.subscribe(broadcast_event)
    
    logger.info(f"Starting visualization server on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
