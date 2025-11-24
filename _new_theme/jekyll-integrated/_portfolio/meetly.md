---
layout: portfolio
title: "Meetly"
date: 2025-09-24
description: "Meetly è un assistente AI autonomo progettato per automatizzare completamente il processo di pianificazione degli appuntamenti, integrandosi con sistemi esterni e gestendo conversazioni complesse."
image: "/assets/images/portfolio/meetly/meetly.jpg"
image-header: "/assets/images/portfolio/meetly/meetly.jpg"
image-paint: "/assets/images/portfolio/meetly/meetly.jpg"
tags: [Chatbot, AI, Backend, Python, FastAPI, Docker, Google Calendar API, System Integration, Automation]
---

> *"L'obiettivo non era creare un semplice chatbot, ma un agente autonomo affidabile. Un sistema capace di comprendere, pianificare e agire nel mondo reale, liberando tempo e riducendo l'attrito nei processi di business."*

**Meetly** è la materializzazione di una visione: quella di un assistente digitale intelligente che non si limita a rispondere a domande, ma gestisce attivamente un intero processo di business. Nato come un'esplorazione approfondita dell'**ingegneria dei sistemi AI-centrici**, questo progetto dimostra come orchestrare tecnologie diverse per creare una soluzione end-to-end robusta, scalabile e genuinamente utile.

L'idea era semplice ma sfidante: costruire un sistema di prenotazione appuntamenti che potesse essere integrato in qualsiasi sito web con un semplice copia-incolla, ma che nascondesse al suo interno una potente architettura guidata dall'intelligenza artificiale.

### Architettura del Sistema: Un Deep Dive

L'architettura di Meetly è stata progettata per essere modulare e disaccoppiata, permettendo a ogni componente di evolvere in modo indipendente. Si articola in quattro strati principali, ognuno con una responsabilità specifica.

*(Qui andrebbe inserito un diagramma architetturale che mostra il flusso dal Widget Frontend fino ai servizi esterni come Google Calendar e OpenAI).*

#### 1. Presentation Layer (Widget Web Integrabile)
Il punto di contatto con l'utente finale è un **widget di chat leggero e personalizzabile**. Realizzato con **HTML, CSS e JavaScript** vanilla, è progettato per essere integrato in qualsiasi pagina web con il minimo sforzo. Questo strato, contenuto nelle directory `static/` e `templates/`, ha un unico scopo: fornire un'interfaccia utente pulita e reattiva per la conversazione, delegando tutta l'intelligenza al backend. La sua semplicità è una scelta di design deliberata per massimizzare la compatibilità e la velocità di caricamento.

#### 2. Application Layer (API & Business Logic)
Il cuore del sistema è un'API RESTful costruita con **FastAPI**, che funge da controllore centrale. Questo strato (`main.py`, `auth.py`) è responsabile di:
*   **Esporre API Sicure:** Fornisce endpoint protetti da token per la comunicazione con il widget frontend.
*   **Orchestrazione dei Servizi:** Riceve i messaggi dell'utente, li inoltra all'Intelligence Layer e coordina le chiamate agli altri servizi (come il calendario o le email) in base alla risposta dell'AI.
*   **Gestione dello Stato:** Mantiene il contesto della conversazione per ogni utente, permettendo al chatbot di avere memoria e portare a termine dialoghi complessi su più turni.

#### 3. Intelligence Layer (Conversational AI)
Qui risiede l'intelligenza di Meetly. Questo strato, implementato in `chat.py`, sfrutta un modello linguistico avanzato (**GPT-4o**) per alimentare la conversazione. La sua implementazione va oltre una semplice chiamata API:
*   **Ingegneria dei Prompt:** Utilizza un `SYSTEM_PROMPT` meticolosamente progettato che istruisce l'AI a seguire un flusso di prenotazione preciso e strutturato: raccolta informazioni (nome, email, data), verifica della disponibilità e richiesta di conferma.
*   **Estrazione di Entità:** Analizza le risposte dell'utente per estrarre informazioni chiave (date, orari, email) utilizzando sia l'AI che espressioni regolari.
*   **Logica Dinamica:** In base allo stato della conversazione, decide autonomamente se procedere, chiedere ulteriori dettagli o suggerire alternative, rendendo il dialogo naturale e orientato all'obiettivo.

#### 4. Integration & Services Layer (Connessione al Mondo Esterno)
Questo strato connette Meetly ai servizi esterni, rendendolo veramente funzionale.
*   **Integrazione con Google Calendar (`calendar_api.py`):** È il componente più complesso. Gestisce l'autenticazione sicura tramite **OAuth2**, controlla in tempo reale la disponibilità sul calendario, suggerisce slot alternativi quando un orario è occupato e, infine, crea l'evento, aggiungendo automaticamente un link per Google Meet e inviando gli inviti ai partecipanti.
*   **Servizio di Notifica (`mailer.py`):** Una volta confermato un appuntamento, questo modulo si occupa di inviare un'email di riepilogo all'utente, completando il processo e fornendo una conferma tangibile.

### Tecnologie e Competenze Chiave

La scelta di ogni tecnologia è stata guidata da principi di performance, scalabilità e aderenza agli standard moderni dello sviluppo software.

*   **Python & FastAPI:** Python è il linguaggio che unifica l'intero stack, dall'API all'AI. FastAPI è stato scelto per le sue performance eccezionali, la natura asincrona (ideale per gestire operazioni I/O come le chiamate API esterne) e la generazione automatica della documentazione, che promuove la creazione di API pulite e manutenibili.

*   **Modelli LLM (OpenAI GPT-4o):** Il cervello del sistema. La sua integrazione dimostra la capacità di usare l'AI non come un gadget, ma come un motore funzionale per automatizzare compiti complessi basati sul linguaggio naturale. L'attenzione all'ingegneria dei prompt è fondamentale per renderlo affidabile.

*   **Google Calendar API & OAuth2:** L'integrazione con Google Calendar mostra la capacità di interfacciarsi con API di terze parti complesse e di gestire flussi di autenticazione sicuri come OAuth2, un requisito fondamentale per qualsiasi applicazione enterprise.

*   **Docker & Docker Compose:** L'intero sistema è containerizzato. Questo non solo semplifica drasticamente il processo di deployment (`docker-compose up`), ma garantisce anche che l'ambiente di sviluppo sia identico a quello di produzione, eliminando il classico problema del "funziona sulla mia macchina". È un'applicazione pratica dei principi DevOps.

*   **JavaScript, HTML & CSS:** La scelta di usare tecnologie web standard per il frontend dimostra la capacità di costruire soluzioni full-stack, garantendo che il backend potente sia completato da un'interfaccia utente funzionale e facilmente integrabile.

### Cosa Dimostra Questo Progetto

**Meetly** non è solo un chatbot. È una risposta pratica alla domanda: "Come si progetta, si costruisce e si orchestra un sistema software moderno che sfrutta l'intelligenza artificiale per automatizzare un processo reale, end-to-end?".

Dimostra competenza in:
*   **System Design & Architettura:** Progettare sistemi modulari, scalabili e disaccoppiati.
*   **Sviluppo Backend:** Costruire API performanti, sicure e ben documentate.
*   **Integrazione di Sistemi Complessi:** Far comunicare tra loro servizi eterogenei (AI, API di terze parti, servizi email) in modo affidabile.
*   **Ingegneria dell'AI:** Sfruttare i modelli linguistici in modo mirato e controllato per risolvere problemi di business.
*   **Automazione dei Processi:** Analizzare un processo manuale e tradurlo in un flusso di lavoro completamente automatizzato.
*   **Pratiche DevOps:** Utilizzare la containerizzazione per creare applicazioni portabili e facili da distribuire.

> Ti invito a esplorare il codice sorgente su GitHub per analizzare i dettagli implementativi di ogni componente descritto.
> 
> **[Esplora il progetto su GitHub](https://github.com/antonio-backend-projects/meetly)**
