"""
Multi-Agent Orchestrator for Strategic Intelligence
"""
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """Coordinates multiple AI agents for strategic intelligence tasks."""

    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.task_queue: List[Dict[str, Any]] = []

    def register_agent(self, name: str, agent: Any) -> None:
        """Register an agent with the coordinator."""
        self.agents[name] = agent
        logger.info(f"Registered agent: {name}")

    def assign_task(self, agent_name: str, task: str, **kwargs) -> Dict[str, Any]:
        """Assign a task to a specific agent."""
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not registered")
        task_entry = {
            "agent": agent_name,
            "task": task,
            "kwargs": kwargs,
            "status": "pending"
        }
        self.task_queue.append(task_entry)
        return task_entry

    async def execute_task(self, task_entry: Dict[str, Any]) -> Any:
        """Execute a single task."""
        agent_name = task_entry["agent"]
        agent = self.agents[agent_name]
        task_entry["status"] = "running"

        try:
            if hasattr(agent, "arun"):
                result = await agent.arun(task_entry["task"], **task_entry["kwargs"])
            elif hasattr(agent, "run"):
                result = agent.run(task_entry["task"], **task_entry["kwargs"])
            else:
                raise AttributeError(f"Agent '{agent_name}' has no run or arun method")

            task_entry["status"] = "completed"
            task_entry["result"] = result
            return result
        except Exception as e:
            task_entry["status"] = "failed"
            task_entry["error"] = str(e)
            logger.error(f"Task failed for agent {agent_name}: {e}")
            raise

    async def run_all(self) -> List[Dict[str, Any]]:
        """Execute all pending tasks."""
        results = []
        for task in self.task_queue:
            if task["status"] == "pending":
                result = await self.execute_task(task)
                results.append(result)
        return results


# Backwards compatibility alias
AgentExecutor = AgentCoordinator
