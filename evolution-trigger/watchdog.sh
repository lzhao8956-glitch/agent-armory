#!/bin/bash
# evolution-trigger watchdog - 监控执行日志，自动触发进化
# 放在OpenClaw端运行，持续监控
SHARED_DIR="/mnt/c/hermes-openclaw-shared/agent-memory-bridge"
LOG_DIR="$SHARED_DIR/logs"
ARCHIVE_DIR="$SHARED_DIR/archive"
PATTERN_DIR="$SHARED_DIR/patterns"
TRIGGER_FILE="$SHARED_DIR/.evolution_trigger"

mkdir -p "$LOG_DIR" "$ARCHIVE_DIR" "$PATTERN_DIR"

# 失败计数器
declare -A FAIL_COUNT
TRIGGER_THRESHOLD=3

# 监听新日志
inotifywait -m -e CREATE "$LOG_DIR" 2>/dev/null | while read path action file; do
    if [[ "$file" == *.json ]]; then
        LOG_PATH="$path$file"
        RESULT=$(cat "$LOG_PATH")
        
        # 提取关键信息
        TASK=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('task_type','unknown'))" 2>/dev/null)
        STATUS=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null)
        ERROR=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error_type',''))" 2>/dev/null)
        
        if [[ "$STATUS" == "failed" ]]; then
            KEY="${TASK}_${ERROR}"
            FAIL_COUNT[$KEY]=$(( ${FAIL_COUNT[$KEY]:-0} + 1 ))
            
            if [[ ${FAIL_COUNT[$KEY]} -ge $TRIGGER_THRESHOLD ]]; then
                echo "[EVOLUTION-TRIGGER] 检测到${TASK}任务失败${FAIL_COUNT[$KEY]}次，触发进化"
                echo "$KEY|${FAIL_COUNT[$KEY]}|$(date +%s)" >> "$TRIGGER_FILE"
                
                # 归档同类失败日志
                mv "$LOG_PATH" "$ARCHIVE_DIR/${file%.json}_$(date +%s).json"
                
                # 重置计数
                FAIL_COUNT[$KEY]=0
            fi
        fi
    fi
done
