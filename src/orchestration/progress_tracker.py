"""
Progress Tracker for Pipeline Execution
Tracks and reports progress of data processing pipeline
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class StageStatus(Enum):
    """Status of a pipeline stage"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StageProgress:
    """Progress information for a pipeline stage"""
    stage_name: str
    status: StageStatus
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    progress_percent: float = 0.0
    current_step: str = ""
    total_steps: int = 0
    completed_steps: int = 0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> Optional[float]:
        """Get duration in seconds"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.time() - self.start_time
        return None

    @property
    def estimated_time_remaining(self) -> Optional[float]:
        """Estimate time remaining based on current progress"""
        if self.progress_percent > 0 and self.start_time:
            elapsed = time.time() - self.start_time
            total_estimated = elapsed / (self.progress_percent / 100)
            return total_estimated - elapsed
        return None


class ProgressTracker:
    """
    Tracks progress of pipeline execution with real-time updates
    """

    def __init__(self, stages: Optional[List[str]] = None):
        """
        Initialize progress tracker
        
        Args:
            stages: List of stage names in order
        """
        self.stages: Dict[str, StageProgress] = {}
        self.stage_order: List[str] = stages or []
        self.current_stage: Optional[str] = None
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.callbacks: List[callable] = []
        
        # Initialize stages
        for stage in self.stage_order:
            self.stages[stage] = StageProgress(
                stage_name=stage,
                status=StageStatus.PENDING
            )

    def add_stage(self, stage_name: str, total_steps: int = 0):
        """
        Add a new stage to track
        
        Args:
            stage_name: Name of the stage
            total_steps: Total number of steps in stage
        """
        if stage_name not in self.stages:
            self.stages[stage_name] = StageProgress(
                stage_name=stage_name,
                status=StageStatus.PENDING,
                total_steps=total_steps
            )
            if stage_name not in self.stage_order:
                self.stage_order.append(stage_name)
            logger.info(f"Added stage: {stage_name}")

    def start_stage(self, stage_name: str, total_steps: int = 0):
        """
        Mark a stage as started
        
        Args:
            stage_name: Name of the stage
            total_steps: Total number of steps in stage
        """
        if stage_name not in self.stages:
            self.add_stage(stage_name, total_steps)
        
        stage = self.stages[stage_name]
        stage.status = StageStatus.IN_PROGRESS
        stage.start_time = time.time()
        stage.total_steps = total_steps or stage.total_steps
        stage.completed_steps = 0
        stage.progress_percent = 0.0
        
        self.current_stage = stage_name
        
        if not self.start_time:
            self.start_time = time.time()
        
        logger.info(f"Started stage: {stage_name}")
        self._notify_callbacks()

    def update_stage(
        self,
        stage_name: str,
        progress_percent: Optional[float] = None,
        current_step: Optional[str] = None,
        completed_steps: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Update progress of a stage
        
        Args:
            stage_name: Name of the stage
            progress_percent: Progress percentage (0-100)
            current_step: Description of current step
            completed_steps: Number of completed steps
            metadata: Additional metadata
        """
        if stage_name not in self.stages:
            logger.warning(f"Stage {stage_name} not found")
            return
        
        stage = self.stages[stage_name]
        
        if progress_percent is not None:
            stage.progress_percent = min(100.0, max(0.0, progress_percent))
        
        if current_step is not None:
            stage.current_step = current_step
        
        if completed_steps is not None:
            stage.completed_steps = completed_steps
            if stage.total_steps > 0:
                stage.progress_percent = (completed_steps / stage.total_steps) * 100
        
        if metadata is not None:
            stage.metadata.update(metadata)
        
        self._notify_callbacks()

    def complete_stage(self, stage_name: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Mark a stage as completed
        
        Args:
            stage_name: Name of the stage
            metadata: Additional metadata
        """
        if stage_name not in self.stages:
            logger.warning(f"Stage {stage_name} not found")
            return
        
        stage = self.stages[stage_name]
        stage.status = StageStatus.COMPLETED
        stage.end_time = time.time()
        stage.progress_percent = 100.0
        stage.completed_steps = stage.total_steps
        
        if metadata:
            stage.metadata.update(metadata)
        
        logger.info(f"Completed stage: {stage_name} in {stage.duration:.2f}s")
        self._notify_callbacks()

    def fail_stage(self, stage_name: str, error_message: str):
        """
        Mark a stage as failed
        
        Args:
            stage_name: Name of the stage
            error_message: Error message
        """
        if stage_name not in self.stages:
            logger.warning(f"Stage {stage_name} not found")
            return
        
        stage = self.stages[stage_name]
        stage.status = StageStatus.FAILED
        stage.end_time = time.time()
        stage.error_message = error_message
        
        logger.error(f"Stage {stage_name} failed: {error_message}")
        self._notify_callbacks()

    def skip_stage(self, stage_name: str, reason: str = ""):
        """
        Mark a stage as skipped
        
        Args:
            stage_name: Name of the stage
            reason: Reason for skipping
        """
        if stage_name not in self.stages:
            logger.warning(f"Stage {stage_name} not found")
            return
        
        stage = self.stages[stage_name]
        stage.status = StageStatus.SKIPPED
        stage.metadata['skip_reason'] = reason
        
        logger.info(f"Skipped stage: {stage_name} - {reason}")
        self._notify_callbacks()

    def get_overall_progress(self) -> float:
        """
        Calculate overall progress across all stages
        
        Returns:
            Overall progress percentage (0-100)
        """
        if not self.stages:
            return 0.0
        
        total_progress = sum(
            stage.progress_percent for stage in self.stages.values()
        )
        return total_progress / len(self.stages)

    def get_estimated_time_remaining(self) -> Optional[float]:
        """
        Estimate total time remaining for all stages
        
        Returns:
            Estimated seconds remaining, or None if cannot estimate
        """
        overall_progress = self.get_overall_progress()
        
        if overall_progress > 0 and self.start_time:
            elapsed = time.time() - self.start_time
            total_estimated = elapsed / (overall_progress / 100)
            return total_estimated - elapsed
        
        return None

    def get_status_summary(self) -> Dict[str, Any]:
        """
        Get summary of current status
        
        Returns:
            Dictionary with status information
        """
        completed = sum(1 for s in self.stages.values() if s.status == StageStatus.COMPLETED)
        failed = sum(1 for s in self.stages.values() if s.status == StageStatus.FAILED)
        in_progress = sum(1 for s in self.stages.values() if s.status == StageStatus.IN_PROGRESS)
        pending = sum(1 for s in self.stages.values() if s.status == StageStatus.PENDING)
        
        overall_progress = self.get_overall_progress()
        time_remaining = self.get_estimated_time_remaining()
        
        elapsed_time = None
        if self.start_time:
            elapsed_time = time.time() - self.start_time
        
        return {
            "overall_progress": overall_progress,
            "total_stages": len(self.stages),
            "completed_stages": completed,
            "failed_stages": failed,
            "in_progress_stages": in_progress,
            "pending_stages": pending,
            "current_stage": self.current_stage,
            "elapsed_time": elapsed_time,
            "estimated_time_remaining": time_remaining,
            "stages": {
                name: {
                    "status": stage.status.value,
                    "progress": stage.progress_percent,
                    "current_step": stage.current_step,
                    "duration": stage.duration,
                    "error": stage.error_message
                }
                for name, stage in self.stages.items()
            }
        }

    def print_progress(self):
        """Print current progress to console"""
        summary = self.get_status_summary()
        
        print("\n" + "=" * 80)
        print(f"Pipeline Progress: {summary['overall_progress']:.1f}%")
        print("=" * 80)
        
        if summary['elapsed_time']:
            elapsed = str(timedelta(seconds=int(summary['elapsed_time'])))
            print(f"Elapsed Time: {elapsed}")
        
        if summary['estimated_time_remaining']:
            remaining = str(timedelta(seconds=int(summary['estimated_time_remaining'])))
            print(f"Estimated Time Remaining: {remaining}")
        
        print(f"\nStages: {summary['completed_stages']}/{summary['total_stages']} completed")
        
        if summary['failed_stages'] > 0:
            print(f"Failed: {summary['failed_stages']}")
        
        print("\nStage Details:")
        for stage_name in self.stage_order:
            if stage_name in self.stages:
                stage = self.stages[stage_name]
                status_icon = {
                    StageStatus.PENDING: "⏳",
                    StageStatus.IN_PROGRESS: "🔄",
                    StageStatus.COMPLETED: "✅",
                    StageStatus.FAILED: "❌",
                    StageStatus.SKIPPED: "⏭️"
                }.get(stage.status, "❓")
                
                print(f"  {status_icon} {stage_name}: {stage.progress_percent:.1f}%", end="")
                
                if stage.current_step:
                    print(f" - {stage.current_step}", end="")
                
                if stage.duration:
                    print(f" ({stage.duration:.1f}s)", end="")
                
                print()
        
        print("=" * 80 + "\n")

    def register_callback(self, callback: callable):
        """
        Register a callback to be called on progress updates
        
        Args:
            callback: Function to call with progress updates
        """
        self.callbacks.append(callback)

    def _notify_callbacks(self):
        """Notify all registered callbacks of progress update"""
        summary = self.get_status_summary()
        for callback in self.callbacks:
            try:
                callback(summary)
            except Exception as e:
                logger.error(f"Error in progress callback: {e}")

    def complete_pipeline(self):
        """Mark entire pipeline as complete"""
        self.end_time = time.time()
        logger.info(f"Pipeline completed in {self.end_time - self.start_time:.2f}s")
        self._notify_callbacks()

    def reset(self):
        """Reset all progress tracking"""
        for stage in self.stages.values():
            stage.status = StageStatus.PENDING
            stage.start_time = None
            stage.end_time = None
            stage.progress_percent = 0.0
            stage.current_step = ""
            stage.completed_steps = 0
            stage.error_message = None
        
        self.current_stage = None
        self.start_time = None
        self.end_time = None
        
        logger.info("Progress tracker reset")


# Example usage
def example_usage():
    """Example of using ProgressTracker"""
    
    # Define pipeline stages
    stages = [
        "Data Ingestion",
        "Quality Check",
        "Data Cleaning",
        "Analysis",
        "Visualization",
        "Report Generation"
    ]
    
    tracker = ProgressTracker(stages)
    
    # Register a callback for real-time updates
    def progress_callback(summary):
        print(f"Progress: {summary['overall_progress']:.1f}%")
    
    tracker.register_callback(progress_callback)
    
    # Simulate pipeline execution
    for stage in stages:
        tracker.start_stage(stage, total_steps=10)
        
        for step in range(10):
            time.sleep(0.1)  # Simulate work
            tracker.update_stage(
                stage,
                current_step=f"Processing step {step + 1}",
                completed_steps=step + 1
            )
        
        tracker.complete_stage(stage)
        tracker.print_progress()
    
    tracker.complete_pipeline()


if __name__ == "__main__":
    example_usage()

# Made with Bob
