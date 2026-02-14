from typing import Any

from app.providers.interfaces import AgentAutomationProvider


class NovaActClient(AgentAutomationProvider):
    """
    Interface for Nova Act automation.

    Maps to Nova Act concept: agents that execute browser/UI workflows.
    """

    def run_playbook(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "playbook": name,
            "status": "not_configured",
            "summary": "Nova Act integration stub. TODO: invoke Nova Act agent runtime with workflow steps.",
            "input": payload,
        }

