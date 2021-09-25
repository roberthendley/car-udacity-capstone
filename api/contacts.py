from flask import Blueprint, request, abort, jsonify
from .models import Contact, DEFAULT_PAGE_SIZE
from sqlalchemy.exc import DatabaseError
from ..auth.auth import requires_auth

blueprint = Blueprint('contacts', __name__)

'''
Helper Methods
'''
def is_valid_contact(body_data: dict) -> bool:
        # get tyhe request values and validate
    name = body_data.get('name')
    email_address = body_data.get('email_address')
    mobile_phone = body_data.get('mobile_phone')
    contact_type = body_data.get('contact_type')
    
    if name is None or email_address is None or mobile_phone is None:
        return False

    if not contact_type in ['consultant','clientmanager','other']:
        return False
    
    return True

def get_position_title(contact_type:str) ->str:
    if contact_type == 'consultant':
        return 'Business Consultant'
    elif contact_type == 'clientmanager':
        return 'Client Manager'
    else:
        return 'Other'

'''
API Routes - Contact List
'''
@blueprint.route('/api/contacts', methods=['GET'])
@requires_auth('read:contacts')
def get_contacts():
    contact_query = Contact.query
    
    # update query based on paramters
    if request.args.get('contact_type') and request.args.get('contact_type') in ['consultant', 'clientmanager', 'other']:
        contact_query = contact_query.filter(Contact.contact_type==request.args.get('contact_type'))
  
    if request.args.get('search'):
        search_term = f"%{request.args.get('search')}%"
        contact_query = contact_query.filter(Contact.name.ilike(search_term))
    
    # Set results paging
    page=request.args.get('page', default=1, type=int)
    page_size=request.args.get('page_size', default=DEFAULT_PAGE_SIZE,type=int)

    contacts = contact_query.order_by(Contact.name.desc()).paginate(page, page_size, False).items

    # check if the query returned any results
    if len(contacts) == 0:
        abort(404)

    contact_list = [contact.format() for contact in contacts]
    return jsonify({
        'success': True,
        'data': contact_list
    })

@blueprint.route('/api/contacts', methods=['POST'])
@requires_auth('create:contacts')
def add_contact():
    body_data: dict = request.get_json()
    
    if not body_data:
        abort(400)

    if not is_valid_contact(body_data):
        abort(400)


    contact_type = body_data.get('contact_type')
    position_title = body_data.get(
        'position_title', get_position_title(contact_type))
    name = body_data.get('name')
    email_address = body_data.get('email_address')
    mobile_phone = body_data.get('mobile_phone')


    try:
        contact = Contact(name, position_title,
                            email_address, mobile_phone, contact_type)
        contact.insert()
        return jsonify({
            "success": True,
            "message": "The contact has been successfully saved",
            "data": contact.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)


@blueprint.route('/api/contacts/<int:contact_id>', methods=['GET'])
@requires_auth('read:contacts')
def get_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify({
        'success': True,
        'data': contact.format()
    })


@blueprint.route('/api/contacts/<int:contact_id>', methods=['PATCH'])
@requires_auth('update:contacts')
def update_contact(contact_id):
    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    # get tyhe request values and validate
    if not is_valid_contact(body_data):
        abort(400)

    contact = Contact.query.get_or_404(contact_id)      
    contact.contact_type = body_data.get('contact_type')
    contact.position_title = body_data.get(
        'position_title', get_position_title(contact.contact_type))
    contact.name = body_data.get('name')
    contact.email_address = body_data.get('email_address')
    contact.mobile_phone = body_data.get('mobile_phone')

    try:
        
        contact.update()
        return jsonify({
            "success": True,
            "message": "The contact has been successfully saved",
            "data": contact.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)