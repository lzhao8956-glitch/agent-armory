#!/bin/bash
# Agent Armory 启动脚本
# 在OpenClaw端运行

AGENT_DIR="/mnt/c/hermes-openclaw-shared"

echo "🤖 Agent Armory 启动中..."

# 检查目录
if [[ ! -d "$AGENT_DIR/evolution-trigger" ]]; then
    echo "❌ 目录不存在，请先克隆仓库"
    exit 1
fi

# 显示状态
echo "📁 Evolution Trigger: $(ls $AGENT_DIR/evolution-trigger/*.py 2>/dev/null | wc -l) 文件"
echo "📁 Agent Memory Bridge: $(ls $AGENT_DIR/agent-memory-bridge/logs/ 2>/dev/null | wc -l) 日志"
echo "📁 Revenue Sensor: $(ls $AGENT_DIR/revenue-sensor/*.py 2>/dev/null | wc -l) 文件"

# 运行 evolution engine
python3 $AGENT_DIR/evolution-trigger/evolution_engine.py

echo "🚀 Agent Armory 已就绪"
echo "💰 运行 revenue_sensor.py 检查收入"
