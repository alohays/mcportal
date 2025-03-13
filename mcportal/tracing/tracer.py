"""
Tracing implementation for MCPortal
"""
import datetime
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

class Tracer:
    """
    Simple tracing implementation for MCPortal that records execution events.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize a new tracer.
        
        Args:
            storage_path: Optional path to store trace data. Defaults to a local directory.
        """
        self.trace_id = str(uuid.uuid4())
        self.events = []
        self.start_time = datetime.datetime.now()
        self.storage_path = storage_path or str(Path.home() / ".mcportal" / "traces")
        
        # Create storage directory if it doesn't exist
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        
        print(f"Tracer initialized with trace ID: {self.trace_id}")
        
    @property
    def current_trace_id(self) -> str:
        """Get the current trace ID."""
        return self.trace_id
        
    def record_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Record an event in the trace.
        
        Args:
            event_type: Type of event to record.
            data: Data associated with the event.
        """
        timestamp = datetime.datetime.now()
        elapsed = (timestamp - self.start_time).total_seconds()
        
        event = {
            "timestamp": timestamp.isoformat(),
            "elapsed_seconds": elapsed,
            "event_type": event_type,
            "data": data,
        }
        
        self.events.append(event)
        self._persist_event(event)
        
    def _persist_event(self, event: Dict[str, Any]) -> None:
        """
        Persist an event to storage.
        
        Args:
            event: Event to persist.
        """
        trace_file = Path(self.storage_path) / f"{self.trace_id}.jsonl"
        
        with open(trace_file, "a") as f:
            f.write(json.dumps(event) + "\n")
            
    def get_timeline(self) -> List[Dict[str, Any]]:
        """
        Get a timeline of all events in the trace.
        
        Returns:
            List of events in chronological order.
        """
        return sorted(self.events, key=lambda e: e["timestamp"])
        
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the trace.
        
        Returns:
            Summary statistics about the trace.
        """
        event_types = {}
        for event in self.events:
            event_type = event["event_type"]
            if event_type not in event_types:
                event_types[event_type] = 0
            event_types[event_type] += 1
            
        return {
            "trace_id": self.trace_id,
            "start_time": self.start_time.isoformat(),
            "event_count": len(self.events),
            "event_types": event_types,
            "duration": (datetime.datetime.now() - self.start_time).total_seconds(),
        }
