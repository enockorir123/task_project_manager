# project_manager/cli.py

import sys
import os

# Ensure the project root is on Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create tables if they don’t exist
from project_manager.models import Base, engine
import project_manager.models.project
import project_manager.models.task
import project_manager.models.user
Base.metadata.create_all(bind=engine)

from project_manager.helpers import (
    exit_program,
    create_project,
    list_projects,
    find_project,
    update_project,       # ← new
    delete_project,
    view_project_tasks,
    create_task,
    list_tasks,
    find_task,
    update_task,          # ← new
    delete_task,
    view_task_details,
    create_user,
    list_users,
    find_user,
    delete_user,
)

def main():
    while True:
        print("\n=== TASK & PROJECT MANAGER ===")
        print("1. Projects")
        print("2. Tasks")
        print("3. Users")
        print("0. Exit")
        choice = input("> ").strip()

        if choice == "0":
            exit_program()
        elif choice == "1":
            project_menu()
        elif choice == "2":
            task_menu()
        elif choice == "3":
            user_menu()
        else:
            print("❌ Invalid choice. Please select 0, 1, 2, or 3.")

def project_menu():
    while True:
        print("\n--- PROJECT MENU ---")
        print("1. Create a project")
        print("2. List all projects")
        print("3. Find a project by name or ID")
        print("4. Update a project")
        print("5. Delete a project")
        print("6. View tasks for a project")
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
            update_project()    
        elif choice == "5":
            delete_project()
        elif choice == "6":
            view_project_tasks()
        else:
            print("❌ Invalid choice. Choose 0–6.")

def task_menu():
    while True:
        print("\n--- TASK MENU ---")
        print("1. Create a task")
        print("2. List all tasks")
        print("3. Find a task by name or ID")
        print("4. Update a task")
        print("5. Delete a task")
        print("6. View task details")
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
            update_task()          
        elif choice == "5":
            delete_task()
        elif choice == "6":
            view_task_details()
        else:
            print("❌ Invalid choice. Choose 0–6.")

def user_menu():
    while True:
        print("\n--- USER MENU ---")
        print("1. Create a user")
        print("2. List all users")
        print("3. Find a user by name or ID")
        print("4. Delete a user")
        print("0. Back to main menu")
        choice = input("> ").strip()

        if choice == "0":
            return
        elif choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            find_user()
        elif choice == "4":
            delete_user()
        else:
            print("❌ Invalid choice. Choose 0–4.")

if __name__ == "__main__":
    main()
