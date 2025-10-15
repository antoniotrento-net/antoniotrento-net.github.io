---
layout: portfolio
title: "Cloudetta"
date: 2025-10-05
description: "Cloudetta è un ecosistema digitale open-source e sovrano per PMI. Integra ERP, marketing, BI, e collaborazione in uno stack Docker unificato, per un controllo totale dei dati e dei processi aziendali."
image: "/assets/images/portfolio/cloudetta/cloudetta.jpg"
image-header: "/assets/images/portfolio/cloudetta/cloudetta.jpg"
image-paint: "/assets/images/portfolio/cloudetta/cloudetta.jpg"
tags: [Open Source, DevOps, Cloud, Docker, Odoo, Django, Mautic, Apache Superset, Business Intelligence, n8n, Prometheus, Grafana, Loki, CrowdSec, Restic, System Architecture, SaaS]
---

> *"L’obiettivo non era costruire l’ennesima suite gestionale, ma una piattaforma unificata, realmente open-source, capace di offrire a qualsiasi azienda — anche la più piccola — la potenza e l’integrazione di un ecosistema enterprise."*

**Cloudetta** nasce da un’idea precisa: **rendere accessibile la complessità aziendale**, fornendo un’infrastruttura moderna, scalabile e completamente automatizzata, basata su tecnologie open-source mature e interoperabili.

Il progetto rappresenta la sintesi di anni di esperienza in **integrazione di sistemi, DevOps e architetture cloud modulari**, racchiusa in un toolkit unico, pronto per essere usato come base per prodotti SaaS, ERP o CRM avanzati.

---

> "L'obiettivo di Cloudetta non è fornire software, ma restituire sovranità. È un ecosistema digitale integrato, open-source e self-hosted, che permette alle aziende di possedere e controllare i propri strumenti e i propri dati, liberandosi dal vendor lock-in."

---

## La Visione: Un Ecosistema Digitale Unificato

Cloudetta nasce per risolvere la frammentazione che affligge le PMI: decine di servizi cloud disconnessi, costi mensili crescenti e dati aziendali sparsi presso terzi. La piattaforma aggrega i migliori strumenti open-source in un unico **stack coerente e pre-integrato**, orchestrato da Docker e installabile su qualsiasi infrastruttura (cloud, on-premise, VPS).

Il risultato è un ambiente di lavoro centralizzato, dove i processi fluiscono senza interruzioni tra i vari reparti, dall'ERP al marketing, dalla collaborazione alla business intelligence.

---

## I Componenti: Una Suite Aziendale Completa

Cloudetta è modulare. Ogni strumento è un container indipendente ma interconnesso, raggruppato per aree funzionali.

### 1. Gestione e Operatività
Il nucleo che governa l'azienda.
- **Odoo (ERP):** La colonna vertebrale gestionale. Unisce CRM, vendite, acquisti, magazzino, contabilità e fatturazione elettronica italiana (l10n_it, l10n_it_edi).
- **Django + Stripe (SaaS & Billing):** Il motore per la creazione di servizi SaaS, gestisce utenti, abbonamenti, pagamenti e fornisce API sicure per l'integrazione.

### 2. Marketing e Comunicazione
Strumenti per acquisire clienti e facilitare la collaborazione interna.
- **Mautic (Marketing Automation):** Piattaforma per la gestione di campagne email, lead nurturing, segmentazione del pubblico e landing page.
- **Mattermost (Team Chat):** L'alternativa open-source a Slack. Canali di discussione, team, integrazioni e notifiche centralizzate per una comunicazione interna fluida.

### 3. Produttività e Collaborazione
L'ufficio digitale dove il lavoro viene svolto e documentato.
- **Nextcloud (File Sharing):** Archiviazione, condivisione e sincronizzazione sicura dei file aziendali, con client desktop e mobile.
- **Redmine (Project Management):** Strumento robusto per il tracciamento di ticket, la gestione di progetti complessi e il monitoraggio delle attività.
- **DokuWiki (Knowledge Base):** Un wiki semplice e potente per costruire la base di conoscenza interna, documentare procedure e manuali.

### 4. Analisi e Decisioni Strategiche
Trasformare i dati grezzi in insight per guidare le scelte aziendali.
- **Apache Superset (Business Intelligence):** Il cruscotto di BI che si connette ai database di Odoo, Django e Mautic. Permette di creare dashboard interattive per visualizzare KPI di vendita, metriche di marketing e andamento degli abbonamenti.
- **Plausible / Umami (Web Analytics):** Una soluzione di analytics cookieless e rispettosa della privacy per monitorare il traffico e l'utilizzo delle applicazioni web (es. portale Django, sito Odoo) senza compromettere i dati degli utenti.

---

## Il Sistema Nervoso: n8n per l'Automazione dei Workflow

**n8n** è il collante che trasforma questa collezione di strumenti in un vero ecosistema. Attraverso i suoi workflow visuali, automatizza i processi che attraversano più applicazioni.

**Esempi di flussi di lavoro integrati:**
- **Onboarding Cliente Automatizzato:** Un nuovo ordine in **Odoo** scatena un workflow in **n8n** che:
  1. Aggiunge il cliente a una campagna di benvenuto su **Mautic**.
  2. Crea un task di "kick-off" su **Redmine** per il project manager.
  3. Invia una notifica al team vendite su un canale **Mattermost** dedicato.
  4. Crea una cartella cliente condivisa su **Nextcloud**.
- **Sincronizzazione Dati:** I dati dei clienti vengono mantenuti allineati tra **Odoo** e **Django**.
- **Notifiche Intelligenti:** Eventi critici (es. un pagamento fallito su Stripe) generano ticket automatici su **Redmine** e allerte su **Mattermost**.

---

## Architettura e Fondamenta DevOps

Cloudetta è costruita su principi DevOps per garantire stabilità, sicurezza e manutenibilità.

- **Gateway e Sicurezza Perimetrale:**
  - **Caddy Server:** Reverse proxy automatico che gestisce tutto il traffico in entrata, fornisce certificati SSL/TLS e instrada le richieste ai servizi corretti.
  - **CrowdSec:** Sistema di prevenzione delle intrusioni (IPS) che analizza i log di Caddy per identificare e bloccare traffico malevolo in tempo reale.

- **Stack di Osservabilità (Monitoring & Logging):**
  - **Prometheus & Grafana:** Monitoraggio proattivo delle performance di ogni container, dell'uso di CPU/RAM e dello stato dell'infrastruttura. Dashboard preconfigurate in Grafana offrono una vista completa sulla salute del sistema.
  - **Loki & Promtail:** Sistema di logging centralizzato. Tutti i log dei container vengono raccolti, indicizzati e resi ricercabili tramite Grafana, semplificando il troubleshooting.

- **Data Integrity e Disaster Recovery:**
  - **Restic & MinIO:** Soluzione di backup robusta. Restic esegue backup crittografati, deduplicati e incrementali di tutti i volumi Docker e li archivia su uno storage S3-compatibile fornito da MinIO, garantendo restore rapidi e sicuri.
  - **Trivy:** Scanner di vulnerabilità che analizza periodicamente le immagini Docker in uso per identificare falle di sicurezza note, permettendo un hardening proattivo.

---

## Diagramma Architetturale Interattivo

Questo diagramma mostra come i vari componenti di Cloudetta interagiscono tra loro, dal gateway di ingresso fino ai servizi di backend e agli stack operativi.
<style>
/* Wrapper base */
.mermaid-wrap {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;                 /* sfondo bianco anche non-FS */
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(0,0,0,.05);
}

/* Contenuto mermaid */
.mermaid-wrap .mermaid {
  display: block;
  overflow: auto;
  min-height: 520px;                /* leggibile anche non in FS */
  padding: 12px;
}

/* L’SVG di Mermaid si adatti al contenitore */
.mermaid-wrap svg {
  width: 100%;
  height: auto;
}

/* Toolbar */
.mermaid-toolbar{
  position:absolute; top:.5rem; right:.5rem; z-index:2;
  padding:.35rem .55rem; border:0; border-radius:8px; cursor:pointer;
  background:rgba(0,0,0,.62); color:#fff; font:600 14px/1 system-ui;
  box-shadow: 0 2px 8px rgba(0,0,0,.2);
}

/* FULLSCREEN: centrato, quasi tutto schermo, sfondo bianco */
.mermaid-wrap:fullscreen,
.mermaid-wrap:-webkit-full-screen {
  background: #fff;           /* sfondo bianco */
  display: flex;              /* centrare verticalmente/orizzontalmente */
  align-items: center;
  justify-content: center;
}

/* il contenitore del diagramma si espande in FS */
.mermaid-wrap:fullscreen .mermaid,
.mermaid-wrap:-webkit-full-screen .mermaid {
  background: #fff;
  width: 100vw;
  height: 100vh;              /* spazio utile per centrare */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;                 /* niente padding in FS */
  overflow: hidden;           /* tolgo scrollbar esterna */
}

/* l’SVG occupa quasi tutto lo schermo, mantenendo proporzioni */
.mermaid-wrap:fullscreen svg,
.mermaid-wrap:-webkit-full-screen svg {
  width: 95vw;                /* larghezza quasi piena */
  height: 92vh;               /* altezza quasi piena */
  max-width: 95vw;
  max-height: 92vh;
  display: block;
  margin: 0 auto;
}

/* tema chiaro coerente con la pagina (fallback se il tema del sito è scuro) */
:root {
  color-scheme: light;
}
</style>

<div id="cloudetta-diagram" class="mermaid-wrap">
  <button class="mermaid-toolbar" type="button" aria-label="Schermo intero">⛶</button>
<div class="mermaid">
graph TD
    subgraph Utente
        Client[Browser / Client API]
    end

    subgraph "Gateway & Sicurezza"
        Caddy(Caddy Reverse Proxy)
        CrowdSec(CrowdSec IPS)
    end

    subgraph "Applicazioni Core"
        Django(Django + Stripe)
        Odoo(Odoo ERP)
        Mautic(Mautic)
        Mattermost(Mattermost)
        Nextcloud(Nextcloud)
        Redmine(Redmine)
        DokuWiki(DokuWiki)
    end

    subgraph "Business Intelligence & Analytics"
        Superset(Apache Superset)
        Analytics(Analytics Cookieless)
    end
    
    subgraph "Automazione"
        N8N(n8n Workflow)
    end

    subgraph "Database"
        PostgresOdoo[(PostgreSQL - Odoo)]
        PostgresDjango[(PostgreSQL - Django)]
        PostgresMattermost[(PostgreSQL - Mattermost)]
        MariaDBNextcloud[(MariaDB - Nextcloud)]
        MariaDBMautic[(MariaDB - Mautic)]
        MariaDBRedmine[(MariaDB - Redmine)]
    end

    subgraph "Stack di Osservabilità"
        Grafana(Grafana)
        Prometheus(Prometheus)
        Loki(Loki)
        Promtail(Promtail)
    end

    subgraph "Backup & Storage"
        Restic(Restic Backup)
        MinIO(MinIO S3 Storage)
    end

    %% Connessioni Principali
    Client --> Caddy
    Caddy --> Django
    Caddy --> Odoo
    Caddy --> Mautic
    Caddy --> Mattermost
    Caddy --> Nextcloud
    Caddy --> Redmine
    Caddy --> DokuWiki
    Caddy --> Superset
    Caddy --> Grafana
    Caddy --> Analytics

    %% Connessioni Database
    Django --> PostgresDjango
    Odoo --> PostgresOdoo
    Mattermost --> PostgresMattermost
    Nextcloud --> MariaDBNextcloud
    Mautic --> MariaDBMautic
    Redmine --> MariaDBRedmine
    Superset --> PostgresOdoo
    Superset --> PostgresDjango
    Superset --> MariaDBMautic

    %% Connessioni Automazione (n8n)
    N8N -.-> Django
    N8N -.-> Odoo
    N8N -.-> Mautic
    N8N -.-> Mattermost
    N8N -.-> Nextcloud
    N8N -.-> Redmine
    
    %% Connessioni Operative (Logging, Monitoring, Sicurezza, Backup)
    Caddy -- Log --> CrowdSec
    Caddy -- Log --> Promtail
    Promtail -- Log --> Loki
    Loki --> Grafana
    Prometheus --> Grafana
    Django -- "Metriche & Log" --> Prometheus
    Django -- "Metriche & Log" --> Promtail
    Odoo -- "Metriche & Log" --> Prometheus
    Odoo -- "Metriche & Log" --> Promtail
    Restic -- Backup dei Volumi --> MinIO

</div>
</div>
<script defer src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', async () => {
  // Tema chiaro + impostazioni di resa più nitide
  mermaid.initialize({
    startOnLoad: false,                 // render controllato
    securityLevel: 'loose',
    theme: 'base',                      // base è neutro/chiaro
    themeVariables: {
      background: '#ffffff',            // sfondo bianco
      primaryColor: '#ffffff',
      primaryTextColor: '#111827',
      primaryBorderColor: '#e5e7eb',
      lineColor: '#374151',
      secondaryColor: '#f9fafb',
      tertiaryColor: '#f3f4f6',
      fontFamily: 'Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, "Apple Color Emoji", "Segoe UI Emoji"'
    },
    flowchart: {
      htmlLabels: true,
      padding: 8,                       // riduce margini e “scatola nera”
      useMaxWidth: true                 // usa tutta la larghezza disponibile
    }
  });

  const wrap  = document.getElementById('cloudetta-diagram');
  const btn   = wrap?.querySelector('.mermaid-toolbar');
  const block = wrap?.querySelector('.mermaid');
  if (!wrap || !block) return;

  // Render del SOLO blocco
  await mermaid.run({ nodes: [block] });

  const svg = wrap.querySelector('svg');

  // Fit “responsive” fuori da full-screen
  function fitNormal() {
    if (!svg) return;
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    svg.style.width = '100%';
    svg.style.height = 'auto';
  }
  fitNormal();
  window.addEventListener('resize', fitNormal);

  // Fullscreen toggle
  btn?.addEventListener('click', async () => {
    if (!document.fullscreenElement) {
      await wrap.requestFullscreen?.();
      setTimeout(() => { /* ridisegna bounding box in FS */
        // In FS non forziamo width/height: ci pensa il CSS FS sopra
        // ma un tick aiuta i browser a ricalcolare il layout
      }, 120);
    } else {
      await document.exitFullscreen?.();
    }
  });

  // quando entri/esci dal full-screen, un piccolo delay per stabilizzare layout
  document.addEventListener('fullscreenchange', () => {
    setTimeout(() => {
      if (!document.fullscreenElement) {
        fitNormal(); // rimetto il comportamento responsive standard
      }
    }, 120);
  }, { passive: true });
});
</script>





## Tabella Tecnologica Completa
<div class="table-responsive">
  {{ "
| Ambito | Strumento | Tecnologia | Ruolo Principale |
|---|---|---|---|
| **Gateway** | Caddy | Go | Reverse Proxy, SSL automatico, Routing |
| **ERP & CRM** | Odoo | Python, PostgreSQL | Gestione aziendale, Fatturazione Elettronica |
| **SaaS & Billing** | Django | Python, PostgreSQL | Gestione abbonamenti, API, pagamenti Stripe |
| **Marketing** | Mautic | PHP, MariaDB | Marketing Automation, Campagne Email |
| **Team Chat** | Mattermost | Go, React, PostgreSQL | Comunicazione interna, Notifiche |
| **File Storage** | Nextcloud | PHP, MariaDB | Archiviazione e condivisione file |
| **Project Mgmt** | Redmine | Ruby on Rails, MariaDB | Ticketing, Gestione progetti |
| **Knowledge Base** | DokuWiki | PHP | Documentazione interna, Wiki |
| **Automazione** | n8n | Node.js, Vue.js | Orchestrazione workflow tra servizi |
| **Business Intel.**| Apache Superset | Python, React | Creazione dashboard e analisi dati |
| **Web Analytics** | Plausible/Umami | Go/Node.js | Statistiche d'uso cookieless |
| **Monitoring** | Prometheus, Grafana | Go, TypeScript | Raccolta metriche e visualizzazione |
| **Logging** | Loki, Promtail | Go | Aggregazione e ricerca log |
| **Backup** | Restic, MinIO | Go | Backup crittografati su storage S3 |
| **Sicurezza** | CrowdSec, Trivy | Go | Intrusion Prevention, Scansione vulnerabilità |
| **Orchestrazione**| Docker Compose | YAML | Definizione e gestione dello stack |
" | markdownify }}
</div>
---

## Competenze Dimostrate

Lo sviluppo di Cloudetta dimostra una competenza profonda e trasversale in:

- **System Architecture & DevOps:** Progettazione di architetture a microservizi complesse, containerizzate e resilienti.
- **Full-Stack Development:** Padronanza di ecosistemi diversi (Python/Django, PHP, Ruby, Go, Node.js).
- **Integrazione di Sistemi:** Capacità di far dialogare applicativi eterogenei tramite API, webhook e middleware di automazione (n8n).
- **Cloud & Infrastructure Management:** Gestione di stack Docker, networking, storage persistente e sicurezza perimetrale.
- **Osservabilità e Affidabilità (SRE):** Implementazione di stack completi per monitoring, logging e alerting (Prometheus, Grafana, Loki).
- **Sicurezza Informatica:** Hardening di sistemi, gestione degli accessi, backup e disaster recovery (Caddy, CrowdSec, Restic).
- **Business Process Analysis:** Comprensione dei flussi aziendali per tradurli in soluzioni tecniche integrate (ERP, CRM, Marketing).

---

## 🧰 DevOps e Automazione

Cloudetta è costruita attorno a **Docker Compose**, ma l’intera architettura è facilmente migrabile a **Kubernetes** o **Portainer**.
Ogni container è configurato per essere stateless e facilmente sostituibile.

* Logging centralizzato (stdout + file rotazione)
* Volumi persistenti per ogni servizio
* Healthcheck automatici
* Compatibilità con CI/CD (GitHub Actions)

---

## 📊 Caso d’Uso Tipico

Un’azienda può usare Cloudetta per:

1. Gestire clienti e contratti su Odoo
2. Creare abbonamenti SaaS via Django + Stripe
3. Automatizzare notifiche e ticket con n8n + Redmine
4. Archiviare documenti e fatture in Nextcloud
5. Documentare processi su DokuWiki
6. Fare backup automatici ogni notte

Tutto in **un unico ecosistema coerente**, installabile in meno di 15 minuti.

---

## 🧑‍💻 Competenze Dimostrate

Cloudetta dimostra competenza profonda in:

* **System Architecture & DevOps:** progettazione di stack containerizzati modulari.
* **Full-stack Development:** Django, Odoo, API REST, automazioni.
* **Cloud Integration:** collegamento tra servizi eterogenei.
* **Sicurezza e Scalabilità:** SSL, backup, ambienti riproducibili.
* **Automation Engineering:** n8n come orchestratore universale.
* **Open-source Product Design:** documentazione chiara, distribuzione pubblica, licenza MIT.

---

## 📈 Impatto e Scalabilità

Cloudetta è già pronta per:

* **Implementazioni multi-azienda**
* **Branding personalizzato (white-label)**
* **Distribuzioni gestite come servizio (Cloudetta Managed)**

La sua modularità permette di adottarla come:

* **Base per un SaaS**, con Django come front-end commerciale.
* **ERP completo**, con Odoo al centro.
* **Digital Workplace**, per file, ticket e knowledge management.

---

## 💼 Servizi Professionali

> *"Open-source non significa senza supporto — significa libertà con competenza."*

Per le aziende che desiderano adottare Cloudetta, offro:

* Installazione su VPS o cloud privato
* Configurazione domini, SSL, Cloudflare Tunnel
* Personalizzazioni Odoo (SDI/PEC)
* Branding e deployment automatizzati
* Formazione team tecnico e operativo

📩 **Contatto diretto:** [antonio@antoniotrento.net](mailto:antonio@antoniotrento.net)

---

## 🔗 Risorse

* **Repository GitHub:** [github.com/cloudetta/cloudetta](https://github.com/cloudetta/cloudetta)
* **Documentazione:** disponibile nel pacchetto `/docs`
* **Licenza:** MIT © 2025 Antonio Trento
* **Sito ufficiale:** [https://antoniotrento.net](https://antoniotrento.net)

---

> *Cloudetta è il mio modo di rendere la tecnologia gestionale più libera, aperta e umana.
> Un toolkit per costruire ecosistemi digitali etici, sostenibili e completamente sotto il tuo controllo.*


