from flask import Blueprint, request, abort, jsonify
from app.database import get_connection
from app.status_code import StatusCodes
import logging
import psycopg2

doctor_blueprint = Blueprint('doctor', __name__)

logger = logging.getLogger('werkzeug')

@doctor_blueprint.route('/dbproj/register/doctor', methods=['POST'])
def create_doctor():
    conn = get_connection()
    cur = conn.cursor()
    body = request.get_json()
    try:
        id = body['employe_id']
        name = body['name']
        contact_info = body['contact_info']
        password = body['password']
        contract_details = body['contract_details']
        medical_license = body['medical_license']

        statement = """
                INSERT INTO employe (employe_id, name, contact_info,password, contract_details) 
                VALUES (%s, %s, %s, %s, %s)"""
        values = (id, name, contact_info,password, contract_details)

        cur.execute("BEGIN TRANSACTION")
        cur.execute("LOCK TABLE employe IN EXCLUSIVE MODE")
        cur.execute(statement, values)
        conn.commit()  # Commit the transaction

        statement_d = """
                INSERT INTO doctor (medical_license, employe_employe_id) 
                VALUES (%s, %s)"""
        values_d = (medical_license,id)
        
        cur.execute("BEGIN TRANSACTION")
        cur.execute("LOCK TABLE doctor IN EXCLUSIVE MODE")
        cur.execute(statement_d, values_d)
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

            

    
    
        

    