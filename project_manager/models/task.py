# project_manager/models/task.py

from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from . import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="To Do")  # To Do, In Progress, Done
    due_date = Column(Date, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    project = relationship("Project", back_populates="tasks", lazy="joined")
    user = relationship("User", back_populates="tasks", lazy="joined")

    @validates("due_date")
    def validate_due_date(self, key, due_value):
        """
        Ensure due_date is not in the past and, if project.deadline exists, not after it.
        """
        if due_value and due_value < date.today():
            raise ValueError(f"Due date ({due_value}) cannot be in the past.")
        if self.project and self.project.deadline and due_value and due_value > self.project.deadline:
            raise ValueError(
                f"Due date ({due_value}) cannot exceed project deadline ({self.project.deadline})."
            )
        return due_value

    @property
    def days_remaining(self) -> int | None:
        if not self.due_date:
            return None
        return (self.due_date - date.today()).days

    def __repr__(self):
        user_part = f", user_id={self.user_id}" if self.user_id else ""
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status}'{user_part})>"
