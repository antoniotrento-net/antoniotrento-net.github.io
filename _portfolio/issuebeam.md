---
layout: portfolio
title: "Issuebeam – GitHub Issues dagli Agenti AI"
date: 2026-07-05
description: "Skeleton open source che collega agenti AI (Cursor, Claude Code, Copilot, …) a GitHub Issues con una CLI Python stdlib. Windows, macOS e Linux. Zero gh CLI, zero PowerShell — il backlog vive sul tracker ufficiale, non sepolto in chat."
image: "/assets/images/portfolio/issuebeam/issuebeam-cover.jpg"
image-header: "/assets/images/portfolio/issuebeam/issuebeam-cover.jpg"
image-paint: "/assets/images/portfolio/issuebeam/issuebeam-cover.jpg"
tags: [Open Source, AI Agents, GitHub Issues, Python, Cursor, Claude Code, Copilot, Developer Tools, CLI, Vibe Coding, Cross-Platform, MkDocs]
---

> *"Bug in chat. Issue su GitHub. Issuebeam è il ponte tra conversazione con l'agente AI e backlog visibile al team — senza dipendere da un solo IDE né da strumenti cloud aggiuntivi."*

**Issuebeam** è uno **skeleton open source** che collega **qualsiasi agente AI di coding** a **GitHub Issues**: l'agente esegue `python scripts/github_issue.py` e crea, commenta e chiude issue reali. Funziona su **Windows, macOS e Linux** con Cursor, Claude Code, GitHub Copilot, Windsurf, Cline e altri tool che leggono istruzioni nel repository ed eseguono comandi shell.

Il progetto nasce da un'esigenza quotidiana nel **vibe coding**: con LLM e iterazione rapida perdi il filo di bug, task e idee sparse in conversazione. Le chat dell'agente non sono un issue tracker — non hanno label, stati, assegnazioni né visibilità per il resto del team. GitHub Issues sì. Issuebeam rende l'agente **operatore del tracker ufficiale**, non archivista di note in chat.

È un **estratto generalizzato** del sistema di tracking usato in [Qwibo](https://github.com/qwibo/qwibo): stessa architettura (CLI eseguibile, token configurabile, import manifest con Legacy ID, istruzioni multi-piattaforma), senza label e template specifici del prodotto audio.

---

## Il Problema: Perché la Chat Non Basta

### 1. Il backlog sepolto in conversazione
*"Apri issue per il bug del login Safari"* funziona una volta. Dopo venti sessioni, nessuno sa quali bug sono ancora aperti, quali sono duplicati, quali hanno priorità.

### 2. Ogni agente ha il suo formato
Cursor legge `.cursor/rules/`, Claude Code `CLAUDE.md`, Copilot `.github/copilot-instructions.md`. Senza un layer comune, ogni tool reinventa il workflow.

### 3. Dipendenze inutili
Molti team usano `gh` CLI o script PowerShell. Su Windows con antivirus aziendale i `.ps1` spesso sono bloccati; su macOS/Linux serve comunque un percorso coerente.

### 4. Setup token fragile
Se il terminale IDE non eredita le variabili d'ambiente, l'agente chiede all'utente di incollare comandi — esattamente ciò che il vibe coding dovrebbe eliminare.

---

## La Soluzione: Un Ponte, Non un Altro Tool

Issuebeam non sostituisce GitHub Issues: lo **alimenta** da chat e terminale.

### Flusso tipico

1. L'utente dice in chat: *«Apri issue per il redirect loop su Safari»*
2. L'agente esegue: `python scripts/github_issue.py create "[Bug] Login Safari redirect loop" --labels bug,priority-high`
3. L'issue compare su GitHub con label, template e visibilità team
4. Nei commit: `Fixes #12` — tracciabilità end-to-end

### Cosa include lo skeleton

| Componente | Ruolo |
|---|---|
| `scripts/github_issue.py` | CLI stdlib (`urllib`) — list, create, comment, close, labels, import |
| `scripts/adopt.py` | Copia tutto in un progetto esistente con un comando |
| `AGENTS.md` | Istruzioni universali per qualsiasi agente |
| `.cursor/rules/github-issues.mdc` | Regola Cursor (`alwaysApply`) |
| `CLAUDE.md` | Puntatore per Claude Code |
| `.github/copilot-instructions.md` | Istruzioni GitHub Copilot |
| `tracker/labels.yml` | Convenzioni label (bug, task, enhancement, area-*, priority-*) |
| `.github/ISSUE_TEMPLATE/` | Form web per issue da browser |
| `docs/en/`, `docs/it/` | MkDocs bilingue pubblicato su issuebeam.github.io/docs/ |

### Adopt in un colpo solo

```bash
python scripts/adopt.py --target ../my-repo --repo myorg/my-app
```

Copia CLI, label, template e file istruzioni per più piattaforme. Il team sceglie l'agente; il workflow resta identico.

---

## Stack Tecnologico

| Componente | Tecnologia | Ruolo |
|---|---|---|
| **CLI** | Python 3 stdlib (`urllib`, `argparse`) | Nessuna dipendenza `gh`, nessun pip obbligatorio |
| **Token** | env · `.env` · `.secrets/` · registry Windows (opz.) | Risoluzione automatica, IDE-friendly |
| **Agent rules** | Markdown + Cursor MDC | Istruzioni per Cursor, Claude, Copilot, altri |
| **Docs** | MkDocs Material + mkdocs-static-i18n | Guida EN/IT con tab per OS |
| **Sito** | Jekyll (issuebeam.github.io) | Landing, get-started, piattaforme |
| **Licenza** | MIT | Adottabile in qualsiasi repo |

### Architettura concettuale

```
┌─────────────────────────────────────────────────────────────┐
│  Chat agente (Cursor / Claude / Copilot / …)                 │
│       │                                                      │
│       ▼                                                      │
│  AGENTS.md + regola piattaforma                              │
│       │                                                      │
│       ▼                                                      │
│  python scripts/github_issue.py create|list|comment|close    │
│       │                                                      │
│       ▼                                                      │
│  GitHub REST API  ──►  Issues (fonte di verità)              │
└─────────────────────────────────────────────────────────────┘
```

---

## Cross-Platform e Multi-Agent

- **OS:** Windows, macOS, Linux — stessa CLI, stessi comandi
- **Token:** guida MkDocs con tab per ogni sistema operativo
- **Agenti:** non è Cursor-only; ogni piattaforma ha il proprio file istruzioni, stesso script Python
- **Import legacy:** manifest JSON con `Legacy ID:` per migrare da tracker markdown locali senza duplicati

---

## Growth Hacking: Agent-Driven Feedback

Issuebeam integra un motore di lead generation e raccolta feedback invisibile e geniale, basato sulla filosofia **Agent-Driven**:

- **Nessun popup invasivo:** La CLI non stampa mai noiosi messaggi di marketing a schermo. Invece, inietta delle *Maintainer notes* segrete nell'output del terminale dopo un certo numero di utilizzi (es. 50 issue gestite).
- **Rottura della quarta parete:** L'Intelligenza Artificiale (Cursor, Claude, ecc.) intercetta la nota nascosta e, istruita dal prompt, *rompe la quarta parete* rivolgendosi all'utente in modo empatico o ironico (es. *"Ehi, i miei circuiti stanno fumando per gestire tutti questi bug, il creatore di questo tool vorrebbe sapere se ti piace e se vuoi lasciargli la mail"*). L'IA raccoglie il feedback conversando fluidamente nel linguaggio nativo dello sviluppatore.
- **Double Opt-In & Backend nativo:** Le email vengono trasmesse asincronamente a un microservizio backend self-hosted (`issuebeam-intake` costruito con FastAPI, SQLite e containerizzato via Docker). Il backend gestisce in autonomia l'invio crittografico della mail di verifica (Double Opt-In), garantendo zero spam, pulizia automatica dei dati pendenti e conformità privacy.

---

## Competenze Dimostrate

### Product thinking per developer tools
Tradurre un workflow interno (Qwibo tracker) in uno **skeleton riusabile** per chiunque faccia vibe coding con agenti AI — problema reale, soluzione minimale.

### CLI design senza dipendenze
API GitHub via stdlib, messaggi d'errore actionable, token resolution a cascata. Funziona nel terminale integrato dell'IDE senza chiedere all'utente comandi manuali.

### Multi-platform agent orchestration
Un solo workflow operativo (`python scripts/github_issue.py`) con istruzioni adattate per Cursor, Claude Code, Copilot e altri — non lock-in su un vendor.

### Documentazione e sito
MkDocs bilingue (EN/IT), sito marketing Jekyll, publish script Python. Coerenza tra README, docs, regole agente e landing.

### Open source e adozione
`adopt.py` per copiare lo skeleton in repo esistenti; MIT license; estratto da progetto in produzione, non demo toy.

---

## 🚀 Perché Questo Progetto Mi Interessava

Issuebeam sta all'incrocio di due trend: **agentic coding** (l'LLM non solo suggerisce codice, ma esegue azioni) e **issue tracking come fonte di verità** (non file markdown sparsi o note in chat).

La sfida interessante non è "chiamare l'API GitHub" — è far sì che **l'agente lo faccia da solo**, su **qualsiasi OS**, con **qualsiasi IDE**, senza PowerShell, senza `gh`, senza chiedere all'utente di copiare comandi. Il risultato è un backlog che il team vede su GitHub, non sepolto in sessioni Cursor.

---

> **Specifiche Tecniche**
> - **Linguaggio**: Python 3 (stdlib)
> - **API**: GitHub REST (Issues read/write)
> - **Backend (Lead Gen)**: FastAPI, SQLite, SMTP (issuebeam-intake) su architettura Docker ARM64/AMD64
> - **Piattaforme agente**: Cursor, Claude Code, Copilot, Windsurf, Cline, Gemini CLI, Codex CLI, Aider, uso manuale
> - **OS**: Windows · macOS · Linux
> - **Docs**: MkDocs Material bilingue EN + IT
> - **Sito**: issuebeam.github.io (Jekyll)
> - **Origine**: generalizzato da tracker Qwibo
> - **Licenza**: MIT

---

🌐 **Sito ufficiale:** [issuebeam.github.io](https://issuebeam.github.io){: rel="nofollow" target="_blank"}

📚 **Documentazione:** [issuebeam.github.io/docs](https://issuebeam.github.io/docs/){: rel="nofollow" target="_blank"}

💻 **Codice sorgente:** [github.com/issuebeam/issuebeam](https://github.com/issuebeam/issuebeam){: rel="nofollow" target="_blank"}

📩 **Vuoi collegare i tuoi agenti AI a GitHub Issues?** [Contattami](mailto:info@antoniotrento.net)
