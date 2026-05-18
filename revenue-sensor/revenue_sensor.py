#!/usr/bin/env python3
"""
Revenue Sensor - 收入感知闭环
自动监控爱发电/GitHub/其他平台的收入数据
发现问题或机会时自动通知并建议行动
"""
import os
import time
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# ============ 配置 ============
IFDIAN_TOKEN = os.environ.get("IFDIAN_TOKEN", "TKM7RJtuNjPvmqwF5s94SkHr6VgU8XYa")
IFDIAN_API = "https://api.ifdian.net/api"

STATE_FILE = Path("/mnt/c/hermes-openclaw-shared/revenue-sensor/state.json")
ALERT_FILE = Path("/mnt/c/hermes-openclaw-shared/revenue-sensor/alerts.json")
HISTORY_FILE = Path("/mnt/c/hermes-openclaw-shared/revenue-sensor/history.json")

STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

# ============ 爱发电API ============
def get_ifdian_orders():
    """获取爱发电订单数据"""
    try:
        url = IFDIAN_API
        data = {
            "token": IFDIAN_TOKEN,
            "page": 1,
            "page_size": 20
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, headers=headers, json=data, timeout=10)
        if r.status_code == 200:
            resp = r.json()
            if resp.get("code") == 0:
                return resp.get("data", {}).get("list", [])
    except Exception as e:
        print(f"爱发电API错误: {e}")
    return []

def parse_ifdian_amount(orders):
    """解析订单金额"""
    total = 0.0
    new_orders = []
    for o in orders:
        amount = float(o.get("amount", 0)) / 100  # 爱发电单位是分
        if amount > 0:
            total += amount
            new_orders.append({
                "platform": "ifdian",
                "amount": amount,
                "time": o.get("create_time", ""),
                "user": o.get("user", {}).get("name", "匿名"),
                "product": o.get("product", {}).get("name", "未知商品")
            })
    return total, new_orders

# ============ 收入分析 ============
def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "last_check": None,
        "last_total": 0.0,
        "last_order_count": 0,
        "trend": "unknown",
        "alerts": []
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {"daily": [], "weekly": [], "monthly": []}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def analyze_trend(current_total, current_count, state):
    """分析收入趋势"""
    last_total = state.get("last_total", 0)
    last_count = state.get("last_order_count", 0)
    
    delta_amount = current_total - last_total
    delta_count = current_count - last_count
    
    if delta_amount > 0:
        trend = "up"
        trend_emoji = "📈"
    elif delta_amount < 0:
        trend = "down"
        trend_emoji = "📉"
    else:
        trend = "flat"
        trend_emoji = "➡️"
    
    return {
        "delta_amount": delta_amount,
        "delta_count": delta_count,
        "trend": trend,
        "emoji": trend_emoji
    }

def check_alerts(current_total, current_count, state):
    """检查是否需要告警"""
    alerts = []
    last_alerts = state.get("alerts", [])
    
    # 新订单通知
    last_count = state.get("last_order_count", 0)
    if current_count > last_count and last_count > 0:
        new_orders = current_count - last_count
        alerts.append({
            "type": "new_order",
            "level": "success",
            "message": f"🎉 新订单！+{new_orders}单，当前总收入: ¥{current_total:.2f}",
            "time": datetime.now().isoformat()
        })
    
    # 收入异常（突然下降50%以上）
    last_total = state.get("last_total", 0)
    if last_total > 100 and current_total < last_total * 0.5:
        alerts.append({
            "type": "revenue_drop",
            "level": "warning",
            "message": f"⚠️ 收入异常下降！从 ¥{last_total:.2f} 跌至 ¥{current_total:.2f}",
            "time": datetime.now().isoformat()
        })
    
    # 连续3天无收入
    history = load_history()
    daily = history.get("daily", [])
    if len(daily) >= 3:
        recent = daily[-3:]
        if all(d.get("amount", 0) == 0 for d in recent):
            alerts.append({
                "type": "no_revenue_3days",
                "level": "warning",
                "message": "⚠️ 连续3天无收入！需要调整推广策略",
                "time": datetime.now().isoformat()
            })
    
    return alerts

def generate_recommendations(trend_data, state):
    """基于趋势生成行动建议"""
    recommendations = []
    
    if trend_data["trend"] == "up":
        recommendations.append("收入在涨，保持当前策略")
        recommendations.append("考虑增加推广力度，趁热打铁")
    elif trend_data["trend"] == "down":
        recommendations.append("⚠️ 收入下滑，立即分析原因")
        recommendations.append("检查：商品价格、平台曝光、竞品动态")
        recommendations.append("行动：优化商品描述、发布新动态、考虑促销")
    else:
        recommendations.append("收入平稳，可以测试新推广方式")
    
    # 检查历史数据
    history = load_history()
    daily = history.get("daily", [])
    if daily:
        recent_7 = daily[-7:] if len(daily) >= 7 else daily
        avg = sum(d.get("amount", 0) for d in recent_7) / len(recent_7)
        recommendations.append(f"近7天日均收入: ¥{avg:.2f}")
    
    return recommendations

# ============ 主流程 ============
def main():
    print(f"\n[Revenue Sensor] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 加载状态
    state = load_state()
    
    # 获取收入数据
    orders = get_ifdian_orders()
    total_amount, parsed_orders = parse_ifdian_amount(orders)
    order_count = len(parsed_orders)
    
    print(f"爱发电订单: {order_count}单，总收入: ¥{total_amount:.2f}")
    
    # 分析趋势
    trend = analyze_trend(total_amount, order_count, state)
    print(f"趋势: {trend['emoji']} {trend['trend']} (金额变化: ¥{trend['delta_amount']:+.2f}, 订单变化: {trend['delta_count']:+.0f})")
    
    # 检查告警
    alerts = check_alerts(total_amount, order_count, state)
    for alert in alerts:
        print(f"\n🚨 [{alert['level'].upper()}] {alert['message']}")
    
    # 生成建议
    print("\n📋 行动建议:")
    recommendations = generate_recommendations(trend, state)
    for rec in recommendations:
        print(f"  • {rec}")
    
    # 更新状态
    new_state = {
        "last_check": datetime.now().isoformat(),
        "last_total": total_amount,
        "last_order_count": order_count,
        "trend": trend["trend"],
        "alerts": alerts
    }
    save_state(new_state)
    
    # 更新历史
    history = load_history()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 日历史
    daily = history.get("daily", [])
    today_entry = {"date": today, "amount": total_amount, "orders": order_count}
    
    # 如果今天已有记录则更新，否则追加
    today_exists = False
    for d in daily:
        if d.get("date") == today:
            d.update(today_entry)
            today_exists = True
            break
    if not today_exists:
        daily.append(today_entry)
    
    # 保留30天
    if len(daily) > 30:
        daily = daily[-30:]
    
    history["daily"] = daily
    save_history(history)
    
    print(f"\n[Revenue Sensor] 完成，下次检查请重新运行或设置定时任务")
    print("=" * 50)
    
    return {
        "total": total_amount,
        "orders": order_count,
        "trend": trend,
        "alerts": alerts,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    result = main()
