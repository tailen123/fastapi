# models.py

from sqlalchemy import Column, Integer, String
from ManageOrder.database.databases_order import Base



class Message(Base):
    __tablename__ = "message_table"
    id = Column(Integer, primary_key=True, index=True)
    dialog_id = Column(Integer)
    text = Column(String)
    text_zh = Column(String)
    created_at = Column(String)
    stage = Column(Integer)
    # from_user是bool型变量
    from_user = Column(Integer)
    reason = Column(String)
    reason_type = Column(String)
    is_del = Column(Integer)
    message_id = Column(Integer)
    extend_existing = True


