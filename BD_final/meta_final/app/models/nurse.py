import psycopg2
from flask import abort

from app.status_code import StatusCodes
from app.database import get_connection

class Nurse:
    def __init__(self, internal_hierarchical_category=None, employe_employe_id=None ):
        self.internal_hierarchical_category = internal_hierarchical_category
        self.employe_employe_id = employe_employe_id
        
        

    def fetch(self):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM nurse WHERE employe_employe_id = %s', (self.id,))

                nurse = cursor.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            abort(StatusCodes.InternalServerError.value)

        if not nurse:
            self.__init__()

            return

        self.__init__(*nurse)
        