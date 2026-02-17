from Flask import Blueprint

bp = Blueprint("amenities", __name__, url_prefix="/api/v1/amenities")

@bp.get("/")
def list_amenities():
    return {"message": "Amenities endpoint ready"}
