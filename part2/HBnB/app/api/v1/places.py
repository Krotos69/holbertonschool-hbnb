from Flask import Blueprint

bp = Blueprint("places", __name__, url_prefix="/api/v1/places")

@bp.get("/")
def list_places():
    return {"message": "Places endpoint ready"}
