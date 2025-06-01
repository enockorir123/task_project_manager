# project_manager/models/project.py

from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship, validates
from . import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=False, default=date.today)
    deadline = Column(Date, nullable=False)
    priority = Column(String, nullable=False, default="Medium")  # High, Medium, Low
    status = Column(String, nullable=False, default="Active")    # Active or Completed

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    @validates("deadline")
    def validate_deadline(self, key, deadline_value):
        """
        Ensure that deadline is not before start_date.
        """
        if deadline_value < self.start_date:
            raise ValueError(
                f"Deadline ({deadline_value}) cannot be before start date ({self.start_date})."
            )
        return deadline_value

    @property
    def completion_percentage(self) -> float:
        """
        Returns percentage of tasks marked “Done” for this project.
        """
        if not self.tasks:
            return 0.0
        total = len(self.tasks)
        done_count = sum(1 for t in self.tasks if t.status.lower() == "done")
        return (done_count / total) * 100.0

    @property
    def days_remaining(self) -> int:
        """
        Days until deadline. Negative if past.
        """
        delta = self.deadline - date.today()
        return delta.days

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
