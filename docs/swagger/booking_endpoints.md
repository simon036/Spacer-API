### Booking API

#### POST `/api/bookings/`

Create a new booking for a space.

**Request Body:**
```json
{
  "space_id": 1,
  "start_time": "2024-06-01T10:00:00",
  "end_time": "2024-06-01T12:00:00"
}
```

**Responses:**

- **201 Created**
    - Returns the booking details, including calculated amount (for invoicing).

```json
{
  "id": 1,
  "user_id": 2,
  "space_id": 1,
  "start_time": "2024-06-01T10:00:00",
  "end_time": "2024-06-01T12:00:00",
  "amount": 200.0,
  "status": "confirmed",
  "created_at": "2024-05-30T09:00:00"
}
```

---

#### POST `/api/bookings/<booking_id>/cancel`

Cancel a confirmed booking (if allowed by cancellation policy).

**Responses:**

- **200 OK**
    - `{ "message": "Booking cancelled" }`
- **400 Bad Request**
    - `{ "error": "Cannot cancel less than 24 hours before start time." }`

---

#### GET `/api/bookings/`

List all bookings for the current user.

**Responses:**

- **200 OK**
    - Returns a list of bookings.

```json
[
  {
    "id": 1,
    "user_id": 2,
    "space_id": 1,
    "start_time": "2024-06-01T10:00:00",
    "end_time": "2024-06-01T12:00:00",
    "amount": 200.0,
    "status": "confirmed",
    "created_at": "2024-05-30T09:00:00"
  }
]
```