from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from model import Base
from model.user import User


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    zip_code = Column(String(9), nullable=False)
    street = Column(String(100), nullable=False)
    complement = Column(String(100), nullable=True)
    neighborhood = Column(String(50), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    ibge_code = Column(Integer, nullable=True)
    gia_code = Column(Integer, nullable=True)
    ddd_code = Column(Integer, nullable=True)
    siafi_code = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='addresses')

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self,
                 zip_code: str,
                 street: str,
                 complement: str,
                 neighborhood: str,
                 city: str,
                 state: str,
                 ibge_code: int,
                 gia_code: int,
                 ddd_code: int,
                 siafi_code: int,
                 user: User
                 ):
        """
        create a new address.

        Arguments:
            zip_code: cep code witth - separator like 12345-678.
            street: The street name of the address.
            complement: The complement of the address.
            neighborhood: The neighborhood of the address.
            city: The city of the address.
            state: The state of the address.
            ibge_code: The IBGE code of the address.
            gia_code: The GIA code of the address.
            ddd_code: The DDD code of the address.
            siafi_code: The SIAFI code of the address.    
        """
        self.zip_code = zip_code
        self.street = street
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.ibge_code = ibge_code
        self.gia_code = gia_code
        self.ddd_code = ddd_code
        self.siafi_code = siafi_code
        self.user = user
