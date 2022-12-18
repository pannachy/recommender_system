from sqlalchemy import Column, String, Integer
from .database import Base

'''
модели SQLAlchemy
'''

class Post(Base):
    __tablename__ = "post_text_df"
    id = Column(Integer, primary_key=True, name="post_id")
    text = Column(String)
    topic = Column(String)