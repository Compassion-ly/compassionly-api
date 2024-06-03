from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.api.deps import SessionDep, get_current_user
from app.models import Topic, TopicCreate, TopicRead, ResponseModel

router = APIRouter()

# Retrieve a specific topic by ID
@router.get("/topics/{id}", response_model=ResponseModel[TopicRead])
def get_topic_by_id(
        *,
        session: SessionDep,
        id: int,
        current_user: str = Depends(get_current_user)  # Ensure the user is authenticated
) -> ResponseModel[TopicRead]:
    # Check if the user is authenticated
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Retrieve the topic by ID
    db_topic = session.get(Topic, id)
    if not db_topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

    return ResponseModel(
        message="success",
        data=db_topic
    )
