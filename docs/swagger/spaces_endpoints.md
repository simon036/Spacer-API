## Spaces API Swagger Documentation

### GET `/api/spaces/`
List all spaces (paginated).

```yaml
get:
  tags:
    - Spaces
  summary: List all spaces (paginated)
  parameters:
    - in: query
      name: page
      schema:
        type: integer
      description: Page number
    - in: query
      name: per_page
      schema:
        type: integer
      description: Items per page
  responses:
    200:
      description: List of spaces
      content:
        application/json:
          schema:
            type: object
            properties:
              items:
                type: array
                items:
                  $ref: '#/components/schemas/Space'
              total:
                type: integer
                example: 100
              pages:
                type: integer
                example: 10
              current_page:
                type: integer
                example: 1
components:
  schemas:
    Space:
      type: object
      properties:
        id:
          type: integer
          example: 1
        name:
          type: string
          example: "Conference Room"
        description:
          type: string
          example: "A spacious conference room with projector."
        image_url:
          type: string
          example: "https://res.cloudinary.com/demo/image/upload/v1234567890/spaces/room.jpg"
        price_per_hour:
          type: number
          format: float
          example: 100.0
        status:
          type: string
          example: "available"
        owner_id:
          type: integer
          example: 2
        created_at:
          type: string
          format: date-time
          example: "2024-05-30T09:00:00"
```

---

### GET `/api/spaces/{space_id}`
Get details of a specific space.

```yaml
get:
  tags:
    - Spaces
  summary: Get details of a space
  parameters:
    - in: path
      name: space_id
      schema:
        type: integer
      required: true
      description: ID of the space
  responses:
    200:
      description: Space details
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Space'
    404:
      description: Space not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Not found"
```

---

### POST `/api/spaces/`
Create a new space.

```yaml
post:
  tags:
    - Spaces
  summary: Create a new space
  security:
    - bearerAuth: []
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Conference Room"
            description:
              type: string
              example: "A spacious conference room with projector."
            price_per_hour:
              type: number
              format: float
              example: 100.0
          required:
            - name
            - description
            - price_per_hour
  responses:
    201:
      description: Space created successfully
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Space'
    400:
      description: Invalid input
      content:
        application/json:
          schema:
            type: object
            properties:
              errors:
                type: object
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

### PUT `/api/spaces/{space_id}`
Update a space.

```yaml
put:
  tags:
    - Spaces
  summary: Update a space
  security:
    - bearerAuth: []
  parameters:
    - in: path
      name: space_id
      schema:
        type: integer
      required: true
      description: ID of the space
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Conference Room"
            description:
              type: string
              example: "A spacious conference room with projector."
            price_per_hour:
              type: number
              format: float
              example: 100.0
            status:
              type: string
              example: "available"
  responses:
    200:
      description: Space updated successfully
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Space'
    400:
      description: Invalid input
      content:
        application/json:
          schema:
            type: object
            properties:
              errors:
                type: object
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
    404:
      description: Space not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Not found"
```

---

### DELETE `/api/spaces/{space_id}`
Delete a space.

```yaml
delete:
  tags:
    - Spaces
  summary: Delete a space
  security:
    - bearerAuth: []
  parameters:
    - in: path
      name: space_id
      schema:
        type: integer
      required: true
      description: ID of the space
  responses:
    200:
      description: Space deleted successfully
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                example: "Space deleted"
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
    404:
      description: Space not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Not found"
```