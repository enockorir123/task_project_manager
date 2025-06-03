Task & Project Manager

A command-line interface (CLI) application that helps small teams model real-world workflows. It
uses SQLAlchemy ORM with SQLite and Alembic for migrations. 
Supports CRUD for:
 Projects: High-level initiatives (e.g., "Dukakit POS system", "Moringa School end-of-phase-project").
 Tasks: Work items (e.g., Prototyping, Development, Testing, Documentation, Deployment).
 Users: People (e.g., Enock, Victor, Erick, Zawadi) who can be assigned to tasks.

Table of Contents

1. Features
2. Prerequisites
3. Installation & Setup
4. Database & Migrations
5. Project Structure
6. Usage Examples
7. Data Model
8. Future Enhancements

Features

 Project Management

 - Create, list, find, update, delete projects.
 - Track progress (percent complete, days remaining).
 - Enforce business rules: deadlines >= start dates.

 Task Management

 - CRUD tasks linked to projects, optionally assigned to users.
 - Track status (To Do, In Progress, Done), due dates, and overdue warnings.
 - Enforce: due dates <= project deadline.

 User Management

 - CRUD users, assign tasks to Enock, Victor, Erick, or Zawadi.
- Database Integrity & Migrations
 - SQLite database via SQLAlchemy.
 - Alembic for safe, in-place schema changes.

 Interactive CLI

 - Intuitive, looping menus for Projects, Tasks, Users.
 - Validates input with clear error messages.

Prerequisites

- OS: Linux, macOS, or Windows with WSL.
- Python: 3.9+
- pipenv: For virtual environment and dependencies.

Installation & Setup

1. Clone:
 git clone https://github.com/your-username/task-project-manager.git
 cd task-project-manager
2. Install & Activate:
 pipenv install
 pipenv shell
3. Initial Database (creates tables for Projects, Tasks, Users):

 pipenv run python - << 'EOF'
 from project_manager.models import Base, engine
 import project_manager.models.project
 import project_manager.models.task
 import project_manager.models.user
 Base.metadata.create_all(bind=engine)
 print(" Tables created.")
 EOF

Database & Migrations

All changes to schema use Alembic. Commands:
- Stamp current schema (mark as up-to-date):
 pipenv run alembic stamp head
- Generate new migration (after updating models):
 pipenv run alembic revision --autogenerate -m "Describe changes"
- Apply migrations:
 pipenv run alembic upgrade head
- View current revision:
 pipenv run alembic current
Existing migrations include:
- Initial creation of Projects & Tasks.
- Adding Users table and user_id to Tasks.

Project Structure

task-project-manager/
|-- alembic/
| |-- env.py
| \-- versions/
| |-- <uuid>_initial_schema.py
| \-- <uuid>_add_users_and_task_user_id.py
|-- db/
| \-- database.db
|-- project_manager/
| |-- cli.py
| |-- helpers.py
| \-- models/
| |-- project.py
| |-- task.py
| \-- user.py
|-- Pipfile
|-- Pipfile.lock
\-- README.md

Usage Examples

Launch the CLI:
pipenv run python project_manager/cli.py
You'll see:

=== TASK & PROJECT MANAGER ===
1. Projects
2. Tasks
3. Users
0. Exit

Projects Menu

1. Create a project

 > 1
 Project: Dukakit POS system
 Description: Retail point-of-sale for local stores
 Start date (default 2025-06-03):
 Deadline [YYYY-MM-DD]: 2025-07-01
 Priority (1=High,2=Medium,3=Low) [default=2]: 1
 Project 'Dukakit POS system' created.

2. List all projects

 > 2
 ID: 1 | Dukakit POS system | Deadline: 2025-07-01 | Priority: High | Progress: 0% | 28 days
remaining

3. Find a project

 > 3
 Enter ID or name: Moringa
 ID: 2
 Name: Moringa School end-of-phase project
 Description: Compile final deliverables
 Start: 2025-06-03 | Deadline: 2025-06-30 | Priority: Medium | Progress: 0% | 27 days remaining

4. Update a project

 > 4
 ID to update: 1
 New name (leave blank): Dukakit Retail POS
 New desc (leave blank): Add mobile scanning
 New deadline [YYYY-MM-DD] (blank):
 New priority (1-High,2-Med,3-Low): 2
 Project ID 1 updated.

5. Delete a project

 > 5
 ID to delete: 2
 Confirm deletion Moringa School? (y/n): y
 Project deleted.

6. View tasks for a project

 > 6
 ID: 1
 Tasks:
 ID: 3 | Development | Status: In Progress | Due: 2025-06-15 (12 days) | User: Enock
(enock@example.com)
 ID: 5 | Testing | Status: To Do | Due: 2025-06-20 (17 days) | None

Tasks Menu

1. Create a task

 > 1
 Task name: Prototyping
 Project ID: 1
 Description: Initial wireframes
 Status (1=To Do,2=In Progress,3=Done): 1
 Due date [YYYY-MM-DD]: 2025-06-10
 Assign user (1=Enock,2=Victor,3=Erick,4=Zawadi) or blank: 1
 Task 'Prototyping' created under 'Dukakit POS system'.

2. List all 

 > 2
 ID: 1 | Prototyping | Project: Dukakit POS system | Status: To Do | Due: 2025-06-10 (7 days) |
User: Enock (enock@example.com)
 ID: 2 | Development | Project: Dukakit POS system | Status: To Do | Due: 2025-06-15 (12 days) |
None

3. Find a task

 > 3
 Enter ID or name: Development
 ID: 2
 Name: Development
 Description: Backend API
 Status: In Progress
 Due: 2025-06-15 (12 days) | Project: Dukakit POS system | Assigned to: Victor
(victor@example.com)

4. Update a task

 > 4
 ID to update: 2
 New name (blank): Documentation
 New description (blank): API docs
 New status (1-3) (blank): 2
 New due date [YYYY-MM-DD] (blank): 2025-06-18
 New project ID (blank):
 Reassign user (blank or 0 to unassign): 3
 Task ID 2 updated.

5. Delete a task

 > 5
 ID to delete: 1
 Confirm Prototyping deletion? (y/n): y
 Task deleted.

6. View task details

 > 6
 ID: 2
 Name: Documentation
 Description: API docs
 Status: In Progress
 Due: 2025-06-18 (15 days)
 Project: Dukakit POS system
 Assigned to: Erick (erick@example.com)

Users Menu

1. Create a user
 > 1
 User name: Zawadi
 Email: zawadi@example.com
 User 'Zawadi' created (ID: 4).

2. List all users

 > 2
 ID: 1 | Name: Enock | Email: enock@example.com
 ID: 2 | Name: Victor | Email: victor@example.com
 ID: 3 | Name: Erick | Email: erick@example.com
 ID: 4 | Name: Zawadi | Email: zawadi@example.com

3. Find a user

 > 3
 Enter ID: 2
 USER DETAILS
 ID: 2
 Name: Victor
 Email: victor@example.com

4. Delete a user

 > 4
 ID: 4
 Confirm Zawadi deletion? (y/n): y
 User deleted.

5. Return to main menu

 > 0


Data Model

 Project

 - id (PK)
 - name (unique, non-null)
 - description (nullable)
 - start_date (non-null)
 - deadline (non-null)
 - priority (High/Medium/Low)
 - status (Active/Completed)
 - tasks (one-to-many)

 Task

 - id (PK)
 - name (non-null)
 - description (nullable)
 - status (To Do/In Progress/Done)
 - due_date (nullable)
 - project_id (FK projects.id)
 - user_id (FK users.id, nullable)

 User

 - id (PK)
 - name (unique, non-null)
 - email (unique, non-null)

Future Enhancements

- Filtering & Reporting: Tasks due soon, by priority/status; At-risk projects.
- Notifications: Email/CLI alerts for overdue tasks or upcoming deadlines.
- Rich CLI: Colors/tables with libraries like `rich`.
- Authentication: Passwords, roles, permissions.
