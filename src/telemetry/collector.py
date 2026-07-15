"""
Telemetry Collector

Stores execution telemetry in memory.

Version 1:
In-memory storage.

Version 2:
Persistent database.
"""

from src.schemas import (TelemetryRecord,)

class TelemetryCollector:
    def __init__(self):
        self.records : list[TelemetryRecord] = []
    
    def add_record(self,record : TelemetryRecord,)-> None:
        self.records.append(record)
        print(f"Record added : {record}")

    def get_records(self)-> list[TelemetryRecord]:
        return self.records
    
    def clear(self) -> None:
        self.records.clear()
    