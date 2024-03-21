from fastapi import HTTPException
from sqlalchemy.orm import Session
from ManageOrder.models import models_order
from ManageOrder.models import models_message, models_result
from ManageOrder.schemas import schemas_order, schemas_result, schemas_message


# 指定模型和消息查询模型结果
def get_result_by_ctx_id(db: Session, message_id: int, source: str):
    db_results = db.query(models_result.Result).filter(models_result.Result.message_id == message_id,
                                                       models_result.Result.source == source).all()

    return schemas_result.Result_list(results=db_results)


# 获取todo数量，返回acc
def get_todoresult_by_message_id(db: Session, message_id: int, source: str):
    db_acc = db.query(models_result.Acc).filter(models_result.Acc.message_id == message_id,
                                                models_result.Acc.source == source).first()
    if db_acc is None:
        raise HTTPException(status_code=404, detail=" 结果不存在")
    else:
        if db_acc.total == 0:  # 避免除零错误
            raise HTTPException(status_code=400, detail="Total is zero, division by zero is not allowed.")
        done = db_acc.onenums + db_acc.twonums
        data = {"todonums": db_acc.todonums, "onenums": db_acc.onenums, "twonums": db_acc.twonums,
                "total": db_acc.total,
                "acc": (db_acc.onenums + db_acc.twonums) / db_acc.total if db_acc.total else 0}
        return data


# 更新模型评分
def update_score_by_result_id(db: Session, result_id: int, score: int):
    db_result = db.query(models_result.Result).filter(models_result.Result.result_id == result_id).first()
    if db_result is None:
        raise HTTPException(status_code=404, detail=" 结果不存在")
    else:
        db_result.score = score
        db.commit()
        db.refresh(db_result)
        return db_result


# 获取所有可用模型
def get_sources(db: Session):
    db_sources = db.query(models_result.Result.source).distinct().all()
    source_list = [source[0] for source in db_sources]
    source = {"source": source_list}
    # print(source_list)
    return source
