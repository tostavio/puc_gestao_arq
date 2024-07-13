from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request

from sqlalchemy.exc import IntegrityError

from model import Session, Address, User
from schemas import *
from flask_cors import CORS

info = Info(title="address API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# tags
home_tag = Tag(name="Documentação",
               description="Choose your documentation: Swagger, Redoc or RapiDoc")
addresses_tag = Tag(
    name="Addresses", description="Add, view, list, update and remove addresses")

users_tag = Tag(
    name="Users", description="Add, view, list, update and remove users")


@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi, the page that allows you to choose the documentation style.
    """
    return redirect('/openapi')


# ADDRESS ROUTES ##############################################################

@app.get('/address/', tags=[addresses_tag],
         responses={"200": GetAddressResponseSchema, "404": ErrorSchema})
def get_address(query: AddessGetQuerySchema):
    """Get a single address by address_id

    Return the address or error message if not found.
    """
    address_id = query.address_id
    session = Session()
    address = session.query(Address).filter(Address.id == address_id).first()

    if address:
        return return_address(address), 200
    else:
        return {"message": "Address not found"}, 404


@app.post('/address', tags=[addresses_tag],
          responses={"200": AddressSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_address(form: AddressCreateSchema):
    """Add a new address to the database

    Return created address or error message.
    """
    session = Session()

    print(form)
    try:
        # Check if the user with user_id exists
        user = session.query(User).filter(User.id == form.user_id).first()
        if not user:
            return {"message": "User not found"}, 404

        # Create Address instance
        address = Address(
            zip_code=form.zip_code,
            street=form.street,
            complement=form.complement,
            neighborhood=form.neighborhood,
            city=form.city,
            state=form.state,
            ibge_code=form.ibge_code,
            gia_code=form.gia_code,
            ddd_code=form.ddd_code,
            siafi_code=form.siafi_code,
            user=user
        )

        # Add and commit the new address
        session.add(address)
        session.commit()

        # Return the created address
        return return_address(address), 200

    except IntegrityError as e:
        # Duplicate address
        session.rollback()
        message = f"Address '{address}' already exists '{e}'"
        return {"message": message}, 409

    except Exception as e:
        # Unexpected error
        session.rollback()
        message = "We couldn't save your address, try again later"
        print(f"Exception: {e}")
        return {"message": message}, 400

    finally:
        session.close()


@app.get('/addresses', tags=[addresses_tag],
         responses={"200": ListAddressResponseSchema, "404": ErrorSchema})
def get_addresses():
    """Get a list of all addresses

    Return a list of all addresses.
    """
    session = Session()
    # searching for all addresses
    addresses = session.query(Address).all()

    if not addresses:
        # don't have any addresses
        return {"addresses": []}, 200
    else:
        # return all addresses
        return return_addresses(addresses), 200


@app.put('/address/', tags=[addresses_tag],
         responses={"200": AddressSchema, "400": ErrorSchema, "404": ErrorSchema})
def update_address(query: AddressUpdateQuerySchema, form: AddressUpdateSchema):
    """Update an existing address in the database by id

    Return updated address or error message.
    """
    address_id = query.address_id
    session = Session()
    address = session.query(Address).filter(Address.id == address_id).first()

    if not address:
        return {"message": "Address not found"}, 404

    try:
        # Update address fields if they are provided in the form
        if form.zip_code not in (None, ''):
            address.zip_code = form.zip_code
        if form.street not in (None, ''):
            address.street = form.street
        if form.complement not in (None, ''):
            address.complement = form.complement
        if form.neighborhood not in (None, ''):
            address.neighborhood = form.neighborhood
        if form.city not in (None, ''):
            address.city = form.city
        if form.state not in (None, ''):
            address.state = form.state
        if form.ibge_code not in (None, ''):
            address.ibge_code = form.ibge_code
        if form.gia_code not in (None, ''):
            address.gia_code = form.gia_code
        if form.ddd_code not in (None, ''):
            address.ddd_code = form.ddd_code
        if form.siafi_code not in (None, ''):
            address.siafi_code = form.siafi_code

        session.commit()
        return return_address(address), 200

    except Exception as e:
        session.rollback()
        return {"message": f"Failed to update address: {str(e)}"}, 400

    finally:
        session.close()


@app.delete('/address', tags=[addresses_tag],
            responses={"200": DeleteAddressResponseSchema, "404": ErrorSchema})
def delete_address(query: DeleteAddressQuerySchema):
    """Delete an existing address from the database by id

    return id of deleted address or error message.
    """
    address_id = query.address_id

    session = Session()
    try:
        # Searching for the address
        count = session.query(Address).filter(
            Address.id == address_id).delete()
        session.commit()

        if count:
            return {"id": address_id}, 200
        else:
            return {"message": "Address not found"}, 404

    except Exception as e:
        # In case of any exception, rollback the session
        session.rollback()
        return {"message": f"Failed to delete address: {str(e)}"}, 400

    finally:
        # Always close the session to release resources
        session.close()

# USER ROUTES ##############################################################


@app.get('/user', tags=[users_tag],
         responses={"200": GetUserResponseSchema, "404": ErrorSchema})
def get_user(query: UserGetQuerySchema):
    """Get a single user by user_id

    Return the user or error message if not found.
    """
    user_id = query.user_id
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()

    if user:
        return return_user(user), 200
    else:
        return {"message": "User not found"}, 404


@app.post('/user', tags=[users_tag],
          responses={"200": UserSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_user(form: UserCreateSchema):
    """Add a new user to the database

    Return created user or error message.
    """
    user = User(
        name=form.name,
        email=form.email
    )

    session = Session()
    try:
        session.add(user)
        session.commit()
        return return_user(user), 200

    except IntegrityError as e:
        # Duplicate user
        session.rollback()
        message = f"User '{user.email}' already exists. Error: {e}"
        return {"message": message}, 409

    except Exception as e:
        # Unexpected error
        session.rollback()
        message = f"We couldn't save your user, try again later. Error: {e}"
        return {"message": message}, 400

    finally:
        session.close()


@app.get('/users', tags=[users_tag],
         responses={"200": ListUserResponseSchema, "404": ErrorSchema})
def get_users():
    """Get a list of all users

    Return a list of all users.
    """
    session = Session()
    # searching for all users
    users = session.query(User).all()

    if not users:
        # don't have any users
        return {"users": []}, 200
    else:
        # return all users
        return return_users(users), 200


@app.put('/user', tags=[users_tag],
         responses={"200": UserSchema, "400": ErrorSchema, "404": ErrorSchema})
def update_user(query: UserUpdateQuerySchema, form: UserUpdateSchema):
    """Update an existing user in the database by id

    Return updated user or error message.
    """
    user_id = query.user_id
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        return {"message": "User not found"}, 404

    try:
        # Update user fields if they are provided in the form
        if form.name not in (None, ''):
            user.name = form.name
        if form.email not in (None, ''):
            user.email = form.email

        session.commit()
        return return_user(user), 200

    except Exception as e:
        session.rollback()
        return {"message": f"Failed to update user: {str(e)}"}, 400

    finally:
        session.close()


@app.delete('/user', tags=[users_tag],
            responses={"200": DeleteUSerResponseSchema, "404": ErrorSchema})
def delete_user(query: DeleteUserQuerySchema):
    """Delete an existing user from the database by id

    return id of deleted user or error message.
    """
    user_id = query.user_id

    session = Session()
    try:
        # Procurar o usuário e seus endereços associados
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            return {"message": "User not found"}, 404

        # Deletar todos os endereços associados ao usuário
        session.query(Address).filter(Address.user_id == user_id).delete()

        # Deletar o usuário
        session.delete(user)
        session.commit()

        return {"id": user_id}, 200

    except Exception as e:
        # Em caso de qualquer exceção, realizar rollback na sessão
        session.rollback()
        return {"message": f"Failed to delete user: {str(e)}"}, 400

    finally:
        # Sempre fechar a sessão para liberar recursos
        session.close()
