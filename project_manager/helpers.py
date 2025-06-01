# project_manager/helpers.py

from datetime import datetime, date
from project_manager.models import SessionLocal
from project_manager.models.project import Project
from project_manager.models.task import Task

def exit_program():
    print("\nGoodbye!")
    exit()

# ─── Project Helpers ─────────────────────────────────────────────────────────

def create_project():
    """Create a new project with validation and save to the database."""
    session = SessionLocal()
    try:
        print("\n📋 CREATE NEW PROJECT")
        print("=" * 40)

        name = input("Project name: ").strip()
        if not name:
            print("❌ Project name cannot be empty!")
            return

        existing = session.query(Project).filter(Project.name == name).first()
        if existing:
            print(f"❌ A project named '{name}' already exists!")
            return

        description = input("Project description (optional): ").strip()
        if description == "":
            description = None

        default_start = date.today()
        start_input = input(f"Start date [YYYY-MM-DD] (default {default_start}): ").strip()
        if start_input == "":
            start_date = default_start
        else:
            try:
                start_date = datetime.strptime(start_input, "%Y-%m-%d").date()
                if start_date < date.today():
                    print("❌ Start date cannot be in the past!")
                    return
            except ValueError:
                print("❌ Invalid date format! Use YYYY-MM-DD")
                return

        deadline_input = input("Deadline [YYYY-MM-DD]: ").strip()
        try:
            deadline = datetime.strptime(deadline_input, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Invalid date format for deadline! Use YYYY-MM-DD")
            return

        if deadline < start_date:
            print(f"❌ Deadline ({deadline}) cannot be before start date ({start_date})!")
            return

        print("Priority levels: 1=High, 2=Medium, 3=Low")
        priority_choice = input("Select priority (1-3) [default=2]: ").strip()
        priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
        priority = priority_map.get(priority_choice, 'Medium')

        project = Project(
            name=name,
            description=description,
            start_date=start_date,
            deadline=deadline,
            priority=priority
        )

        session.add(project)
        session.commit()

        print(f"✅ Project '{name}' created successfully!")
        print(f"   Start date:  {start_date}")
        print(f"   Deadline:    {deadline}")
        print(f"   Priority:    {priority}")

    except Exception as e:
        session.rollback()
        print(f"❌ Error creating project: {e}")
    finally:
        session.close()

def list_projects():
    """List all projects."""
    session = SessionLocal()
    try:
        projects = session.query(Project).order_by(Project.deadline).all()
        if not projects:
            print("\n⚠️ No projects found.\n")
            return
        print("\n📋 PROJECT LIST")
        print("=" * 50)
        for p in projects:
            print(f"ID: {p.id} | Name: {p.name} | Deadline: {p.deadline} | Priority: {p.priority}")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Error listing projects: {e}")
    finally:
        session.close()

def find_project():
    """Find a project by ID or name."""
    session = SessionLocal()
    try:
        search_term = input("Enter project ID or name to search: ").strip()
        if search_term.isdigit():
            project = session.query(Project).filter(Project.id == int(search_term)).first()
        else:
            project = session.query(Project).filter(Project.name.ilike(f"%{search_term}%")).first()

        if not project:
            print(f"⚠️ Project '{search_term}' not found.")
            return

        print("\n📋 PROJECT DETAILS")
        print("=" * 40)
        print(f"ID:          {project.id}")
        print(f"Name:        {project.name}")
        print(f"Description: {project.description or '-'}")
        print(f"Start Date:  {project.start_date}")
        print(f"Deadline:    {project.deadline}")
        print(f"Priority:    {project.priority}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error finding project: {e}")
    finally:
        session.close()

def delete_project():
    """Delete a project and its tasks."""
    session = SessionLocal()
    try:
        project_id = input("Enter the project ID to delete: ").strip()
        if not project_id.isdigit():
            print("❌ Invalid project ID.")
            return

        project = session.query(Project).filter(Project.id == int(project_id)).first()
        if not project:
            print(f"⚠️ No project found with ID {project_id}.")
            return

        confirm = input(f"Are you sure you want to delete project '{project.name}' and all its tasks? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Deletion cancelled.")
            return

        # Delete all tasks associated with the project
        session.query(Task).filter(Task.project_id == project.id).delete()

        # Delete the project itself
        session.delete(project)
        session.commit()
        print(f"✅ Project '{project.name}' and its tasks have been deleted.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting project: {e}")
    finally:
        session.close()

def view_project_tasks():
    """Display all tasks for a given project."""
    session = SessionLocal()
    try:
        project_id = input("Enter the project ID to view tasks: ").strip()
        if not project_id.isdigit():
            print("❌ Invalid project ID.")
            return

        project = session.query(Project).filter(Project.id == int(project_id)).first()
        if not project:
            print(f"⚠️ No project found with ID {project_id}.")
            return

        tasks = session.query(Task).filter(Task.project_id == project.id).order_by(Task.due_date).all()
        if not tasks:
            print(f"\n⚠️ No tasks found for project '{project.name}'.\n")
            return

        print(f"\n📋 TASKS FOR PROJECT: {project.name}")
        print("=" * 50)
        for t in tasks:
            print(f"ID: {t.id} | Name: {t.name} | Status: {t.status} | Due: {t.due_date}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error viewing project tasks: {e}")
    finally:
        session.close()

# ─── Task Helpers ────────────────────────────────────────────────────────────

def create_task():
    """Prompt user to create a new task."""
    session = SessionLocal()
    try:
        print("\n📝 CREATE NEW TASK")
        print("=" * 40)

        name = input("Task name: ").strip()
        if not name:
            print("❌ Task name cannot be empty!")
            return

        # Select project for task
        project_id = input("Project ID to assign task to: ").strip()
        if not project_id.isdigit():
            print("❌ Invalid project ID.")
            return

        project = session.query(Project).filter(Project.id == int(project_id)).first()
        if not project:
            print(f"❌ Project with ID {project_id} does not exist!")
            return

        description = input("Task description (optional): ").strip()
        if description == "":
            description = None

        # Status (To Do, In Progress, Done)
        status_map = {'1': 'To Do', '2': 'In Progress', '3': 'Done'}
        print("Task status options: 1=To Do, 2=In Progress, 3=Done")
        status_choice = input("Select status (1-3) [default=1]: ").strip()
        status = status_map.get(status_choice, 'To Do')

        # Due date (optional)
        due_input = input("Due date [YYYY-MM-DD] (optional): ").strip()
        if due_input == "":
            due_date = None
        else:
            try:
                due_date = datetime.strptime(due_input, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid due date format! Use YYYY-MM-DD")
                return

        task = Task(
            name=name,
            description=description,
            status=status,
            due_date=due_date,
            project_id=project.id
        )

        session.add(task)
        session.commit()

        print(f"✅ Task '{name}' created successfully under project '{project.name}'!")
        if due_date:
            print(f"   Due date: {due_date}")
        print(f"   Status: {status}")

    except Exception as e:
        session.rollback()
        print(f"❌ Error creating task: {e}")
    finally:
        session.close()

def list_tasks():
    """List all tasks."""
    session = SessionLocal()
    try:
        tasks = session.query(Task).order_by(Task.due_date).all()
        if not tasks:
            print("\n⚠️ No tasks found.\n")
            return

        print("\n📝 TASK LIST")
        print("=" * 60)
        for t in tasks:
            project_name = t.project.name if t.project else "No Project"
            print(f"ID: {t.id} | Name: {t.name} | Project: {project_name} | Status: {t.status} | Due: {t.due_date or '-'}")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error listing tasks: {e}")
    finally:
        session.close()

def find_task():
    """Find a task by ID or name."""
    session = SessionLocal()
    try:
        search_term = input("Enter task ID or name to search: ").strip()
        if search_term.isdigit():
            task = session.query(Task).filter(Task.id == int(search_term)).first()
        else:
            task = session.query(Task).filter(Task.name.ilike(f"%{search_term}%")).first()

        if not task:
            print(f"⚠️ Task '{search_term}' not found.")
            return

        print("\n📝 TASK DETAILS")
        print("=" * 40)
        print(f"ID:          {task.id}")
        print(f"Name:        {task.name}")
        print(f"Description: {task.description or '-'}")
        print(f"Status:      {task.status}")
        print(f"Due Date:    {task.due_date or '-'}")
        print(f"Project:     {task.project.name if task.project else 'No Project'}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error finding task: {e}")
    finally:
        session.close()

def delete_task():
    """Delete a task."""
    session = SessionLocal()
    try:
        task_id = input("Enter the task ID to delete: ").strip()
        if not task_id.isdigit():
            print("❌ Invalid task ID.")
            return

        task = session.query(Task).filter(Task.id == int(task_id)).first()
        if not task:
            print(f"⚠️ No task found with ID {task_id}.")
            return

        confirm = input(f"Are you sure you want to delete task '{task.name}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Deletion cancelled.")
            return

        session.delete(task)
        session.commit()
        print(f"✅ Task '{task.name}' has been deleted.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting task: {e}")
    finally:
        session.close()

def view_task_details():
    """Display details for a given task."""
    # This function can reuse find_task() logic or just call find_task()
    # but to keep consistency, we will implement it fully here.

    session = SessionLocal()
    try:
        task_id = input("Enter the task ID to view details: ").strip()
        if not task_id.isdigit():
            print("❌ Invalid task ID.")
            return

        task = session.query(Task).filter(Task.id == int(task_id)).first()
        if not task:
            print(f"⚠️ No task found with ID {task_id}.")
            return

        print("\n📝 TASK DETAILS")
        print("=" * 40)
        print(f"ID:          {task.id}")
        print(f"Name:        {task.name}")
        print(f"Description: {task.description or '-'}")
        print(f"Status:      {task.status}")
        print(f"Due Date:    {task.due_date or '-'}")
        print(f"Project:     {task.project.name if task.project else 'No Project'}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error viewing task details: {e}")
    finally:
        session.close()
