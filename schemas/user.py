from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    """ Define como um user deve ser representado
    """
    id: int
    name: str
    email: str
    created_at: str
    updated_at: str


class UserCreateSchema(BaseModel):
    """ Define como deve ser a estrutura que representa o a criação
        de um novo user.
    """
    name: str
    email: str


class ListUserResponseSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a resposta da
        requisição de listagem de todos os user.
    """
    users: List[UserSchema]


class DeleteUSerResponseSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a resposta da
        requisição de remoção de um user.
    """
    id: int


class DeleteUserQuerySchema(BaseModel):
    """ Define como deve ser a estrutura que representa a query string
        da requisição de remoção de um user.
    """
    user_id: int


class GetUserResponseSchema(BaseModel):
    """ Define the structure that represents the response of a get user request.
    """
    user: UserSchema


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserUpdateQuerySchema(BaseModel):
    """ Define the structure that represents the query string of an update user request.
    """
    user_id: int


class UserGetQuerySchema(BaseModel):
    """ Define the structure that represents the query string of a get user request.
    """
    user_id: int


def return_user(user: UserSchema):
    """ Retorna um user no formato de dicionário
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }


def return_users(users: List[UserSchema]):
    """ Retorna uma lista de users no formato de dicionário
    """

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })

    return {"user": result}
