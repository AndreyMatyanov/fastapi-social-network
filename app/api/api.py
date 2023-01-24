from fastapi import APIRouter

from .endpoints import auth, post, reaction, user

api_routers = APIRouter()
api_routers.include_router(post.router, prefix="/post", tags=["Post"])
api_routers.include_router(reaction.router, prefix="/reaction", tags=["Reaction"])
api_routers.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_routers.include_router(user.router, prefix="/user", tags=["User"])
