from flask import Blueprint, request, abort, jsonify
from .models import DEFAULT_PAGE_SIZE, Client, ClientContact, DEFAULT_PAGE_SIZE
from sqlalchemy.exc import DatabaseError
from ..auth.auth import requires_auth

blueprint = Blueprint('clients', __name__)

'''
Helper Methods
'''

def is_valid_client(body_data: dict) -> bool:
        # get tyhe request values and validate
    name = body_data.get('name')
    bus_reg_nbr = body_data.get('bus_reg_nbr')
    abbreviation = body_data.get('abbreviation')

    if name is None or bus_reg_nbr is None or abbreviation is None:
        return False

    return True

def is_valid_client_contact(body_data: dict) -> bool:
    name = body_data.get('name')

    if name is None:
        return False

    return True


'''
Routes - Clients
'''
@blueprint.route('/api/clients', methods=['GET'])
@requires_auth('read:clients')
def get_clients():

    client_query = Client.query
    
    if request.args.get('search'):
        search_term = f"%{request.args.get('search')}%"
        client_query = client_query.filter(Client.name.ilike(search_term))

    # Set the paging details
    page_size = request.args.get('page_size', default=DEFAULT_PAGE_SIZE, type=int)
    page = request.args.get('page', default=1, type=int)

    clients_page = client_query.order_by(Client.name.desc()).paginate(page, page_size, False)
    clients = clients_page.items
    # check if the query returned any results
    if len(clients) == 0:
        abort(404)

    client_list = [client.format() for client in clients]
    return jsonify({
        'success': True,
        'page': clients_page.page,
        'pages': clients_page.pages,
        'data': client_list
    })

@blueprint.route('/api/clients', methods=['POST'])
@requires_auth('create:clients')
def add_client():
    body_data: dict = request.get_json()
    
    if not body_data:
        abort(400)

    if not is_valid_client(body_data):
        abort(400)

    name = body_data.get('name')
    bus_reg_nbr = body_data.get('bus_reg_nbr')
    abbreviation = body_data.get('abbreviation')


    try:
        client = Client(name, bus_reg_nbr, abbreviation)
        client.insert()
        return jsonify({
            "success": True,
            "message": "The client has been successfully saved",
            "data": client.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)


@blueprint.route('/api/clients/<int:client_id>', methods=['GET'])
@requires_auth('read:clients')
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'success': True,
        'data': client.format()
    })


@blueprint.route('/api/clients/<int:client_id>', methods=['PATCH'])
@requires_auth('update:clients')
def update_client(client_id):
    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    # get tyhe request values and validate
    if not is_valid_client(body_data):
        abort(400)

    client = Client.query.get_or_404(client_id)      
    client.name = body_data.get('name')
    client.bus_reg_nbr = body_data.get('bus_reg_nbr')
    client.abbreviation = body_data.get('abbreviation')

    try:
        
        client.update()
        return jsonify({
            "success": True,
            "message": "The client has been successfully saved",
            "data": client.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)

'''
Routes - Client Contacts
'''
@blueprint.route('/api/clients/<int:client_id>/contacts', methods=['GET'])
@requires_auth('read:client-contacts')
def get_client_contacts(client_id: int):

    client_contact_query = ClientContact.query.filter(ClientContact.client_id == client_id)
    
    # Apply search criteria
    if request.args.get('search'):
        search_term = f"%{request.args.get('search')}%"
        client_contact_query = client_contact_query.filter(ClientContact.name.ilike(search_term))

    # Set the paging details
    page_size = request.args.get('page_size', default=DEFAULT_PAGE_SIZE, type=int)
    page = request.args.get('page', default=1, type=int)
    
    client_contact_page = client_contact_query.order_by(ClientContact.name.desc()).paginate(page, page_size, False)
    client_contacts = client_contact_page.items
    client_contact_page.pages

    # check if the query returned any results
    if len(client_contacts) == 0:
        abort(404)

    client_contact_list = [client_contact.format() for client_contact in client_contacts]
    return jsonify({
        'success': True,
        'page': page,
        'pages': client_contact_page.pages,
        'data': client_contact_list
    })

@blueprint.route('/api/clients/<int:client_id>/contacts', methods=['POST'])
@requires_auth('create:client-contacts')
def add_client_contact(client_id):
    body_data: dict = request.get_json()
    
    if not body_data:
        abort(400)

    if not is_valid_client_contact(body_data):
        abort(400)
    
    try:
        name = body_data.get('name')
        client_contact = ClientContact(name)
        client_contact.client_id = client_id
        client_contact.email_address = body_data.get('email_address')
        client_contact.phone = body_data.get('phone')
        client_contact.position_title = body_data.get('position_title')
        client_contact.address_1 = body_data.get('address_1')
        client_contact.address_2 = body_data.get('address_2')
        client_contact.address_3 = body_data.get('address_3')
        client_contact.city = body_data.get('city')
        client_contact.state = body_data.get('state')
        client_contact.post_code = body_data.get('post_code')

        client_contact.insert()
        return jsonify({
            "success": True,
            "message": "The client has been successfully saved",
            "data": client_contact.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)


@blueprint.route('/api/clients/<int:client_id>/contacts/<int:contact_id>', methods=['GET'])
@requires_auth('read:client-contacts')
def get_client_contact(client_id, contact_id):
    client = ClientContact.query.get_or_404(contact_id)
    return jsonify({
        'success': True,
        'data': client.format()
    })


@blueprint.route('/api/client/<int:client_id>/contacts/<int:contact_id>', methods=['PATCH'])
@requires_auth('update:client-contacts')
def update_client_contact(client_id, contact_id):
    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    # get the request values and validate
    if not is_valid_client_contact(body_data):
        abort(400)

    client_contact = ClientContact.query.get_or_404(contact_id)      
    client_contact.name = body_data.get('name')
    client_contact.client_id = client_id
    client_contact.email_address = body_data.get('email_address')
    client_contact.phone = body_data.get('phone')
    client_contact.position_title = body_data.get('position_title')
    client_contact.address_1 = body_data.get('address_1')
    client_contact.address_2 = body_data.get('address_2')
    client_contact.address_3 = body_data.get('address_3')
    client_contact.city = body_data.get('city')
    client_contact.state = body_data.get('state')
    client_contact.post_code = body_data.get('post_code')

    try:
        
        client_contact.update()
        return jsonify({
            "success": True,
            "message": "The client contact has been successfully saved",
            "data": client_contact.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)

@blueprint.route('/api/clients/<int:client_id>/contacts/<int:contact_id>', methods=['DELETE'])
@requires_auth('delete:client-contacts')
def delete_client_contact(client_id, contact_id):

    client_contact = ClientContact.query.get_or_404(contact_id)

    try:
        client_contact.delete()

        return jsonify({
            "success": True,
            "message": "The client contact has been successfully deleted",
            "id": contact_id
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)

