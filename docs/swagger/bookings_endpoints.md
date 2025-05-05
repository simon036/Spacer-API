## Bookings API Swagger Documentation

### POST `/api/bookings/`
Create a new booking for a space.

```yaml
post:
  tags:
    - Bookings
  summary: Create a new booking
  security:
    - bearerAuth: []
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            space_id:
              type: integer
              example: 1
            start_time:
              type: string
              format: date-time
              example: "2024-06-01T10:00:00"
            end_time:
              type: string
              format: date-time
              example: "2024-06-01T12:00:00"
          required:
            - space_id
            - start_time
            - end_time
  responses:
    201:
      description: Booking created successfully
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Booking'
    400:
      description: Invalid input or business rule violation
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Space not available"
    401:
      description: Unauthorized
      content:
        application/json:
          schema:
            type: object
            properties:
              msg:
                type: string
                example: "Missing Authorization Header"
components:
  schemas:
    Booking:
      type: object
      properties:
        id:
          type: integer
          example: 1
        user_id:
          type: integer
          example: 2
        space_id:
          type: integer
          example: 1
        start_time:
          type: string
          format: date-time
          example: "2024-06-01T10:00:00"
        end_time:
          type: string
          format: date-time
          example: "2024-06-01T12:00:00"
        amount:
          type: number
          format: float
          example: 200.0
        status:
          type: string
          example: "confirmed"
        created_at:
          type: string
          format: date-time
          example: "2024-05-30T09:00:00"
```

---

### POST `/api/bookings/{booking_id}/cancel`
Cancel a confirmed booking.

```yaml
post:
  tags:
    - Bookings
  summary: Cancel a booking
  security:
    - bearerAuth: []
  parameters:
    - in: path
      name: booking_id
      schema:
        type: integer
      required: true
      description: ID of the booking to cancel
  responses:
    200:
      description: Booking cancelled successfully
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                example: "Booking cancelled"
    400:
      description: Cannot cancel booking
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Cannot cancel less than 24 hours before start time."
    401:
      description: Unauthorized
      content:
        application/json:
          schema:
            type: object
            properties:
              msg:
                type: string
                example: "Missing Authorization Header"
```

---

### GET `/api/bookings/`
List all bookings for the current user.

```yaml
get:
  tags:
    - Bookings
  summary: List all bookings for the current user
  security:
    - bearerAuth: []
  responses:
    200:
      description: List of bookings
      content:
        application/json:
          schema:
            type: array
            items:
              $ref: '#/components/schemas/Booking'
    401:
      description: Unauthorized
      content:
        application/json:
          schema:
            type: object
            properties:
              msg:
                type: string
                example: "Missing Authorization Header"
```