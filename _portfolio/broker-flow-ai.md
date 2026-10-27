---
layout: portfolio
title: "BrokerFlow AI - Deep Dive Architettonico"
date: 2025-09-20
description: "Un'analisi approfondita di BrokerFlow AI, un progetto dimostrativo che esplora architetture software complesse, intelligenza artificiale e automazione end-to-end nel settore assicurativo."
image: "/assets/images/portfolio/broker-flow-ai/broker-flow-ai.jpg"
image-header:
image-paint: "/assets/images/portfolio/broker-flow-ai/broker-flow-ai.jpg"
og_image: "og/broker-flow-ai.jpg"
tags: [System Design, Backend, AI, Python, FastAPI, Docker, Automation, Data Science, Architettura]
---

> *"Questo non è solo un progetto. È un'esplorazione ingegneristica: la costruzione di un gemello digitale di una soluzione enterprise per dimostrare come l'automazione intelligente possa rivoluzionare un intero settore."*

**BrokerFlow AI** è nato come un' sfida personale: progettare e costruire da zero un sistema complesso, modulare e intelligente, capace di risolvere un problema reale. L'ho concepito come un **laboratorio di ingegneria del software** per sperimentare, applicare e dimostrare un ampio spettro di competenze che vanno dal **system design** al **backend engineering**, fino all'integrazione di **modelli di intelligenza artificiale**.

L'obiettivo è simulare una piattaforma B2B per il settore assicurativo, un ambito tradizionalmente lento e appesantito da processi manuali. BrokerFlow AI agisce come un agente autonomo che prende in carico una richiesta di preventivo (contenuta in un'email o in un PDF) e la processa attraverso una catena di montaggio automatizzata, fino a produrre un'offerta completa e una comunicazione pronta per il cliente.

Questo documento è un'immersione profonda nell'architettura, nelle scelte tecnologiche e nelle sfide affrontate. Sebbene sia un **work-in-progress**, ogni sua parte è stata pensata per essere scalabile e robusta, come se fosse destinata a un ambiente di produzione reale.

---

### 🏛️ Architettura a Livelli: un'Analisi Dettagliata

L'architettura di BrokerFlow AI è stratificata per separare le responsabilità (Separation of Concerns), garantendo manutenibilità e scalabilità. Ogni livello ha uno scopo preciso.

#### 1. Presentation Layer (Frontend)
Il volto dell'applicazione è una dashboard interattiva costruita con **Streamlit**. La scelta non è casuale: Streamlit permette di creare interfacce web data-centriche direttamente in Python, con una velocità di sviluppo impareggiabile. Questo strato, contenuto nella directory `frontend/`, serve a:
*   **Visualizzare i dati:** Mostra lo stato delle richieste, le performance e i KPI in tempo reale.
*   **Interagire con il sistema:** Permette agli utenti (amministratori, broker) di monitorare il flusso, gestire gli utenti e, in futuro, forzare azioni manuali.
*   **Prototipazione rapida:** Dimostra la capacità di costruire rapidamente strumenti interni funzionali e utili senza dover ricorrere a complessi framework JavaScript.

#### 2. Application Layer (API & Business Logic)
Questo è il cuore pulsante del sistema. È composto da due elementi principali:
*   **API B2B (`api_b2b.py`):** Un'API RESTful sviluppata con **FastAPI**, progettata per essere il punto di contatto per integrazioni esterne (B2B2B). FastAPI è stato scelto per le sue performance eccezionali, il supporto nativo all'asincronia e la generazione automatica di documentazione interattiva (Swagger UI), fondamentale per le integrazioni enterprise.
*   **Moduli di Business Logic (`modules/`):** Questa directory contiene la logica applicativa suddivisa in moduli specializzati, ognuno responsabile di una fase specifica del workflow. Tra i principali:
    *   `auth.py`: Gestisce l'autenticazione e l'autorizzazione basata su ruoli e token JWT.
    *   `extract_data.py`: Il punto di ingresso dei dati non strutturati.
    *   `classify_risk.py`: Utilizza l'AI per categorizzare il tipo di rischio.
    *   `compile_forms.py`: Si occupa della generazione di documenti PDF.
    *   `generate_email.py`: Compone le comunicazioni per i clienti.

#### 3. Processing Layer (AI & Core Automation)
Qui avviene la "magia". Questo strato è responsabile della trasformazione dei dati grezzi in informazioni strutturate e azioni concrete.
*   **Pipeline di Estrazione Dati:** Il modulo `extract_data.py` implementa una logica sofisticata per gestire la varietà dei documenti del mondo reale. Prima rileva se un PDF è **digitale** (con testo) o **scansionato** (un'immagine). Nel primo caso, usa **PyMuPDF** per un'estrazione testuale rapida e precisa. Nel secondo, attiva una pipeline OCR con **Tesseract** e **pdf2image** per digitalizzare il contenuto. Questo approccio duale dimostra la capacità di gestire input eterogenei e ottimizzare le risorse.
*   **Intelligenza Artificiale (LLM):** Una volta estratto il testo grezzo, questo viene inviato a un modello linguistico avanzato (**GPT-4o**). Attraverso un'attenta **ingegneria dei prompt**, il modello non si limita a leggere, ma *comprende* il contesto e restituisce un **JSON strutturato** contenente tutte le informazioni chiave (dati del cliente, dettagli del rischio, ecc.). Questa è la competenza chiave che permette al sistema di interfacciarsi con il caos del mondo reale e trasformarlo in ordine.

#### 4. Integration & Data Layer
*   **Integration Layer:** Il sistema è progettato per non vivere in isolamento. Moduli come `b2b_integrations.py` sono predisposti per dialogare con API di terze parti (es. portali di compagnie assicurative, sistemi di pagamento), mostrando una progettazione orientata all'espandibilità.
*   **Data Layer (`db.py`, `schema.sql`):** La persistenza dei dati è affidata a un database relazionale **MySQL**, gestito tramite un schema SQL ben definito. Questo strato si occupa di tracciare lo stato di ogni richiesta, gestire le anagrafiche di clienti e utenti, archiviare le polizze generate e alimentare il sistema di tracking per i rinnovi. La scelta di un database SQL garantisce integrità, transazionalità e la possibilità di eseguire query complesse per analisi e reporting.

### 🛠️ Stack Tecnologico: Gli Strumenti del Mestiere

La scelta di ogni tecnologia è stata deliberata per dimostrare competenza in un ecosistema moderno e performante.

*   **Python:** Il linguaggio che unifica l'intero stack, dal backend all'AI, fino al frontend, garantendo coerenza e velocità di sviluppo.
*   **FastAPI:** Scelto per la sua natura asincrona e le performance ai vertici della categoria, ideale per costruire servizi API robusti e scalabili.
*   **Docker & Docker Compose:** Fondamentali per applicare i principi **DevOps** e **Infrastructure-as-Code**. L'intero ambiente (applicazione, database, servizi accessori) è containerizzato, garantendo una configurazione riproducibile, un deployment semplificato e un isolamento totale dall'ambiente sottostante.
*   **Modelli LLM (OpenAI GPT-4o):** Il cervello del sistema. La sua integrazione dimostra la capacità di sfruttare l'AI per risolvere problemi che erano quasi impossibili da automatizzare con la programmazione tradizionale, come la comprensione del linguaggio naturale in documenti non strutturati.
*   **PyMuPDF, Tesseract, pdf2image:** La cassetta degli attrezzi per la manipolazione dei PDF. Il loro uso combinato mostra la capacità di costruire pipeline di elaborazione documenti robuste e resilienti, capaci di affrontare la scarsa qualità e la varietà dei formati di input.

### 🚀 Stato del Progetto e Visione Futura

BrokerFlow AI è un progetto vivo, un **sandbox di sviluppo** in continua evoluzione. La sua natura di proof-of-concept lo rende il terreno ideale per sperimentare nuove tecnologie e architetture.

La visione futura è quella di trasformarlo in un **MVP (Minimum Viable Product)** completo, con possibili sviluppi che includono:
*   **Espansione delle integrazioni:** Connessione a API reali di compagnie assicurative.
*   **Addestramento di modelli specifici:** Fine-tuning di modelli open-source per migliorare ulteriormente la precisione nell'estrazione dati per nicchie assicurative specifiche.
*   **Interfaccia utente più ricca:** Sviluppo di un frontend completo in React o Vue.js per offrire un'esperienza utente più sofisticata.

---

> Questo progetto è la mia risposta alla domanda: "Come applicheresti le tue competenze per costruire una soluzione complessa, end-to-end e ad alto valore aggiunto?".
> 
> **Ti invito a esplorare il codice sorgente su GitHub per vedere i dettagli implementativi di ogni componente descritto.**
> 
> **[Esplora il progetto su GitHub](https://github.com/broker-flow-ai/broker-flow-ai)**