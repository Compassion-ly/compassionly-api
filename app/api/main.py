from fastapi import APIRouter

from app.api.routes import auth, users, schools, colleges
from app.api.routes.topics import user_topic_rating, topic_category, topics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(schools.router, prefix="/schools", tags=["schools"])

api_router.include_router(user_topic_rating.router, prefix="/topics", tags=["user-topic-rating"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(topic_category.router, prefix="/topics", tags=["topic-category"])

api_router.include_router(colleges.router, prefix="/colleges", tags=["colleges"])


