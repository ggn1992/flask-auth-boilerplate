# Flask Authentication Boilerplate

## Features

This project is under active development and may contain bugs.

- Made with Python 3, Flask, Bootstrap 5, MariaDB, Redis (for server-side sessions), Docker
- User Management: Login / Logout / Change Password / Register / Reset Password
- Containerized deployment

### Feature Wishlist

- Role-based authentication
- 2-Factor-Authentication (e.g. Google Authenticator, Yubikey)

## Project Structure

```plaintext
❯ tree -L 3
.
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── utils.py
│   ├── email.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static
│   │   ├── css
│   │   └── js
│   ├── templates
│   │   ├── auth
│   │   ├── auth.html
│   │   ├── base.html
│   │   ├── main
│   │   ├── partials
│   │   └── user
│   └── user
│       ├── __init__.py
│       ├── forms.py
│       ├── models.py
│       └── routes.py
├── config.py
├── docker-compose.yml
├── requirements.txt
├── tests
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_main.py
└── wsgi.py
```

## Dockerfile & docker-compose.yml

The `Dockerfile` uses Python 3.12.4 and Alpine 3.20:

```plaintext
FROM python:3.12.4-alpine3.20
```

If you need a MariaDB management frontend for development, just add these lines to the end of `docker-compose.yml`:

```plaintext
  adminer:
    image: adminer:latest
    container_name: adminer
    environment:
      ADMINER_DEFAULT_SERVER: db
    restart: always
    ports:
      - 8080:8080
```

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtualenv (optional but recommended)
- Docker (optional but recommended)

### Installation

1. Clone the repository

```sh
git clone https://github.com/yourusername/flask-auth-boilerplate.git
cd flask-auth-boilerplate
```

2. Create and activate a virtual environment (optional but recommended)

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies

```sh
pip install -r requirements.txt
```

4. Set up environment variables

Create a .env file in the root directory and add the following variables:

```plaintext
APP_TITLE=My Flask App

FLASK_APP=wsgi.py
# Uncomment for development
#FLASK_DEBUG=1
#FLASK_ENV=development

MARIADB_USER=app_user
MARIADB_PASSWORD=my-secret-pw
MARIADB_ROOT_PASSWORD=my-secret-pw
MARIADB_DATABASE=app_db
#MARIADB_HOST=127.0.0.1
# if using docker-compose.yml
MARIADB_HOST=db
DATABASE_URI=mariadb+mariadbconnector://${MARIADB_USER}:${MARIADB_PASSWORD}@${MARIADB_HOST}:3306/${MARIADB_DATABASE}

#REDIS_URI=redis://localhost:6379
# if using docker-compose.yml
REDIS_URI=redis://redis:6379

# Set secret key and CSRF secret key for Flask-WTF
# Generate using: openssl rand -hex 32
SECRET_KEY=your_secret_key
CSRF_SECRET_KEY=your_csrf_secret_key

# Set environment variables for configuring Flask-Mail
MAIL_SERVER=your_mail_server
MAIL_USERNAME=your_email_username
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=${MAIL_USERNAME}
MAIL_USE_TLS=true
```

5. Optional step: Setup Docker containers

```sh
docker compose up --build
# use -d to detach:
docker compose up --build -d
```

6. Initialize the database

```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

7. Run the application

```sh
flask run
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.