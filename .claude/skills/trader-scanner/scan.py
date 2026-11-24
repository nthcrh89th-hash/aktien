#!/usr/bin/env python3
"""Chart-Scanner: python3 scan.py IREN IONQ  (Daten: Yahoo Finance, nur Analyse, keine Orders)"""
import json, sys, urllib.request

def fetch(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1y&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    rows = [(c, h, l, v) for c, h, l, v in zip(q["close"], q["high"], q["low"], q["volume"]) if c is not None]
    return [x[0] for x in rows], [x[1] for x in rows], [x[2] for x in rows], [x[3] for x in rows]

def sma(a, n): return sum(a[-n:]) / n

def rsi(c, n=14):
    g = l = 0.0
    for i in range(-n, 0):
        d = c[i] - c[i - 1]
        g += max(d, 0); l += max(-d, 0)
    return 100.0 if l == 0 else 100 - 100 / (1 + g / l)

def atr(c, h, lo, n=14):
    tr = [max(h[i] - lo[i], abs(h[i] - c[i - 1]), abs(lo[i] - c[i - 1])) for i in range(-n, 0)]
    return sum(tr) / n

def scan(sym):
    c, h, lo, v = fetch(sym)
    p = c[-1]; s20, s50 = sma(c, 20), sma(c, 50)
    s200 = sma(c, 200) if len(c) >= 200 else None
    hi20, lo20 = max(h[-21:-1]), min(lo[-21:-1])
    hi52, lo52 = max(h), min(lo)
    vr = v[-1] / sma(v, 20)
    a = atr(c, h, lo)
    sig = []
    trend = "Aufwärtstrend" if p > s20 > s50 else "Abwärtstrend" if p < s20 < s50 else "Seitwärts/gemischt"
    if p > hi20: sig.append("Breakout über 20-Tage-Hoch")
    if p < lo20: sig.append("Breakdown unter 20-Tage-Tief")
    if vr > 1.5: sig.append(f"Volumen {vr:.1f}x Durchschnitt")
    r = rsi(c)
    if r > 70: sig.append("RSI überkauft")
    if r < 30: sig.append("RSI überverkauft")
    if p >= 0.95 * hi52: sig.append("nahe 52W-Hoch")
    print(f"\n== {sym} ==  Kurs {p:.2f}  ({(p/c[-2]-1)*100:+.1f}% heute)")
    print(f"Trend: {trend} | SMA20 {s20:.2f} SMA50 {s50:.2f}" + (f" SMA200 {s200:.2f}" if s200 else ""))
    print(f"RSI14 {r:.0f} | ATR14 {a:.2f} ({a/p*100:.1f}%) | 52W {lo52:.2f}-{hi52:.2f}")
    print(f"20T-Range {lo20:.2f}-{hi20:.2f} | Vol-Ratio {vr:.1f}x")
    print("Signale: " + (", ".join(sig) or "keine"))
    print(f"Orientierung: Stop ~{p-2*a:.2f} (2xATR) unter Kurs")

for s in sys.argv[1:] or ["SPY"]:
    try: scan(s.upper())
    except Exception as e: print(f"{s}: Fehler {e}")
