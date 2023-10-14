from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SampleModel(Base):
    __tablename__ = 'sample'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)