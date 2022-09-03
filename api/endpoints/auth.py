from typing import List, Dict

from fastapi import APIRouter, Depends, Query, HTTPException
from requests import Session
from colorama import Fore
from colorama import Style
from api import deps
from schemas.auth import AuthSchema

router = APIRouter()


@router.post('/update')
async def get_users(
        auth: AuthSchema,
        db: Session = Depends(deps.get_db)
):
    try:
        db.execute(f'''
            INSERT INTO auth(student_id, j_session_id)
            VALUES ({auth.student_id}, '{auth.j_session_id}')
            ON CONFLICT ON CONSTRAINT auth_pkey
            DO UPDATE SET j_session_id = '{auth.j_session_id}';
        ''')
        print(f'Updated {Fore.LIGHTBLUE_EX}auth{Style.RESET_ALL} table: {Fore.GREEN}student_id={auth.student_id}{Style.RESET_ALL}')
        db.execute(f'''
            INSERT INTO profiles(student_id, last_logged)
            VALUES ({auth.student_id}, NOW())
            ON CONFLICT ON CONSTRAINT profiles_pkey
            DO UPDATE SET last_logged = NOW();
        ''')
        print(f'Updated {Fore.LIGHTBLUE_EX}profiles{Style.RESET_ALL} table: {Fore.GREEN}student_id={auth.student_id}{Style.RESET_ALL}')
        db.commit()
        print(f'{Fore.GREEN}Committed all to database:){Style.RESET_ALL}')
        return auth
    except:
        raise HTTPException(status_code=500, detail="Can't update token.")
