from sqlalchemy import Column, Integer, String, Float
from db.base import Base


class PlanORM(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, default=0)
    max_projects = Column(Integer, nullable=True)  # None = unlimited