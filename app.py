import logging
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, g, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

DATABASE = os.environ.get("DATABASE_PATH", "users_secure.db")
SECRET_KEY = os.environ.get("SECRET_KEY")
DEFAULT_RATE_LIMIT = os.environ.get(
    "DEFAULT_RATE_LIMIT",
    "100 per hour",
)

LOGIN_RATE_LIMIT = os.environ.get(
    "LOGIN_RATE_LIMIT",
    "5 per minute",
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required")

app.config["SECRET_KEY"] = SECRET_KEY
app.config["RATELIMIT_HEADERS_ENABLED"] = True

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[DEFAULT_RATE_LIMIT],
    storage_uri="memory://",
)


def get_required_environment_variable(name):
    value = os.environ.get(name)

    if not value:
        raise RuntimeError(f"{name} environment variable is required")

    return value


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    users = [
        (
            "amr",
            "amr@example.local",
            "admin",
            get_required_environment_variable("ADMIN_PASSWORD"),
        ),
        (
            "alice",
            "alice@example.local",
            "user",
            get_required_environment_variable("ALICE_PASSWORD"),
        ),
        (
            "bob",
            "bob@example.local",
            "user",
            get_required_environment_variable("BOB_PASSWORD"),
        ),
    ]

    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )

    for username, email, role, password in users:
        connection.execute(
            """
            INSERT OR IGNORE INTO users
            (username, email, role, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                email,
                role,
                generate_password_hash(password),
            ),
        )

    connection.commit()
    connection.close()


def token_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")

        if not authorization.startswith("Bearer "):
            return jsonify({"error": "Authentication required"}), 401

        token = authorization.removeprefix("Bearer ").strip()

        try:
            payload = jwt.decode(
                token,
                app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        g.current_user = payload

        return function(*args, **kwargs)

    return decorated_function


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"

    return response


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(_error):
    logger.exception("Unexpected internal application error")
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(429)
def rate_limit_exceeded(_error):
    return jsonify(
        {
            "error": "Too many requests",
            "message": "Rate limit exceeded. Please try again later.",
        }
    ), 429

@app.get("/health")
@limiter.exempt
def health():
    return jsonify({"status": "healthy"})


@app.post("/api/login")
@limiter.limit(LOGIN_RATE_LIMIT)
def login():
    body = request.get_json(silent=True) or {}

    username = body.get("username")
    password = body.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Username and password are required"}), 400

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username, role, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    connection.close()

    if user is None or not check_password_hash(
        user["password_hash"],
        password,
    ):
        logger.warning("Failed login attempt username=%s", username)
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "sub": str(user["id"]),
            "username": user["username"],
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    logger.info("Successful login username=%s", username)

    return jsonify(
        {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 1800,
        }
    )


@app.get("/api/users/<int:user_id>")
@token_required
def get_user(user_id):
    current_user_id = int(g.current_user["sub"])
    current_role = g.current_user["role"]

    if current_role != "admin" and current_user_id != user_id:
        logger.warning(
            "Authorization denied user_id=%s requested_user_id=%s",
            current_user_id,
            user_id,
        )
        return jsonify({"error": "Access denied"}), 403

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username, email, role
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()

    connection.close()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user))


@app.get("/api/search")
@token_required
def search_users():
    if g.current_user["role"] != "admin":
        return jsonify({"error": "Administrator access required"}), 403

    search_term = request.args.get("q", "")

    if not isinstance(search_term, str) or len(search_term) > 50:
        return jsonify({"error": "Invalid search value"}), 400

    connection = get_connection()

    users = connection.execute(
        """
        SELECT id, username, email, role
        FROM users
        WHERE username LIKE ?
        """,
        (f"%{search_term}%",),
    ).fetchall()

    connection.close()

    return jsonify([dict(user) for user in users])


if __name__ == "__main__":
    initialize_database()

    app.run(
        host=os.environ.get("APP_HOST", "127.0.0.1"),
        port=int(os.environ.get("APP_PORT", "5001")),
        debug=False,
        use_reloader=False,
    )