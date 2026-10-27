---
layout: portfolio
title: "Kinetic Core"
date: 2025-12-05
description: "Kinetic Core è una libreria Python production-ready pensata per rendere semplici e affidabili l’integrazione, il sync dati e le operazioni ETL verso Salesforce, con autenticazione sicura, client ad alto livello, mapping flessibile e pipeline dichiarative."
image: "/assets/images/portfolio/kinetic-core/kinetic-core.jpg"
image-header: "/assets/images/portfolio/kinetic-core/kinetic-core.jpg"
image-paint: "/assets/images/portfolio/kinetic-core/kinetic-core.jpg"
og_image: "og/kinetic-core.jpg"
tags: [Salesforce, Python, Library, ETL, Data Integration, API, CLI, Logging, Automation, Docker, DevOps]
---

> *In ogni progetto enterprise finivo per riscrivere da zero le stesse integrazioni Salesforce. Ho deciso di trasformare quel codice sparso in un toolkit unico, robusto e riusabile, progettato come se dovesse andare in produzione domani.* 

**Kinetic Core** è una libreria Python pensata per sviluppatori, data engineer e team di integrazione che lavorano quotidianamente con Salesforce.

Invece di avere mille script ad-hoc per autenticarsi, fare CRUD, gestire mapping e sincronizzazioni, il toolkit offre un set coerente di componenti:

- autenticazione multipla (JWT, OAuth2),
- un client Salesforce ad alto livello,
- un motore di **field mapping** flessibile,
- un framework di **sync/ETL** dichiarativo,
- logging e CLI pensati per ambienti reali.

È un progetto orientato alla **manutenibilità**: nessun “quick & dirty”, ma codice strutturato, documentato e testabile. Ora è anche **Docker-ready** e pubblicato su **[PyPI](https://pypi.org/project/kinetic-core/){: rel="nofollow"}**.

---

## Architettura del toolkit

Il pacchetto è organizzato in moduli chiari e indipendenti, all’interno della directory `salesforce_toolkit/`.

### 1. Autenticazione: `auth/`

Gestire correttamente l’autenticazione verso Salesforce è il primo punto critico di qualsiasi integrazione.  
Il modulo `auth` incapsula tutta la complessità:

- **`JWTAuthenticator`**  
  Usa il *JWT Bearer Flow*, ideale per ambienti server-to-server e scenari production senza password utente.

- **`OAuthAuthenticator`**  
  Implementa il flusso OAuth 2.0 “password” classico, utile in contesti legacy o di sviluppo.

Entrambi gli authenticator possono essere configurati via `.env` o parametri espliciti, e restituiscono una **sessione autenticata** pronta per essere consumata dal client Salesforce.

---

### 2. Core client Salesforce: `core/`

Nel modulo `core` vive il cuore del toolkit:

- **`SalesforceSession`**: gestisce endpoint, token, refresh e gestione delle richieste HTTP.
- **`SalesforceClient`**: espone un’API Pythonica e ad alto livello per:

  - **CRUD completo** (create, retrieve, update, delete) su qualsiasi oggetto Salesforce (standard o custom),
  - **upsert** basato su External ID,
  - **query SOQL** con gestione automatica della paginazione,
  - **count** e utility per statistiche veloci,
  - supporto a operazioni batch e Composite API (dove ha senso).

L’obiettivo è avere un’unica interfaccia coerente per tutte le integrazioni, riducendo boilerplate e punti di errore.

---

### 3. Motore di Field Mapping: `mapping/field_mapper.py`

Ogni integrazione dati ha lo stesso problema: lo schema sorgente non coincide mai con quello di destinazione.  
`FieldMapper` è un **engine di trasformazione** generico pensato proprio per questo.

Supporta:

- rinomina campi (`source_field -> target_field`),
- valori di default,
- **transform function** personalizzate,
- mapping condizionale,
- accesso a campi annidati (`"address.city"`),
- composizione di regole riusabili.

Il risultato è un layer di mapping **dichiarativo**, che può essere descritto in Python o configurato esternamente, separando la logica ETL dal codice applicativo.

---

### 4. Framework di Sync / ETL: `pipeline/sync_pipeline.py`

Per i casi più avanzati, il toolkit include un **framework di sincronizzazione dati**:

- classe `SyncPipeline` per orchestrare un intero flusso **Extract → Transform → Load**;
- enum `SyncMode` per definire il comportamento:

  - `INSERT`, `UPDATE`, `UPSERT`, `DELETE`,
  - modalità ibride per gestire dataset complessi;

- possibilità di:

  - leggere da qualsiasi sorgente (DB, CSV, API…), grazie a funzioni di estrazione pluggable,
  - applicare `FieldMapper` come livello di trasformazione,
  - inviare i dati a Salesforce con gestione di errori, retry e report finale (`SyncResult`).

L’interfaccia è pensata per essere **estendibile**: puoi collegare qualsiasi sorgente custom senza modificare il core del toolkit.

---

### 5. Logging production-ready: `logging/logger.py`

Il modulo di logging nasce con in mente ambienti reali:

- configurazione centralizzata dei logger,
- output su file e console,
- **log rotation** automatica,
- livelli configurabili (`DEBUG` → `ERROR`),
- messaggi arricchiti con contesto (oggetto Salesforce, batch, pipeline, ecc.).

In pratica, non solo *logga*, ma rende **osservabile** il processo di integrazione, facilitando debugging e incident analysis.

---

### 6. Interfaccia a riga di comando: `cli.py`

Per rendere il toolkit subito sfruttabile anche senza scrivere codice, è disponibile una CLI (pensata per essere installata come comando globale).

Da terminale è possibile:

- testare l’autenticazione,
- eseguire query SOQL veloci,
- creare/aggiornare/eliminare record,
- lanciare pipeline di sync definite in YAML.

Questo rende Kinetic Core adatto sia a task occasionali (un export veloce) sia a pipeline schedulate via cron/CI.

---

## DevOps & Distribuzione

Uno degli obiettivi principali era rendere questo toolkit un **prodotto** distribuibile e riproducibile, non solo codice sorgente.

### 🐳 Docker & Riproducibilità
Il progetto include un ambiente **Docker** completo che isola l'esecuzione.
- `Dockerfile` ottimizzato per Python 3.11-slim.
- Volume mapping intelligente per gestire certificati (`certs/`) e config senza "sporcare" il container.
- Garantisce che i test (e le pipeline) girino allo stesso modo su un laptop Windows, un Mac o un server Linux CI/CD.

### 📦 Pubblicazione PyPI
Il pacchetto è strutturato secondo gli standard moderni di packaging Python (`pyproject.toml` / `setup.py`):
- Build automatico di wheel (`.whl`) e source distribution (`.tar.gz`).
- Pronto per la distribuzione su **PyPI**, rendendolo installabile con un semplice:
  ```bash
  pip install kinetic-core
  ```

---

## Configurazione dichiarativa

Nel repository sono presenti file di esempio che mostrano l’approccio **config-first**:

- `config/.env.example` – definisce tutte le variabili ambientali attese (credenziali, login URL, logging, ecc.);
- `config/sync_config_example.yaml` – esempio di configurazione per una pipeline ETL:

  - sorgente dati,
  - mapping dei campi,
  - oggetto Salesforce di destinazione,
  - modalità di sync,
  - batch size e opzioni avanzate.

Questo approccio permette di:

- riusare la stessa pipeline in ambienti diversi modificando solo la configurazione,
- versionare il comportamento ETL insieme al codice,
- rendere il sistema più leggibile per team misti dev/analyst.

---

## Esempi & documentazione

Per ridurre il tempo di onboarding, il progetto include una serie di esempi pratici in `examples/` e guide dettagliate:

- **Guide**: `QUICK_START`, `DOCKER_GUIDE` e `PUBLISHING_GUIDE` per coprire ogni aspetto, dall'uso base alla pubblicazione.
- **Esempi**: Script completi per CRUD (`02_crud_operations.py`) e pipeline (`03_data_sync_pipeline.py`).

---

## Cosa dimostra questo progetto

Più che una singola feature, **Kinetic Core** rappresenta un modo di progettare integrazioni enterprise:

- **Design di librerie riusabili** in Python, con moduli chiari e separazione delle responsabilità (SOLID).
- **Integrazione profonda con API Salesforce**, incluse le complessità di autenticazione e gestione sessioni.
- **Progettazione di pipeline ETL** robuste, osservabili e configurabili.
- **DevOps Mindset**: Containerizzazione (**Docker**), Packaging (**PyPI**) e gestione configurazioni (YAML/.env).
- **Attenzione alla production-readiness**: logging, struttura del pacchetto, esempi, documentazione, test.

In un contesto reale, questo toolkit permette di:

- sostituire script sparsi e fragili con un’unica base solida,
- standardizzare le integrazioni Salesforce tra progetti diversi,
- ridurre drasticamente il tempo necessario a costruire nuove pipeline.

> Se vuoi approfondire l’implementazione interna dei moduli (`auth`, `core`, `mapping`, `pipeline`, `logging`), puoi esplorare il codice sorgente direttamente su GitHub.
>
> **[Esplora il progetto su GitHub](https://github.com/KineticMCP/kinetic-core)**
