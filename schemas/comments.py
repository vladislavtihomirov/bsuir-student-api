from pydantic import BaseModel


class CommentCreateSchema(BaseModel):
    student_id: int
    date: str
    type: str
    content_text: str
    content_file: str
