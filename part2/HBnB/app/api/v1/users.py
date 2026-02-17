from flask import Blueprint

bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

@bp.get("/")
def list_users():
    return {"message": "Users endpoint ready"}
