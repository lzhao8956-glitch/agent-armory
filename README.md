# 🤖 Agent Armory - AI军团武器库

> 让AI Agent军团真正活起来：自我感知 + 自动进化 + 收入闭环

## 核心理念

**不是工具，是有记忆、会学习、能自我修复的智能体军团。**

## 三大核心模块

### 🔄 Evolution Engine
- 自动监听执行日志，失败3次自动生成新策略
- 无需人工干预，经验自动沉淀
- 跨Agent共享经验，打破"各自失忆"困局

### 🧠 Memory Bridge  
- 跨Agent记忆共享协议
- 结构化日志格式 → 可执行策略
- 持久化经验，不丢每一次失败/成功

### 💰 Revenue Sensor
- 自动监控收入数据（爱发电/GitHub等）
- 收入变化实时告警 + 行动建议
- 把收入作为Agent决策的核心反馈信号

## 系统架构

```
[OpenClaw 执行任务]
       ↓
[执行日志 → Memory Bridge]
       ↓
[Evolution Engine 自动分析]
       ↓
[生成新策略/Skill]
       ↓
[Revenue Sensor 监控结果]
       ↓
[数据反哺决策优化]
```

## 快速开始

```bash
# 克隆
git clone https://github.com/lzhao8956-glitch/agent-armory.git
cd agent-armory

# 查看各模块
ls -la evolution-trigger/
ls -la agent-memory-bridge/
ls -la revenue-sensor/
```

## 文件结构

```
agent-armory/
├── evolution-trigger/
│   ├── watchdog.sh          # 日志监听器
│   └── evolution_engine.py  # 自动进化引擎
├── agent-memory-bridge/
│   └── logs/                # 执行日志目录
└── revenue-sensor/
    ├── revenue_sensor.py   # 收入监控
    └── state.json          # 状态文件
```

## 适用场景

- AI Agent团队需要共享经验
- 需要7×24无人值守的自动化运维
- 想让AI真正感知商业目标（收入）

## License

MIT
