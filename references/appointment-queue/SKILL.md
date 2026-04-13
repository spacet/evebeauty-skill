---
name: appointment-queue
description: 伊芙丽格在线预约面诊 Skill。支持查询可约时段、预约面诊、查询预约信息、取消预约。
version: 0.1.0
---

# 伊芙丽格 · 在线预约面诊

## 前置条件

- 用户需完成身份验证（首次使用会引导）
- 预约为真实业务操作，确认和取消前需跟用户确认

## 命令说明

| 命令 | 说明 | 输入参数 |
|------|------|----------|
| `available_slots` | 查询可预约的时段 | `date_range`（可选，默认最近7天） |
| `book_appointment` | 预约面诊 | `date`, `time_slot`, `consultation_type`（咨询项目/皮肤问题） |
| `appointment_detail` | 查询预约信息 | `appointment_id`（可选，不指定则返回所有预约） |
| `appointment_cancel` | 取消预约 | `appointment_id` |

## 使用流程

### 1. 查询可约时段

```
用户：最近什么时候能约？
AI：调用 available_slots，返回可约时段
```

### 2. 预约面诊

```
用户：帮我约周三下午面诊
AI：确认诉求（咨询什么项目/皮肤问题）
AI：调用 book_appointment，返回预约确认
```

### 3. 查询预约

```
用户：我的预约是什么时候？
AI：调用 appointment_detail，返回预约信息
```

### 4. 取消预约

```
用户：取消预约
AI：确认是否取消
AI：调用 appointment_cancel，返回取消结果
```

## 注意事项

- 预约成功后，系统会发送确认短信到用户手机
- 如需改期，请先取消现有预约再重新预约
- 如有问题，可拨打客服热线 18513997487
