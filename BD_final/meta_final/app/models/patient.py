import psycopg2
from flask import abort
from flask import Blueprint, request, abort, jsonify

from app.status_code import StatusCodes
from app.database import get_connection

class Patient:
    def __init__(self, patient_id=None, name=None, contact_info=None,password=None):
        self.patient_id = patient_id
        self.name = name
        self.contact_info = contact_info
        self.password = password

    def fetch(self):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM employe WHERE employe_id = %s', (self.id,))

                employe = cursor.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            abort(StatusCodes.InternalServerError.value)

        if not employe:
            self.__init__()

            return

        self.__init__(*employe)
    
    def auth_fetch(self):
        conn = get_connection()

        query = 'SELECT * FROM patient WHERE name = %s AND password = %s'
        query_values = (self.name, self.password)

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, query_values)

                person_info = cursor.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            abort(StatusCodes.InternalServerError.value)

        if not person_info:
            self.__init__()

            return

        self.__init__(*person_info)

    
    