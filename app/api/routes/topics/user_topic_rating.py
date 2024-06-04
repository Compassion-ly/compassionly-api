from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Body
from app.api.deps import SessionDep, get_current_user
from app.models import (
    UserTopicRating,
    UserTopicRatingCreate,
    UserTopicRatingRead,
    ResponseModel
)

router = APIRouter()

# Create a new UserTopicRating
@router.post("/user-topic-rating", response_model=ResponseModel[UserTopicRatingRead], status_code=status.HTTP_201_CREATED)
async def create_user_topic_rating(
        *,
        session: SessionDep,
        user_topic_rating: UserTopicRatingCreate = Body(
            ...,
            example={
                "rating": "somestring",
                "topic_id": 1
            }
        ),
        current_user: str = Depends(get_current_user)  # Ensure the user is authenticated
) -> ResponseModel[UserTopicRatingRead]:
    # Extract the user ID from current_user object
    user_id = current_user.id

    # Create a new UserTopicRating object
    db_user_topic_rating = UserTopicRating(
        user_id=user_id,
        rating=user_topic_rating.rating,
        topic_id=user_topic_rating.topic_id
    )

    # Save to the database
    session.add(db_user_topic_rating)
    session.commit()
    session.refresh(db_user_topic_rating)

    return ResponseModel(
        message="success",
        data=db_user_topic_rating
    )

# Retrieve UserTopicRatings by user_id
@router.get("/user-topic-rating/user-history", response_model=ResponseModel[List[UserTopicRatingRead]])
async def get_user_topic_ratings_by_user_id(
        *,
        session: SessionDep,
        current_user: str = Depends(get_current_user)  # Ensure the user is authenticated
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

# Retrieve a specific UserTopicRating by ID
@router.get("/user-topic-rating/{id}", response_model=ResponseModel[UserTopicRatingRead])
async def get_user_topic_rating_by_id(
        *,
        session: SessionDep,
        id: int,
        current_user: str = Depends(get_current_user)  # Ensure the user is authenticated
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


