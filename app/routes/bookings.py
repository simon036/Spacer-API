from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from ..models import Booking, Space
from ..extensions import db
from ..schemas import BookingSchema
from ..utils.decorators import role_required
from ..utils.validation import validate_schema
from ..utils.pagination import paginate
import os

bookings_bp = Blueprint('bookings', __name__)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

MIN_BOOKING_DURATION = int(os.getenv("MIN_BOOKING_DURATION", 1))
MAX_BOOKING_DURATION = int(os.getenv("MAX_BOOKING_DURATION", 24))
MIN_CANCELLATION_TIME = int(os.getenv("MIN_CANCELLATION_TIME", 24))

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
@validate_schema(booking_schema)
def create_booking(data):
    user_id = get_jwt_identity()
    space_id = data.get("space_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    space = Space.query.get_or_404(space_id)
    if space.status != "available":
        return {"error": "Space not available"}, 400
    duration_hours = (end_time - start_time).total_seconds() / 3600
    if duration_hours < MIN_BOOKING_DURATION or duration_hours > MAX_BOOKING_DURATION:
        return {"error": f"Booking duration must be between {MIN_BOOKING_DURATION} and {MAX_BOOKING_DURATION} hours."}, 400
    amount = duration_hours * space.price_per_hour
    booking = Booking(
        user_id=user_id,
        space_id=space_id,
        start_time=start_time,
        end_time=end_time,
        amount=amount,
        status="confirmed"
    )
    space.status = "booked"
    db.session.add(booking)
    db.session.commit()
    # No payment simulation, just return booking info (amount for invoicing)
    return booking_schema.dump(booking), 201

@bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    now = datetime.utcnow()
    if booking.status != "confirmed":
        return {"error": "Cannot cancel"}, 400
    # Only allow cancellation if more than MIN_CANCELLATION_TIME hours before start
    if (booking.start_time - now) < timedelta(hours=MIN_CANCELLATION_TIME):
        return {"error": f"Cannot cancel less than {MIN_CANCELLATION_TIME} hours before start time."}, 400
    booking.status = "cancelled"
    booking.space.status = "available"
    db.session.commit()
    return {"message": "Booking cancelled"}

@bookings_bp.route('/', methods=['GET'])
@jwt_required()
def list_bookings():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = Booking.query.filter_by(user_id=user_id)
    return paginate(query, bookings_schema, page, per_page)
