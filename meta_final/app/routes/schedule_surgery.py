import psycopg2
from flask import jsonify, Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
from app.status_code import StatusCodes
from datetime import datetime
from app.permissions import role_required
import random, string

surgery_blueprint = Blueprint('surgery', __name__)

logger = logging.getLogger('werkzeug')

def generate_unique_random_number_surgery(cur):
    while True:
        random_number = ''.join(random.choices(string.digits, k=2))
        cur.execute("SELECT 1 FROM surgery WHERE surgery_id = %s", (random_number,))
        if cur.fetchone() is None:
            return random_number

def generate_unique_random_number_hospitalization(cur):
    while True:
        random_number = ''.join(random.choices(string.digits, k=2))
        cur.execute("SELECT 1 FROM hospitalization WHERE hospitalization_id = %s", (random_number,))
        if cur.fetchone() is None:
            return random_number



@surgery_blueprint.route('/dbproj/surgery', methods=['POST'])
@jwt_required()
@role_required(['assistant'])
def schedule_surgery():
    body = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    user = body['patient_id']
    doctor = body['doctor_user_id']
    nurses = body['nurses']
    assistant_id = body['assistant_id']
    date = body['date']
    surgery_id = generate_unique_random_number_surgery(cur)
    hospitalization_id = generate_unique_random_number_hospitalization(cur)

    if ('patient_id' and 'doctor_user_id' and 'nurses' and 'assistant_id' and 'date') not in body:
        return jsonify({'status': StatusCodes.BadRequest.value})

    surgery_query="""
       INSERT INTO surgery (surgery_id, doctor_employe_employe_id, hospitalization_hospitalization_id)
       VALUES (%s, %s, %s)
       RETURNING surgery_id;
    """
    hospitalization_query="""
       INSERT INTO hospitalization (hospitalization_id, patient_patient_id, assistant_employe_employe_id, nurse_employe_employe_id, date)
       VALUES (%s, %s, %s, %s, %s)
       RETURNING hospitalization_id;
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(hospitalization_query, (hospitalization_id, user,assistant_id,nurses,date))
            cursor.execute(surgery_query,(surgery_id,doctor,hospitalization_id))
            

        conn.commit()

        return jsonify(
            {'status': StatusCodes.OK.value, 'results': {'surgery_id':surgery_id,'hospitalization_id':hospitalization_id},'patient_id':user,'doctor_id':doctor,'date':date}), StatusCodes.OK.value

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /Scheduling surgery - error: {error}')

        conn.rollback()

        return jsonify({'status': StatusCodes.InternalServerError.value, 'errors': str(error)})
    
@surgery_blueprint.route('/dbproj/surgery/<string:hospitalization_id>', methods=['POST'])
@jwt_required()

def schedule_another_surgery(hospitalization_id):

    body = request.get_json()
    doctor = body['doctor_user_id']
    patient = body['patient_id']
    conn = get_connection()
    cur = conn.cursor()
    surgery = generate_unique_random_number_surgery(cur)
    query = 'INSERT INTO surgery (surgery_id,doctor_employe_employe_id, hospitalization_hospitalization_id) ' \
            'VALUES (%s, %s, %s) RETURNING surgery_id'
    
    query_values = (surgery, doctor, hospitalization_id)

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, query_values)

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /surgery - error: {error}')

        conn.rollback()

        return jsonify({'status': StatusCodes.InternalServerError.value, 'errors': str(error)})

    return jsonify(
            {'status': StatusCodes.OK.value, 'results': {'surgery_id':surgery,'hospitalization_id':hospitalization_id},'patient_id':patient,'doctor_id':doctor}), StatusCodes.OK.value



