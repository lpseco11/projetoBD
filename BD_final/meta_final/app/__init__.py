from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from app.status_code import StatusCodes
from app.database import get_connection, close_connection


from app.error_handlers import *
from config import Config

from app.routes.create_doctor import doctor_blueprint
from app.routes.create_nurse import nurse_blueprint
from app.routes.create_assistant import assistant_blueprint
from app.routes.create_patient import patient_blueprint
from app.routes.login import login_auth
from app.routes.schedule_appointment import appointment_blueprint
from app.routes.see_apointments import see_appointment_blueprint
from app.routes.schedule_surgery import surgery_blueprint
from app.routes.add_prescription import prescription_blueprint
from app.routes.get_prescription import see_prescription_blueprint
from app.routes.execute_payment import pay_bill_blueprint
from app.routes.top3 import see_top3_blueprint
from app.routes.daily_summary import daily_summary_blueprint

def init_app():
    app = Flask(__name__)

    app.debug = True
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    jwt = JWTManager(app)

    app.register_blueprint(doctor_blueprint)
    app.register_blueprint(login_auth)
    app.register_blueprint(nurse_blueprint)
    app.register_blueprint(patient_blueprint)
    app.register_blueprint(assistant_blueprint)
    app.register_blueprint(appointment_blueprint)
    app.register_blueprint(see_appointment_blueprint)
    app.register_blueprint(surgery_blueprint)
    app.register_blueprint(prescription_blueprint)
    app.register_blueprint(see_prescription_blueprint)
    app.register_blueprint(pay_bill_blueprint)
    app.register_blueprint(see_top3_blueprint)
    app.register_blueprint(daily_summary_blueprint)

    app.register_error_handler(StatusCodes.NotFound.value, not_found_error_handler)
    app.register_error_handler(StatusCodes.BadRequest.value, bad_request_handler)

    @app.teardown_appcontext

    def teardown_connection(exception):
        conn = get_connection()
        conn.close()

    return app