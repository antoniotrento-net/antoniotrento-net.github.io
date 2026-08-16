---
layout: portfolio
title: "SP500 AI Bubble Monitor"
date: 2026-08-16
description: "Monitor di fragilità vs innesco per il mercato azionario USA in regime di bolla AI. Non predice il giorno del crollo: misura quanto è carica la molla (valutazioni, leva, concentrazione) e se lo scatto tipico — credito, Fed, utili Mag7 — è ancora spento."
image: "/assets/images/portfolio/sp500-ai-bubble-monitor/sp500-ai-bubble-index.jpg"
image-header: "/assets/images/portfolio/sp500-ai-bubble-monitor/sp500-ai-bubble-cover.jpg"
image-paint: "/assets/images/portfolio/sp500-ai-bubble-monitor/sp500-ai-bubble-cover.jpg"
tags: [Markets, S&P 500, AI Bubble, Python, FRED, Dashboard, Data Engineering, Risk, Fintech, Open Source]
---

> *"Non indovinare il giorno dello scoppio. Misura la molla e l'innesco come due assi distinti — perché una bolla tarda può restare in piedi a lungo, e un alert verde con Buffett a 219% è un difetto del modello, non un mercato safe."*

**SP500 AI Bubble Monitor** è un cruscotto read-only che traduce lo scenario *tarda bolla — molla carica, innesco spento* in score, banner e card. Nasce da un piano di scenario su dati pubblici (CAPE, indicatore di Buffett, equity delle famiglie, margin debt FINRA, pesi Mag7, HY OAS, curva, Fed, probabilità di recessione NY Fed) e da un vincolo operativo preciso: **la UI non scarica nulla**. L'engine fa fetch e scoring; la dashboard serve solo HTML e JSON da disco.

Il prodotto non è un predittore. È uno strumento per non confondere *valutazioni estreme* con *crollo imminente*, e per non leggere un aggregato fuorviante come segnale di calma.

Codice: **[github.com/antonio-backend-projects/SP500-ai-bubble-monitor](https://github.com/antonio-backend-projects/SP500-ai-bubble-monitor)**{: rel="nofollow" target="_blank"}

---

## Il problema

I dashboard di mercato mischiano tutto in un unico "rischio". In tarda bolla AI succede il contrario di ciò che quell'aggregato suggerisce:

1. **La molla è carica** — CAPE ~42, Buffett ~219%, famiglie con equity da record, margin debit FINRA nell'ordine del trilione, Mag7 che pesano ~30% dell'S&P.
2. **L'innesco è spento** — HY OAS sotto la soglia di stress (~271 bp vs 350 di compiacenza), curva non invertita, niente recessione conclamata.
3. **I proxy mentono se li medi male** — un CAPE Shiller fermo al 2023 e un margin FRED Z.1 (altra metodologia, ~$600B) azzerano lo score e producono un banner verde *RISCHIO CONTENUTO* mentre Buffett e household sono da fine-ciclo.

Serve un monitor che tenga gli assi separati, dichiari la qualità del dato (`as_of`, fonte, seed vs live) e non martelli Yahoo/FINRA da un IP residenziale.

---

## La soluzione: due assi, una pipeline fail-soft

### Fragilità (la molla)

CAPE, Buffett (CMV se FRED World Bank è stale), household equity, concentrazione Mag7, margin debt (FINRA mirror → Z.1 solo come fallback, con peso ridotto).

### Innesco (la scintilla)

HY OAS, curva 2s10s, probabilità di recessione NY Fed, path Fed, rischio utili AI (news + EPS NASDAQ + 8-K SEC).

### Prossimità

Mix pesato fragilità / innesco / news. Banner nel codice, non nel JSON: quorum tarda-bolla se due tra CAPE/Buffett/household sono estremi — così un pezzo proxy non dipinge il mercato di verde.

### Architettura

```
engine (CLI / cron)  →  data/cache/bubble_state.json  →  dashboard GET /api/state
```

- Engine Python: FRED API, Shiller/multpl, FINRA mirror, Slickcharts, NASDAQ, SEC, NY Fed, RSS
- UI vanilla HTML/CSS/JS (stile igedge) — **niente Streamlit**, niente fetch dal browser
- Cache 24h, rate limit 3–8s, Yahoo Mag7 **off**
- Produzione target: Raspberry Pi + Docker + cron + Cloudflare Tunnel (contratto documentato; compose ancora da implementare)

---

## Stack

| Pezzo | Tecnologia |
|-------|------------|
| Engine | Python 3, pandas, fail-soft per fonte |
| Macro | FRED API (`FRED_API_KEY`), fallback Treasury / H.15 / CMV |
| CAPE | Shiller XLS → **multpl** se stale/404 |
| Margin | FINRA HTML → CSV thetrading.tools → Z.1 |
| Mag7 | NASDAQ quote + earnings; Slickcharts pesi |
| UI | `web/dashboard.html` + `ThreadingHTTPServer` porta 8891 |
| Test | pytest offline |

Run di riferimento (2026-08-15): alert **TARDA BOLLA — INNESCO ANCORA SPENTO**, fragilità 77, innesco 23, prossimità 59. CAPE 42.6 (multpl), margin FINRA mirror $1.42T YoY +39%, HY 271 bp, SPX sui massimi mentre il campione titoli è in media ~−14% dai 52w.

---

## Competenze dimostrate

### Product thinking su rischio, non su previsioni
Separare fragilità e innesco è una scelta di modello, non un grafico in più. Il banner e il quorum esistono perché l'aggregato ingenuo *mente*.

### Ingestion anti-ban
Probe delle fonti, TTL, jitter, niente `fredgraph.csv`, niente Yahoo Mag7, niente scrape FINRA in loop. Lezione da produzione (stesso IP, stesso problema di altri progetti).

### Qualità del dato in UI
`data_quality`, badge fixture/seed/live, `cape_as_of`, `margin_source`. Un numero senza fonte non entra nel cruscotto come verità.

### Docs e identità
Documentazione tecnica in inglese (config, scoring, runbook, ops Pi). Marchio: sigillo teal con molla in negativo + lockup inverse.

---

## Perché questo progetto

Sta all'incrocio di tre cose che di solito non stanno insieme: **dati macro ufficiali**, **disciplina da ops** (cache, ban, fail-soft) e **un'idea di scenario** che si può leggere in tre secondi dal banner.

La domanda utile non è "quando scoppia". È: *la molla è già al livello 2000/2021? Lo scatto da credito o da Fed è acceso?* Oggi la risposta del monitor è: sì, e no.

---

> **Specifiche**
> - **Linguaggio**: Python 3
> - **UI**: HTML/CSS/JS + Chart.js, server read-only
> - **Fonti**: FRED, Shiller/multpl, FINRA mirror, NASDAQ, SEC, NY Fed, RSS
> - **Output**: `bubble_state.json` → http://localhost:8891
> - **Licenza**: MIT
> - **Repo**: [github.com/antonio-backend-projects/SP500-ai-bubble-monitor](https://github.com/antonio-backend-projects/SP500-ai-bubble-monitor)

---

💻 **Codice:** [github.com/antonio-backend-projects/SP500-ai-bubble-monitor](https://github.com/antonio-backend-projects/SP500-ai-bubble-monitor){: rel="nofollow" target="_blank"}

📩 **Monitor analoghi o dashboard di rischio su misura?** [Contattami](mailto:info@antoniotrento.net)
