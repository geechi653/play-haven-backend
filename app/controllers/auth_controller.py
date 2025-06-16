from flask import Blueprint, request, jsonify
from app.utils.validators import is_valid_email, is_valid_first_name, is_valid_last_name, is_valid_username, is_valid_country, is_valid_password
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if 'email' not in data or not data.get("email"):
        return jsonify({"error": "email cannot be empty"}), 400

    if not is_valid_email(data.get("email")):
        return jsonify({"error": "Invalid email format"}), 400

    if 'username' not in data or not data.get("username"):
        return jsonify({"error": "username cannot be empty"}), 400

    if not is_valid_username(data.get("username")):
        return jsonify({"error": "Invalid username format"}), 400

    if 'first_name' not in data or not data.get("first_name"):
        return jsonify({"error": "first_name cannot be empty"}), 400

    if not is_valid_first_name(data.get("first_name")):
        return jsonify({"error": "Invalid first_name format"}), 400

    if 'last_name' not in data or not data.get("last_name"):
        return jsonify({"error": "last_name cannot be empty"}), 400

    if not is_valid_last_name(data.get("last_name")):
        return jsonify({"error": "Invalid last_name format"}), 400

    if 'country' not in data or not data.get("country"):
        return jsonify({"error": "country cannot be empty"}), 400

    if not is_valid_country(data.get("country")):
        return jsonify({"error": "Invalid country format"}), 400

    if 'password' not in data or not data.get("password"):
        return jsonify({"error": "password cannot be empty"}), 400

    if not is_valid_password(data.get("password")):
        return jsonify({"error": "Invalid password format"}), 400

    try:
        user = AuthService.register(**data)
        return jsonify({"message": "user successfully created", "user": user.serialize()})
    except ValueError as e:
        return jsonify({"error": f"registration failed", "messgae": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"})

    user = UserService.get_user_by_username(data.get("username"))

    if not user:
        return jsonify({"error": "user not found"})

    if not data.get("password"):
        return jsonify({"error": "Password is required"})

    if not user.check_password(data.get("password")):
        return jsonify({"error": "password does not match"})

    access_token = create_access_token(identity=str(user.id), additional_claims={"username": data.get("username")})

    return jsonify({"user": user.serialize(), "token": access_token})
