from typing import List, Dict

from fastapi import APIRouter, Depends, Query, HTTPException
from requests import Session
from colorama import Fore
from colorama import Style
from api import deps
from schemas.auth import AuthSchema
from schemas.comments import CommentCreateSchema

router = APIRouter()


@router.get('/')
async def get_comments(
        date: str,
        db: Session = Depends(deps.get_db)
):
    return db.execute(f'''
        SELECT * FROM comments
        WHERE is_archived=FALSE 
        AND date = '{date}'
        ORDER BY timestamp_created DESC
    ''').fetchall()


@router.post('/create')
async def get_comments(
        student_id: int,
        comment_create: CommentCreateSchema,
        db: Session = Depends(deps.get_db)
):
    pass
    # return db.execute(f'''
    #     SELECT * FROM comments WHERE student_id={student_id} AND is_archived=FALSE ORDER BY timestamp_created DESC
    # ''').fetchall()