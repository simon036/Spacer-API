from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import Space, User
from ..extensions import db
from ..schemas import SpaceSchema
from ..utils.cloudinary_utils import upload_image
from ..utils.decorators import role_required
from ..utils.validation import validate_schema
from ..utils.pagination import paginate

spaces_bp = Blueprint('spaces', __name__)
space_schema = SpaceSchema()
spaces_schema = SpaceSchema(many=True)

@spaces_bp.route('/', methods=['GET'])
def list_spaces():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = Space.query
    return paginate(query, spaces_schema, page, per_page)

@spaces_bp.route('/<int:space_id>', methods=['GET'])
def get_space(space_id):
    space = Space.query.get_or_404(space_id)
    return space_schema.dump(space)

@spaces_bp.route('/', methods=['POST'])
@jwt_required()
@role_required("admin", "owner")
@validate_schema(space_schema)
def create_space(data):
    owner_id = get_jwt_identity()
    file = request.files.get("image")
    image_url = upload_image(file) if file else None
    space = Space(
        name=data["name"],
        description=data["description"],
        price_per_hour=data["price_per_hour"],
        owner_id=owner_id,
        image_url=image_url
    )
    db.session.add(space)
    db.session.commit()
    return space_schema.dump(space), 201

@spaces_bp.route('/<int:space_id>', methods=['PUT'])
@jwt_required()
@role_required("admin", "owner")
@validate_schema(space_schema)
def update_space(data, space_id):
    space = Space.query.get_or_404(space_id)
    for key in ["name", "description", "price_per_hour", "status"]:
        if key in data:
            setattr(space, key, data[key])
    db.session.commit()
    return space_schema.dump(space)

@spaces_bp.route('/<int:space_id>', methods=['DELETE'])
@jwt_required()
@role_required("admin", "owner")
def delete_space(space_id):
    space = Space.query.get_or_404(space_id)
    db.session.delete(space)
    db.session.commit()
    return {"message": "Space deleted"}
