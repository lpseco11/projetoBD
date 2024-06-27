import psycopg2
from flask import jsonify, Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
from app.status_code import StatusCodes
import random
import string
from app.permissions import role_required

appointment_blueprint = Blueprint('schedule_appointment', __name__)

logger = logging.getLogger('werkzeug')

def generate_unique_random_number(cur):
    while True:
        random_number = ''.join(random.choices(string.digits, k=1))
        cur.execute("SELECT 1 FROM appointments WHERE appointment_id = %s", (random_number,))
        if cur.fetchone() is None:
            return random_number

@appointment_blueprint.route('/dbproj/appointment', methods=['POST'])
@jwt_required()
@role_required(['patient'])
def schedule_appointment():

    current_user = get_jwt_identity()
    user_id = current_user.get('user_id')
    body = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    try:
        date = body.get('appointment_datetime')
        patient_id = body.get('patient_patient_id')
        assistant = body.get('assistant_employe_employe_id')
        doctor = body.get('doctor_employe_employe_id')

        if not date or not patient_id or not assistant or not doctor:
            abort(StatusCodes.BadRequest.value)

        # Generate a unique appointment ID
        appointment_id = generate_unique_random_number(cur)

        query = """
            INSERT INTO appointments (appointment_id, appointment_datetime, patient_patient_id, assistant_employe_employe_id, doctor_employe_employe_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        query_values = (appointment_id, date, patient_id, assistant, doctor)

        cur.execute(query, query_values)
        conn.commit()

        result = {
            'status': StatusCodes.OK.value,
            'message': 'Appointment created successfully',
            'appointment_id': appointment_id
        }

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /appointment - error: {error}')
        conn.rollback()
        abort(StatusCodes.InternalServerError.value, description=str(error))

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return jsonify(result)
