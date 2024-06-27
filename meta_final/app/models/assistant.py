import psycopg2
from flask import abort

from app.status_code import StatusCodes
from app.database import get_connection

class Assistant:
    def __init__(self, employe_employe_id=None):
        self.employe_employe_id = employe_employe_id
        
        
    def fetch(self):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM employe WHERE employe_employe_id = %s', (self.employe_employe_id,))

                assistant = cursor.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            abort(StatusCodes.InternalServerError.value)

        if not assistant:
            self.__init__()

            return

        self.__init__(*assistant)
        