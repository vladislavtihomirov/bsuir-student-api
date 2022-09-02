from typing import Generator
from db.session import get_session
session = get_session("main")

def get_db() -> Generator:
    try:
        db = session()
        yield db
    finally:
        db.close()