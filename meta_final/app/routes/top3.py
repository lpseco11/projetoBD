import psycopg2
from flask import jsonify, Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
from app.status_code import StatusCodes
from app.permissions import role_required

see_top3_blueprint = Blueprint('top3', __name__)

logger = logging.getLogger('werkzeug')

@see_top3_blueprint.route('/dbproj/top3', methods=['GET'])
@jwt_required()
@role_required(['assistant'])
def top3():
    conn = get_connection()
    query = """
    SELECT COALESCE(h.patient_patient_id, a.patient_patient_id) AS patient_id, 
    p.name, 
    SUM(b.money_paid) AS total_spent, 
    STRING_AGG(COALESCE(h.hospitalization_id::text, ''), ',') AS hospitalization_ids, 
    STRING_AGG(COALESCE(a.appointment_id::text, ''), ',') AS appointment_ids
    FROM bill AS b
    LEFT JOIN hospitalization AS h ON h.hospitalization_id = b.hospitalization_hospitalization_id
    LEFT JOIN appointments AS a ON a.appointment_id = b.appointments_appointment_id
    LEFT JOIN patient AS p ON p.patient_id = COALESCE(h.patient_patient_id, a.patient_patient_id)
    GROUP BY COALESCE(h.patient_patient_id, a.patient_patient_id), p.name
    ORDER BY total_spent DESC
    LIMIT 3
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            fetched_top3 = cursor.fetchall()

            if not fetched_top3:
                return abort(StatusCodes.NotFound.value)

            top_spenders = []
            for row in fetched_top3:
                hospitalization_ids = row[3].split(',') if row[3] else []
                appointment_ids = row[4].split(',') if row[4] else []
                hospitalization_ids = [id for id in hospitalization_ids if id]  # Remove empty strings
                appointment_ids = [id for id in appointment_ids if id]  # Remove empty strings

                top_spenders.append({
                    'patient_id': row[0],
                    'name': row[1],
                    'total_spent': row[2],
                    'hospitalization_ids': hospitalization_ids,
                    'appointment_ids': appointment_ids
                })

            conn.commit()
        
        return jsonify({'status': StatusCodes.OK.value, 'results': top_spenders})

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /top3 - error: {error}')
        conn.rollback()
        return jsonify({'status': StatusCodes.InternalServerError.value, 'errors': str(error)}), StatusCodes.InternalServerError.value

    finally:
        if conn is not None:
            conn.close()
