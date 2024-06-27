from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import create_access_token
from app.status_code import StatusCodes
from app.models.employe import Employe
from app.models.patient import Patient
import logging
from app import get_connection

login_auth = Blueprint('login', __name__)

logger = logging.getLogger('werkzeug')

@login_auth.route('/dbproj/user', methods=['PUT'])
def login():
    body = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    try:
        user = Employe(name=body['name'], password=body['password'])
        user.auth_fetch()

        if user.employe_id is None:
            patient = Patient(name=body['name'], password=body['password'])
            patient.auth_fetch()
            if patient.patient_id is None:
                abort(StatusCodes.NotFound.value)
            jwt = create_access_token(identity={'user_id': patient.patient_id, 'role': 'patient'})
            return jsonify({'status': StatusCodes.OK.value, 'message': 'login successful', 'token': jwt})

        # Check for employee roles
        role_query = """
            SELECT 
                CASE
                    WHEN EXISTS (SELECT 1 FROM doctor WHERE employe_employe_id = %s) THEN 'doctor'
                    WHEN EXISTS (SELECT 1 FROM nurse WHERE employe_employe_id = %s) THEN 'nurse'
                    WHEN EXISTS (SELECT 1 FROM assistant WHERE employe_employe_id = %s) THEN 'assistant'
                    ELSE 'employe'
                END as role
        """
        cur.execute(role_query, (user.employe_id, user.employe_id, user.employe_id))
        role = cur.fetchone()[0]

        jwt = create_access_token(identity={'user_id': user.employe_id, 'role': role})
        return jsonify({'status': StatusCodes.OK.value, 'message': 'login successful', 'token': jwt})

    except Exception as e:
        logger.error(f'Error during login: {e}')
        abort(StatusCodes.InternalServerError.value, description=str(e))

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
