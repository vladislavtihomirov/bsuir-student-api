from pydantic import BaseModel


class AuthSchema(BaseModel):
    student_id: int
    j_session_id: str
