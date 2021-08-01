from werkzeug.security import check_password_hash
from api.User.user_model import User
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

login = Blueprint('login', __name__)

@login.route('/login', methods=["POST"])
def log_in():
    data = request.get_json()

    user= User.query.filter_by(email=data["email"]).first()
    if user:
        if check_password_hash(user.password, data["password"]):
            jwt_token = create_access_token(identity=user.email)
            return jsonify({"token": jwt_token})
        return jsonify({"error": "Invalid credentials"}), 400