from cashews import cache
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.api.depends import get_db
from app.schemas.reaction import CountOfReactions, ReactionBase, ReactionCreate
from app.service import reaction_service, user_service

router = APIRouter()
cache.setup("redis://")


@router.get("/count-on-post/{post_id}", response_model=CountOfReactions)
@cache(ttl="10h")
async def get_count_of_reactions_on_post(post_id: int, db: Session = Depends(get_db)):
    return reaction_service.get_count_of_reactions(post_id=post_id, db=db)


@router.post("/")
@cache.invalidate(get_count_of_reactions_on_post)
async def set_reaction(
    reaction: ReactionCreate,
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends(),
):
    try:
        authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    user = user_service.get_user_by_auth(db=db, authorize=authorize)

    reaction_create = ReactionBase(
        post_id=reaction.post_id,
        user_id=user.id,
        reaction=reaction.reaction,
        date=reaction.date,
    )
    return reaction_service.set_reaction(db=db, reaction=reaction_create)
