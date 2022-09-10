from pydantic import BaseModel


class AuthSchema(BaseModel):
    student_id: int
    fio: str
    j_session_id: str


class AuthJSSchema(BaseModel):
    student_id: int
