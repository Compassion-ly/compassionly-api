from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Body
from requests import Session

from app.api.deps import SessionDep, get_current_user
from app.core.db import get_session
from app.models import (
    UserTopicRating,
    UserTopicRatingCreate,
    UserTopicRatingRead,
    ResponseModel, User, Topic
)

router = APIRouter()

@router.post("/user-topic-rating", response_model=ResponseModel[UserTopicRatingRead], status_code=status.HTTP_201_CREATED)
async def create_user_topic_rating(
        *,
        session: Session = Depends(get_session),
        user_topic_rating: UserTopicRatingCreate = Body(
            ...,
            example={
                "rating": 4,
                "topic_id": 1
            }
        ),
        current_user: User = Depends(get_current_user)
) -> ResponseModel[UserTopicRatingRead]:
    user_id = current_user.id

    db_user_topic_rating = UserTopicRating(
        user_id=user_id,
        rating=user_topic_rating.rating,
        topic_id=user_topic_rating.topic_id
    )

    session.add(db_user_topic_rating)
    session.commit()
    session.refresh(db_user_topic_rating)

    user = session.query(User).filter(User.id == user_id).first()
    if user:
        new_rating = session.query(UserTopicRating).filter(
            UserTopicRating.user_id == user_id,
            UserTopicRating.topic_id == user_topic_rating.topic_id
        ).order_by(UserTopicRating.id.desc()).first()

        if new_rating:
            topic = session.query(Topic).filter(Topic.id == new_rating.topic_id).first()
            if topic and topic.topic_weight:
                multiplied_weights = [new_rating.rating * weight for weight in topic.topic_weight]
                print(f"New Rating: {new_rating.rating}, Topic Weight: {topic.topic_weight}, Multiplied Weights: {[round(weight, 2) for weight in multiplied_weights]}")
                user_topic_weights = user.user_topic_weight if user.user_topic_weight else [0.0] * 17
                user_topic_weights = [x + y for x, y in zip(user_topic_weights, multiplied_weights)]

                user.user_topic_weight = user_topic_weights
                session.commit()

                print(f"Updated User Topic Weights: {[round(weight, 2) for weight in user_topic_weights]}")

    return ResponseModel(
        message="success",
        data=db_user_topic_rating
    )

@router.get("/user-topic-rating/user-history", response_model=ResponseModel[List[UserTopicRatingRead]])
async def get_user_topic_ratings_by_user_id(
        *,
        session: SessionDep,
        current_user: str = Depends(get_current_user)
) -> ResponseModel[List[UserTopicRatingRead]]:
    """
    Retrieve UserTopicRatings by user_id.
    """
    user_id = current_user.id
    user_topic_ratings = session.query(UserTopicRating).filter(UserTopicRating.user_id == user_id).all()

    return ResponseModel(
        message="success",
        data=user_topic_ratings
    )

@router.get("/user-topic-rating/{id}", response_model=ResponseModel[UserTopicRatingRead])
async def get_user_topic_rating_by_id(
        *,
        session: SessionDep,
        id: int,
        current_user: str = Depends(get_current_user)
) -> ResponseModel[UserTopicRatingRead]:
    """
    Retrieve a specific UserTopicRating by ID.
    """
    db_user_topic_rating = session.get(UserTopicRating, id)
    if not db_user_topic_rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserTopicRating not found")

    return ResponseModel(
        message="success",
        data=db_user_topic_rating
    )


