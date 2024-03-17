import uuid
from flask import jsonify
from . import api_blueprint

@api_blueprint.route('/api/session/create', methods=['GET'])
def create_session():
    session_id = uuid.uuid4()
    return jsonify({"session_id": str(session_id)})
