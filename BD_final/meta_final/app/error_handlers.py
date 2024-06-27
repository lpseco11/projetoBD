from flask import jsonify

from app.status_code import StatusCodes


def not_found_error_handler(error):
    response = jsonify({'status':StatusCodes.NotFound.value,'error': 'User not found'})
    response.status_code = StatusCodes.NotFound.value

    return response


def bad_request_handler(error):
    response = jsonify({'error': '👎 Bad Request',
                        'message': 'The browser (or proxy) sent a request that this server could not understand.'})
    response.status_code = StatusCodes.BadRequest.value

    return response
