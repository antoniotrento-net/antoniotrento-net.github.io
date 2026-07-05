---
layout: portfolio
title: "Qwibo – Trascrizione Audio e Video Offline per Windows"
date: 2026-07-04
description: "App desktop Windows per trascrivere riunioni, podcast, interviste e lezioni in testo e sottotitoli SRT sul proprio PC. Installer Electron retail, ASR NeMo Parakeet, riassunti LLM opzionali. Privato, gratuito per uso personale."
image: "/assets/images/portfolio/qwibo/qwibo-cover.jpg"
image-header: "/assets/images/portfolio/qwibo/qwibo-cover.jpg"
image-paint: "/assets/images/portfolio/qwibo/qwibo-cover.jpg"
tags: [AI, Python, Electron, NeMo, ASR, Speech-to-Text, Desktop, LLM, On-Premise, Windows, FastAPI]
---

> *"Qwibo nasce da un'esigenza semplice: hai una registrazione e vuoi il testo senza caricarla su un servizio cloud né pagare al minuto. Scarichi l'installer, fai il setup una volta, e trascrizione e sottotitoli restano sul tuo PC."*

**Qwibo** è un'**app desktop Windows** per la trascrizione automatica di audio e video in italiano, progettata per l'utente finale: niente Python da installare, niente terminale, niente Docker. Trasforma riunioni, podcast, interviste e lezioni in testo cercabile e sottotitoli SRT, con riassunti LLM opzionali — senza upload obbligatori, senza abbonamenti, senza costi al minuto.

Il progetto nasce da un'esigenza concreta e diffusa: chiunque lavori con l'audio — consulenti che vivono di call, creator che pubblicano ogni settimana, giornalisti che devono citare con precisione, studenti che ripassano da lezioni lunghe — si scontra con lo stesso collo di bottiglia. La registrazione ce l'hai già; quello che manca è il testo, e il tempo per ricavarlo a mano.

Le soluzioni cloud esistono (Otter, servizi a pagamento al minuto, trascrizione delle piattaforme di videoconferenza), ma condividono due limiti fondamentali: **costano in proporzione ai minuti** e **richiedono di caricare i file su server di terzi**. Per chi tratta call con clienti, interviste non pubblicate o contenuti riservati, questo secondo punto non è un dettaglio: è un vincolo di privacy che spesso rende quelle soluzioni semplicemente non utilizzabili.

Qwibo risolve il problema alla radice: **la trascrizione gira sul tuo PC**, i file restano tuoi dall'inizio alla fine, e per uso personale è gratuito.

---

## Il Prodotto: App Desktop Electron (retail)

La **punta di diamante** del progetto è l'installer Windows `Qwibo-Setup-*.exe`:

1. **Doppio click** → installazione guidata → l'app si apre
2. **Setup iniziale** (~4–5 GB, una sola volta): modello vocale Parakeet + opzionale Qwen locale se RAM ≥ 16 GB
3. **Uso quotidiano**: carica file, attendi, scarica trascrizione e SRT

L'utente non vede Python, ffmpeg o configurazioni di rete. Electron avvia un backend Python **embedded** in background; l'interfaccia è la stessa pipeline FastAPI + HTMX già collaudata in sviluppo, ma incapsulata in una finestra desktop con tray icon e log diagnostici.

### Cosa include l'installer

| Componente | Dettaglio |
|---|---|
| **Runtime** | Python standalone + venv con torch, NeMo, FastAPI |
| **Media** | ffmpeg statico bundled |
| **Backend** | Codice `qwibo` sincronizzato in `backend/vendor/` |
| **UI** | Electron + finestra nativa, backend su `127.0.0.1` |
| **Dati utente** | `%APPDATA%\qwibo-desktop\` (modelli, job, log) |

### Sfide tecniche affrontate (Electron)

- **Runtime relocatable** su hardware consumer senza AVX (mini PC, CPU baseline)
- **llama-cpp-python** compilato MinGW baseline per evitare crash `0xC000001D` su CPU senza AVX
- **Cache scrivibili** (numba, matplotlib) — Program Files è read-only su Windows
- **Worker separato** dal processo web: NeMo non gira dentro uvicorn
- **Wizard modelli** al primo avvio, senza download durante la prima trascrizione
- **NSIS installer** ~2–3 GB (normale per ASR locale offline)

---

## Il Problema: Perché Trascrivere Bene l'Italiano È Difficile

### 1. Il parlato reale non è pulito
Le riunioni hanno voci sovrapposte, interruzioni, ritmo informale, microfoni mediocri e rumore di fondo. Serve un modello robusto al parlato spontaneo.

### 2. L'italiano è cittadino di seconda classe
La maggior parte dei modelli ASR ottimizza sull'inglese. Qwibo adotta **NeMo Parakeet TDT 0.6B v3** con forte focus sul parlato italiano.

### 3. I file lunghi non devono bloccare la giornata
L'elaborazione procede in background: carichi, chiudi la finestra (l'app resta in tray), torni quando il risultato è pronto.

### 4. Privacy come requisito, non come opzione
La trascrizione locale non è un'ottimizzazione: è la precondizione all'adozione per contenuti sensibili.

---

## La Soluzione: Come Funziona

### Step 1 — Installazione e setup
Scarica l'installer, completa il wizard modelli (una volta). Nessun account obbligatorio per il primo risultato.

### Step 2 — Upload
Trascina un file (MP4, MKV, WAV, MP3, …) nell'app. Nessuna conversione manuale.

### Step 3 — Trascrizione (in background)
Parakeet elabora in locale. Job asincrono con progresso live nella pagina dettaglio.

### Step 4 — Download
Testo completo + sottotitoli SRT. Opzionale: riassunto LLM (cloud o Qwen locale).

---

## Stack Tecnologico

| Componente | Tecnologia | Ruolo |
|---|---|---|
| **Desktop shell** | Electron 33 + NSIS | Installer retail, tray, avvio backend |
| **ASR** | NVIDIA NeMo Parakeet (TDT 0.6B v3) | Trascrizione speech-to-text in italiano |
| **Web UI** | FastAPI + HTMX | Upload, coda job, download risultati |
| **Riassunti LLM** | DeepSeek · OpenAI · Claude · Gemini · Kimi · Qwen locale | Sintesi opt-in |
| **Media** | ffmpeg (bundled) | Estrazione e normalizzazione audio |
| **CLI** | `qwibo` (Python, dev/Docker) | Automazione e self-hosted |
| **Self-hosted** | Docker (`qwibo-docker`) | Deploy su mini PC / NAS Linux |

### Architettura desktop

```
┌─────────────────────────────────────────────────────────────┐
│  Qwibo Desktop (Electron)                                    │
│                                                              │
│  Installer ──► Electron ──► Python embedded (entrypoint)     │
│                    │              │                          │
│                    │              ├── uvicorn (FastAPI UI)   │
│                    │              └── worker (NeMo ASR)      │
│                    │                                         │
│                    └── %APPDATA%\qwibo-desktop\              │
│                         models · data · logs                 │
└─────────────────────────────────────────────────────────────┘
```

- **Coda job:** stati tracciati (`queued`, `running`, `completed`, `failed`)
- **Worker in background:** elaborazione non blocca l'interfaccia
- **Storico consultabile:** lista job e pagina dettaglio per singolo file
- **Output multipli:** TXT, SRT, riassunto opzionale

---

## Competenze Dimostrate

### Product Engineering (retail desktop)
Portare una pipeline AI da prototipo Python/Docker a **installer Windows one-click** per utenti non tecnici. Packaging di runtime pesante (torch, NeMo), gestione modelli al primo avvio, UX tray + log diagnostici.

### AI Engineering / ASR
Integrazione NeMo Parakeet in pipeline locale, qualità sul parlato italiano reale, file lunghi con chunking. LLM multi-provider per sintesi (cloud + Qwen locale CPU).

### Architettura Software
Pipeline a job asincroni con stati deterministici, worker subprocess separato dalla UI, disaccoppiamento ingestion / elaborazione / output.

### DevOps e Packaging
Build installer con `electron-builder`, runtime verification (no AVX), sync backend vendor, repo separati (`qwibo`, `qwibo-docker`, `qwibo.github.io`). Documentazione MkDocs bilingue.

### Privacy-by-Design
Trascrizione interamente on-device. La privacy è requisito di prodotto, non feature accessoria.

---

## Modello di Licenza

Qwibo è **gratuito per uso personale e non commerciale**. Per uso aziendale/commerciale è prevista licenza dedicata. Nessuna bolletta cloud per la trascrizione: il costo è spazio disco e tempo di elaborazione sul proprio hardware.

---

## 🚀 Perché Questo Progetto Mi Interessava

Qwibo sta all'incrocio di tre temi stimolanti: esecuzione locale di modelli AI su hardware consumer, packaging retail di software AI complesso, e traduzione di un problema quotidiano in un prodotto che un non-tecnico può installare stasera.

La sfida interessante non è solo "far girare un modello ASR" — è portarlo su **mini PC Windows senza GPU**, compilare dipendenze native in modo relocatable, e consegnare un flusso **carica → aspetta → scarica** senza che l'utente tocchi un terminale.

---

> **Specifiche Tecniche**
> - **Desktop**: Electron + Python embedded + NSIS installer
> - **Linguaggio**: Python 3.12+
> - **ASR**: NVIDIA NeMo Parakeet (TDT 0.6B v3)
> - **Web / API**: FastAPI + HTMX (in finestra Electron)
> - **Riassunti LLM**: DeepSeek / OpenAI / Claude / Gemini / Kimi / Qwen locale (opt-in)
> - **Output**: TXT, SRT, riassunto opzionale
> - **Deploy**: Windows installer (retail) · Docker self-hosted (repo separato)
> - **Documentazione**: MkDocs bilingue EN + IT
> - **Licenza**: gratuita per uso personale · commerciale su licenza dedicata

---

🌐 **Sito ufficiale:** [qwibo.github.io](https://qwibo.github.io){: rel="nofollow" target="_blank"}

📚 **Documentazione:** [qwibo.github.io/docs](https://qwibo.github.io/docs/){: rel="nofollow" target="_blank"}

💻 **Codice sorgente:** [github.com/qwibo/qwibo](https://github.com/qwibo/qwibo){: rel="nofollow" target="_blank"}

🐳 **Docker self-hosted:** [github.com/qwibo/qwibo-docker](https://github.com/qwibo/qwibo-docker){: rel="nofollow" target="_blank"}

📩 **Vuoi trascrivere i tuoi file in locale?** [Contattami](mailto:info@antoniotrento.net)
