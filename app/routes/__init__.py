from .auth_routes import auth_router
from .user_routes import user_router
from .tree_routes import tree_router

routes = [auth_router, user_router, tree_router]
