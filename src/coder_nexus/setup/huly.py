"""Huly CLI commands: `setup huly` (login), `setup huly --check` (status) and read-only task queries."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from ..huly.auth import load_client_credentials
from ..huly.client import HulyClient
from ..huly.models import HulyCredentials


def cmd_login(args: argparse.Namespace) -> int:
    """Handle `coder_nexus login` command."""
    workspace_path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()

    email = args.email
    password = args.password
    url = args.url or "https://huly.app"

    if not email:
        email = input("Huly Account Email / Username: ").strip()
    if not password:
        import getpass
        password = getpass.getpass("Huly Account Password: ").strip()

    client = HulyClient(credentials=HulyCredentials(workspace_url=url, email=email, password=password))

    async def _do_login():
        return await client.login(
            workspace_url=url,
            email=email,
            password=password,
            workspace_path=workspace_path,
        )

    try:
        token = asyncio.run(_do_login())
        masked_token = f"{token[:12]}..." if len(token) > 12 else token
        env_file = Path(workspace_path) / ".env"
        print(f"✅ Huly Login Success!")
        print(f"   Workspace URL : {url}")
        print(f"   Email         : {email}")
        print(f"   Workspace ID  : {client.credentials.workspace_id or '(default)'}")
        print(f"   Session Token : {masked_token}")
        print(f"   Client .env   : {env_file}")
        return 0
    except Exception as exc:
        print(f"❌ Login failed: {exc}", file=sys.stderr)
        return 1


def cmd_my_tasks(args: argparse.Namespace) -> int:
    """Handle `coder_nexus my-tasks` command."""
    workspace_path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()
    client = HulyClient.from_workspace(workspace_path)

    async def _fetch():
        return await client.get_my_uncompleted_tasks(workspace_path=workspace_path)

    try:
        tasks = asyncio.run(_fetch())
        if args.json:
            print(json.dumps([t.model_dump() for t in tasks], indent=2))
            return 0

        print(f"\n📋 My Uncompleted Tasks ({len(tasks)} tasks):")
        print(f"{'ID':<12} | {'PRIORITY':<8} | {'STATUS':<12} | {'TITLE'}")
        print("-" * 75)
        for t in tasks:
            print(f"{t.id:<12} | {t.priority.upper():<8} | {t.status:<12} | {t.title}")
        print("-" * 75 + "\n")
        return 0
    except Exception as exc:
        print(f"❌ Failed to fetch tasks: {exc}", file=sys.stderr)
        return 1


def cmd_task_detail(args: argparse.Namespace) -> int:
    """Handle `coder_nexus task-detail <task_id>` command."""
    workspace_path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()
    client = HulyClient.from_workspace(workspace_path)

    async def _fetch():
        return await client.get_task_detail(args.task_id, workspace_path=workspace_path)

    try:
        detail = asyncio.run(_fetch())
        if args.json:
            print(json.dumps(detail.model_dump(), indent=2))
            return 0

        print(f"\n========================================================")
        print(f"📌 Task: [{detail.id}] {detail.title}")
        print(f"   Status: {detail.status} | Priority: {detail.priority} | Assignee: {detail.assignee or 'Unassigned'}")
        print(f"========================================================")
        print(f"\n📝 Description:\n{detail.description}\n")
        print("🎯 Acceptance Criteria:")
        for idx, ac in enumerate(detail.acceptance_criteria, 1):
            print(f"  [{idx}] {ac}")
        if detail.figma_url:
            print(f"\n🎨 Figma URL: {detail.figma_url}")
        if detail.attachments:
            print(f"📎 Attachments: {', '.join(detail.attachments)}")
        print("========================================================\n")
        return 0
    except Exception as exc:
        print(f"❌ Failed to fetch task detail: {exc}", file=sys.stderr)
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    """Check current authentication status in client workspace .env."""
    workspace_path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()
    creds = load_client_credentials(workspace_path)

    print(f"\n🔍 Huly Client Environment Status:")
    print(f"   Workspace Path : {workspace_path}")
    print(f"   Target .env    : {Path(workspace_path) / '.env'}")
    print(f"   Workspace URL  : {creds.workspace_url}")
    print(f"   Email          : {creds.email or '(not set)'}")
    print(f"   Workspace ID   : {creds.workspace_id or '(not resolved)'}")
    print(f"   Has Session    : {'Yes' if creds.session_token else 'No'}")
    print(f"   Authenticated  : {'Yes' if creds.is_authenticated else 'No'}\n")
    return 0


def cmd_setup_huly(args: argparse.Namespace) -> int:
    """`coder-nexus setup huly`: log in, or with --check report status (exit 0 only when authenticated)."""
    if not args.check:
        return cmd_login(args)
    cmd_status(args)
    path = str(Path(args.workspace_path).resolve()) if args.workspace_path else os.getcwd()
    return 0 if load_client_credentials(path).is_authenticated else 1
