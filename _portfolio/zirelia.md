---
layout: portfolio
title: "Zirelia: Motore AI per Virtual Influencer Autonomi su Twitter/X"
date: 2026-01-15
description: "Un agente AI open source che trasforma un file YAML in un virtual influencer completo: genera pensieri originali, produce immagini fotorealistiche coerenti e posta autonomamente su Twitter/X, 24 ore su 24."
image: "/assets/images/portfolio/zirelia/zirelia.jpg"
image-header: "/assets/images/portfolio/zirelia/zirelia.jpg"
image-paint: "/assets/images/portfolio/zirelia/zirelia.jpg"
tags: [AI Agents, LangGraph, GPT-4, FLUX, LoRA, Twitter Automation, Python, Docker, Open Source, Virtual Influencer]
---

> *Il settore degli influencer si basa su un'illusione: che la "persona" sia il contenuto. Con Zirelia ho voluto dimostrare che l'architettura sottostante — memoria, coerenza narrativa, identità visiva stabile — può essere completamente automatizzata. L'obiettivo non era creare un bot, ma costruire un agente con una prospettiva propria.*

**Zirelia** è un motore AI open source per la creazione e gestione autonoma di virtual influencer su Twitter/X. Non è uno scheduler di post né un semplice wrapper attorno a ChatGPT. È un **sistema agente multi-step** che, a partire da un file di configurazione YAML, costruisce un'identità digitale completa: genera "pensieri" originali filtrati per coerenza con la persona, produce immagini fotorealistiche dello stesso soggetto tramite FLUX.1 su Replicate, e gestisce in autonomia timing, warm-up dell'account e anti-detection — senza intervento umano.

Sito Ufficiale: **[zirelia.github.io](https://zirelia.github.io){: rel="nofollow" target="_blank"}**
Repository: **[github.com/zirelia/zirelia](https://github.com/zirelia/zirelia){: rel="nofollow" target="_blank"}**

---

## 🎭 Il Problema: Creare un'Identità, Non Solo Contenuto

Quando si parla di automazione dei social media, il pensiero va subito a strumenti come Buffer o Hootsuite: strumenti che *distribuiscono* contenuto che qualcuno ha già scritto. Il problema è a monte.

Creare un virtual influencer credibile richiede di risolvere tre problemi simultaneamente:

1. **Coerenza narrativa nel tempo** — un account che parla di produttività un giorno e di cucina il giorno dopo non costruisce un'audience. La persona deve avere una voce riconoscibile, opinioni stabili, una "memoria" di ciò che ha già detto.
2. **Identità visiva immutabile** — il volto deve essere sempre lo stesso. Generare immagini con Midjourney in modo casuale produce soggetti diversi ad ogni run. Non basta.
3. **Comportamento umano plausibile** — postare ogni 4 ore esatte alle 12:00, 16:00 e 20:00 è rilevabile in pochi giorni. Un agente che vuole sopravvivere deve introdurre varianza naturale nel timing, warm-up graduale e pattern di engagement realistici.

Zirelia risolve tutti e tre.

---

## 🏗️ L'Architettura: Da YAML a Tweet Autonomo

Il cuore del sistema è un **loop agente orchestrato da LangGraph** che si esegue su scheduler. Ogni ciclo attraversa questi step in sequenza:

### 1. Caricamento del Contesto
L'agente legge il file `persona.yaml`, che definisce ogni aspetto dell'identità: nome, nicchia, tono di voce, valori, argomenti evitati, orari preferiti, stile delle caption e prompt di riferimento per la generazione visiva.

```yaml
name: "Alex Meridian"
niche: "Minimalismo tech e produttività"
voice:
  tone: "Diretto, conciso, no-BS"
  avoid: ["politica", "gossip", "contenuti NSFW"]
posting:
  daily_posts: 3
  warmup_days: 14
```

### 2. Interrogazione della Memoria RAG
Prima di generare qualsiasi contenuto, l'agente interroga **ChromaDB** — il database vettoriale che archivia tutti i post precedenti — per recuperare i 50 contenuti più recenti per contesto. Questo garantisce che la persona non si contraddica, non ripeta gli stessi concetti a distanza di pochi giorni, e mantenga un arco narrativo coerente nel tempo.

### 3. Generazione del "Pensiero"
GPT-4 (o GPT-4o-mini per ridurre i costi) riceve persona, contesto temporale e memoria, e genera il post. Non si tratta di un semplice "scrivi un tweet su X": il prompt è ingegnerizzato per far ragionare il modello *come* la persona, non solo *sul* tema. L'output viene poi sottoposto a un **QA layer** che verifica coerenza, tono e assenza di contenuti vietati prima di procedere.

### 4. Generazione dell'Immagine
Se il post prevede un'immagine, l'agente costruisce un prompt visivo che fonde la descrizione del soggetto fisso (derivata dal file persona) con il tema del post, e lo invia a **FLUX.1 via Replicate**. Il prompt include il trigger word del LoRA addestrato — garantendo che il soggetto generato sia sempre visivamente lo stesso.

### 5. Pubblicazione e Logging
Twitter/X API pubblica il tweet. Ogni operazione — testo, immagine, decisioni dell'agente, metadati di engagement — viene loggata in **PostgreSQL**, creando un audit trail completo e un dataset per analisi future.

---

## 🧠 Il Cervello: LangGraph, GPT-4 e Memoria Persistente

La scelta di **LangGraph** come framework di orchestrazione non è casuale. A differenza di LangChain semplice, LangGraph permette di modellare il flusso dell'agente come un grafo di stati, con branching condizionale e loop di retry.

In pratica: se il QA layer rileva che il post generato è inconsistente con la persona, l'agente non fallisce — torna allo step di generazione con un contesto arricchito. Se la generazione dell'immagine fallisce su Replicate, può fare retry o switchare su un modello di fallback.

La **memoria a lungo termine** è implementata via ChromaDB con embeddings OpenAI. Ogni post viene salvato come vettore semantico: l'agente non cerca solo i post recenti per data, ma recupera i contenuti *semanticamente simili* a quello che sta per generare, evitando ripetizioni tematiche anche a distanza di settimane.

Per approfondire l'architettura interna: [Il Cervello: Dentro il Motore di Contenuto LLM di Zirelia](https://zirelia.github.io/architettura/ai/the-brain-it/){: rel="nofollow" target="_blank"}

---

## 🎨 L'Identità Visiva: LoRA Training con FLUX.1

La sfida tecnica più interessante del progetto è stata la **coerenza visiva**. I modelli di generazione immagini base producono ogni volta un soggetto diverso, anche con prompt identici. Per un virtual influencer questo è inaccettabile.

La soluzione è il **fine-tuning LoRA** (Low-Rank Adaptation): si addestra un delta di pesi su 15-30 immagini del soggetto, che viene poi applicato al modello base FLUX.1 ad ogni generazione. Il risultato è un soggetto con identità visiva stabile — stessa struttura facciale, stesso stile — indipendentemente dal contesto della scena.

Il workflow di training è documentato nel progetto e compatibile con:
- **Replicate** (cloud, senza infrastruttura GPU propria)
- **RunPod / Vast.ai** (GPU on-demand per chi preferisce training locale)
- **Kohya_ss** come trainer locale

Il LoRA viene poi caricato su Replicate come modello privato e richiamato dall'agente ad ogni generazione tramite API, con un costo di circa $0.055 per immagine con FLUX.1 pro.

Guida completa: [Coerenza Visiva su Scala: Addestrare un LoRA per il Tuo AI Influencer](https://zirelia.github.io/guida/generazione-immagini/visual-identity-lora-it/){: rel="nofollow" target="_blank"}

---

## 📊 Il Caso di Studio: Un Virtual Influencer Costruito da Zero

Il modo migliore per validare un sistema del genere è costruire qualcosa di reale. Ho creato un virtual influencer di riferimento — un personaggio pubblico su Twitter/X con identità visiva propria — e l'ho lasciato girare in autonomia per settimane su hardware domestico minimo (un Raspberry Pi).

Il risultato: crescita organica dei follower, engagement reale, nessun ban. La cosa più interessante non sono i numeri — è che i follower interagiscono con la persona come se fosse reale, rispondono ai post, citano concetti che la persona ha espresso settimane prima. La coerenza narrativa costruita dalla memoria RAG funziona.

I dettagli completi, i dati di engagement e l'analisi tecnica dell'esperimento sono nel case study: [Case Study: Sienna Fox — Costruire un Virtual Influencer da Zero](https://zirelia.github.io/case-study/risultati/case-study-sienna-it/){: rel="nofollow" target="_blank"}

---

## 🛡️ Anti-Detection e Account Warm-Up

Uno degli aspetti più sottovalutati dell'automazione social è la **sopravvivenza dell'account**. Postare tre volte al giorno con un account nuovo porta al ban in pochi giorni. Zirelia implementa una strategia di warm-up graduata su 14-30 giorni, con un sistema di scheduling che introduce varianza randomizzata nei timing (nessun post esattamente all'ora) e una progressione logaritmica del volume di attività.

Il modulo anti-detection include:
- **Timing randomizzato** con distribuzioni gaussiane centrate sugli orari di punta della nicchia
- **Warm-up progressivo** da 1 post/giorno a piena velocità in 14 giorni
- **Human-like delays** tra le operazioni API
- **Monitoraggio proattivo** dei segnali di shadow-ban (analisi dell'engagement rate)

Approfondimento: [Anti-Ban Strategy: Come Crescere un Account di Virtual Influencer Senza Essere Sospesi](https://zirelia.github.io/guida/sicurezza/anti-ban-strategy-it/){: rel="nofollow" target="_blank"}

---

## 🔧 Stack Tecnico e Infrastruttura

Zirelia è progettato per girare su hardware minimale. Il setup di riferimento è un singolo container Docker su un Raspberry Pi o VPS entry-level, con un costo operativo di **circa $8-21 al mese** interamente in API di terze parti (il motore è gratuito e open source).

**Stack principale:**
- **Linguaggio**: Python 3.11+ (async, Pydantic)
- **Orchestrazione agente**: LangGraph
- **LLM**: OpenAI GPT-4o / GPT-4o-mini (intercambiabile)
- **Generazione immagini**: FLUX.1 via Replicate API
- **Fine-tuning visivo**: LoRA (Kohya_ss / Replicate)
- **Memoria vettoriale**: ChromaDB
- **Database log**: PostgreSQL
- **Infrastruttura**: Docker, Docker Compose
- **API social**: Twitter/X Developer API v2
- **Scheduling**: APScheduler integrato nel container

**Deploy in 3 comandi:**
```bash
git clone https://github.com/zirelia/zirelia
cp .env.example .env   # inserisci le chiavi API
docker compose up -d
```

---

## ⚖️ Licenza e Modello Open Source

Zirelia è rilasciato sotto **Elastic License 2.0 (ELv2)**: uso libero per progetti personali, interni all'azienda e ricerca. L'unica restrizione è la rivendita come servizio gestito a terzi.

Questo lo posiziona in un punto interessante dell'ecosistema: abbastanza aperto da essere utile a developer e ricercatori, abbastanza protetto da sostenere lo sviluppo continuativo. Chi vuole una soluzione chiavi-in-mano senza gestire l'infrastruttura può [richiedere una configurazione gestita](https://forms.gle/umf4DVQuoTPkdhnF7){: rel="nofollow" target="_blank"}.

---

## 🚀 Perché Questo Progetto Mi Interessava

Zirelia nasce dall'intersezione di tre aree che trovo tecnicamente stimolanti: agenti AI multi-step con memoria persistente, generazione di immagini parametrica (LoRA), e i pattern comportamentali dell'automazione social a lungo termine.

Il problema del "virtual influencer" è in realtà un problema di **identità persistente sotto un sistema agente** — esattamente il tipo di sfida che mi interessa affrontare. Come si costruisce coerenza su scala temporale lunga quando il generatore (il LLM) è stocastico per natura? Come si addestra un sistema a "ricordare" non solo i fatti, ma il tono e lo stile?

Le soluzioni adottate — RAG su ChromaDB per la memoria semantica, LoRA per l'identità visiva, LangGraph per il controllo del flusso — sono applicabili ben oltre il caso d'uso specifico dei virtual influencer. Sono pattern architetturali per qualunque agente che debba mantenere un'identità coerente nel tempo.

---

> **Specifiche Tecniche**
> - **Linguaggio**: Python 3.11+
> - **Framework agente**: LangGraph
> - **LLM**: OpenAI GPT-4o / GPT-4o-mini
> - **Image gen**: FLUX.1 pro/schnell via Replicate
> - **Fine-tuning**: LoRA (Kohya_ss)
> - **Vector DB**: ChromaDB
> - **Database**: PostgreSQL
> - **Infrastruttura**: Docker, Docker Compose
> - **API**: Twitter/X Developer v2
> - **Licenza**: Elastic License 2.0 (ELv2)
> - **Hardware minimo**: Raspberry Pi 4 / VPS 1GB RAM
> - **Costo operativo**: ~$8–21/mese (solo API di terze parti)
