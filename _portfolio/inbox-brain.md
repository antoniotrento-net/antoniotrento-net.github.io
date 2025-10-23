---
layout: portfolio
title: "Inbox Brain"
date: 2025-10-23
description: "Inbox Brain è un motore open-source che legge le email via IMAP, le normalizza, le classifica con AI e rende tutto interrogabile via API e SQL. Perfetto per cruscotti, automazioni e workflow data-driven."
image: "/assets/images/portfolio/inbox-brain/inbox-brain.jpg"
image-header: "/assets/images/portfolio/inbox-brain/inbox-brain.jpg"
image-paint: "/assets/images/portfolio/inbox-brain/inbox-brain.jpg"
tags: [Open Source, Email, IMAP, AI, LLM, FastAPI, MySQL, Docker, DevOps, ETL, Data Engineering, Triage, Classification, REST API, Automation, Superset, Metabase]
---

> *"Trasformare la casella di posta in un database vivo, interrogabile e automatizzabile: questo è Inbox Brain."*

**Inbox Brain** è un progetto open-source progettato per **ingestire email da qualsiasi provider IMAP**, **normalizzare i messaggi**, **classificarli con AI** e **pubblicare risultati e metriche** tramite **MySQL** e **API REST**. È pensato come **spina dorsale dati** per dashboard (Metabase/Superset), automazioni (n8n) e prodotti che necessitano di una base *inbox-centric* affidabile e scalabile. :contentReference[oaicite:0]{index=0}

---

## Cosa fa, in breve

- **Ingest IMAP**: importa messaggi dalla casella (Yahoo/Gmail/Outlook/qualsiasi IMAP), con **deduplica robusta** e **checkpoint** per ripartenze sicure. :contentReference[oaicite:1]{index=1}  
- **Coda su DB**: ogni email normalizzata viene messa in **`email_queue`** per l’elaborazione asincrona. :contentReference[oaicite:2]{index=2}  
- **AI Triage**: un **worker AI** classifica e arricchisce i messaggi, salvando gli esiti in **`email_ai`** (es. *intent*, *confidence*, *extracted_json*). :contentReference[oaicite:3]{index=3}  
- **API veloci**: **FastAPI** espone endpoint di **health** e **listing** con **token** semplice per prototipi e integrazioni. :contentReference[oaicite:4]{index=4}

---

## Schema Dati Principale

Inbox Brain popola quattro tabelle chiave, pensate per essere interoperabili con BI e automazioni:  
- **`emails_raw`**: ingest normalizzato (headers, body, metadata)  
- **`email_queue`**: coda di lavorazione, stati e timestamp  
- **`email_ai`**: esito AI (intent, confidence, JSON estratto)  
- **`runs`**: **checkpoint** (IMAP UID / Gmail history id) per continuità e deduplica  
Inoltre è predisposta **`email_attachments`** per la gestione degli allegati. :contentReference[oaicite:5]{index=5}

---

## Pipeline & Ruoli

Il comportamento dell’app è modulare tramite la variabile **`APP_ROLE`**:  
- `ingestor` → solo ingest IMAP  
- `worker` → solo classificazione AI  
- `api` → solo API  
- `combo` *(default dev)* → tutto-in-uno per partire in fretta  
Questa separazione rende semplice passare da **dev monolitico** a **prod a servizi separati**. :contentReference[oaicite:6]{index=6}

---

## Flusso Operativo

1. **Ingestor IMAP** legge la mailbox e salva in `emails_raw`, **accoda** in `email_queue` e aggiorna `runs`. *(Alla prima run importa per default gli **ultimi 200 UID** per bootstrap controllato).* :contentReference[oaicite:7]{index=7}  
2. **Worker AI** consuma la coda, chiama il modello e scrive in `email_ai`, marcando la lavorazione *done*. :contentReference[oaicite:8]{index=8}  
3. **API** espone `/health` e `/emails?limit=…` protetti da **`x-api-token`** per query rapide, integrazioni e QA. :contentReference[oaicite:9]{index=9}

---

## Architettura & DevOps

- **Docker Compose**: `app` (FastAPI+Ingestor+Worker in dev), **MySQL 8** e volumi persistenti. Healthcheck e log container-first. :contentReference[oaicite:10]{index=10}  
- **Configurazione .env**: IMAP, **OpenAI API Key**, DSN MySQL, **APP_ROLE**, token API. :contentReference[oaicite:11]{index=11}  
- **Ripartenze sicure**: dedup su `(provider, mailbox, message_id, external_id, uid)` e/o `hash_dedupe`; checkpoint in `runs`. :contentReference[oaicite:12]{index=12}  
- **Troubleshooting**: log via `docker compose logs -f app`, shell su MySQL container, comandi rapidi nel README. :contentReference[oaicite:13]{index=13}

---

## API & Query Esempio

- **Health**  
  `GET http://localhost:8000/health` → `{"ok": true}` :contentReference[oaicite:14]{index=14}  
- **Elenco email**  
  `GET /emails?limit=20` con `x-api-token` → record da `emails_raw` **+** arricchimenti `email_ai` (se presenti). :contentReference[oaicite:15]{index=15}

---

## Estensioni & Roadmap

- **Gmail via API (Watch/Pub/Sub)** con checkpoint **`gmail_history_id`** per near-real-time senza polling IMAP. :contentReference[oaicite:16]{index=16}  
- **Rules Engine**: auto-reply, assegnazioni, SLA e dispatch per team. :contentReference[oaicite:17]{index=17}  
- **OCR & Parsing Allegati**: estrazione da PDF/immagini con salvataggio strutturato su DB. :contentReference[oaicite:18]{index=18}  
- **Dashboard out-of-the-box** (Superset/Metabase) con KPI di volume, intent, tempi di gestione, code aging. :contentReference[oaicite:19]{index=19}  
- **Security Hardening**: JWT per API, rate-limit, reverse proxy (Caddy/Traefik) e scansioni CVE (Trivy).

---

## Perché è diverso

- **Database-first**: i dati email diventano **asset aziendale** interrogabile (SQL), non solo “testi da leggere”.  
- **Modulare per design**: ingest/AI/API separabili e scalabili per carichi reali.  
- **Developer-friendly**: Docker, README ricco, env chiara, **run locale in 1 comando**. :contentReference[oaicite:20]{index=20}

---

## Casi d’Uso

- **Triage automatico** per supporto/Vendite con intent e priorità.  
- **Lead & Compliance Mining**: estrazione dati strutturati dagli allegati (ordini, fatture, KYC).  
- **Ops Intelligence**: cruscotti su volumi, tempi risposta, code aging, SLA per team multi-brand.  
- **Agent Orchestration**: integra n8n per risposte, tagging, inoltri e creazione ticket.

---

## Avvio rapido (dev)

1) copia `.env.example` in `.env` e compila IMAP + `OPENAI_API_KEY`, lascia `APP_ROLE=combo`  
2) `docker compose up -d --build`  
3) `curl http://localhost:8000/health` → ok  
4) `curl -H "x-api-token: changeme" "http://localhost:8000/emails?limit=20"`  
*(Per la prima run verranno importati gli ultimi **200 UID**, poi si prosegue incrementale.)* :contentReference[oaicite:21]{index=21}

---

## Competenze dimostrate

- **Data Engineering su email** (ingest, normalizzazione, dedup, checkpoint)  
- **AI Application Pattern** (worker asincrono, scoring, explainability di base)  
- **Backend & API Design** (FastAPI, token, paging)  
- **DevOps** (Docker Compose, ambienti riproducibili, osservabilità attivabile)  
- **BI Enablement** (schema relazionale chiaro, perfetto per Metabase/Superset)

---

## 🔗 Risorse

- **Repository GitHub**: [InboxBrain/InboxBrain](https://github.com/InboxBrain/InboxBrain) :contentReference[oaicite:22]{index=22}  
- **README con comandi e .env** (IMAP/AI/APP_ROLE, troubleshooting) :contentReference[oaicite:23]{index=23}  
- **Licenza**: OSS (vedi repo)

---

> *Inbox Brain è il “connettore neurale” tra posta e processi: da rumore a segnali, da messaggi a decisioni.*
