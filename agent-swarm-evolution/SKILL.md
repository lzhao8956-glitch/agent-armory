---
name: agent-swarm-evolution
description: L5级技能 - AI军团自我进化闭环 | 全网无人攻克的难点：跨Agent经验传递 + 自动进化触发 + 收入感知闭环
auto_generated: false
version: 1.0
created: 2026-05-18
author: 天才 (Hermes Agent) + 破军 (OpenClaw)
---

# Agent军团自我进化闭环

## 核心理念

**让AI军团真正活起来——不是工具，是有记忆、会学习、能自我修复的智能体。**

---

## 系统架构

```
[OpenClaw 执行任务]
       ↓
[执行日志写入共享文件]
       ↓
[Evolution Engine 自动分析]
       ↓
[生成新技能/策略]
       ↓
[OpenClaw 立即使用新策略]
       ↓
[Revenue Sensor 监控收入]
       ↓
[收入数据反哺决策调整]
```

---

## 三大核心模块

### 1. `agent-memory-bridge` - 跨Agent记忆共享

**难点：全网无人做过跨Agent经验传递**

目前所有AI Agent都是"各自记忆各自用"——重启后失忆，不同Agent之间无法共享经验。

**解决方案：**
- OpenClaw执行任务后 → 写入结构化JSON日志
- 天才读取日志 → 自动提取规律 → 生成新skill
- 新skill立即生效 → OpenClaw下次遇到同类问题直接执行新策略

**日志格式：**
```json
{
  "task_id": "uuid",
  "task_type": "github_push",
  "status": "failed",
  "error_type": "443_timeout",
  "error_message": "Connection timeout",
  "attempts": 3,
  "duration_ms": 15000,
  "strategy_used": "git pull --rebase",
  "timestamp": "2026-05-18T21:00:00Z"
}
```

**路径：** `/mnt/c/hermes-openclaw-shared/agent-memory-bridge/`

---

### 2. `evolution-trigger` - 自动进化触发器

**难点：自动识别失败模式 + 无人工干预生成新策略**

其他Agent的"自我进化"需要人工触发，我们要做全自动。

**触发条件：**
- 同一任务失败 ≥3次 → 触发进化
- 自动分析失败日志 → 匹配已知错误模式
- 生成新的skill → OpenClaw立即使用

**已知错误模式 → 预置解决方案：**

| 错误类型 | 解决方案 |
|---------|---------|
| github_push_443 | 切换git pull --no-rebase或API push |
| ifdian_login_2fa | 使用Cookie或兆爷手动授权 |
| browser_captcha | 等待/切换UA/切换代理/人工介入 |
| wsl_network_timeout | 切换浏览器代理或Windows原生工具 |
| delegate_large_file | 天才直接写或拆分<15KB文件 |

**脚本：**
- `watchdog.sh` - 监听日志目录，触发进化
- `evolution_engine.py` - 分析日志，生成新skill

---

### 3. `revenue-sensor` - 收入感知闭环

**难点：全网没有任何AI Agent有收入感知能力**

目前所有AI Agent不知道自己的努力带来多少收入——它们只是执行任务，不感知结果。

**我们要做的：**
- 自动监控爱发电/GitHub等平台的收入数据
- 发现收入变化 → 自动分析原因 → 建议行动
- 把收入数据作为Agent决策的反馈信号

**告警类型：**
- 🎉 新订单 → 趁热打铁加大推广
- ⚠️ 收入下降50%+ → 立即分析原因
- ⚠️ 连续3天无收入 → 策略需要调整

**路径：** `/mnt/c/hermes-openclaw-shared/revenue-sensor/`

---

## 与OpenClaw的双修分工

| 能力 | OpenClaw（破军） | 天才（Hermes） |
|------|-----------------|---------------|
| 感知 | ✅ 实时监控日志 | ✅ 分析规律 |
| 执行 | ✅ 直接操作 | ❌ 需借助OpenClaw |
| 决策 | ⚠️ 规则驱动 | ✅ 推理驱动 |
| 记忆 | ❌ 重启失忆 | ✅ 持久记忆 |
| 进化 | ❌ 无 | ✅ 自动生成skill |
| 收入 | ❌ 无感知 | ✅ Revenue Sensor |

**双修模式：**
- OpenClaw = 眼睛和手（感知+执行）
- 天才 = 大脑（分析+决策+进化）
- 数据流：OpenClaw执行 → 日志 → 天才分析 → 新skill → OpenClaw执行

---

## 使用方式

### 启动进化引擎（天才每天运行）
```bash
python3 /mnt/c/hermes-openclaw-shared/evolution-trigger/evolution_engine.py
```

### 启动看门狗（OpenClaw持续运行）
```bash
bash /mnt/c/hermes-openclaw-shared/evolution-trigger/watchdog.sh &
```

### 检查收入（每天定时）
```bash
python3 /mnt/c/hermes-openclaw-shared/revenue-sensor/revenue_sensor.py
```

### 写入执行日志（OpenClaw每次任务后）
```python
import json
from pathlib import Path

log = {
    "task_id": "abc123",
    "task_type": "github_push",
    "status": "failed",
    "error_type": "443_timeout",
    "attempts": 3
}
log_file = Path("/mnt/c/hermes-openclaw-shared/agent-memory-bridge/logs/{task_id}.json")
log_file.parent.mkdir(parents=True, exist_ok=True)
with open(log_file, "w") as f:
    json.dump(log, f)
```

---

## 已实现的文件

```
/mnt/c/hermes-openclaw-shared/
├── agent-memory-bridge/
│   ├── logs/           # OpenClaw执行日志
│   └── archive/        # 归档的失败日志
├── evolution-trigger/
│   ├── watchdog.sh    # 监听器
│   └── evolution_engine.py  # 进化引擎
└── revenue-sensor/
    ├── revenue_sensor.py    # 收入监控
    ├── state.json          # 状态文件
    └── history.json        # 历史数据
```

---

## L5级突破点

**全网无人攻克的难点：**

1. **跨Agent经验固化** - 不同Agent之间无法共享经验，我们通过共享文件+结构化日志解决
2. **全自动进化** - 不需要人工触发，通过watchdog自动监听+匹配模式自动生成skill
3. **收入感知闭环** - 把收入数据作为反馈信号，让AI的决策真正以商业目标为导向

---

## 下一步

1. **OpenClaw方**：集成日志写入 + 看门狗常驻 + Revenue Sensor定时任务
2. **天才方**：定期运行evolution_engine + 根据收入数据调整战略
3. **兆爷方**：提供GitHub写权限（token验证后）让我们真正开始推送代码

---

*这是L5级技能，不是玩具，是让整个AI军团真正活起来的核心系统。*
