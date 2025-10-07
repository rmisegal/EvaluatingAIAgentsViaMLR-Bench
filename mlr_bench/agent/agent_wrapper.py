"""Wrapper for agents with event bus integration."""

from typing import Any, Dict
from functools import wraps
from loguru import logger

from mlr_bench.ui.event_bus import event_bus, AgentEvent


def emit_agent_event(agent_name: str, stage: str, event_type: str, data: Any = None):
    """Emit agent event to event bus.
    
    Args:
        agent_name: Name of the agent
        stage: Research stage
        event_type: Event type
        data: Event data
    """
    event = AgentEvent(
        agent_name=agent_name,
        stage=stage,
        event_type=event_type,
        data=data
    )
    event_bus.emit(event)


def track_agent_execution(agent_name: str, stage: str):
    """Decorator to track agent execution.
    
    Args:
        agent_name: Name of the agent
        stage: Research stage
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Emit started event
            emit_agent_event(agent_name, stage, "started")
            
            try:
                # Get input data
                input_data = {
                    "args": str(args)[:200] if args else None,
                    "kwargs": str(kwargs)[:200] if kwargs else None
                }
                emit_agent_event(agent_name, stage, "input", input_data)
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Emit output event
                output_data = {
                    "type": type(result).__name__,
                    "preview": str(result)[:200] if result else None
                }
                emit_agent_event(agent_name, stage, "output", output_data)
                
                # Emit completed event
                emit_agent_event(agent_name, stage, "completed")
                
                return result
                
            except Exception as e:
                # Emit error event
                error_data = {
                    "error": str(e),
                    "type": type(e).__name__
                }
                emit_agent_event(agent_name, stage, "error", error_data)
                raise
        
        return wrapper
    return decorator
