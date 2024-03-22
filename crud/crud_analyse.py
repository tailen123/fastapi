from fastapi import HTTPException
from sqlalchemy.orm import Session
from ManageOrder.models import models_order
from ManageOrder.models import models_message, models_result
from ManageOrder.schemas import schemas_order, schemas_result, schemas_message


# 计算该ctx相关模型的困难度
def get_ctxdata_analyse(db: Session, message_id: int, diff_level: float):
    # 确保他是ctx消息
    db_ctx = db.query(models_message.Message).filter(models_message.Message.message_id == message_id
                                                     , models_message.Message.reason_type != 0).first()
    if db_ctx is None:
        raise HTTPException(status_code=404, detail="不存在该ctx")
    if diff_level > 1 or diff_level < 0:
        raise HTTPException(status_code=404, detail="请输入正确的困难度参数")

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
    if reason_type == 0:
        raise HTTPException(status_code=404, detail="请输入正确的ctx类型")
    db_type = db.query(models_result.Hard).filter(models_result.Hard.reason_type == reason_type).all()
    if db_type is None:
        raise HTTPException(status_code=404, detail="不存在该ctx")
    if diff_level > 1 or diff_level < 0:
        raise HTTPException(status_code=404, detail="请输入正确的困难度参数")
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
    if diff_level > 1 or diff_level < 0:
        raise HTTPException(status_code=404, detail="请输入正确的困难度参数")
    db_results = db.query(models_result.Hard).filter(models_result.Hard.reason_type != 0).all()
    result = []

    for record in db_results:
        msg_id = record.message_id
        is_hard = record.total > 0 and (record.onenums / record.total) > diff_level
        found = False

        for item in result:
            if item['reason_type'] == record.reason_type and item['is_hard'] == is_hard:
                found = True
                item['msg_idx'].append(msg_id)
                break  # 找到对应的组，更新列表后可以退出循环

        if not found:
            result.append({
                'reason_type': record.reason_type,
                'is_hard': is_hard,
                'msg_idx': [msg_id]  # 新建列表并加入当前消息ID
            })

    return result
