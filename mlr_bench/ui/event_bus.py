"""Event bus for agent orchestration visualization."""

from typing import Dict, Any, List, Callable
from datetime import datetime
from loguru import logger


class AgentEvent:
    """Event representing agent activity."""
    
    def __init__(
        self,
        agent_name: str,
        stage: str,
        event_type: str,
        data: Dict[str, Any] = None
    ):
        """Initialize agent event.
        
        Args:
            agent_name: Name of the agent
            stage: Research stage
            event_type: Type of event (started, input, output, completed, error)
            data: Event data
        """
        self.agent_name = agent_name
        self.stage = stage
        self.event_type = event_type
        self.data = data or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "agent_name": self.agent_name,
            "stage": self.stage,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp
        }


class EventBus:
    """Central event bus for agent orchestration."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize event bus."""
        if self._initialized:
            return
        
        self.events: List[AgentEvent] = []
        self.listeners: List[Callable] = []
        self._initialized = True
        logger.info("Event bus initialized")
    
    def emit(self, event: AgentEvent):
        """Emit an event.
        
        Args:
            event: Agent event
        """
        self.events.append(event)
        logger.debug(f"Event emitted: {event.agent_name} - {event.event_type}")
        
        # Notify all listeners (in-process)
        for listener in self.listeners:
            try:
                listener(event)
            except Exception as e:
                logger.error(f"Error in event listener: {e}")
        
        # Send to UI server via HTTP (cross-process)
        try:
            import requests
            requests.post(
                'http://localhost:5000/api/event',
                json=event.to_dict(),
                timeout=0.5
            )
        except Exception as e:
            # Silently fail if UI server is not running
            pass
    
    def subscribe(self, listener: Callable):
        """Subscribe to events.
        
        Args:
            listener: Callback function
        """
        self.listeners.append(listener)
        logger.debug(f"New listener subscribed (total: {len(self.listeners)})")
    
    def unsubscribe(self, listener: Callable):
        """Unsubscribe from events.
        
        Args:
            listener: Callback function
        """
        if listener in self.listeners:
            self.listeners.remove(listener)
    
    def get_events(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get recent events.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of events
        """
        events = self.events[-limit:] if limit else self.events
        return [e.to_dict() for e in events]
    
    def clear(self):
        """Clear all events."""
        self.events.clear()
        logger.info("Event bus cleared")


# Global event bus instance
event_bus = EventBus()
