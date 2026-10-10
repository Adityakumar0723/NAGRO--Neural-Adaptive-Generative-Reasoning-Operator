"""
NAGRO 4.1 — Task Planning Engine.

Decomposes complex tasks into executable sub-tasks with dependencies.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SubTask:
    """A single sub-task in the execution plan."""
    id: int
    description: str
    agent_type: str
    dependencies: list[int] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: str = ""


@dataclass
class ExecutionPlan:
    """A complete execution plan for a complex task."""
    goal: str
    sub_tasks: list[SubTask] = field(default_factory=list)
    current_step: int = 0

    @property
    def is_complete(self) -> bool:
        return all(t.status == TaskStatus.COMPLETED for t in self.sub_tasks)

    @property
    def progress(self) -> float:
        if not self.sub_tasks:
            return 0.0
        completed = sum(1 for t in self.sub_tasks if t.status == TaskStatus.COMPLETED)
        return completed / len(self.sub_tasks)

    def get_next_tasks(self) -> list[SubTask]:
        """Get tasks whose dependencies are all completed."""
        completed_ids = {t.id for t in self.sub_tasks if t.status == TaskStatus.COMPLETED}
        return [
            t for t in self.sub_tasks
            if t.status == TaskStatus.PENDING
            and all(dep in completed_ids for dep in t.dependencies)
        ]


class TaskPlanner:
    """
    Decomposes complex problems into structured execution plans.
    """

    PLANNING_PROMPT = """You are NAGRO 4.1's planning engine. Break this complex task into an executable plan.

TASK: {task}

Create a step-by-step plan. For each step, specify:
- Step number
- What to do (clear, specific action)
- Which NAGRO agent should handle it: chat, code, research, image, math, creative
- Dependencies (which previous steps must complete first)

Format each step as:
STEP [number] | [agent_type] | depends:[comma-separated step numbers or "none"]
[Description of what to do]

Rules:
- Each step should be atomic (one clear action)
- Minimize dependencies to allow parallel execution
- Include verification steps for critical outputs
- Be specific — vague steps are useless

Example:
STEP 1 | research | depends:none
Research current best practices for React state management

STEP 2 | code | depends:1
Implement a React store based on research findings

STEP 3 | code | depends:2
Write unit tests for the store implementation

Now plan the task."""

    REPLAN_PROMPT = """A step in the plan failed. Adjust the plan.

ORIGINAL TASK: {task}
FAILED STEP: {failed_step}
ERROR: {error}

Provide an alternative approach for this step, and adjust any dependent steps."""

    def build_planning_prompt(self, task: str) -> str:
        return self.PLANNING_PROMPT.format(task=task)

    def build_replan_prompt(self, task: str, failed_step: str, error: str) -> str:
        return self.REPLAN_PROMPT.format(task=task, failed_step=failed_step, error=error)

    def parse_plan(self, llm_output: str, goal: str) -> ExecutionPlan:
        """Parse the LLM's planning output into a structured ExecutionPlan."""
        plan = ExecutionPlan(goal=goal)
        lines = llm_output.strip().split("\n")

        current_step_id = None
        current_agent = "chat"
        current_deps: list[int] = []
        current_desc_lines: list[str] = []

        for line in lines:
            line = line.strip()
            if line.upper().startswith("STEP"):
                # Save previous step
                if current_step_id is not None:
                    plan.sub_tasks.append(SubTask(
                        id=current_step_id,
                        description="\n".join(current_desc_lines).strip(),
                        agent_type=current_agent,
                        dependencies=current_deps,
                    ))

                # Parse new step header
                parts = line.split("|")
                try:
                    step_part = parts[0].strip()
                    current_step_id = int("".join(c for c in step_part if c.isdigit()))
                except (ValueError, IndexError):
                    current_step_id = len(plan.sub_tasks) + 1

                current_agent = parts[1].strip().lower() if len(parts) > 1 else "chat"
                current_deps = []
                if len(parts) > 2:
                    dep_str = parts[2].strip()
                    dep_str = dep_str.replace("depends:", "").strip()
                    if dep_str and dep_str.lower() != "none":
                        current_deps = [
                            int(d.strip()) for d in dep_str.split(",")
                            if d.strip().isdigit()
                        ]
                current_desc_lines = []
            elif current_step_id is not None and line:
                current_desc_lines.append(line)

        # Save last step
        if current_step_id is not None:
            plan.sub_tasks.append(SubTask(
                id=current_step_id,
                description="\n".join(current_desc_lines).strip(),
                agent_type=current_agent,
                dependencies=current_deps,
            ))

        return plan
