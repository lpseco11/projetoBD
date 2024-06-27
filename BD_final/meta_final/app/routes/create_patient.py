from flask import Blueprint, request, abort, jsonify
from app.database import get_connection
from app.status_code import StatusCodes
import logging
import psycopg2

patient_blueprint = Blueprint('patient', __name__)

logger = logging.getLogger('werkzeug')

@patient_blueprint.route('/dbproj/register/patient', methods=['POST'])
def create_patient():
    conn = get_connection()
    cur = conn.cursor()
    body = request.get_json()
    try:
        id = body['patient_id']
        name = body['name']
        contact_info = body['contact_info']
        password = body['password']
        
        statement = """
                INSERT INTO patient (patient_id, name, contact_info,password) 
                VALUES (%s, %s, %s, %s)"""
        values = (id, name, contact_info,password)

        cur.execute("BEGIN TRANSACTION")
        cur.execute("LOCK TABLE employe IN EXCLUSIVE MODE")
        cur.execute(statement, values)
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

            

    
    
        

    