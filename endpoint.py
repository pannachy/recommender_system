from datetime import datetime
from .database import SessionLocal
from fastapi import Depends, FastAPI
from .model import Post
from .prediction_and_features import get_recommended_posts
from .schemas import Response
from sqlalchemy.orm import Session

'''
endpoint
'''


# подключаем сессию
app = FastAPI()
def get_db():
    with SessionLocal() as db:
        return db


# endpoint: получаем в качестве запроса id пользователя, запрашиваем ответ, возвращаем предсказания и № группы для A/B тестирования

@app.get("/post/recommendations/", response_model=Response)
def get_recommendations(id: int, time: datetime, limit: int = 5, db: Session = Depends(get_db)) -> Response:
    best_posts, exp_group = get_recommended_posts(id, time, limit)

    result = db.query(Post) \
        .filter(Post.id.in_(best_posts)) \
        .limit(limit) \
        .all()
    db.close()

    return Response(exp_group=exp_group, recommendations=result)