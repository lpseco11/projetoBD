from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
import psycopg2
from app.status_code import StatusCodes
from app.permissions import role_required

pay_bill_blueprint = Blueprint('pay_bill', __name__)
logger = logging.getLogger('werkzeug')

@pay_bill_blueprint.route('/dbproj/bills/<string:bill_id>', methods=['POST'])
@jwt_required()
@role_required(['patient'])
def pay_bill(bill_id):
    body = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    amount = body['amount']
    payment_method = body['payment_method']

    if not amount or not payment_method:
        abort(StatusCodes.BadRequest.value)

    try:
        current_user = get_jwt_identity()
        patient_id = current_user.get('user_id')
        logger.debug(f"Current User ID: {patient_id}")

        # Verify bill ownership and status
        verify_query = """
        SELECT b.bill_id, b.status, b.cost, b.money_paid
        FROM bill b
        LEFT JOIN hospitalization h ON b.hospitalization_hospitalization_id = h.hospitalization_id
        LEFT JOIN appointments a ON b.appointments_appointment_id = a.appointment_id
        LEFT JOIN patient p1 ON h.patient_patient_id = p1.patient_id
        LEFT JOIN patient p2 ON a.patient_patient_id = p2.patient_id
        WHERE b.bill_id = %s AND (p1.patient_id = %s OR p2.patient_id = %s)
        """
        cur.execute(verify_query, (bill_id, patient_id, patient_id))
        bill = cur.fetchone()

        if bill is None:
            return jsonify({'status': StatusCodes.Forbidden.value, 'message': 'You are not authorized to pay this bill'}), StatusCodes.Forbidden.value
        
        if bill[1] == 'paid':
            return jsonify({'status': StatusCodes.BadRequest.value, 'message': 'This bill is already paid'}), StatusCodes.BadRequest.value

        # Update bill cost
        new_cost = bill[2] - int(amount)
        payed_cost = bill[3] + int(amount)
        if new_cost < 0:
            return jsonify({'status': StatusCodes.BadRequest.value, 'message': 'Amount exceeds the outstanding cost'}), StatusCodes.BadRequest.value

        update_query = """UPDATE bill SET cost = %s, status = %s, money_paid = %s WHERE bill_id = %s"""
    
        if new_cost == 0:
            cur.execute(update_query, (new_cost, 'paid', payed_cost, bill_id))
            message = 'Bill fully paid and marked as paid'
        else:
            cur.execute(update_query, (new_cost, 'unpaid',payed_cost, bill_id))
            message = 'Partial payment applied'

        conn.commit()

        result = {
            'status': StatusCodes.OK.value,
            'Amount left': new_cost,
            'message': message
        }

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /bills/{bill_id} - error: {error}')
        conn.rollback()
        abort(StatusCodes.InternalServerError.value, description=str(error))

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return jsonify(result)
