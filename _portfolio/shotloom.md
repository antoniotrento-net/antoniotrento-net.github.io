---
layout: portfolio
title: "Shotloom – Montaggio Multicam AI Locale"
date: 2026-08-06
description: "Drop in 2–4 clip multicam: sync, rough cut AI, sottotitoli ed export multi-piattaforma sul tuo PC via Docker. Dashboard Shotloom; in roadmap app Electron e taglio documentaristico con voce fuori campo."
image: "/assets/images/portfolio/shotloom/shotloom-cover.jpg"
image-header: "/assets/images/portfolio/shotloom/shotloom-cover.jpg"
image-paint: "/assets/images/portfolio/shotloom/shotloom-cover.jpg"
tags: [AI, Video, Multicam, Docker, FastAPI, Python, NLE, Captions, On-Premise, Electron]
---

> *"Hai già girato l'episodio. Quello che manca è sync, montaggio, caption ed export — senza caricare i rushes su un NLE cloud. Shotloom gira in locale: bootstrap Docker, dashboard, 2–4 camere in input."*

**Shotloom** è un **NLE locale guidato dall'AI** per footage multicam: podcast, eventi, interviste, workshop. Il flusso primario è automatico — *analizza e monta* — poi raffini ritmo, stile sottotitoli e parametri nella dashboard. Nessun upload obbligatorio: la pipeline resta sulla macchina (o sul VPS che controlli tu).

Il nome è intenzionale: **shot** (inquadrature) + **loom** (telaio). Più camere entrano; ne esce un solo montaggio utilizzabile.

---

## Stato attuale (cosa c'è già)

Il prodotto è in **early access** su GitHub. Oggi puoi già:

| Area | Cosa fa |
|---|---|
| **Bootstrap** | Script Docker: API + worker + dashboard su `http://127.0.0.1:8765` |
| **Ingest multicam** | Drop di 2–4 clip camera (MP4 e formati tipici da ripresa) |
| **Sync + rough cut** | Allineamento e montaggio AI verso un cut utilizzabile |
| **Caption** | Sottotitoli con stile configurabile in dashboard |
| **Export multi-piattaforma** | Profili YouTube, TikTok, Instagram, Facebook |
| **Privacy** | Elaborazione locale; niente bolletta cloud di montaggio |
| **Sito** | Landing bilingue EN/IT su [shotloom.github.io](https://shotloom.github.io){: rel="nofollow" target="_blank"} |

La **stella polare** del prodotto: *clip multicam in → Shotloom fa tutto → se sei precisino, raffini nella dashboard*. Un solo frontend (`apps/web`): niente canvas NLE da imparare per il percorso primario.

### Dashboard (refine)

Tab di raffinamento (grade, effetti, transizioni, mask) sono presenti in UI come layer di preview; il cablaggio completo su export è lavoro tracciato a parte. Il montaggio automatico resta il percorso veloce.

---

## Il problema

### 1. Il footage c'è, il tempo no
Chi gira multicam ogni settimana (podcast, eventi, lezioni) passa ore a sync manuale, switch camere e export per ogni piattaforma.

### 2. I cloud NLE costano privacy e abbonamento
Caricare rushes non pubblicati o riprese clienti su servizi terzi non è sempre accettabile. CapCut/Descript risolvono la velocità; non risolvono il vincolo *i file restano qui*.

### 3. Un NLE tradizionale è troppo lento per il rough cut
Premiere e DaVinci restano ottimi per il finish. Shotloom punta al tratto precedente: da rushes a cut esportabile **prima di pranzo**.

---

## Come funziona (oggi)

1. **Bootstrap** — Docker + script una volta; apri la dashboard in browser  
2. **Drop** — 2–4 clip camera nel progetto  
3. **Analizza e monta** — sync, rough cut, caption  
4. **Affina** — ritmo, stile sottotitoli, profili piattaforma  
5. **Export** — master e verticali pronti

---

## Roadmap in evidenza

Due evolutive già (o appena) sul tracker GitHub:

### 1. App desktop Electron (post-v1)
Stesso pattern retail di Qwibo: installer one-shot (Windows in primis, poi macOS/Linux), backend embedded, niente Docker obbligatorio per l'utente finale. Tracciata come **[#51](https://github.com/Shotloom/Shotloom/issues/51)**{: rel="nofollow" target="_blank"}.

### 2. Taglio documentaristico AI (multi-video + voce fuori campo)
Oltre al multicam sync “podcast/evento”: ingest di **tanti clip di ripresa** + traccia **voce fuori campo**, con AI che propone un **taglio narrativo** documentaristico (selezione e ordine riprese guidati dal VO e dal ritmo). Tracciata come **[#52](https://github.com/Shotloom/Shotloom/issues/52)**{: rel="nofollow" target="_blank"}.

Altre linee aperte: export FCPXML/ZIP verso Premiere/DaVinci, burn-in sottotitoli brand-aware, refine cablato su export, UX timeline Creator.

---

## Stack tecnologico

| Componente | Tecnologia | Ruolo |
|---|---|---|
| **API / worker** | Python · FastAPI · Docker Compose | Pipeline sync, montaggio, export |
| **Dashboard** | Frontend `apps/web` servito dall'API | Flusso primario + refine |
| **Media** | ffmpeg / toolchain locale | Proxy, cut, export |
| **Deploy** | Docker (dev e VPS) | Bind locale `127.0.0.1:8765` |
| **Docs / site** | Jekyll (shotloom.github.io) · MkDocs in evoluzione | Landing + documentazione |
| **Roadmap desktop** | Electron (pattern Qwibo) | Installer retail post-v1 |

### Architettura (vista semplice)

```
┌─────────────────────────────────────────────────────────────┐
│  Shotloom (oggi: Docker)                                     │
│                                                              │
│  Clip cam A/B/C/D ──► API + worker ──► rough cut + captions  │
│         │                      │                             │
│         │                      └──► export YT / TikTok / …   │
│         └── dashboard (browser)                              │
│                                                              │
│  Roadmap: Electron shell · modalità documentario + VO        │
└─────────────────────────────────────────────────────────────┘
```

---

## Competenze dimostrate

### Product / AI video
Tradurre un bisogno creativo (multicam → cut pubblicabile) in un flusso automatico con privacy locale, non in un clone CapCut cloud.

### Architettura full-stack
API, worker, artifact, dashboard unica; stella polare chiara (ADR: un frontend Shotloom, niente studio OpenCut parallelo).

### Packaging e go-to-market
Percorso Docker per early access; roadmap Electron ispirata a Qwibo per l'utente non tecnico.

### Brand e presence
Identità visiva (coral → magenta), logo mark “tre camere → timeline”, sito portfolio e landing pubbliche.

---

## Licenza

Termini di licenza **in definizione** (early access su GitHub). Nessuna bolletta cloud di montaggio: il costo è disco, GPU/CPU e tempo sul tuo hardware.

---

## Perché questo progetto

Dopo Qwibo (trascrizione locale retail), Shotloom affronta il pezzo successivo della catena creativa: **dal rushes al cut**, ancora on-device. La sfida non è solo “montare con AI”, è farlo su footage reale multicam, con export multi-piattaforma e un percorso che un creator possa usare ogni settimana senza diventare un colorist.

---

> **Specifiche tecniche (snapshot)**
> - **Runtime attuale**: Docker Compose · API FastAPI · dashboard web
> - **Input**: 2–4 clip multicam tipici
> - **Output**: rough cut, caption, export piattaforma
> - **Privacy**: elaborazione locale / self-hosted
> - **Roadmap**: Electron [#51](https://github.com/Shotloom/Shotloom/issues/51) · documentario multi-video + VO [#52](https://github.com/Shotloom/Shotloom/issues/52) · export NLE
> - **Sito**: [shotloom.github.io](https://shotloom.github.io)

---

🌐 **Sito ufficiale:** [shotloom.github.io](https://shotloom.github.io){: rel="nofollow" target="_blank"}

💻 **Codice sorgente:** [github.com/Shotloom/Shotloom](https://github.com/Shotloom/Shotloom){: rel="nofollow" target="_blank"}

📩 **Vuoi montare i tuoi multicam in locale?** [Contattami](mailto:info@antoniotrento.net)
