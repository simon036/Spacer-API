from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..models import User
from ..extensions import db
from ..schemas import UserSchema
from ..utils.decorators import role_required
from ..utils.pagination import paginate

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/', methods=['GET'])
@jwt_required()
@role_required("admin")
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = User.query
    return paginate(query, users_schema, page, per_page)

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required("admin")
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    if "role" in data:
        user.role = data["role"]
    db.session.commit()
    return user_schema.dump(user)
