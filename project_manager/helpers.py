# project_manager/helpers.py

from datetime import datetime, date
import sqlalchemy as sa
from project_manager.models import SessionLocal
from project_manager.models.project import Project
from project_manager.models.task import Task
from project_manager.models.user import User

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
    """List all projects with progress and days remaining."""
    session = SessionLocal()
    try:
        projects = session.query(Project).order_by(Project.deadline).all()
        if not projects:
            print("\n⚠️ No projects found.\n")
            return

        print("\n📋 PROJECT LIST")
        print("=" * 60)
        for p in projects:
            perc = f"{p.completion_percentage:.0f}%"
            days = p.days_remaining
            days_str = f"{days} days remaining" if days >= 0 else f"Overdue by {abs(days)} days"
            print(
                f"ID: {p.id} | Name: {p.name} | Deadline: {p.deadline} | "
                f"Priority: {p.priority} | Progress: {perc} | {days_str}"
            )
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error listing projects: {e}")
    finally:
        session.close()

def find_project():
    """Find a project by ID or name, and show progress and days remaining."""
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

        perc = f"{project.completion_percentage:.0f}% complete"
        days = project.days_remaining
        days_str = (
            (f"{days} days remaining" if days >= 0 else f"Overdue by {abs(days)} days")
            if days is not None else "No deadline"
        )

        print("\n📋 PROJECT DETAILS")
        print("=" * 40)
        print(f"ID:          {project.id}")
        print(f"Name:        {project.name}")
        print(f"Description: {project.description or '-'}")
        print(f"Start Date:  {project.start_date}")
        print(f"Deadline:    {project.deadline}")
        print(f"Priority:    {project.priority}")
        print(f"Status:      {project.status}")
        print(f"Progress:    {perc}")
        print(f"Time Left:   {days_str}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error finding project: {e}")
    finally:
        session.close()

def update_project():
    """Update a project’s name, description, deadline, or priority."""
    session = SessionLocal()
    try:
        project_id = input("Enter the project ID to update: ").strip()
        if not project_id.isdigit():
            print("❌ Invalid project ID.")
            return

        project = session.query(Project).filter(Project.id == int(project_id)).first()
        if not project:
            print(f"⚠️ No project found with ID {project_id}.")
            return

        print("\n--- UPDATE PROJECT ---")
        print(f"Current name: {project.name}")
        new_name = input("New name (leave blank to keep current): ").strip()
        if new_name:
            project.name = new_name

        print(f"Current description: {project.description or '-'}")
        new_desc = input("New description (leave blank to keep current): ").strip()
        if new_desc:
            project.description = new_desc

        print(f"Current deadline: {project.deadline}")
        new_dead = input("New deadline [YYYY-MM-DD] (leave blank to keep current): ").strip()
        if new_dead:
            try:
                new_dead_dt = datetime.strptime(new_dead, "%Y-%m-%d").date()
                if new_dead_dt < project.start_date:
                    print("❌ Deadline cannot be before start date!")
                    return
                project.deadline = new_dead_dt
            except ValueError:
                print("❌ Invalid date format! Use YYYY-MM-DD")
                return

        print(f"Current priority: {project.priority}")
        print("Priority levels: 1=High, 2=Medium, 3=Low")
        new_prio = input("Select new priority (1-3) (leave blank to keep current): ").strip()
        if new_prio in ('1', '2', '3'):
            priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
            project.priority = priority_map[new_prio]

        session.commit()
        print(f"✅ Project ID {project.id} updated successfully.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error updating project: {e}")
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

        session.query(Task).filter(Task.project_id == project.id).delete()
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
        print("=" * 60)
        for t in tasks:
            days = t.days_remaining
            time_str = (
                f"{days}d remaining" if days >= 0
                else f"Overdue by {abs(days)}d"
            ) if t.due_date else "No due date"
            user_info = f" | User: {t.user.name} ({t.user.email})" if t.user else ""
            print(
                f"ID: {t.id} | Name: {t.name} | Status: {t.status} | "
                f"Due: {t.due_date or '-'} ({time_str}){user_info}"
            )
        print("=" * 60)

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

        status_map = {'1': 'To Do', '2': 'In Progress', '3': 'Done'}
        print("Task status options: 1=To Do, 2=In Progress, 3=Done")
        status_choice = input("Select status (1-3) [default=1]: ").strip()
        status = status_map.get(status_choice, 'To Do')

        due_input = input("Due date [YYYY-MM-DD] (optional): ").strip()
        if due_input == "":
            due_date = None
        else:
            try:
                due_date = datetime.strptime(due_input, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid due date format! Use YYYY-MM-DD")
                return

        # Select user for this task (optional)
        print("\nAssign a user to this task (optional):")
        users = session.query(User).all()
        if users:
            for u in users:
                print(f"  {u.id}. {u.name} ({u.email})")
            user_choice = input("Select user ID or leave blank: ").strip()
            if user_choice == "":
                user_id = None
            elif user_choice.isdigit():
                chosen = session.query(User).filter(User.id == int(user_choice)).first()
                if chosen:
                    user_id = chosen.id
                else:
                    print("❌ Invalid user selection!")
                    return
            else:
                print("❌ Invalid input for user ID.")
                return
        else:
            user_id = None

        task = Task(
            name=name,
            description=description,
            status=status,
            due_date=due_date,
            project_id=project.id,
            user_id=user_id
        )

        session.add(task)
        session.commit()

        print(f"✅ Task '{name}' created successfully under project '{project.name}'!")
        if due_date:
            print(f"   Due date: {due_date}")
        print(f"   Status: {status}")
        if user_id:
            print(f"   Assigned to user ID: {user_id}")

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
            due = t.due_date or "-"
            days = t.days_remaining
            time_str = (
                f"{days}d remaining" if days is not None and days >= 0
                else (f"Overdue by {abs(days)}d" if days is not None else "No due date")
            )
            user_info = f" | User: {t.user.name} ({t.user.email})" if t.user else ""
            print(
                f"ID: {t.id} | Name: {t.name} | Project: {project_name} | "
                f"Status: {t.status} | Due: {due} ({time_str}){user_info}"
            )
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

        days = task.days_remaining
        if days is None:
            time_str = "No due date"
        else:
            time_str = f"{days}d remaining" if days >= 0 else f"Overdue by {abs(days)}d"

        user_info = f"{task.user.name} ({task.user.email})" if task.user else "No user assigned"

        print("\n📝 TASK DETAILS")
        print("=" * 40)
        print(f"ID:          {task.id}")
        print(f"Name:        {task.name}")
        print(f"Description: {task.description or '-'}")
        print(f"Status:      {task.status}")
        print(f"Due Date:    {task.due_date or '-'} ({time_str})")
        print(f"Project:     {task.project.name if task.project else 'No Project'}")
        print(f"Assigned to: {user_info}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error finding task: {e}")
    finally:
        session.close()

def update_task():
    """Update a task’s name, description, status, due date, project, or user."""
    session = SessionLocal()
    try:
        task_id = input("Enter the task ID to update: ").strip()
        if not task_id.isdigit():
            print("❌ Invalid task ID.")
            return

        task = session.query(Task).filter(Task.id == int(task_id)).first()
        if not task:
            print(f"⚠️ No task found with ID {task_id}.")
            return

        print("\n--- UPDATE TASK ---")
        print(f"Current name: {task.name}")
        new_name = input("New name (leave blank to keep current): ").strip()
        if new_name:
            task.name = new_name

        print(f"Current description: {task.description or '-'}")
        new_desc = input("New description (leave blank to keep current): ").strip()
        if new_desc:
            task.description = new_desc

        print(f"Current status: {task.status}")
        print("Status options: 1=To Do, 2=In Progress, 3=Done")
        new_status = input("Select new status (1-3) (leave blank to keep current): ").strip()
        if new_status in ('1', '2', '3'):
            status_map = {'1': 'To Do', '2': 'In Progress', '3': 'Done'}
            task.status = status_map[new_status]

        print(f"Current due date: {task.due_date or '-'}")
        new_due = input("New due date [YYYY-MM-DD] (leave blank to keep current): ").strip()
        if new_due:
            try:
                new_due_dt = datetime.strptime(new_due, "%Y-%m-%d").date()
                if new_due_dt < date.today():
                    print("❌ Due date cannot be in the past!")
                    return
                if new_due_dt > task.project.deadline:
                    print(f"❌ Due date cannot exceed project deadline ({task.project.deadline})!")
                    return
                task.due_date = new_due_dt
            except ValueError:
                print("❌ Invalid date format! Use YYYY-MM-DD")
                return

        # Reassign project (optional)
        print(f"Current project ID: {task.project_id}")
        new_proj = input("New project ID (leave blank to keep current): ").strip()
        if new_proj:
            if not new_proj.isdigit():
                print("❌ Invalid project ID.")
                return
            proj = session.query(Project).filter(Project.id == int(new_proj)).first()
            if not proj:
                print(f"❌ Project with ID {new_proj} does not exist!")
                return
            task.project_id = proj.id

        # Reassign user (optional)
        print(f"Current assigned user ID: {task.user_id or 'None'}")
        users = session.query(User).all()
        if users:
            for u in users:
                print(f"  {u.id}. {u.name} ({u.email})")
        new_user = input("New user ID (leave blank to keep current or '0' to unassign): ").strip()
        if new_user == '0':
            task.user_id = None
        elif new_user.isdigit():
            u = session.query(User).filter(User.id == int(new_user)).first()
            if not u:
                print("❌ Invalid user ID.")
                return
            task.user_id = u.id

        session.commit()
        print(f"✅ Task ID {task.id} updated successfully.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error updating task: {e}")
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

        days = task.days_remaining
        if days is None:
            time_str = "No due date"
        else:
            time_str = f"{days}d remaining" if days >= 0 else f"Overdue by {abs(days)}d"

        user_info = f"{task.user.name} ({task.user.email})" if task.user else "No user assigned"

        print("\n📝 TASK DETAILS")
        print("=" * 40)
        print(f"ID:          {task.id}")
        print(f"Name:        {task.name}")
        print(f"Description: {task.description or '-'}")
        print(f"Status:      {task.status}")
        print(f"Due Date:    {task.due_date or '-'} ({time_str})")
        print(f"Project:     {task.project.name if task.project else 'No Project'}")
        print(f"Assigned to: {user_info}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error viewing task details: {e}")
    finally:
        session.close()

# ─── User Helpers ────────────────────────────────────────────────────────────

def create_user():
    """Create a new user with name and email."""
    session = SessionLocal()
    try:
        print("\n👤 CREATE NEW USER")
        print("=" * 40)

        name = input("User name: ").strip()
        if not name:
            print("❌ User name cannot be empty!")
            return

        email = input("Email address: ").strip()
        if not email:
            print("❌ Email cannot be empty!")
            return

        # Check for duplicate email or name
        existing = session.query(User).filter(
            sa.or_(User.email == email, User.name == name)
        ).first()
        if existing:
            print("❌ A user with that name or email already exists!")
            return

        user = User(name=name, email=email)
        session.add(user)
        session.commit()

        print(f"✅ User '{name}' created successfully (ID: {user.id})")

    except Exception as e:
        session.rollback()
        print(f"❌ Error creating user: {e}")
    finally:
        session.close()

def list_users():
    """List all users."""
    session = SessionLocal()
    try:
        users = session.query(User).order_by(User.name).all()
        if not users:
            print("\n⚠️ No users found.\n")
            return

        print("\n👥 USER LIST")
        print("=" * 50)
        for u in users:
            print(f"ID: {u.id} | Name: {u.name} | Email: {u.email}")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Error listing users: {e}")
    finally:
        session.close()

def find_user():
    """Find a user by ID or name."""
    session = SessionLocal()
    try:
        search_term = input("Enter user ID or name to search: ").strip()
        if search_term.isdigit():
            user = session.query(User).filter(User.id == int(search_term)).first()
        else:
            user = session.query(User).filter(User.name.ilike(f"%{search_term}%")).first()

        if not user:
            print(f"⚠️ User '{search_term}' not found.")
            return

        print("\n👤 USER DETAILS")
        print("=" * 40)
        print(f"ID:    {user.id}")
        print(f"Name:  {user.name}")
        print(f"Email: {user.email}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error finding user: {e}")
    finally:
        session.close()

def delete_user():
    """Delete a user by ID."""
    session = SessionLocal()
    try:
        user_id = input("Enter the user ID to delete: ").strip()
        if not user_id.isdigit():
            print("❌ Invalid user ID.")
            return

        user = session.query(User).filter(User.id == int(user_id)).first()
        if not user:
            print(f"⚠️ No user found with ID {user_id}.")
            return

        confirm = input(f"Are you sure you want to delete user '{user.name}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Deletion cancelled.")
            return

        session.delete(user)
        session.commit()
        print(f"✅ User '{user.name}' has been deleted.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting user: {e}")
    finally:
        session.close()
