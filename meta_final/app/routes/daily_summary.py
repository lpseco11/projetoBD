import psycopg2
from flask import jsonify, Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app import get_connection
from app.status_code import StatusCodes
from app.permissions import role_required

daily_summary_blueprint = Blueprint('daily_summary', __name__)

logger = logging.getLogger('werkzeug')

@daily_summary_blueprint.route('/dbproj/daily/<string:date>', methods=['GET'])
@jwt_required()
@role_required(['assistant'])

def daily_summary(date):
    conn = get_connection()
    query = """
    WITH hospitalization_data AS (
        SELECT hospitalization_id
        FROM hospitalization
        WHERE DATE(date) = %s
    ),
    surgery_count AS (
        SELECT COUNT(*) AS surgeries
        FROM surgery
        WHERE hospitalization_hospitalization_id IN (SELECT hospitalization_id FROM hospitalization_data)
    ),
    payment_sum AS (
        SELECT COALESCE(SUM(money_paid), 0) AS amount_spent
        FROM bill
        WHERE hospitalization_hospitalization_id IN (SELECT hospitalization_id FROM hospitalization_data)
    ),
    prescription_count AS (
        SELECT COUNT(*) AS prescriptions
        FROM prescription
        WHERE hospitalization_hospitalization_id IN (SELECT hospitalization_id FROM hospitalization_data)
    )
    SELECT
        s.surgeries,
        p.amount_spent,
        pr.prescriptions
    FROM
        surgery_count s,
        payment_sum p,
        prescription_count pr;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (date,))
            result = cursor.fetchone()
            if not result:
                return jsonify({
                    'status': StatusCodes.NotFound.value,
                    'message': 'No data found for the given date'
                }), StatusCodes.NotFound.value

            response = {
                'status': StatusCodes.OK.value,
                'results': {
                    'amount_spent': result[1],
                    'surgeries': result[0],
                    'prescriptions': result[2]
                }
            }

            conn.commit()
            return jsonify(response)

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /daily/{date} - error: {error}')
        conn.rollback()
        return jsonify({'status': StatusCodes.InternalServerError.value, 'errors': str(error)}), StatusCodes.InternalServerError.value

    finally:
        if conn is not None:
            conn.close()
