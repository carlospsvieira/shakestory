from .user import user_routes
from .story import story_routes
from .segment import segment_routes

def routes(app):
    user_routes(app)
    story_routes(app)
    segment_routes(app)
