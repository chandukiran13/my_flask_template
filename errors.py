from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from flask.logging import default_handler
def error_404(e: Exception):
    return jsonify({'error': str(e)}), 404

def error_500(e: Exception):
    code = 500
    if isinstance(e ,HTTPException):
        code = e.code
        if not code:
            code = 500
    return jsonify({'error': str(e)}), code

