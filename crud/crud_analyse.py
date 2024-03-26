import collections


from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import models_message, models_result
from schemas import schemas_result
from database.databases_order import engine, SessionLocal
from schemas.schemas_result import InputDiff


# 计算该ctx相关模型的困难度
def get_ctxdata_analyse(db: Session, message_id: int, diff_level: float):
    # 确保他是ctx消息
    db_ctx = db.query(models_message.Message).filter(models_message.Message.message_id == message_id
                                                     , models_message.Message.reason_type != 0).first()
    try:
        inputData = InputDiff(diff_level=diff_level)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"diff_level参数输入错误{e}")

    if db_ctx is None:
        raise HTTPException(status_code=404, detail="不存在该ctx")

    # 在视图表查询与该ctx相关的模型信息
    db_results = db.query(models_result.Hard).filter(models_result.Hard.message_id == message_id).first()
    hard_level = db_results.onenums / db_results.total
    print(hard_level)
    if hard_level > diff_level:
        return f"该ctx属于困难level，通过率为{hard_level}"
    else:
        return f"该ctx不属于困难level，通过率为{hard_level}"


# 计算传入的reason_type数据集的困难度

def get_reason_type_analyse(db: Session, reason_type: int, diff_level: float):
    try:
        inputData = InputDiff(diff_level=diff_level)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"diff_level参数输入错误{e}")
    if reason_type == 0:
        raise HTTPException(status_code=404, detail="请输入正确的ctx类型")
    db_type = db.query(models_result.Hard).filter(models_result.Hard.reason_type == reason_type).all()
    if db_type is None:
        raise HTTPException(status_code=404, detail="不存在该ctx")

    if diff_level > 1 or diff_level < 0:
        # http code 不要乱写 能规范就规范一下
        raise HTTPException(status_code=422, detail="请输入正确的困难度参数")

    # 定义一个存放输出结果的字典

    result = {}
    for item in db_type:
        message_id = item.message_id
        hard_level = item.onenums / item.total
        if hard_level > diff_level:
            result[message_id] = f"该ctx属于困难level，通过率为{hard_level}"
        else:
            result[message_id] = f"该ctx不属于困难level，通过率为{hard_level}"
    return result


# 输出所有reason_type的结果
def get_all_analyse(db: Session, diff_level: float):
    try:
        inputData = InputDiff(diff_level=diff_level)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"diff_level参数输入错误")

    db_results = db.query(models_result.Hard).filter(models_result.Hard.reason_type != 0).all()
    result = []

    ishard_reason_type2msg_idxs = collections.defaultdict(list)

    for record in db_results:
        msg_id = record.message_id
        a = record.onenums / record.total
        print(a)
        is_hard = True if record.onenums / record.total > diff_level else False

        key = f"{is_hard}_{record.reason_type}"
        ishard_reason_type2msg_idxs[key].append(msg_id)

    for key, msg_ids in ishard_reason_type2msg_idxs.items():
        is_hard, reason_type = key.split("_")

        if is_hard == "True":
            is_hard = bool(1)
        else:
            is_hard = bool()
        reason_type = int(reason_type)
        result.append({
            'reason_type': reason_type,
            'is_hard': is_hard,
            'msg_idx': msg_ids
        })

    return result


# 对不同模型进行对比分析
def get_model_analyse(db: Session, modelA: str, modelB: str, reason_type: list[int]):
    # 能索引就直接索引，可读性、时间复杂度都会好一点。
    result_dict = {}
    for reasontype in reason_type:
        if reasontype == 0:
            raise HTTPException(status_code=400, detail="reason_type不能为0")
        db_a = db.query(models_result.Hard).filter(models_result.Hard.reason_type == reasontype,
                                                   models_result.Hard.source == modelA).all()

        new_db = Session(bind=engine)
        db_b = new_db.query(models_result.Hard).filter(
            models_result.Hard.reason_type == reasontype,
            models_result.Hard.source == modelB).all()

        for record in db_a:
            msg_id = record.message_id
            benchmark_a = record.onenums / record.total

            result_dict[msg_id] = {
                'message_id': msg_id,
                'benchmark_a': benchmark_a,
            }

        for record1 in db_b:
            msg_id = record1.message_id
            benchmark_b = record1.onenums / record1.total

            if msg_id not in result_dict:
                # 这里，某一个msg没有，就全盘否定所有结果？是不是可以处理的更优雅一点。
                del result_dict[msg_id]
            else:
                result_dict[msg_id]['benchmark_b'] = benchmark_b

    return list(result_dict.values())
