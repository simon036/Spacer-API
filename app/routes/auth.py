from flask import Blueprint, request, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from datetime import timedelta
from ..models import User
from ..extensions import db
from ..schemas import UserSchema
from ..utils.email import send_email
from ..utils.validation import validate_schema
import os

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY", "supersecret"))

@auth_bp.route('/register', methods=['POST'])
@validate_schema(user_schema)
def register(data):
    email = data.get("email")
    password = request.json.get("password")
    role = data.get("role", "client")
    if User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}, 400
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        is_active=False
    )
    db.session.add(user)
    db.session.commit()
    # Send verification email
    token = serializer.dumps(email, salt="email-confirm")
    link = url_for('auth.verify_email', token=token, _external=True)
    send_email(email, "Verify your Spacer account", f"Click to verify: {link}")
    return {"message": "Registration successful. Please check your email to verify your account."}, 201

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=3600)
    except (SignatureExpired, BadSignature):
        return {"error": "Invalid or expired token"}, 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404
    user.is_active = True
    db.session.commit()
    return {"message": "Email verified. You can now log in."}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {"error": "Invalid credentials"}, 401
    if not user.is_active:
        return {"error": "Please verify your email first."}, 403
    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role},
        expires_delta=timedelta(hours=12)
    )
    return {"access_token": access_token, "user": user_schema.dump(user)}

# Social auth endpoints would go here (Google/Facebook OAuth)

@auth_bp.route('/password-reset/request', methods=['POST'])
def request_password_reset():
    data = request.json
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404
    token = serializer.dumps(email, salt="password-reset")
    link = url_for('auth.confirm_password_reset', token=token, _external=True)
    send_email(email, "Spacer Password Reset", f"Click to reset your password: {link}")
    return {"message": "Password reset email sent."}

@auth_bp.route('/password-reset/confirm/<token>', methods=['POST'])
def confirm_password_reset(token):
    data = request.json
    new_password = data.get("password")
    try:
        email = serializer.loads(token, salt="password-reset", max_age=3600)
    except (SignatureExpired, BadSignature):
        return {"error": "Invalid or expired token"}, 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return {"message": "Password reset successful."}
