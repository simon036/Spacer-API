# Spacer Backend

## Overview

This is the backend API for the Spacer platform, built with Flask and PostgreSQL.  
It supports user authentication, space management, bookings, image uploads, and more.

## Features

- Flask + PostgreSQL database
- JWT authentication (multi-role: admin, owner, client)
- User, space, and booking management
- 2-step email verification (SendGrid)
- Cloudinary image uploads (with resizing)
- Booking system with notifications
- Pagination, validation, error handling
- Swagger/OpenAPI documentation
- CI/CD ready (GitHub Actions)
- Testing scaffold (pytest)

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your environment variables
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run database migrations:
    ```bash
    flask db upgrade
    ```
5. Start the server:
    ```bash
    python run.py
    ```

## Testing

```bash
pytest
```

## API Documentation

- Swagger UI available at `/apidocs` when the server is running.
- See `docs/swagger/` for YAML docs for each endpoint group.

## Deployment

- See `.github/workflows/ci.yml` for CI/CD pipeline example.

## Contributing

- Please open issues and submit pull requests for improvements or bug fixes.

## License

MIT
