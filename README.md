# Aplikasi Kolegium - OSCE Management System

A comprehensive CRUD application for managing OSCE (Objective Structured Clinical Examination) participants, sessions, and statistics using Flask and MySQL.

## Features

- **Participant Management**: Add, view, edit, and delete OSCE participants
- **Bulk Upload**: Excel file upload for batch participant registration
- **OSCE Sessions**: Manage examination sessions with scheduling
- **Statistics Dashboard**: Real-time analytics by university and attempt status
- **Authentication**: Secure login system with role-based access
- **Responsive UI**: Modern interface with dark mode support

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL 8.0
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Libraries**: Flask-Login, PyMySQL, Pandas
- **Containerization**: Docker & Docker Compose

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- At least 2GB free RAM

### 1. Clone and Setup
```bash
git clone <your-repository-url>
cd flask
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your secure credentials
nano .env
```

### 3. Launch Application
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f aplikasi-kolegium-app
```

### 4. Access Application
- **Application**: http://localhost:8080 (via Nginx)
- **Direct Flask App**: http://localhost:8181 (development only)
- **Default Login**: admin / adminpass (change in .env!)

### 5. Database Access
```bash
# Connect to MySQL container
docker-compose exec mysql mysql -u dev -p crud_flask
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_DATABASE` | crud_flask | Database name |
| `MYSQL_USER` | app_user | MySQL user |
| `MYSQL_PASSWORD` | secure_password_change_me | MySQL password |
| `ADMIN_USERNAME` | admin | Admin username |
| `ADMIN_PASSWORD` | adminpass | Admin password |
| `APP_PORT` | 8181 | Flask app port |
| `NGINX_PORT` | 8080 | Nginx proxy port |

## Development Setup

### Using Docker for Development
```bash
# Copy development overrides
cp docker-compose.override.yml.example docker-compose.override.yml

# Start with development settings
docker-compose up -d
```

### Local Development (without Docker)
```bash
# Install dependencies
pip install -r source_code/requirements.txt

# Set environment variables
export DB_HOST=localhost
export DB_USER=dev
export DB_PASSWORD=dev
export DB_NAME=crud_flask

# Run application
cd source_code
python server.py
```

## Docker Services

- **aplikasi-kolegium-app**: Flask web application
- **aplikasi-kolegium-mysql**: MySQL 8.0 database
- **nginx**: Reverse proxy and load balancer

## Security Notes

⚠️ **Important**: Change default passwords before deploying to production!

- Default admin credentials: `admin` / `adminpass`
- Default MySQL credentials: `app_user` / `secure_password_change_me`
- Use strong, unique passwords in production
- Consider using Docker secrets for sensitive data

## Database Schema

The application includes the following tables:
- `university`: University information
- `peserta`: OSCE participants
- `lokasi_osce`: Examination locations
- `osce`: Examination sessions
- `osce_peserta`: Participant-session relationships

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /login`: Authentication page
- `GET /`: Dashboard (requires login)
- `GET /peserta/`: Participant list
- `POST /peserta/add`: Add participant
- `POST /peserta/upload`: Bulk upload participants

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change ports in .env file
   APP_PORT=8182
   NGINX_PORT=8081
   ```

2. **Database connection failed**
   ```bash
   # Check MySQL container logs
   docker-compose logs mysql

   # Verify environment variables
   docker-compose exec app env | grep DB_
   ```

3. **Permission denied on volumes**
   ```bash
   # Fix permissions on host
   sudo chown -R 1000:1000 ./source_code
   ```

### Health Checks

All services include health checks:
```bash
# Check service health
docker-compose ps

# View health status
docker inspect aplikasi-kolegium-app | grep -A 5 "Health"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## License

This project is licensed under the terms specified in the License file.
