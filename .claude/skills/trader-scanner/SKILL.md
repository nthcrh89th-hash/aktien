---
name: trader-scanner
description: Scannt Aktien-Charts nach Setups (Trend, Breakout, RSI, Volumen, ATR). Nutzen bei "Scanne Charts", "Setups für TICKER", "trader-scanner".
---

# trader-scanner

1. Ticker aus der Anfrage übernehmen (z. B. IREN, IONQ).
2. `python3 .claude/skills/trader-scanner/scan.py TICKER [TICKER...]` ausführen (Daten: Yahoo Finance, 1 Jahr Tageskerzen).
3. Ergebnis pro Ticker knapp zusammenfassen: Trend, Signale, Schlüsselniveaus (20T-Hoch/Tief, SMAs), Stop-Orientierung (2x ATR).
4. Bewertung: Setup vorhanden / abwarten / kein Setup, mit kurzer Begründung.

Regeln: Nur Analyse. Keine Orders senden. Kein Anlagerat, auf Unsicherheit hinweisen. Bei Datenfehlern das offen sagen, nichts erfinden.
