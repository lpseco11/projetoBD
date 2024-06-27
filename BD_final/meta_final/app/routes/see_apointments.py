import psycopg2
from flask import jsonify, Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
from app.status_code import StatusCodes
from app.permissions import role_required

see_appointment_blueprint = Blueprint('see_appointments', __name__)

logger = logging.getLogger('werkzeug')


@see_appointment_blueprint.route('/dbproj/appointments/<string:patient_id>', methods=['GET'])
@jwt_required()
@role_required(['assistant','patient'])

def see_appointment(patient_id):

    current_user = get_jwt_identity()
    patient_id_jws = current_user.get('user_id')

    conn = get_connection()
    
    verify_query="""
    select patient_patient_id
    from appointments
    left join patient as p on p.patient_id = patient_patient_id
    where patient_patient_id = %s
    """
    
    query = """
        select array_agg(DISTINCT appointments.appointment_id), array_agg(DISTINCT appointments.appointment_datetime), e1.name, e2.name     
        from appointments
        left join employe as e1 on appointments.doctor_employe_employe_id = e1.employe_id
        left join employe as e2 on appointments.assistant_employe_employe_id = e2.employe_id
        where appointments.patient_patient_id = %s
        group by e1.name, e2.name
    """
    query_values = (patient_id,)

    try:
        with conn.cursor() as cursor:
            if(current_user.get('role') == 'patient'):
                cursor.execute(verify_query,(patient_id_jws,))
                patient = cursor.fetchone()

                if patient is None or patient[0] != patient_id:
                    return jsonify({'status': StatusCodes.Forbidden.value, 'message': 'You are not authorized to see this appointments'}), StatusCodes.Forbidden.value
            
            cursor.execute('SELECT patient_patient_id FROM appointments WHERE patient_patient_id=%s', (patient_id,))

            fetched_artist = cursor.fetchone()

            if fetched_artist is None or fetched_artist[0] is None:
                return abort(StatusCodes.NotFound.value)

            cursor.execute(query, query_values)

            appointment_info = cursor.fetchone()

            appointment_id, appointment_date, doctor, assistant = appointment_info

            conn.commit()
        
        return jsonify({
            'appointment_id': appointment_id,
            'appointment_date': appointment_date,
            'doctor': doctor,
            'assistant': assistant,
        })

    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()

        # TODO: set all exemption handlers like this
        abort(error.code)


