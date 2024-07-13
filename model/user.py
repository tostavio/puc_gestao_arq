from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from model import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    addresses = relationship("Address", back_populates="user")

    def __init__(self,
                 name: str,
                 email: str
                 ):
        """
        create a new user.

        Arguments:
            name: The name of the user.
            email: The email of the user.
        """
        self.name = name
        self.email = email
