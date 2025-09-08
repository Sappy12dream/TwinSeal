# TwinSeal

**TwinSeal**: Secure File-Sharing Platform
===================================

A modern, security-focused application enabling encrypted file transfers between paired users. Built with enterprise-grade technologies and best practices in mind.

## Overview

TwinSeal combines robust security with intuitive user experience:
- **Backend**: FastAPI for high-performance async operations
- **Frontend**: React + TailwindCSS for responsive design
- **Database**: SQLAlchemy with SQLite/PostgreSQL support
- **Security**: End-to-end encryption with military-grade cryptography

## Core Features

### User System
- Secure authentication with JWT
- Account pairing mechanism
- Temporary access IDs (24h validity)
- Optional Google OAuth integration

### File Operations
- Upload files to paired user’s secure box
- Files encrypted at rest using strong cryptography
- Paired user can download and decrypt files

### Activity Tracking
- Logs every user action: upload, download, login, etc.
- Activity visible in paired user’s box

### Security
- File encryption with per-user or per-app key
- Time-limited account IDs for enhanced security
- Rate limiting on sensitive endpoints
- CORS and security headers applied
- Designed for HTTPS deployment

### Admin / Developer Features
- Backend: FastAPI (async & scalable)
- Frontend: React with TailwindCSS (minimal & responsive)
- Modular, extendable architecture
- Async database support with SQLAlchemy + SQLite (or PostgreSQL)
- Background cleanup tasks for expired files and pairing codes

---

## Installation

```bash
## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/twinseal.git
cd twinseal
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -e .
```

## Configuration

1. Create `.env` file from template:
    - Copy `.env.example` to `.env`
    - Update the following settings:
```env
DATABASE_URL=sqlite+aiosqlite:///./twinseal.db
SECRET_KEY=your_strong_secret_key_here
FILE_STORAGE_PATH=./storage
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

2. **Initialize Database**
```bash
alembic upgrade head
```

3. **Start Server**
```bash
uvicorn app.main:app --reload
```

## API Documentation

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `GET /health`

### Available Endpoints

#### Users
- `POST /api/v1/users/signup` - Register new user
- `POST /api/v1/users/login` - Login and get JWT

#### Pairing
- `POST /api/v1/pairing/generate` - Generate pairing code
- `POST /api/v1/pairing/pair/{code}` - Pair with user

#### Files
- `POST /api/v1/files/upload` - Upload encrypted file
- `GET /api/v1/files/download/{file_id}` - Download file

#### Activity
- `GET /api/v1/activity/` - View activity logs

## Production Guidelines

- Enable HTTPS with Nginx/cloud load balancer
- Use strong JWT secrets and encryption keys
- Configure CORS for frontend domains only
- Monitor with Sentry/Prometheus
- Apply rate limiting on sensitive routes

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Open Pull Request

## License

MIT License
