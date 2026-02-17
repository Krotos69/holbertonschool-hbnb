from Flask import Blueprint

bp = Blueprint("reviews", __name__, url_prefix="/api/v1/reviews")

@bp.get("/")
def list_reviews():
    return {"message": "Reviews endpoint ready"}
