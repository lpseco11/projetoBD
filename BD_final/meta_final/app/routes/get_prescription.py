import psycopg2
from flask import jsonify, Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
from app.status_code import StatusCodes
from app.permissions import role_required

see_prescription_blueprint = Blueprint('get_prescriptions', __name__)

logger = logging.getLogger('werkzeug')

@see_prescription_blueprint.route('/dbproj/prescriptions/<string:patient_id>', methods=['GET'])
@jwt_required()
@role_required(['patient', 'nurse', 'doctor', 'assistant'])
def prescriptions(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    
    current_user = get_jwt_identity()
    patient_id_jws = current_user.get('user_id')
    
    verify_query = """
    select h.patient_patient_id, a.patient_patient_id
    from prescription
    left join hospitalization as h on h.hospitalization_id = hospitalization_hospitalization_id
    left join appointments as a on a.appointment_id = appointments_appointment_id
    where h.patient_patient_id = %s or a.patient_patient_id = %s
    """

    query = """
    SELECT p.prescription_id, p.appointments_appointment_id, p.hospitalization_hospitalization_id, m3.name, m3.dosage
    FROM prescription AS p
    LEFT JOIN appointments AS a1 ON a1.appointment_id = p.appointments_appointment_id
    LEFT JOIN hospitalization AS h2 ON h2.hospitalization_id = p.hospitalization_hospitalization_id
    LEFT JOIN medication AS m3 ON m3.prescription_prescription_id = p.prescription_id
    WHERE a1.patient_patient_id = %s OR h2.patient_patient_id = %s
    """

    query_values = (patient_id, patient_id)

    try:
        with conn.cursor() as cursor:
            if current_user.get('role') == 'patient':
                cursor.execute(verify_query, (patient_id_jws,patient_id_jws,))
                patient = cursor.fetchone()

                if patient is None:
                    return jsonify({
                        'status': StatusCodes.Forbidden.value, 
                        'message': 'You are not authorized to see these prescriptions'
                    }), StatusCodes.Forbidden.value

            cursor.execute(query, query_values)
            prescription_info = cursor.fetchall()

            if not prescription_info:
                return jsonify({
                    'status': StatusCodes.NotFound.value, 
                    'message': 'No prescriptions found for this patient'
                }), StatusCodes.NotFound.value

            # Initialize data to collect unique prescriptions
            prescriptions = {}
            for row in prescription_info:
                prescription_id, appointment_id, hospitalization_id, medication_name, medication_dosage = row
                if prescription_id not in prescriptions:
                    prescriptions[prescription_id] = {
                        'prescription_id': prescription_id,
                        'appointment_id': appointment_id if appointment_id is not None else 'N/A',
                        'hospitalization_id': hospitalization_id if hospitalization_id is not None else 'N/A',
                        'medications': []
                    }
                prescriptions[prescription_id]['medications'].append({
                    'medication_name': medication_name,
                    'medication_dosage': medication_dosage
                })

            conn.commit()

            return jsonify({
                'status': StatusCodes.OK.value,
                'prescriptions': list(prescriptions.values())
            })

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /prescriptions - error: {error}')
        conn.rollback()
        return jsonify({'status': StatusCodes.InternalServerError.value, 'errors': str(error)}), StatusCodes.InternalServerError.value

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
