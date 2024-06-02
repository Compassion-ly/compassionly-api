from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.models import (
    UserTopicRating,
    UserTopicRatingCreate,
    UserTopicRatingRead,
    ResponseModel
)

router = APIRouter()

# Create a new UserTopicRating
@router.post("/user-topic-rating", response_model=ResponseModel[UserTopicRatingRead], status_code=status.HTTP_201_CREATED)
def create_user_topic_rating(*, session: SessionDep, user_topic_rating: UserTopicRatingCreate) -> ResponseModel[UserTopicRatingRead]:
    db_user_topic_rating = UserTopicRating.from_orm(user_topic_rating)
    session.add(db_user_topic_rating)
    session.commit()
    session.refresh(db_user_topic_rating)
    return ResponseModel(
        message="success",
        data=db_user_topic_rating
    )

# Retrieve a specific UserTopicRating by ID
@router.get("/user-topic-rating/{id}", response_model=ResponseModel[UserTopicRatingRead])
def get_user_topic_rating(*, session: SessionDep, id: int) -> ResponseModel[UserTopicRatingRead]:
    db_user_topic_rating = session.get(UserTopicRating, id)
    if not db_user_topic_rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserTopicRating not found")
    return ResponseModel(
        message="success",
        data=db_user_topic_rating
    )
