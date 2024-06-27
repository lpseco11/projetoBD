import psycopg2
from flask import abort

from app.status_code import StatusCodes
from app.database import get_connection

class Doctor:
    def __init__(self, medical_license=None, employe_employe_id=None):
        self.medical_license = medical_license
        self.employe_employe_id = employe_employe_id
        
        
    def fetch(self):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM doctor WHERE employe_employe_id = %s', (self.id,))

                doctor = cursor.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            abort(StatusCodes.InternalServerError.value)

        if not doctor:
            self.__init__()

            return

        self.__init__(*doctor)
        