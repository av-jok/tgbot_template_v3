"""Import all routers and add them to routers_list."""
from .admin import admin_router
# from .echo import echo_router
# from .user import user_router
from .start import start_router
from .questions import questions_router
from .any import any_router

routers_list = [
    # admin_router,
    start_router,
    questions_router,
    any_router
]

__all__ = [
    "routers_list",
]
