import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()
app=FastAPI(title="TradeScope API")
KEY=os.getenv("TWELVE_DATA_API_KEY")

@app.get("/api/health")
def health():
    return {"ok": True, "api_key_configured": bool(KEY)}

@app.get("/api/price")
async def price(symbol: str="XAU/USD"):
    if not KEY:
        raise HTTPException(500,"TWELVE_DATA_API_KEY is not configured")
    async with httpx.AsyncClient(timeout=15) as c:
        r=await c.get("https://api.twelvedata.com/price",params={"symbol":symbol,"apikey":KEY})
        data=r.json()
    if "price" not in data:
        raise HTTPException(502, data.get("message","Market data unavailable"))
    return {"symbol":symbol,"price":float(data["price"])}

@app.get("/",response_class=HTMLResponse)
def home():
    return """<!doctype html><html lang='ar' dir='rtl'><meta charset='utf-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>TradeScope</title><style>body{font-family:Tahoma;background:#07111f;color:#eef5fb;
    max-width:800px;margin:50px auto;padding:20px}.c{background:#0d1a2a;border:1px solid #29405b;
    padding:22px;border-radius:18px}button{padding:12px 18px;border:0;border-radius:10px;background:#3bdda0;
    cursor:pointer;font-weight:bold}#x{margin-top:18px;font-size:24px}.m{color:#9fb2c8}</style>
    <div class='c'><h1>TradeScope</h1><p class='m'>اختبار الاتصال الحقيقي بمصدر الأسعار.</p>
    <button id='b'>اختبر سعر الذهب XAU/USD</button><div id='x'>بانتظار الاختبار</div></div>
    <script>b.onclick=async()=>{x.textContent='جاري الاتصال...';try{let r=await fetch('/api/price?symbol=XAU%2FUSD');
    let d=await r.json();x.textContent=r.ok?`${d.symbol}: ${d.price}`:`خطأ: ${d.detail}`}
    catch(e){x.textContent='تعذر الاتصال بالخادم'}}</script></html>"""
