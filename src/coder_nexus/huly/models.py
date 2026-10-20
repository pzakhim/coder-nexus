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


class HulyComment(BaseModel):
    """One comment on an issue, oldest first."""

    author: Optional[str] = Field(default=None, description="Author display name, if resolvable")
    created_at: Optional[str] = Field(default=None, description="ISO-8601 UTC timestamp")
    text: str = Field(default="", description="Comment text; mentions as @Name, links inline")


class HulySource(BaseModel):
    """Something the ticket points to: PO document, image, attachment, file or link."""

    kind: str = Field(description="document | image | attachment | file | link")
    title: str = Field(description="Document title or file name")
    origin: str = Field(description="Where it was found: description, attachments, or 'comment <date> by <author>'")
    url: Optional[str] = Field(default=None, description="Original URL, if any")
    mime: Optional[str] = Field(default=None, description="MIME type, if known")
    status: str = Field(
        description="READ (text included) | DOWNLOADED (saved to local_path) | AVAILABLE (can be downloaded) "
        "| UNREACHABLE (cannot be opened with this account) | EXTERNAL (outside Huly, open manually)"
    )
    local_path: Optional[str] = Field(default=None, description="Saved file when downloaded")
    text: Optional[str] = Field(default=None, description="Document text (Huly documents), truncated")
    note: Optional[str] = Field(default=None, description="Reason for UNREACHABLE, size, etc.")
    blob_id: Optional[str] = Field(default=None, exclude=True)
    object_id: Optional[str] = Field(default=None, exclude=True)


class HulyIssueRef(BaseModel):
    """Lightweight reference to a related issue (e.g. the parent)."""

    id: str = Field(description="Issue identifier (e.g., MOB-15)")
    title: str = Field(default="", description="Issue title")
    status: Optional[str] = Field(default=None, description="Issue status, if fetched")


class HulySubIssue(BaseModel):
    """Direct child issue (one level) with its own acceptance criteria."""

    id: str = Field(description="Issue identifier (e.g., MOB-16)")
    title: str = Field(description="Issue title")
    status: str = Field(default="TODO", description="Current status name (e.g. Dev Done)")
    status_category: Optional[str] = Field(default=None, description="BACKLOG | TODO | ACTIVE | WON | LOST")
    priority: str = Field(default="MEDIUM", description="Task priority")
    assignee: Optional[str] = Field(default=None, description="Assignee Huly person ID")
    assignee_name: Optional[str] = Field(default=None, description="Assignee display name, if resolvable")
    is_closed: bool = Field(default=False, description="True when DONE/CANCELLED: out of scope for new work")
    acceptance_criteria: list[str] = Field(default_factory=list, description="Explicit criteria in this sub-issue")
    acceptance_criteria_source: str = Field(default="none", description="ac_section | checklist | numbered | none")
    sub_issue_count: int = Field(default=0, description="Number of deeper children (not expanded)")


class HulyTaskDetail(BaseModel):
    """Full details of a Huly task including description and acceptance criteria."""

    id: str = Field(description="Task identifier")
    title: str = Field(description="Task title")
    description: str = Field(default="", description="Full task markdown description")
    status: str = Field(default="TODO", description="Current status name (e.g. Dev Done)")
    status_category: Optional[str] = Field(default=None, description="BACKLOG | TODO | ACTIVE | WON | LOST")
    is_closed: bool = Field(default=False, description="True when the status category is WON or LOST")
    priority: str = Field(default="MEDIUM", description="Task priority")
    assignee: Optional[str] = Field(default=None, description="Assignee Huly person ID")
    assignee_name: Optional[str] = Field(default=None, description="Assignee display name, if resolvable")
    due_date: Optional[str] = Field(default=None, description="Due date (ISO date), if set")
    acceptance_criteria: list[str] = Field(default_factory=list, description="List of criteria / checklist items")
    acceptance_criteria_source: str = Field(
        default="none",
        description="Where the criteria came from: ac_section | checklist | numbered | none (none = ask the user)",
    )
    figma_url: Optional[str] = Field(default=None, description="Associated Figma design frame URL")
    attachments: list[str] = Field(default_factory=list, description="Attached image or file paths")
    comments: list[HulyComment] = Field(default_factory=list, description="Comments, oldest first")
    sources: list[HulySource] = Field(default_factory=list, description="Documents, images, attachments, files and links the ticket points to")
    parent: Optional[HulyIssueRef] = Field(default=None, description="Parent issue when this is a sub-issue")
    sub_issues: list[HulySubIssue] = Field(default_factory=list, description="Direct children, sorted by number")

    def to_summary(self) -> HulyTaskSummary:
        """Convert detail to lightweight summary."""
        return HulyTaskSummary(
            id=self.id,
            title=self.title,
            status=self.status,
            priority=self.priority,
            assignee=self.assignee,
        )
