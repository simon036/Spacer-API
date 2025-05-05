from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from ..models import User, Space, Booking
from ..extensions import db
from ..schemas import UserSchema, SpaceSchema, BookingSchema
from ..utils.decorators import role_required

admin_bp = Blueprint('admin', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
space_schema = SpaceSchema()
spaces_schema = SpaceSchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# USERS
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required("admin")
def admin_list_users():
    users = User.query.all()
    return users_schema.dump(users)

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required("admin")
def admin_add_user():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return {"error": "Email already exists"}, 400
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'client'),
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required("admin")
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    if "role" in data:
        user.role = data["role"]
    if "is_active" in data:
        user.is_active = data["is_active"]
    db.session.commit()
    return user_schema.dump(user)

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required("admin")
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}

# SPACES
@admin_bp.route('/spaces', methods=['GET'])
@jwt_required()
@role_required("admin")
def admin_list_spaces():
    spaces = Space.query.all()
    return spaces_schema.dump(spaces)

@admin_bp.route('/spaces/<int:space_id>', methods=['GET'])
@jwt_required()
@role_required("admin")
def admin_get_space(space_id):
    space = Space.query.get_or_404(space_id)
    return space_schema.dump(space)

@admin_bp.route('/spaces/<int:space_id>', methods=['PUT'])
@jwt_required()
@role_required("admin")
def admin_edit_space(space_id):
    space = Space.query.get_or_404(space_id)
    data = request.json
    for key in ["name", "description", "price_per_hour", "status"]:
        if key in data:
            setattr(space, key, data[key])
    db.session.commit()
    return space_schema.dump(space)

@admin_bp.route('/spaces/<int:space_id>', methods=['DELETE'])
@jwt_required()
@role_required("admin")
def admin_delete_space(space_id):
    space = Space.query.get_or_404(space_id)
    db.session.delete(space)
    db.session.commit()
    return {"message": "Space deleted"}

# BOOKINGS
@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required("admin")
def admin_list_bookings():
    bookings = Booking.query.all()
    return bookings_schema.dump(bookings)

@admin_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@jwt_required()
@role_required("admin")
def admin_get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return booking_schema.dump(booking)

@admin_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
@role_required("admin")
def admin_cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status != "confirmed":
        return {"error": "Cannot cancel"}, 400
    booking.status = "cancelled"
    booking.space.status = "available"
    db.session.commit()
    return {"message": "Booking cancelled"}

# STATS
@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required("admin")
def admin_stats():
    total_users = User.query.count()
    total_spaces = Space.query.count()
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Booking.amount)).scalar() or 0
    return {
        "total_users": total_users,
        "total_spaces": total_spaces,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue
    }
