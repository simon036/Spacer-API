from flask import Blueprint, redirect, url_for, session, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from ..models import User
from ..extensions import db
import os

google_auth_bp = Blueprint("google_auth_bp", __name__)

# Flask-Dance Google blueprint
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_url=os.getenv("GOOGLE_REDIRECT_URI"),
    scope=["profile", "email"],
    reprompt_consent=True,
)

@google_auth_bp.route("/login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return jsonify({"error": "Failed to fetch user info from Google"}), 400
    info = resp.json()
    email = info["email"]
    user = User.query.filter_by(email=email).first()
    if not user:
        # Create a new user with a random password (cannot login locally unless they reset)
        user = User(
            email=email,
            password_hash=generate_password_hash(os.urandom(16).hex()),
            role="client",
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()
    # Issue JWT for frontend
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }
    })

# Optionally, add a logout route if you want to clear the OAuth session
@google_auth_bp.route("/logout")
def google_logout():
    session.clear()
    return redirect(url_for("google_auth_bp.google_login"))