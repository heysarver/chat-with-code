import uuid
from flask import session, jsonify
from . import api_blueprint

@api_blueprint.route('/api/session/create', methods=['GET'])
def create_session():
    session_id = uuid.uuid4()
    session['session_id'] = str(session_id)
    return jsonify({"session_id": str(session_id)})

@api_blueprint.route('/api/session/<session_id>', methods=['GET'])
def get_session_value(session_id):
    if 'session_id' in session and session['session_id'] == session_id:
        # Example of accessing a value stored in session
        return jsonify({"message": "Session found", "session_id": session['session_id']})
    else:
        return jsonify({"message": "Session not found"}), 404
