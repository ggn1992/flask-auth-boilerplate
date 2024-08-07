# Flask Authentication Boilerplate

## Features

This project is under active development and may contain bugs.

- Made with Python 3, Flask, Bootstrap 5, MariaDB, Redis (server-side sessions)
- Login / Logout / Change Password
- Register / Reset Password
- E-Mails (SMTP server is needed)

### Feature Wishlist

- Containerized deployment
- Role-based authentication
- 2-Factor-Authentication (Google Authenticator, Yubikey)

## Project Structure

```plaintext
❯ tree -L 3
.
├── app
│   ├── auth
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── email.py
│   ├── __init__.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   └── templates
│       ├── auth
│       ├── base.html
│       └── main
├── config.py
├── docker-compose.yml
├── README.md
├── requirements.txt
├── run.py
```

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtualenv (optional but recommended)

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

# Set environment variables for running the Flask server
FLASK_DEBUG=1
FLASK_APP=run.py
FLASK_ENV=development

# Set Database URI for application:
# For SQLite use: sqlite:///db.sqlite3
# For MySQL/MariaDB use: mariadb+mariadbconnector://your_username:your_password@your_host/database_name
MARIADB_USER=app_user
MARIADB_PASSWORD=my-secret-pw
MARIADB_ROOT_PASSWORD=my-secret-pw
MARIADB_DATABASE=app_db
MARIADB_HOST=127.0.0.1
DATABASE_URI=mariadb+mariadbconnector://${MARIADB_USER}:${MARIADB_PASSWORD}@${MARIADB_HOST}:3306/${MARIADB_DATABASE}

REDIS_URI=redis://localhost:6379

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

*Optional step: Setup Docker containers*

```sh
docker compose up -d
```

5. Initialize the database

```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

6. Run the application

```sh
flask run
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.