""" app/routes/__init__.py """

from flask import Blueprint
from .user import user_bp
from .family_tree import family_tree_bp
from .family_member import family_member_bp

""" blueprint for routes """
routes_bp = Blueprint('routes', __name__)
routes_bp.register_blueprint(user_bp)
routes_bp.register_blueprint(family_tree_bp)
routes_bp.register_blueprint(family_member_bp)

