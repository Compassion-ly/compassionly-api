import json

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from fastapi.params import Query
from sqlmodel import Session, select

from app.api.deps import SessionDep, get_current_user
from app.core.db import get_session
from app.models import Topic, TopicCreate, TopicRead, ResponseModel

router = APIRouter()

# Retrieve a specific topic by ID
@router.get("/topics/{id}", response_model=ResponseModel[TopicRead])
def get_topic_by_id(
        *,
        session: Session = Depends(get_session),
        id: int,
        # current_user: str = Depends(get_current_user)  # Ensure the user is authenticated
) -> ResponseModel[TopicRead]:
    # Check if the user is authenticated
    # if not current_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Retrieve the topic by ID
    db_topic = session.get(Topic, id)
    if not db_topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

    return ResponseModel(
        message="success",
        data=db_topic
    )

@router.get("/topics", response_model=ResponseModel[List[TopicRead]])
def get_all_topics(
        *,
        session: Session = Depends(get_session),
        # current_user: str = Depends(get_current_user),  # Ensure the user is authenticated
        limit: int = Query(25, ge=1, le=100),  # Limit the number of topics returned, default to 25, max 100
        offset: int = Query(0, ge=0)  # Offset for pagination, default to 0
) -> ResponseModel[List[TopicRead]]:
    # Check if the user is authenticated
    # if not current_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Retrieve topics with limit and offset
    db_topics = session.exec(select(Topic).offset(offset).limit(limit)).all()
    if not db_topics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No topics found")

    return ResponseModel(
        message="success",
        data=db_topics
    )
