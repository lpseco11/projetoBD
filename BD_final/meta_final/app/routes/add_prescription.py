import psycopg2
from flask import jsonify, Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
from app.status_code import StatusCodes
from app.permissions import role_required
import random, string

def generate_unique_random_number(cur):
    while True:
        random_number = ''.join(random.choices(string.digits, k=1))  # Generate a 10-digit random number
        cur.execute("SELECT 1 FROM prescription WHERE prescription_id = %s", (random_number,))
        if cur.fetchone() is None:
            return random_number

def generate_unique_random_number_medicine(cur):
    while True:
        random_number = ''.join(random.choices(string.digits, k=1))  # Generate a 10-digit random number
        cur.execute("SELECT 1 FROM medication WHERE medication_id = %s", (random_number,))
        if cur.fetchone() is None:
            return random_number

prescription_blueprint = Blueprint('prescription', __name__)

logger = logging.getLogger('werkzeug')

@prescription_blueprint.route('/dbproj/prescription', methods=['POST'])
@jwt_required()
@role_required(['doctor'])
def add_prescription():
    body = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    try:
        prescription_id = generate_unique_random_number(cur)
        type = body['type']
        event = body['event']
        medicines = body['medicine']  # This should be a list of medicine dictionaries

        if type not in ['hospitalization', 'appointment']:
            abort(StatusCodes.BadRequest.value, description="Invalid type")

        if type == 'hospitalization':
            query = """
            INSERT INTO prescription (prescription_id, hospitalization_hospitalization_id,  appointments_appointment_id)
            VALUES (%s, %s, %s)
            """
            query_prescription_values = (prescription_id, event, None)

        if type == 'appointment':
            query = """
            INSERT INTO prescription (prescription_id, hospitalization_hospitalization_id,appointments_appointment_id)
            VALUES (%s, %s, %s)
            """
            query_prescription_values = (prescription_id,None,event)

        cur.execute(query, query_prescription_values)
        conn.commit()
        
        query_medicine = """
        INSERT INTO medication (medication_id, name, dosage, prescription_prescription_id)
        VALUES (%s, %s, %s, %s)
        """
        
        for med in medicines:
            medication_id = generate_unique_random_number_medicine(cur)
            name = med.get('name')
            dosage = med.get('dosage')

            if not name or not dosage:
                return jsonify({'status': StatusCodes.BadRequest.value, 'errors': 'Medicine name or dosage missing'}), StatusCodes.BadRequest.value

            query_medicine_values = (medication_id, name, dosage, prescription_id)
            cur.execute(query_medicine, query_medicine_values)

        conn.commit()
    

        return jsonify({
            'status': StatusCodes.OK.value,
            'message': 'Prescription and medicines added successfully',
            'prescription_id': prescription_id
        }), StatusCodes.OK.value

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /prescription - error: {error}')
        conn.rollback()
        return jsonify({
            'status': StatusCodes.InternalServerError.value,
            'errors': str(error)
        }), StatusCodes.InternalServerError.value

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
