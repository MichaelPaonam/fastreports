"""
Bob Integration - Session Manager
Manages IBM Bob interaction sessions and logging
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BobSessionManager:
    """Manages IBM Bob interaction sessions."""
    
    def __init__(self, session_dir: str = "bob_sessions"):
        """
        Initialize the Bob session manager.
        
        Args:
            session_dir: Directory to store session logs
        """
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        
        self.current_session = None
        self.session_history = []
        self.interactions = []
    
    def start_session(
        self,
        dataset_name: str,
        purpose: str
    ) -> Dict[str, Any]:
        """
        Start a new Bob interaction session.
        
        Args:
            dataset_name: Name of the dataset being analyzed
            purpose: Purpose of the session
        
        Returns:
            Session information dictionary
        """
        session_id = f"{dataset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_session = {
            'session_id': session_id,
            'dataset_name': dataset_name,
            'purpose': purpose,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'interactions': [],
            'modes_used': set(),
            'total_prompts': 0,
            'total_responses': 0
        }
        
        logger.info(f"Started Bob session: {session_id}")
        logger.info(f"Purpose: {purpose}")
        
        return self.current_session
    
    def log_interaction(
        self,
        mode: str,
        phase: str,
        prompt: str,
        response: Optional[str] = None,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a Bob interaction.
        
        Args:
            mode: Bob mode used (Plan, Code, Advanced, etc.)
            phase: Pipeline phase
            prompt: Prompt sent to Bob
            response: Response from Bob
            success: Whether the interaction was successful
            metadata: Additional metadata
        """
        if not self.current_session:
            logger.warning("No active session. Starting default session.")
            self.start_session("unknown", "default")
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'phase': phase,
            'prompt': prompt,
            'response': response,
            'success': success,
            'metadata': metadata or {}
        }
        
        self.current_session['interactions'].append(interaction)
        self.current_session['modes_used'].add(mode)
        self.current_session['total_prompts'] += 1
        if response:
            self.current_session['total_responses'] += 1
        
        logger.info(f"Logged Bob interaction: {mode} mode, {phase} phase")
    
    def end_session(self) -> Dict[str, Any]:
        """
        End the current Bob session.
        
        Returns:
            Final session information
        """
        if not self.current_session:
            logger.warning("No active session to end")
            return {}
        
        self.current_session['end_time'] = datetime.now().isoformat()
        self.current_session['modes_used'] = list(self.current_session['modes_used'])
        
        # Save session to file
        self._save_session(self.current_session)
        
        # Add to history
        self.session_history.append(self.current_session)
        
        logger.info(f"Ended Bob session: {self.current_session['session_id']}")
        logger.info(f"Total interactions: {self.current_session['total_prompts']}")
        logger.info(f"Modes used: {', '.join(self.current_session['modes_used'])}")
        
        session_summary = self.current_session.copy()
        self.current_session = None
        
        return session_summary
    
    def _save_session(self, session: Dict[str, Any]):
        """Save session to JSON file."""
        session_file = self.session_dir / f"{session['session_id']}.json"
        
        try:
            with open(session_file, 'w') as f:
                json.dump(session, f, indent=2, default=str)
            logger.info(f"Saved session to {session_file}")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    def get_session_summary(self, session_id: Optional[str] = None) -> str:
        """
        Generate a human-readable session summary.
        
        Args:
            session_id: Optional session ID (uses current if not provided)
        
        Returns:
            Formatted summary string
        """
        if session_id:
            session = self._load_session(session_id)
        else:
            session = self.current_session
        
        if not session:
            return "No session found"
        
        lines = []
        lines.append("=" * 80)
        lines.append(f"BOB SESSION SUMMARY: {session['session_id']}")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Dataset: {session['dataset_name']}")
        lines.append(f"Purpose: {session['purpose']}")
        lines.append(f"Start Time: {session['start_time']}")
        if session['end_time']:
            lines.append(f"End Time: {session['end_time']}")
        lines.append("")
        lines.append(f"Total Interactions: {session['total_prompts']}")
        lines.append(f"Modes Used: {', '.join(session.get('modes_used', []))}")
        lines.append("")
        
        # Interaction breakdown
        if session['interactions']:
            lines.append("INTERACTIONS:")
            lines.append("-" * 80)
            for i, interaction in enumerate(session['interactions'], 1):
                status = "✓" if interaction['success'] else "✗"
                lines.append(f"{i}. {status} [{interaction['mode']}] {interaction['phase']}")
                lines.append(f"   Time: {interaction['timestamp']}")
                if interaction.get('metadata'):
                    lines.append(f"   Metadata: {interaction['metadata']}")
                lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session from file."""
        session_file = self.session_dir / f"{session_id}.json"
        
        if not session_file.exists():
            logger.warning(f"Session file not found: {session_file}")
            return None
        
        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return None
    
    def get_mode_usage_stats(self) -> Dict[str, int]:
        """
        Get statistics on Bob mode usage across all sessions.
        
        Returns:
            Dictionary of mode names to usage counts
        """
        mode_counts = {}
        
        for session in self.session_history:
            for mode in session.get('modes_used', []):
                mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        return mode_counts
    
    def get_phase_interaction_stats(self) -> Dict[str, int]:
        """
        Get statistics on interactions per phase.
        
        Returns:
            Dictionary of phase names to interaction counts
        """
        phase_counts = {}
        
        for session in self.session_history:
            for interaction in session.get('interactions', []):
                phase = interaction['phase']
                phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        return phase_counts
    
    def generate_usage_report(self) -> str:
        """
        Generate a comprehensive Bob usage report.
        
        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("IBM BOB USAGE REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append(f"Total Sessions: {len(self.session_history)}")
        
        total_interactions = sum(
            s['total_prompts'] for s in self.session_history
        )
        lines.append(f"Total Interactions: {total_interactions}")
        lines.append("")
        
        # Mode usage
        mode_stats = self.get_mode_usage_stats()
        if mode_stats:
            lines.append("MODE USAGE:")
            lines.append("-" * 80)
            for mode, count in sorted(mode_stats.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  {mode}: {count} sessions")
            lines.append("")
        
        # Phase usage
        phase_stats = self.get_phase_interaction_stats()
        if phase_stats:
            lines.append("PHASE INTERACTIONS:")
            lines.append("-" * 80)
            for phase, count in sorted(phase_stats.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  {phase}: {count} interactions")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def export_sessions(self, output_file: str):
        """
        Export all session history to a single file.
        
        Args:
            output_file: Path to output file
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(self.session_history, f, indent=2, default=str)
            logger.info(f"Exported {len(self.session_history)} sessions to {output_file}")
        except Exception as e:
            logger.error(f"Failed to export sessions: {e}")


# Singleton instance
_bob_session_manager = None


def get_bob_session_manager() -> BobSessionManager:
    """Get the global Bob session manager instance."""
    global _bob_session_manager
    if _bob_session_manager is None:
        _bob_session_manager = BobSessionManager()
    return _bob_session_manager


# Made with Bob