from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from api import deps
from schemas.students import UsersCheckSchema

router = APIRouter()


@router.post('/check')
async def check_users(
        users: UsersCheckSchema,
        db: Session = Depends(deps.get_db)
):
    try:
        return db.execute(f'''
            SELECT fio FROM auth
            WHERE fio in ({', '.join(list(map(lambda x: "'" + x + "'", users.users)))});
        ''').fetchall()
    except:
        raise HTTPException(status_code=500, detail="Some error occurred")
