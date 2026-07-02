---
layout: portfolio
title: "Sbobinator – Trascrizione Audio e Video in Italiano, 100% Locale"
date: 2026-07-02
description: "Applicazione per trascrivere riunioni, podcast, interviste e lezioni in testo e sottotitoli SRT direttamente sul proprio PC. ASR NeMo Parakeet, web UI FastAPI, riassunti LLM opzionali. Privato, gratuito per uso personale, senza costi al minuto."
image: "/assets/images/portfolio/sbobinator/sbobinator-index.jpg"
image-header: "/assets/images/portfolio/sbobinator/sbobinator-cover.jpg"
image-paint: "/assets/images/portfolio/sbobinator/sbobinator-cover.jpg"
tags: [AI, Python, FastAPI, NeMo, ASR, Speech-to-Text, Docker, LLM, On-Premise, Automazione, Streamlit]
---

> *"Sbobinare significa trascrivere da una bobina. Il nome è vecchio, il problema no: due ore di riunione registrata e nessuna voglia di riscriverle a mano. Sbobinator le trasforma in testo cercabile e sottotitoli, senza mandare un solo byte fuori dal tuo computer."*

**Sbobinator** è un'applicazione desktop/web per la **trascrizione automatica di audio e video in italiano**, progettata per girare interamente in locale. Trasforma riunioni, podcast, interviste e lezioni in testo cercabile e sottotitoli SRT, con riassunti LLM opzionali — senza upload obbligatori, senza abbonamenti, senza costi al minuto.

Il progetto nasce da un'esigenza concreta e diffusa: chiunque lavori con l'audio — consulenti che vivono di call, creator che pubblicano ogni settimana, giornalisti che devono citare con precisione, studenti che ripassano da lezioni lunghe — si scontra con lo stesso collo di bottiglia. La registrazione ce l'hai già; quello che manca è il testo, e il tempo per ricavarlo a mano.

Le soluzioni cloud esistono (Otter, servizi a pagamento al minuto, trascrizione delle piattaforme di videoconferenza), ma condividono due limiti fondamentali: **costano in proporzione ai minuti** e **richiedono di caricare i file su server di terzi**. Per chi tratta call con clienti, interviste non pubblicate o contenuti riservati, questo secondo punto non è un dettaglio: è un vincolo di privacy che spesso rende quelle soluzioni semplicemente non utilizzabili.

Sbobinator risolve il problema alla radice: **la trascrizione gira sul tuo PC**, i file restano tuoi dall'inizio alla fine, e per uso personale è gratuito.

---

## Il Problema: Perché Trascrivere Bene l'Italiano È Difficile

Trascrivere audio reale in italiano è significativamente più difficile di quanto suggerisca una demo su un file pulito:

### 1. Il parlato reale non è pulito
Le riunioni hanno voci sovrapposte, interruzioni, ritmo informale, microfoni mediocri e rumore di fondo. Un motore addestrato su audio da studio crolla sul primo audio da sala riunioni. Serve un modello robusto al parlato spontaneo.

### 2. L'italiano è cittadino di seconda classe
La maggior parte dei modelli ASR ottimizza sull'inglese. L'italiano — con la sua morfologia ricca, i nomi propri, i tecnicismi settoriali — riceve meno attenzione. Sbobinator adotta un modello con forte focus sul parlato italiano proprio per questo.

### 3. I file lunghi non devono bloccare la giornata
Una lezione da due ore o un'intervista fiume non possono costringere l'utente a restare davanti a una barra di avanzamento. L'elaborazione deve procedere in background, in modo che l'utente carichi, chiuda pure il browser e torni quando il risultato è pronto.

### 4. Privacy come requisito, non come opzione
Per molti utenti i contenuti audio sono sensibili per contratto o per policy. Un flusso che richiede l'upload obbligatorio è, per loro, un flusso inutilizzabile. La trascrizione locale non è un'ottimizzazione: è la precondizione all'adozione.

---

## La Soluzione: Come Funziona

Il flusso è volutamente ridotto a tre mosse — **carica, aspetta, scarica** — per abbassare al minimo l'attrito iniziale.

### Step 1 — Upload
L'utente trascina un file (MP4, MKV, WAV, MP3, e altri formati comuni) nell'interfaccia web. Nessuna conversione manuale preventiva, nessun account da creare per ottenere il primo risultato.

### Step 2 — Trascrizione (in background)
Il motore ASR **NeMo Parakeet** elabora l'audio in locale. Il lavoro procede come job asincrono: l'utente vede lo stato avanzare e può tornare alle proprie attività. I file lunghi sono trattati come normalità, non come caso limite.

### Step 3 — Download
Al termine l'utente scarica **testo completo** (per rileggere decisioni, recuperare citazioni, preparare appunti) e **sottotitoli SRT** (per montaggio o pubblicazione). Il risultato è immediatamente utilizzabile.

### Step 4 — Riassunto LLM (opzionale)
Chi ha bisogno di una sintesi rapida può attivare il riassunto tramite un provider a scelta (cloud come DeepSeek, OpenAI, Claude, Gemini, Kimi — oppure **Qwen locale** per restare completamente offline). È una funzione opt-in: il valore principale — testo e sottotitoli — è già pronto senza passaggi extra.

---

## Stack Tecnologico

| Componente | Tecnologia | Ruolo |
|---|---|---|
| **ASR** | NVIDIA NeMo Parakeet (TDT 0.6B v3) | Trascrizione speech-to-text in italiano |
| **Web UI** | FastAPI + interfaccia web | Upload, coda job, download risultati |
| **Dashboard / UI** | Streamlit | Monitoraggio e interazione |
| **Riassunti LLM** | DeepSeek · OpenAI · Claude · Gemini · Kimi · Qwen locale | Sintesi opzionale opt-in |
| **Media processing** | ffmpeg | Estrazione e normalizzazione audio |
| **CLI** | `sbobina` (Python) | Trascrizione da riga di comando |
| **Packaging** | pyproject.toml (extra: local / ui / summarize / asr) | Installazione modulare |
| **Deployment** | Windows/Linux nativo · Docker (Linux, mini-PC) | Esecuzione self-hosted |

### Perché NeMo Parakeet
La scelta del motore ASR è stata guidata dall'equilibrio tra qualità sul parlato italiano, robustezza all'audio reale degradato e possibilità di esecuzione locale su hardware consumer. Parakeet offre trascrizione di qualità mantenendo l'intero flusso on-device, senza dipendere da API esterne a consumo.

---

## Architettura: Flusso a Job Asincroni

Il cuore di Sbobinator è una pipeline event-driven con stati di job espliciti, in modo che nessun file "sparisca" tra un passaggio e l'altro:

```
┌──────────────────────────────────────────────────────────┐
│                      Sbobinator (locale)                  │
│                                                           │
│   Upload ──► Coda ──► Worker ASR ──► Validazione ──► Output│
│   (web UI)   (job)   (NeMo)         (TXT/SRT)      (down)  │
│                          │                                 │
│                          └──► Riassunto LLM (opt-in)       │
└──────────────────────────────────────────────────────────┘
```

- **Coda job:** ogni file diventa un job con stato tracciato (`queued`, `running`, `done`, `failed`).
- **Worker in background:** l'elaborazione non blocca l'interfaccia; l'utente può chiudere il browser e tornare.
- **Storico consultabile:** lista job e pagina di dettaglio per singolo file.
- **Output multipli:** TXT e SRT sempre, riassunto solo su richiesta.

---

## Competenze Dimostrate

### AI Engineering / ASR
Integrazione di un modello ASR (NeMo Parakeet) in una pipeline di produzione locale, con attenzione alla qualità sul parlato italiano reale e alla gestione di file lunghi. Integrazione opzionale di LLM multipli (cloud e locale) per la sintesi, con architettura provider-agnostica.

### Architettura Software
Progettazione di una pipeline a job asincroni con stati deterministici (queued → running → done / failed), storico consultabile e output multipli. Interfaccia web con FastAPI, disaccoppiamento tra ingestion, elaborazione e output.

### Product & UX per la Conversione
Riduzione del flusso a "carica, aspetta, scarica" per minimizzare l'attrito iniziale. Funzioni avanzate (riassunto) tenute opt-in per non appesantire il primo utilizzo. Focus esplicito sulle obiezioni reali dell'utente: qualità italiano, file lunghi, privacy, costo.

### DevOps e Packaging
Installazione modulare via `pyproject.toml` con extra dedicati (local, ui, summarize, asr), script di setup, esecuzione nativa su Windows/Linux e opzione Docker per deployment su mini-PC. Documentazione tecnica bilingue (EN + IT) generata con MkDocs.

### Privacy-by-Design
Architettura che mantiene la trascrizione interamente on-device, senza upload obbligatorio. La privacy è trattata come requisito di prodotto, non come feature accessoria — precondizione all'adozione per utenti con contenuti sensibili.

---

## Modello di Licenza

Sbobinator è **gratuito per uso personale e non commerciale**: nessun timer, nessuna carta di credito, nessun trial nascosto. Per l'uso aziendale/commerciale è prevista una licenza dedicata, con condizioni descritte nella documentazione. Non c'è alcuna bolletta cloud per la trascrizione: il costo è lo spazio disco e il tempo di elaborazione sul proprio hardware.

---

## 🚀 Perché Questo Progetto Mi Interessava

Sbobinator sta all'incrocio di tre temi che trovo tecnicamente stimolanti: l'esecuzione locale di modelli AI su hardware consumer, il design di pipeline asincrone affidabili, e la traduzione di un problema quotidiano molto concreto in un prodotto usabile davvero.

La sfida interessante non è "far girare un modello ASR" — è farlo bene sull'italiano reale, gestire file lunghi senza bloccare l'utente, e progettare un flusso così semplice da abbattere la barriera d'ingresso, il tutto mantenendo il vincolo forte della privacy totale. È il tipo di engineering in cui la differenza tra un prototipo e un prodotto sta nei dettagli: la gestione degli stati dei job, la robustezza sull'audio degradato, la scelta di rendere ogni funzione avanzata opt-in.

---

> **Specifiche Tecniche**
> - **Linguaggio**: Python 3.11+
> - **ASR**: NVIDIA NeMo Parakeet (TDT 0.6B v3)
> - **Web / API**: FastAPI + Streamlit
> - **Riassunti LLM**: DeepSeek / OpenAI / Claude / Gemini / Kimi / Qwen locale (opt-in)
> - **Media**: ffmpeg
> - **Output**: TXT, SRT, riassunto opzionale
> - **Deployment**: Windows / Linux nativo · Docker (Linux, mini-PC)
> - **Documentazione**: MkDocs, bilingue EN + IT
> - **Licenza**: gratuita per uso personale · commerciale su licenza dedicata

---

🌐 **Sito ufficiale:** [sbobinator.github.io](https://sbobinator.github.io){: rel="nofollow" target="_blank"}

📚 **Documentazione:** [sbobinator.github.io/docs](https://sbobinator.github.io/docs/){: rel="nofollow" target="_blank"}

💻 **Codice sorgente:** [github.com/sbobinator/sbobinator](https://github.com/sbobinator/sbobinator){: rel="nofollow" target="_blank"}

📩 **Vuoi trascrivere i tuoi file in locale?** [Contattami](mailto:info@antoniotrento.net)
