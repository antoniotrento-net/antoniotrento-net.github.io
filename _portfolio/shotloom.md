---
layout: portfolio
title: "Shotloom – Montaggio Multicam AI Locale"
date: 2026-08-06
description: "NLE locale per footage multicam: 2–4 camere in input, sync e rough cut AI, sottotitoli ed export multi-piattaforma senza upload cloud. Docker oggi; Electron e taglio documentaristico in roadmap."
image: "/assets/images/portfolio/shotloom/shotloom-cover.jpg"
image-header: "/assets/images/portfolio/shotloom/shotloom-cover.jpg"
image-paint: "/assets/images/portfolio/shotloom/shotloom-cover.jpg"
tags: [AI, Video, Multicam, Docker, FastAPI, Python, NLE, Captions, On-Premise, Electron, Product Engineering]
---

> *"Hai già girato l'episodio a due, tre, quattro camere. Quello che manca non è un altro tutorial su Premiere: è sync, rough cut, caption ed export — senza caricare i rushes su un NLE cloud e senza passarci il pomeriggio."*

**Shotloom** è un **NLE locale guidato dall'AI** pensato per chi gira multicam sul serio: podcast settimanali, eventi, interviste, workshop, lezioni. Il percorso primario è automatico — *analizza e monta* — e solo dopo, se sei precisino, raffini ritmo, stile sottotitoli e parametri nella dashboard. I file restano sulla tua macchina (o sul VPS che controlli tu): niente upload obbligatorio, niente bolletta cloud di montaggio.

Il nome non è marketing vuoto: **shot** (inquadrature) + **loom** (telaio). Entrano più camere; ne esce un solo montaggio utilizzabile.

Il progetto è in **early access** su GitHub. Oggi si avvia con Docker e si usa dal browser; la roadmap punta all'installer Electron retail (stesso schema di Qwibo) e a una modalità documentaristica con tanti clip + voce fuori campo.

---

## Perché l'ho fatto

Dopo [Qwibo](/portfolio/qwibo/) — trascrizione audio/video locale, packaging Electron retail — il pezzo successivo della catena creativa era ovvio: **dal rushes al cut**.

Chi produce contenuti multicam conosce il collo di bottiglia. La ripresa c'è. Il tempo per allineare le tracce, scegliere i tagli, bruciare i sottotitoli e esportare quattro formati diversi no. CapCut e Descript risolvono la velocità, ma chiedono di **caricare** i file. Premiere e DaVinci restano ottimi per il finish, ma sono lenti se ti serve solo un rough cut pubblicabile entro sera.

Volevo uno strumento che:

1. Partisse dal caso d'uso reale (2–4 camere, non “un editor generico”)
2. Facesse il lavoro sporco da solo (sync, montaggio, caption, export)
3. Restasse **on-device** per privacy e costi
4. Avrebbe una sola superficie chiara (dashboard Shotloom), non un clone CapCut da imparare prima di ottenere un risultato

Shotloom è la risposta a quella domanda. Non è “un altro NLE con AI appiccicata”: è un prodotto con una **stella polare** esplicita — *clip multicam in → Shotloom fa tutto → se serve, raffini*.

---

## Il problema: il multicam mangia le giornate

### 1. Sync e switch camera non sono “creatività”
Allineare tre microfoni e due videocamere, trovare dove parla chi, tagliare i morti: è lavoro meccanico. L'AI può (e deve) farlo per prima.

### 2. Ogni piattaforma vuole un export diverso
YouTube 16:9, TikTok/Reels 9:16, caption bruciati o file separati, ritmi diversi. Rifare lo stesso episodio quattro volte è il modo più sicuro di odiare il proprio mestiere.

### 3. Privacy e rushes non pubblicati
Episodi non ancora usciti, eventi clienti, interviste sensibili: caricarli su un servizio cloud non è sempre accettabile. Per molti è un **vincolo**, non una preferenza.

### 4. L'NLE tradizionale è sovradimensionato per il rough cut
Color grading, curve, plugin: utili dopo. Prima serve un cut che regga. Shotloom punta a quel tratto — *prima di pranzo*, non “entro fine settimana se tutto va bene”.

---

## Cosa fa Shotloom (funzionalità)

### Flusso primario — automatico
| Funzionalità | Dettaglio |
|---|---|
| **Ingest multicam** | Drop di 2–4 clip camera (MP4 e formati tipici da ripresa) in un progetto |
| **Sync** | Allineamento delle tracce tra camere |
| **Rough cut AI** | Montaggio proposto: switch, ritmo, struttura utilizzabile |
| **Sottotitoli / caption** | Generazione e stile configurabile dalla dashboard |
| **Export multi-piattaforma** | Profili YouTube, TikTok, Instagram, Facebook |
| **Crop / formati** | Percorso verso master e verticali (9:16) coerenti con le piattaforme |
| **Elaborazione locale** | Pipeline su Docker: API + worker + artifact sulla tua macchina |

### Dashboard — dove controlli il risultato
La UI è un'unica dashboard web (`apps/web`) servita dall'API:

- Avvio **Analizza e monta** senza dover imparare una timeline da zero
- Anteprima del cut e dei caption
- Impostazioni di progetto (ritmo, lingue, stile sottotitoli, profili piattaforma)
- Tab di **raffinamento** (grade, effetti, transizioni, mask) come layer di preview — il cablaggio completo su export è lavoro ancora in corso; il percorso veloce resta il montaggio automatico

### Cosa *non* è (di proposito)
- Non è un clone CapCut cloud
- Non è un secondo “studio OpenCut” parallelo: l'amalgama è stato rimosso (ADR di prodotto). Un frontend, una direzione
- Non pretende di sostituire Premiere/DaVinci sul finish fine: punta al tratto *rushes → cut esportabile*, con export NLE in roadmap

---

## Come funziona (oggi)

### Step 1 — Bootstrap
Installi Docker, lanci lo script di bootstrap una volta. Sale lo stack (API, worker, volumi progetti). Apri `http://127.0.0.1:8765` nel browser.

### Step 2 — Progetto e clip
Crei un progetto, trascini 2–4 file camera. Nessuna preparazione manuale tipica: formati da ripresa reali (podcast, evento, intervista).

### Step 3 — Analizza e monta
La pipeline sincronizza, propone il rough cut, prepara i caption. Puoi lasciare elaborare e tornare: non è un processo che deve tenerti incollato a una progress bar tutto il pomeriggio.

### Step 4 — Affina i parametri
Nella dashboard regoli ciò che conta per te: ritmo del montaggio, stile sottotitoli, profili di export. Pochi controlli, non mille pannelli.

### Step 5 — Export
Scarichi master e/o verticali per le piattaforme scelte. I file restano nei volumi locali del progetto.

---

## Il prodotto oggi vs dove sta andando

### Oggi (early access)
- Runtime **Docker Compose** (dev e VPS self-hosted)
- Dashboard browser + API FastAPI + worker
- Landing bilingue EN/IT: [shotloom.github.io](https://shotloom.github.io){: rel="nofollow" target="_blank"}
- Codice aperto su [GitHub](https://github.com/Shotloom/Shotloom){: rel="nofollow" target="_blank"}
- Licenza **in definizione** (early access mentre il prodotto matura)

### Roadmap (già tracciata)
| Evolutiva | Perché conta | Issue |
|---|---|---|
| **App Electron** | Installer one-shot (Windows in primis), niente Docker obbligatorio per l'utente finale — stesso pattern retail di Qwibo | [#51](https://github.com/Shotloom/Shotloom/issues/51){: rel="nofollow" target="_blank"} |
| **Taglio documentaristico AI** | Tanti clip di ripresa + **voce fuori campo**: l'AI propone un taglio narrativo (non solo sync multicam podcast/evento) | [#52](https://github.com/Shotloom/Shotloom/issues/52){: rel="nofollow" target="_blank"} |
| **Export NLE** | Progetto importabile in Premiere / DaVinci (FCPXML/ZIP) per chi finisce fuori | [#50](https://github.com/Shotloom/Shotloom/issues/50){: rel="nofollow" target="_blank"} |
| **Refine su export** | Grade / effetti / transizioni / mask cablati fino all'export, non solo preview | [#49](https://github.com/Shotloom/Shotloom/issues/49){: rel="nofollow" target="_blank"} |

Altre linee aperte sul tracker: burn-in sottotitoli brand-aware, UX timeline Creator, verifica crop 9:16 = export.

---

## Decisioni di prodotto (e perché contano in un portfolio)

### Stella polare esplicita
*Clip multicam in → Shotloom fa tutto → precisino raffina.* Ogni feature si giudica rispetto a questa frase. Se non accelera il percorso automatico, non è prioritaria.

### Un solo frontend
È stata rimossa la tentazione di mantenere uno “studio” parallelo tipo OpenCut. La dashboard Shotloom è la superficie unica: meno confusione per l'utente, meno debito architetturale.

### Privacy come requisito
Come in Qwibo: on-device non è un bullet marketing, è la condizione perché certi creator e producer possano usarlo.

### Docker ora, Electron dopo
Consegnare early access self-hosted velocemente; poi packaging retail quando la pipeline è abbastanza stabile. Stessa lezione di Qwibo, applicata al video.

---

## Stack tecnologico

| Componente | Tecnologia | Ruolo |
|---|---|---|
| **API** | Python · FastAPI | Progetti, job, settings, artifact |
| **Worker** | Pipeline locale (ffmpeg / toolchain media) | Sync, cut, caption, export |
| **Dashboard** | Frontend `apps/web` | Flusso primario + refine |
| **Runtime** | Docker Compose | Dev e deploy VPS (`127.0.0.1:8765` in default sicuro) |
| **Tracking** | GitHub Issues (+ CLI agenti) | Backlog prodotto, non chat sparse |
| **Presence** | Jekyll (shotloom.github.io) | Landing EN/IT |
| **Roadmap desktop** | Electron (pattern Qwibo) | Installer retail post-v1 |

### Architettura (vista d'insieme)

```
┌──────────────────────────────────────────────────────────────┐
│  Shotloom (oggi)                                              │
│                                                               │
│   Cam A/B/C/D ──► ingest ──► API + worker                     │
│                      │            │                           │
│                      │            ├── sync + rough cut AI     │
│                      │            ├── captions                │
│                      │            └── export YT/TikTok/IG/FB  │
│                      │                                        │
│                      └── dashboard (browser)                  │
│                                                               │
│  Dopo: Electron shell · documentario + VO · export NLE        │
└──────────────────────────────────────────────────────────────┘
```

---

## Competenze dimostrate

### Product engineering (AI video)
Definire un problema verticale (multicam → cut) e rifiutare il “editor generico con AI”. Stella polare, ADR, taglio di scope (niente studio parallelo).

### Full-stack / pipeline media
API, worker asincroni, artifact, dashboard unica; vincoli reali di ffmpeg, formati, export piattaforma.

### Privacy-by-design e self-hosting
Stesso filone di Qwibo: software che gira dove stanno i file, non dove sta l'abbonamento.

### Roadmap retail
Saper distinguere early access tecnico (Docker) da prodotto consumer (Electron), e tracciare le evolutive sul tracker pubblico.

### Brand e go-to-market
Identità (coral → magenta), logo “tre camere → timeline”, sito e portfolio: il prodotto si presenta, non solo “compila”.

---

## 🚀 Perché questo progetto mi interessava

Shotloom sta all'incrocio di tre temi che mi interessano:

1. **AI utile su footage reale**, non demo da keynote  
2. **Sovranità dei media** — rushes che non devono uscire di casa  
3. **Prodotto verticalissimo** — meglio fare bene 2–4 camere che fingere di essere Premiere

La sfida non è “mettere un modello su un video”. È costruire un percorso che un creator possa usare **ogni settimana**: bootstrap, drop, cut, export — e solo dopo, se vuole, raffinare.

---

> **Specifiche tecniche (snapshot early access)**
> - **Runtime**: Docker Compose · API FastAPI · worker · dashboard web
> - **Input**: 2–4 clip multicam tipici (podcast, evento, intervista, workshop)
> - **Output**: rough cut, caption, export multi-piattaforma
> - **Privacy**: elaborazione locale / self-hosted
> - **Roadmap**: Electron [#51](https://github.com/Shotloom/Shotloom/issues/51) · documentario + VO [#52](https://github.com/Shotloom/Shotloom/issues/52) · export NLE [#50](https://github.com/Shotloom/Shotloom/issues/50)
> - **Sito**: [shotloom.github.io](https://shotloom.github.io)
> - **Licenza**: in definizione (early access su GitHub)

---

🌐 **Sito ufficiale:** [shotloom.github.io](https://shotloom.github.io){: rel="nofollow" target="_blank"}

💻 **Codice sorgente:** [github.com/Shotloom/Shotloom](https://github.com/Shotloom/Shotloom){: rel="nofollow" target="_blank"}

📩 **Vuoi montare i tuoi multicam in locale?** [Contattami](mailto:info@antoniotrento.net)
