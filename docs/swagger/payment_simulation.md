### Payment Simulation API

#### POST `/api/payments/simulate`

Simulate a payment process with a configurable success rate (for testing and demo purposes).

**Request Body:**
```json
{
  "amount": 100.0
}
```

**Responses:**

- **200 OK**
    - Payment simulation result.

```json
{
  "status": "success",
  "amount": 100.0
}
```
or
```json
{
  "status": "failure",
  "amount": 100.0
}
```

---

#### Flasgger YAML Example

```yaml
post:
  tags:
    - Payments
  summary: Simulate a payment process
  description: Simulates a payment with a configurable success rate for demo/testing.
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            amount:
              type: number
              example: 100.0
          required:
            - amount
  responses:
    200:
      description: Payment simulation result
      content:
        application/json:
          schema:
            type: object
            properties:
              status:
                type: string
                enum: [success, failure]
                example: success
              amount:
                type: number
                example: 100.0
```

---

**How to use:**  
- Add this YAML under your `/api/payments/simulate` endpoint in your Flasgger/OpenAPI docs.
- Adjust the path if your endpoint differs.