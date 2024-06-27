from flask import Blueprint, request, abort, jsonify
from app.database import get_connection
from app.status_code import StatusCodes
import logging
import psycopg2

nurse_blueprint = Blueprint('nurse', __name__)

logger = logging.getLogger('werkzeug')

@nurse_blueprint.route('/dbproj/register/nurse', methods=['POST'])
def create_nurse():
    conn = get_connection()
    cur = conn.cursor()
    body = request.get_json()
    try:
        id = body['employe_id']
        name = body['name']
        contact_info = body['contact_info']
        password = body['password']
        contract_details = body['contract_details']
        internal_hierarchical_category = body['internal_hierarchical_category']

        statement = """
                INSERT INTO employe (employe_id, name, contact_info,password, contract_details) 
                VALUES (%s, %s, %s, %s, %s)"""
        values = (id, name, contact_info,password, contract_details)

        cur.execute("BEGIN TRANSACTION")
        cur.execute("LOCK TABLE employe IN EXCLUSIVE MODE")
        cur.execute(statement, values)
        conn.commit()  # Commit the transaction

        statement_a = """
                INSERT INTO nurse (internal_hierarchical_category, employe_employe_id) 
                VALUES (%s,%s)"""
        values_a = (internal_hierarchical_category,id)
        
        cur.execute("BEGIN TRANSACTION")
        cur.execute("LOCK TABLE nurse IN EXCLUSIVE MODE")
        cur.execute(statement_a, values_a)
        conn.commit()  # Commit the transaction

        result = {'userId': id}

    except (Exception, psycopg2.DatabaseError) as error:
        result = {'error': str(error)}
        conn.rollback()  # Rollback the transaction in case of error

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return jsonify(result)

            

    
    
        

    