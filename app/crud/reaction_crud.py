from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.post_reactions import PostReactions
from app.schemas.reaction import CountOfReactions, ReactionCreate, ReactionUpdate


class CRUDReaction(CRUDBase[PostReactions, ReactionCreate, ReactionUpdate]):
    def get_by_user_id_and_post_id(self, db: Session, reaction: ReactionCreate):
        return (
            db.query(self.model)
            .filter(self.model.post_id == reaction.post_id)
            .filter(self.model.user_id == reaction.user_id)
            .one_or_none()
        )

    def get_counts_on_post(self, db: Session, post_id=id):
        db_query = db.query(self.model).filter(self.model.post_id == post_id)

        count_of_like = db_query.filter(self.model.reaction == "LIKE").count()
        count_of_dislike = db_query.filter(self.model.reaction == "DISLIKE").count()

        counts = CountOfReactions(like=count_of_like, dislike=count_of_dislike)
        return counts


reaction_crud = CRUDReaction(PostReactions)
