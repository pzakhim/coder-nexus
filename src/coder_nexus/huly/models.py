"""Pydantic models for Huly credentials, tasks, and acceptance criteria."""

from typing import Optional
from pydantic import BaseModel, Field


class HulyCredentials(BaseModel):
    """Credentials required to authenticate with Huly."""

    workspace_url: str = Field(default="https://huly.app", description="Huly workspace URL")
    email: Optional[str] = Field(default=None, description="User email for login")
    password: Optional[str] = Field(default=None, description="User password for login")
    session_token: Optional[str] = Field(default=None, description="JWT session token after login")
    workspace_id: Optional[str] = Field(default=None, description="Huly workspace UUID")

    @property
    def is_authenticated(self) -> bool:
        """Check if credentials contain a valid session token or email/password pair."""
        return bool(self.session_token or (self.email and self.password))


class HulyTaskSummary(BaseModel):
    """High-level summary of a Huly task for list view."""

    id: str = Field(description="Task identifier (e.g., AUTH-101)")
    title: str = Field(description="Task title/headline")
    status: str = Field(default="TODO", description="Task status (e.g. TODO, IN_PROGRESS, DONE)")
    priority: str = Field(default="MEDIUM", description="Task priority (LOW, MEDIUM, HIGH, URGENT)")
    assignee: Optional[str] = Field(default=None, description="User email assigned to the task")
    due_date: Optional[str] = Field(default=None, description="Due date string if any")


class HulyTaskDetail(BaseModel):
    """Full details of a Huly task including description and acceptance criteria."""

    id: str = Field(description="Task identifier")
    title: str = Field(description="Task title")
    description: str = Field(default="", description="Full task markdown description")
    status: str = Field(default="TODO", description="Current status")
    priority: str = Field(default="MEDIUM", description="Task priority")
    assignee: Optional[str] = Field(default=None, description="Assignee email")
    acceptance_criteria: list[str] = Field(default_factory=list, description="List of criteria / checklist items")
    figma_url: Optional[str] = Field(default=None, description="Associated Figma design frame URL")
    attachments: list[str] = Field(default_factory=list, description="Attached image or file paths")

    def to_summary(self) -> HulyTaskSummary:
        """Convert detail to lightweight summary."""
        return HulyTaskSummary(
            id=self.id,
            title=self.title,
            status=self.status,
            priority=self.priority,
            assignee=self.assignee,
        )
