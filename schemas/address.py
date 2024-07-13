from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    id: int
    name: str
    email: str


class AddressSchema(BaseModel):
    """ Define how an address should be represented
    """
    id: int
    zip_code: str
    street: str
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: str
    state: str
    ibge_code: Optional[int] = None
    gia_code: Optional[int] = None
    ddd_code: Optional[int] = None
    siafi_code: Optional[int] = None
    created_at: str
    updated_at: str
    user: UserSchema


class AddressCreateSchema(BaseModel):
    """ Define the structure that represents the creation of a new address.
    """
    zip_code: str
    street: str
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: str
    state: str
    ibge_code: Optional[int] = None
    gia_code: Optional[int] = None
    ddd_code: Optional[int] = None
    siafi_code: Optional[int] = None
    user_id: int


class AddressUpdateSchema(BaseModel):
    zip_code: Optional[str] = None
    street: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    ibge_code: Optional[int] = None
    gia_code: Optional[int] = None
    ddd_code: Optional[int] = None
    siafi_code: Optional[int] = None


class GetAddressResponseSchema(BaseModel):
    """ Define the structure that represents the response of a get address request.
    """
    address: AddressSchema


class ListAddressResponseSchema(BaseModel):
    """ Define the structure that represents the response of a list all addresses request.
    """
    addresses: List[AddressSchema]


class DeleteAddressResponseSchema(BaseModel):
    """ Define the structure that represents the response of a delete address request.
    """
    id: int


class DeleteAddressQuerySchema(BaseModel):
    """ Define the structure that represents the query string of a delete address request.
    """
    address_id: int


class AddressUpdateQuerySchema(BaseModel):
    """ Define the structure that represents the query string of an update address request.
    """
    address_id: int


class AddessGetQuerySchema(BaseModel):
    """ Define the structure that represents the query string of a get address request.
    """
    address_id: int


def return_address(address: AddressSchema):
    """ Returns an address in dictionary format
    """
    return {
        "id": address.id,
        "zip_code": address.zip_code,
        "street": address.street,
        "complement": address.complement,
        "neighborhood": address.neighborhood,
        "city": address.city,
        "state": address.state,
        "ibge_code": address.ibge_code,
        "gia_code": address.gia_code,
        "ddd_code": address.ddd_code,
        "siafi_code": address.siafi_code,
        "created_at": address.created_at,
        "updated_at": address.updated_at,
        "user": {
            "id": address.user.id,
            "name": address.user.name,
            "email": address.user.email
        }
    }


def return_addresses(addresses: List[AddressSchema]):
    """ Returns a list of addresses in dictionary format
    """

    result = []
    for address in addresses:
        result.append({
            "id": address.id,
            "zip_code": address.zip_code,
            "street": address.street,
            "complement": address.complement,
            "neighborhood": address.neighborhood,
            "city": address.city,
            "state": address.state,
            "ibge_code": address.ibge_code,
            "gia_code": address.gia_code,
            "ddd_code": address.ddd_code,
            "siafi_code": address.siafi_code,
            "created_at": address.created_at,
            "updated_at": address.updated_at
        })

    return {"address": result}
