# project_manager/cli.py

import sys
import os

# Ensure the project root is on Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ─── Create all tables (projects, tasks, users) if they don’t already exist ───
from project_manager.models import Base, engine

# Import each model so Base.metadata knows about them
import project_manager.models.project
import project_manager.models.task
import project_manager.models.user   # ← New User model import

Base.metadata.create_all(bind=engine)
# ───────────────────────────────────────────────────────────────────────────────

from project_manager.helpers import (
    exit_program,
    create_project,
    list_projects,
    find_project,
    delete_project,
    view_project_tasks,
    create_task,
    list_tasks,
    find_task,
    delete_task,
    view_task_details,
)

def main():
    while True:
        print("\n=== TASK & PROJECT MANAGER ===")
        print("1. Projects")
        print("2. Tasks")
        print("0. Exit")
        choice = input("> ").strip()

        if choice == "0":
            exit_program()
        elif choice == "1":
            project_menu()
        elif choice == "2":
            task_menu()
        else:
            print("❌ Invalid choice. Please select 0, 1, or 2.")

def project_menu():
    while True:
        print("\n--- PROJECT MENU ---")
        print("1. Create a project")
        print("2. List all projects")
        print("3. Find a project by name or ID")
        print("4. Delete a project")
        print("5. View tasks for a project")
        print("0. Back to main menu")
        choice = input("> ").strip()

        if choice == "0":
            return
        elif choice == "1":
            create_project()
        elif choice == "2":
            list_projects()
        elif choice == "3":
            find_project()
        elif choice == "4":
            delete_project()
        elif choice == "5":
            view_project_tasks()
        else:
            print("❌ Invalid choice. Choose 0–5.")

def task_menu():
    while True:
        print("\n--- TASK MENU ---")
        print("1. Create a task")
        print("2. List all tasks")
        print("3. Find a task by name or ID")
        print("4. Delete a task")
        print("5. View task details")
        print("0. Back to main menu")
        choice = input("> ").strip()

        if choice == "0":
            return
        elif choice == "1":
            create_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            find_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            view_task_details()
        else:
            print("❌ Invalid choice. Choose 0–5.")

if __name__ == "__main__":
    main()
