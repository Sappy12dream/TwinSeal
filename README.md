# TwinSeal

A secure document sharing platform that allows users to pair with each other using temporary account IDs and share encrypted documents.

## Features

- User registration and authentication
- Temporary account ID pairing (24-hour validity)
- Encrypted document upload and download
- Secure file sharing between paired users

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your configuration
3. Install dependencies: `pip install -e .`
4. Run migrations: `alembic upgrade head`
5. Start the server: `uvicorn app.main:app --reload`

## API Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /pairs/create` - Generate account ID for pairing
- `POST /pairs/connect` - Connect using account ID
- `POST /documents/upload` - Upload encrypted document
- `GET /documents/{doc_id}` - Download document (if paired)

## Development

- Run tests: `pytest`
- Format code: `black .`
- Sort imports: `isort .`