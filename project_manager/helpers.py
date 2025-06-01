# project_manager/helpers.py

from project_manager.models import SessionLocal
from project_manager.models.project import Project
from project_manager.models.task import Task

def exit_program():
    print("\nGoodbye!")
    exit()

# ─── Project Helpers ─────────────────────────────────────────────────────────

def create_project():
    """Prompt user to create a new project."""
    print("\n[create_project] Not implemented yet.\n")

def list_projects():
    """List all projects."""
    print("\n[list_projects] Not implemented yet.\n")

def find_project():
    """Find a project by name or ID."""
    print("\n[find_project] Not implemented yet.\n")

def delete_project():
    """Delete a project (and its tasks)."""
    print("\n[delete_project] Not implemented yet.\n")

def view_project_tasks():
    """Display all tasks for a given project."""
    print("\n[view_project_tasks] Not implemented yet.\n")

# ─── Task Helpers ────────────────────────────────────────────────────────────

def create_task():
    """Prompt user to create a new task."""
    print("\n[create_task] Not implemented yet.\n")

def list_tasks():
    """List all tasks."""
    print("\n[list_tasks] Not implemented yet.\n")

def find_task():
    """Find a task by name or ID."""
    print("\n[find_task] Not implemented yet.\n")

def delete_task():
    """Delete a task."""
    print("\n[delete_task] Not implemented yet.\n")

def view_task_details():
    """Display details for a given task."""
    print("\n[view_task_details] Not implemented yet.\n")
