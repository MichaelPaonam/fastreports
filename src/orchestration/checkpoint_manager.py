"""
Checkpoint Manager for User Approval Points
Manages user interaction points during the pipeline execution
"""

import json
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CheckpointType(Enum):
    """Types of checkpoints in the pipeline"""
    QUALITY_REVIEW = "quality_review"
    CLEANING_STRATEGY = "cleaning_strategy"
    TRANSFORMATION_APPROVAL = "transformation_approval"
    ANALYSIS_SELECTION = "analysis_selection"
    VISUALIZATION_REVIEW = "visualization_review"
    FINAL_REPORT = "final_report"


class CheckpointStatus(Enum):
    """Status of a checkpoint"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"
    SKIPPED = "skipped"


@dataclass
class CheckpointData:
    """Data structure for a checkpoint"""
    checkpoint_id: str
    checkpoint_type: CheckpointType
    title: str
    description: str
    data: Dict[str, Any]
    options: List[Dict[str, Any]]
    status: CheckpointStatus
    user_response: Optional[Dict[str, Any]]
    timestamp: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        result['checkpoint_type'] = self.checkpoint_type.value
        result['status'] = self.status.value
        return result


class CheckpointManager:
    """
    Manages checkpoints for user approval during pipeline execution
    """

    def __init__(self, interactive: bool = True, auto_approve: bool = False):
        """
        Initialize checkpoint manager
        
        Args:
            interactive: Whether to prompt user for input
            auto_approve: Auto-approve all checkpoints (for testing)
        """
        self.interactive = interactive
        self.auto_approve = auto_approve
        self.checkpoints: List[CheckpointData] = []
        self.current_checkpoint: Optional[CheckpointData] = None
        self.callbacks: Dict[CheckpointType, Callable] = {}

    def register_callback(self, checkpoint_type: CheckpointType, callback: Callable):
        """
        Register a callback for a specific checkpoint type
        
        Args:
            checkpoint_type: Type of checkpoint
            callback: Function to call when checkpoint is reached
        """
        self.callbacks[checkpoint_type] = callback
        logger.info(f"Registered callback for {checkpoint_type.value}")

    def create_checkpoint(
        self,
        checkpoint_type: CheckpointType,
        title: str,
        description: str,
        data: Dict[str, Any],
        options: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CheckpointData:
        """
        Create a new checkpoint
        
        Args:
            checkpoint_type: Type of checkpoint
            title: Checkpoint title
            description: Detailed description
            data: Data to present to user
            options: Available options for user
            metadata: Additional metadata
            
        Returns:
            CheckpointData object
        """
        checkpoint_id = f"{checkpoint_type.value}_{len(self.checkpoints) + 1}"
        
        checkpoint = CheckpointData(
            checkpoint_id=checkpoint_id,
            checkpoint_type=checkpoint_type,
            title=title,
            description=description,
            data=data,
            options=options or [],
            status=CheckpointStatus.PENDING,
            user_response=None,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        
        self.checkpoints.append(checkpoint)
        logger.info(f"Created checkpoint: {checkpoint_id}")
        
        return checkpoint

    def present_checkpoint(self, checkpoint: CheckpointData) -> Dict[str, Any]:
        """
        Present checkpoint to user and get response
        
        Args:
            checkpoint: Checkpoint to present
            
        Returns:
            User response dictionary
        """
        self.current_checkpoint = checkpoint
        
        if self.auto_approve:
            logger.info(f"Auto-approving checkpoint: {checkpoint.checkpoint_id}")
            return self._auto_approve_checkpoint(checkpoint)
        
        if not self.interactive:
            logger.warning(f"Non-interactive mode, skipping checkpoint: {checkpoint.checkpoint_id}")
            checkpoint.status = CheckpointStatus.SKIPPED
            return {"action": "skip"}
        
        # Call registered callback if exists
        if checkpoint.checkpoint_type in self.callbacks:
            try:
                response = self.callbacks[checkpoint.checkpoint_type](checkpoint)
                checkpoint.user_response = response
                checkpoint.status = CheckpointStatus(response.get("status", "approved"))
                return response
            except Exception as e:
                logger.error(f"Error in checkpoint callback: {e}")
                raise
        
        # Default interactive prompt
        return self._interactive_prompt(checkpoint)

    def _auto_approve_checkpoint(self, checkpoint: CheckpointData) -> Dict[str, Any]:
        """Auto-approve checkpoint with default options"""
        checkpoint.status = CheckpointStatus.APPROVED
        
        # Select first option if available
        if checkpoint.options:
            response = {
                "action": "approve",
                "status": "approved",
                "selected_option": checkpoint.options[0],
                "modifications": {}
            }
        else:
            response = {
                "action": "approve",
                "status": "approved"
            }
        
        checkpoint.user_response = response
        return response

    def _interactive_prompt(self, checkpoint: CheckpointData) -> Dict[str, Any]:
        """
        Interactive command-line prompt for checkpoint
        
        Args:
            checkpoint: Checkpoint to present
            
        Returns:
            User response
        """
        print("\n" + "=" * 80)
        print(f"CHECKPOINT: {checkpoint.title}")
        print("=" * 80)
        print(f"\n{checkpoint.description}\n")
        
        # Display data summary
        if checkpoint.data:
            print("Data Summary:")
            for key, value in checkpoint.data.items():
                if isinstance(value, (list, dict)):
                    print(f"  {key}: {len(value)} items")
                else:
                    print(f"  {key}: {value}")
            print()
        
        # Display options
        if checkpoint.options:
            print("Available Options:")
            for idx, option in enumerate(checkpoint.options, 1):
                print(f"  {idx}. {option.get('name', 'Option ' + str(idx))}")
                if 'description' in option:
                    print(f"     {option['description']}")
            print()
        
        # Get user input
        print("Actions:")
        print("  [A]pprove - Accept and continue")
        print("  [R]eject - Reject and stop")
        print("  [M]odify - Make modifications")
        print("  [S]kip - Skip this checkpoint")
        
        while True:
            action = input("\nYour choice (A/R/M/S): ").strip().upper()
            
            if action == 'A':
                checkpoint.status = CheckpointStatus.APPROVED
                response = {"action": "approve", "status": "approved"}
                
                if checkpoint.options:
                    choice = input(f"Select option (1-{len(checkpoint.options)}): ").strip()
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(checkpoint.options):
                            response["selected_option"] = checkpoint.options[idx]
                    except ValueError:
                        pass
                
                checkpoint.user_response = response
                return response
            
            elif action == 'R':
                checkpoint.status = CheckpointStatus.REJECTED
                reason = input("Reason for rejection (optional): ").strip()
                response = {
                    "action": "reject",
                    "status": "rejected",
                    "reason": reason
                }
                checkpoint.user_response = response
                return response
            
            elif action == 'M':
                checkpoint.status = CheckpointStatus.MODIFIED
                print("\nEnter modifications (JSON format or key=value pairs):")
                modifications = {}
                
                while True:
                    mod = input("Modification (or 'done'): ").strip()
                    if mod.lower() == 'done':
                        break
                    
                    if '=' in mod:
                        key, value = mod.split('=', 1)
                        modifications[key.strip()] = value.strip()
                
                response = {
                    "action": "modify",
                    "status": "modified",
                    "modifications": modifications
                }
                checkpoint.user_response = response
                return response
            
            elif action == 'S':
                checkpoint.status = CheckpointStatus.SKIPPED
                response = {"action": "skip", "status": "skipped"}
                checkpoint.user_response = response
                return response
            
            else:
                print("Invalid choice. Please enter A, R, M, or S.")

    def get_checkpoint_history(self) -> List[Dict[str, Any]]:
        """Get history of all checkpoints"""
        return [cp.to_dict() for cp in self.checkpoints]

    def save_checkpoint_state(self, filepath: str):
        """
        Save checkpoint state to file
        
        Args:
            filepath: Path to save state
        """
        state = {
            "checkpoints": self.get_checkpoint_history(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Saved checkpoint state to {filepath}")

    def load_checkpoint_state(self, filepath: str):
        """
        Load checkpoint state from file
        
        Args:
            filepath: Path to load state from
        """
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.checkpoints = []
        for cp_dict in state.get("checkpoints", []):
            cp_dict['checkpoint_type'] = CheckpointType(cp_dict['checkpoint_type'])
            cp_dict['status'] = CheckpointStatus(cp_dict['status'])
            checkpoint = CheckpointData(**cp_dict)
            self.checkpoints.append(checkpoint)
        
        logger.info(f"Loaded {len(self.checkpoints)} checkpoints from {filepath}")

    def get_pending_checkpoints(self) -> List[CheckpointData]:
        """Get all pending checkpoints"""
        return [cp for cp in self.checkpoints if cp.status == CheckpointStatus.PENDING]

    def get_approved_checkpoints(self) -> List[CheckpointData]:
        """Get all approved checkpoints"""
        return [cp for cp in self.checkpoints if cp.status == CheckpointStatus.APPROVED]

    def clear_checkpoints(self):
        """Clear all checkpoints"""
        self.checkpoints.clear()
        self.current_checkpoint = None
        logger.info("Cleared all checkpoints")


# Example usage functions
def create_quality_checkpoint(
    manager: CheckpointManager,
    quality_issues: List[Dict[str, Any]],
    recommendations: List[str]
) -> Dict[str, Any]:
    """Create a quality review checkpoint"""
    checkpoint = manager.create_checkpoint(
        checkpoint_type=CheckpointType.QUALITY_REVIEW,
        title="Data Quality Review",
        description="Review identified data quality issues and approve cleaning strategies",
        data={
            "total_issues": len(quality_issues),
            "issues": quality_issues,
            "recommendations": recommendations
        },
        options=[
            {
                "name": "Approve All",
                "description": "Apply all recommended cleaning strategies",
                "action": "approve_all"
            },
            {
                "name": "Selective Approval",
                "description": "Choose specific strategies to apply",
                "action": "selective"
            },
            {
                "name": "Custom Strategy",
                "description": "Define custom cleaning approach",
                "action": "custom"
            }
        ]
    )
    
    return manager.present_checkpoint(checkpoint)


def create_cleaning_strategy_checkpoint(
    manager: CheckpointManager,
    strategies: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a cleaning strategy approval checkpoint"""
    checkpoint = manager.create_checkpoint(
        checkpoint_type=CheckpointType.CLEANING_STRATEGY,
        title="Cleaning Strategy Approval",
        description="Review and approve data cleaning strategies",
        data={
            "strategies": strategies,
            "total_transformations": sum(len(s.get('transformations', [])) for s in strategies)
        },
        options=[
            {"name": "Approve", "action": "approve"},
            {"name": "Modify", "action": "modify"},
            {"name": "Reject", "action": "reject"}
        ]
    )
    
    return manager.present_checkpoint(checkpoint)

# Made with Bob
