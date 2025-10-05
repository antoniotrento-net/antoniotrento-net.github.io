---
layout: portfolio
title: "Cloudetta"
date: 2025-10-05
description: "Cloudetta è una piattaforma open-source integrata per la gestione aziendale cloud, che unisce ERP, SaaS, automazione e documentazione in un unico stack modulare."
image: "/assets/images/portfolio/cloudetta/cloudetta.jpg"
image-header: "/assets/images/portfolio/cloudetta/cloudetta.jpg"
image-paint: "/assets/images/portfolio/cloudetta/cloudetta.jpg"
tags: [Open Source, SaaS, ERP, Docker, Odoo, Django, n8n, Nextcloud, DevOps, Cloud Automation, Stripe, System Integration]
---

> *"L’obiettivo non era costruire l’ennesima suite gestionale, ma una piattaforma unificata, realmente open-source, capace di offrire a qualsiasi azienda — anche la più piccola — la potenza e l’integrazione di un ecosistema enterprise."*

**Cloudetta** nasce da un’idea precisa: **rendere accessibile la complessità aziendale**, fornendo un’infrastruttura moderna, scalabile e completamente automatizzata, basata su tecnologie open-source mature e interoperabili.

Il progetto rappresenta la sintesi di anni di esperienza in **integrazione di sistemi, DevOps e architetture cloud modulari**, racchiusa in un toolkit unico, pronto per essere usato come base per prodotti SaaS, ERP o CRM avanzati.

---

## 🌍 Visione

> *Cloudetta è il “Business Cloud” open-source: un ecosistema integrato che collega persone, dati e processi, eliminando la frammentazione e semplificando l’automazione.*

Dove molte aziende usano dieci strumenti scollegati (gestionali, ticketing, file sharing, automazioni), Cloudetta unisce tutto in un’unica architettura coerente, distribuita via **Docker Compose** e pronta per il deploy in **on-premise**, **VPS** o **Kubernetes**.

---

## 🏗️ Architettura: Un Ecosistema Modulare

L’architettura di Cloudetta segue un approccio **multi-layer** in cui ogni servizio è un modulo indipendente, connesso attraverso API e orchestrato da un reverse proxy centralizzato (**Caddy**).

*(Di seguito un diagramma architetturale in formato [Mermaid](https://mermaid.js.org/) incluso nel README ufficiale.)*

### 1. Core Application Layer

Il cuore dell’ecosistema è composto da:

- **Django + Stripe** – per la gestione di utenti, abbonamenti e API.  
  Include webhook automatici, API REST e autenticazione sicura.  
- **Odoo ERP** – la colonna vertebrale gestionale: CRM, vendite, contabilità, con moduli italiani (`l10n_it`, `l10n_it_edi`) per la **fatturazione elettronica SDI/PEC**.  
- **n8n Orchestrator** – l’automazione visiva. Gestisce flussi come:
  - Creazione ticket su Redmine da un ordine Django
  - Upload fatture su Nextcloud
  - Invio email automatiche post-pagamento

### 2. Collaboration & Documentation Layer

Lato documentazione e collaborazione:

- **Nextcloud** – per archiviare, condividere e sincronizzare documenti aziendali e fatture PDF.
- **Redmine** – per il ticketing tecnico e il project management.
- **DokuWiki** – per manuali interni e knowledge base operativa.

### 3. Infrastructure Layer

- **Caddy Reverse Proxy** – gestisce SSL automatico e instradamento dei domini `*.example.com` o `*.localhost`.  
  Compatibile con **Cloudflare Tunnel**, consente deploy sicuri senza porte pubbliche.  
- **Backup Container** – esegue backup giornalieri (DB, volumi, immagini Docker) alle 02:00, con log e restore rapido.

### 4. Integration Layer

Il ponte tra tutti i servizi:
- Workflow **Django ↔ Odoo ↔ Nextcloud ↔ Redmine** via **n8n**.
- Sincronizzazione bidirezionale di clienti, prodotti e documenti.
- API REST unificate per automazioni esterne.

---

## ⚙️ Stack Tecnologico

| Componente | Tecnologia | Ruolo |
|-------------|-------------|-------|
| **Backend Core** | Django + Stripe | Gestione utenti, abbonamenti, API |
| **ERP** | Odoo + PostgreSQL | Contabilità, CRM, SDI/PEC |
| **Automazione** | n8n (Node.js) | Workflow orchestration |
| **Storage** | Nextcloud + MariaDB | File sharing e backup |
| **Ticketing** | Redmine + MariaDB | Supporto e project management |
| **Proxy** | Caddy | SSL + routing |
| **Backup** | Bash + cron | Dump e tar periodici |

---

## 💡 Filosofia di Design

Cloudetta non è un semplice “docker-compose.yml” — è un **ecosistema integrato**, concepito per essere estensibile e manutenibile nel tempo.

- **Open-source & Self-hosted** → nessun lock-in, il codice è tuo.  
- **Modulare** → ogni servizio può essere disattivato o sostituito.  
- **Sicuro by design** → Caddy + SSL + gestione centralizzata degli accessi.  
- **DevOps ready** → stesso stack in locale e in produzione.  
- **Scalable** → pronto per Docker Swarm o Kubernetes.

---

## 🧠 Dettagli Tecnici

### Configurazione
Tutti i parametri sono gestiti tramite `.env`, permettendo setup riproducibili:
```bash
MAIL_PROVIDER=sendgrid
DJANGO_SECRET_KEY=...
ODOO_DB_PASSWORD=...
NEXTCLOUD_DB_PASSWORD=...
````

### Deploy

Installazione in un unico comando:

```bash
chmod +x install.sh
./install.sh
```

### Backup

Backup completi schedulati:

```bash
docker exec -it backup /backup/backup.sh
```

### Restore

Ripristino manuale o automatico (prossimamente via `restore.sh`):

```bash
psql -U user -d db < dump.sql
tar -xzvf volume.tar.gz -C /var/lib/docker/volumes/...
```

---

## 🤝 Integrazioni Pronte

| Integrazione           | Funzione                                 |
| ---------------------- | ---------------------------------------- |
| **Django → Redmine**   | Crea ticket da ordini o errori pagamento |
| **Django → Nextcloud** | Carica fatture PDF automaticamente       |
| **Odoo → Django**      | Sincronizza clienti/prodotti             |
| **n8n → Email/SMS**    | Invia notifiche transazionali            |
| **Backup → Nextcloud** | Replica automatica dei backup            |

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


