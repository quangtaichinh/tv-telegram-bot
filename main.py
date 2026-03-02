import os
import json
import requests
from fastapi import FastAPI, Request

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True
    }
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()

@app.post("/tv")
async def tv(req: Request):
    raw = (await req.body()).decode("utf-8", errors="ignore").strip()
    print("=== RECEIVED /tv ===")
    print(raw)

    try:
        data = json.loads(raw)
        msg = f"""🚨 {data.get("action","ALERT")}
Symbol: {data.get("symbol","")}
TF: {data.get("timeframe","")}
Price: {data.get("price","")}
RSI: {data.get("rsi","")}
Power: {data.get("power","")}
VolRatio: {data.get("volRatio","")}
Note: {data.get("note","")}
"""
    except Exception as e:
        print("JSON parse error:", e)
        msg = "📣 TV Alert\n" + raw

    send_telegram(msg)
    return {"ok": True}

    # TradingView sẽ gửi JSON từ alert() trong Pine
    try:
        data = json.loads(raw)
        symbol = data.get("symbol", "UNKNOWN")
        tf = data.get("timeframe", "")
        action = data.get("action", "ALERT")
        price = data.get("price", "")
        rsi = data.get("rsi", "")
        power = data.get("power", "")
        volRatio = data.get("volRatio", "")

        msg = (
            f"📣 TV Signal\n"
            f"Symbol: {symbol}\n"
            f"TF: {tf}\n"
            f"Action: {action}\n"
            f"Price: {price}\n"
            f"RSI: {rsi}\n"
            f"Power: {power}\n"
            f"VolRatio: {volRatio}"
        )
    except Exception:
        msg = "📣 TV Alert\n" + raw

    send_telegram(msg)
    return {"ok": True}

