from app.crud.base import CRUDBase
from app.models.posts import Post
from app.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    pass


post_crud = CRUDPost(Post)
