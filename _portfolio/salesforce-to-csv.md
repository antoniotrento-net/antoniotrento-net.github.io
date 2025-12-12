---
layout: portfolio
title: "Salesforce to CSV Exporter"
date: 2025-12-12
description: "Tool professionale Docker-ready per export automatizzati di dati Salesforce verso CSV con field mapping configurabile, autenticazione JWT, paginazione automatica e documentazione bilingue. Licenza commerciale proprietaria."
image: "/assets/images/portfolio/salesforce-to-csv/salesforce-to-csv.jpg"
image-header: "/assets/images/portfolio/salesforce-to-csv/salesforce-to-csv.jpg"
image-paint: "/assets/images/portfolio/salesforce-to-csv/salesforce-to-csv.jpg"
tags: [Salesforce, CSV Export, Docker, Python, JWT Authentication, SOQL, Data Export, Enterprise, Commercial Software, Source-Available]
---

> *Ogni azienda che lavora con Salesforce prima o poi si trova a dover esportare dati in CSV per reportistica, data warehouse o integrazioni. Ho progettato questo tool per rendere il processo completamente automatizzabile, sicuro e production-ready, con una licenza commerciale che protegge l'IP ma mantiene il codice trasparente.*

**Salesforce to CSV Exporter** è una soluzione professionale containerizzata per l'export automatizzato di dati da Salesforce a file CSV, pensata per ambienti enterprise che richiedono **affidabilità**, **sicurezza** e **manutenibilità**.

Il progetto nasce dall'esigenza di avere uno strumento **generico e riutilizzabile** per esportazioni schedulate, con:

- **autenticazione JWT sicura** (nessuna password in chiaro),
- **query SOQL configurabili** tramite JSON,
- **field mapping flessibile** per adattare lo schema Salesforce alle esigenze CSV,
- **supporto completo per relazioni** e custom fields,
- **Docker containerization** per deployment immediato,
- **documentazione completa in italiano e inglese**.

Diversamente da uno script usa-e-getta, questo tool è stato progettato come **prodotto commerciale source-available**: il codice è pubblico su GitHub per trasparenza e credibilità, ma l'**uso richiede una licenza commerciale**.

---

## Modello di Business: Source-Available con Licenza Proprietaria

Questo progetto adotta un approccio **source-available** (codice visibile) ma **non open source** (uso commerciale a pagamento), simile a quanto fanno MongoDB (SSPL), Elastic Search (Elastic License) e Redis.

### 📜 Licensing Model

**Cosa è GRATIS:**
- ✅ Visualizzare il codice sorgente
- ✅ Studiare l'implementazione
- ✅ Usare come riferimento tecnico

**Cosa RICHIEDE LICENZA COMMERCIALE:**
- ❌ Usare il software in produzione
- ❌ Modificare o creare derivati
- ❌ Integrare in altri progetti
- ❌ Distribuire o rivendere

### 💼 Perché questo approccio?

1. **Trasparenza**: Il codice pubblico dimostra qualità e professionalità
2. **Trust**: I potenziali clienti possono valutare il prodotto prima di acquistare
3. **Protezione IP**: La licenza proprietaria protegge l'investimento in R&D
4. **Business Sostenibile**: Permette di offrire supporto, aggiornamenti e customizzazioni

**Licenza completa:** Vedi `LICENSE` nel repository
**Richieste di licenza:** info@antoniotrento.net

---

## Architettura & Design Tecnico

### 🔐 1. Autenticazione JWT Production-Ready

L'autenticazione con Salesforce avviene tramite **JWT Bearer Flow**, lo standard enterprise per integrazioni server-to-server:

- **Nessuna password** salvata in chiaro o nei log
- **Certificato privato** montato come volume Docker read-only
- **Token management** automatico con refresh trasparente
- Supporto sia per **Production** che **Sandbox** Salesforce

**Modulo:** `salesforce_client_jwt.py`
```python
def get_access_token_jwt():
    """
    Genera access token usando JWT Bearer Flow
    - Legge certificato privato da volume sicuro
    - Crea JWT firmato con RS256
    - Gestisce audience dinamico (prod/sandbox)
    - Ritorna (access_token, instance_url)
    """
```

### 📊 2. Field Mapping Configurabile

Il cuore del sistema è il **field mapper JSON-driven** che permette di:

- **Mappare campi Salesforce → colonne CSV** con nomi personalizzati
- **Supportare relazioni parent** (`Account.Name`, `Owner.Email`)
- **Gestire custom fields** (`Custom_Field__c`)
- **Formattare dati** (date, numeri, booleani) in modo opzionale
- **Configurare delimitatori, encoding, formato date**

**Esempio configurazione:**
```json
{
  "flow_name": "opportunities",
  "salesforce_object": "Opportunity",
  "soql_query": "SELECT Id, Name, Amount, Account.Name, Owner.Email FROM Opportunity WHERE CloseDate >= LAST_N_DAYS:30",
  "field_mappings": [
    {"salesforce_field": "Id", "csv_column": "ID"},
    {"salesforce_field": "Name", "csv_column": "NAME"},
    {"salesforce_field": "Amount", "csv_column": "AMOUNT", "format": "number"},
    {"salesforce_field": "Account.Name", "csv_column": "ACCOUNT"},
    {"salesforce_field": "Owner.Email", "csv_column": "OWNER"}
  ],
  "csv_settings": {
    "delimiter": ";",
    "encoding": "utf-8-sig",
    "date_format": "%Y-%m-%d"
  }
}
```

**Modulo:** `csv_exporter.py` (277 righe, architecture pulita con dataclasses)

### 🔄 3. Query Engine con Paginazione Automatica

Salesforce limita i risultati SOQL a 2000 record per query. Il modulo `sf_entity_reader.py` gestisce **automaticamente la paginazione** tramite `nextRecordsUrl`:

```python
class SalesforceEntityReader:
    """
    Query engine generico per Salesforce
    - Gestisce paginazione automatica (fino a 50k record)
    - Supporta query composte con relazioni
    - Logging dettagliato di ogni operazione
    - Completamente riutilizzabile
    """

    def query(self, soql: str) -> List[dict]:
        """Esegue query con paginazione trasparente"""
```

**Caratteristiche:**
- Supporto per **query complesse** con JOIN impliciti
- **Timeout configurabile** per query lunghe
- **Error handling robusto** con retry logic
- **Logging granulare** per debugging

### 🐳 4. Docker Containerization

Il deployment è completamente **containerizzato** per garantire:

**Dockerfile ottimizzato:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Crea directory per volumi persistenti
RUN mkdir -p /certs /logs /output

# Installa dipendenze (layer cacheable)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia applicazione
COPY *.py .
COPY field_mapping_config.json .

CMD ["python", "sf_to_neta_export.py"]
```

**docker-compose.yml con volume management:**
```yaml
services:
  salesforce-to-csv:
    container_name: salesforce-to-csv-exporter
    volumes:
      - ${SF_PRIVATE_KEY_PATH}:/certs/server.key:ro  # Certificato read-only
      - ${LOG_HOST_PATH:-./logs}:/logs               # Log persistenti
      - ${OUTPUT_HOST_PATH:-./output}:/output        # CSV persistenti
    networks:
      - salesforce-csv-network
```

**Vantaggi:**
- **Isolamento completo** dell'ambiente
- **Riproducibilità** tra dev/stage/prod
- **Gestione volumi** per certificati, log e output
- **Network dedicata** per sicurezza

### 📝 5. Logging Production-Grade

Sistema di logging con **rotazione automatica** pensato per ambienti enterprise:

**Configurazione:**
```python
# logger_config.py
RotatingFileHandler(
    filename="logs/sf_to_csv_export.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,               # 5 backup storici
    encoding='utf-8'
)
```

**Output strutturato:**
```
[2025-12-12 14:30:00] INFO: Autenticazione Salesforce riuscita
[2025-12-12 14:30:05] INFO: Query SOQL: SELECT Id, Name FROM Account...
[2025-12-12 14:30:07] INFO: Recuperati 1523 record da Salesforce
[2025-12-12 14:30:10] INFO: Export completato: /output/accounts_20251212.csv
[2025-12-12 14:30:10] INFO: Record esportati: 1523
```

### ⚙️ 6. Automazione con Cronjob

Script shell production-ready per schedulazione:

**run_export.sh** (206 righe) include:
- ✅ Validazione ambiente (Docker, certificati, config)
- ✅ Gestione timeout configurabile
- ✅ Logging separato per cron execution
- ✅ Report statistiche (file generati, dimensioni, durata)
- ✅ Cleanup automatico container
- ✅ Exit codes per monitoring

**Esempio cronjob:**
```bash
# Export giornaliero alle 2 AM
0 2 * * * /path/to/salesforce-to-csv/run_export.sh >> /logs/cron.log 2>&1
```

---

## Documentazione Bilingue Completa

Una delle caratteristiche distintive del progetto è la **documentazione enterprise-grade** in **italiano e inglese**:

### 📘 Documentazione Italiana (`docs/`)
- **01-introduzione.md** - Overview e caratteristiche
- **02-architettura.md** - Architettura dettagliata dei componenti
- **03-quick-start.md** - Setup rapido in 5 minuti
- **05-field-mapping.md** - Guida completa al field mapping
- **06-query-soql.md** - Best practices per query SOQL
- **08-cronjob-automation.md** - Automazione e scheduling
- **12-troubleshooting.md** - Risoluzione problemi comuni

### 📗 Documentazione Inglese (`docs-eng/`)
Traduzione professionale completa per audience internazionale.

**Conversione DokuWiki → Markdown GitHub:**
- Convertiti oltre **70k caratteri** di documentazione
- Sintassi DokuWiki → Markdown standard
- Link interni aggiornati automaticamente
- Esempi di codice formattati correttamente

---

## Configurazione & Deployment

### 1. Setup Credenziali

```bash
cp .env.example .env
```

**.env** configurabile:
```env
SF_USERNAME="user@company.com"
SF_CLIENT_ID="your_salesforce_connected_app_id"
SF_LOGIN_URL="https://login.salesforce.com"  # o test.salesforce.com per sandbox
SF_PRIVATE_KEY_PATH="/path/to/server.key"

OUTPUT_DIR="./output"
LOG_DIR="./logs"
LOG_LEVEL="INFO"
```

### 2. Configurazione Field Mapping

Personalizza `field_mapping_config.json` per definire:
- Oggetto Salesforce sorgente
- Query SOQL con filtri
- Mappatura campi → colonne CSV
- Formato output (delimiter, encoding, date format)
- Nome file output con pattern dinamico

### 3. Deploy con Docker

```bash
# Build immagine
docker-compose build

# Run export
docker-compose up

# Verifica output
ls -lh ./output/
tail -f ./logs/sf_to_csv_export.log
```

---

## Use Cases Enterprise

### 📊 Data Warehouse Integration
Export schedulati di Account, Contact, Opportunity verso DWH per analytics e BI.

### 🔄 Data Synchronization
Sincronizzazione giornaliera dati Salesforce → sistemi esterni legacy.

### 📈 Custom Reporting
Generazione report CSV con field mapping customizzato per stakeholder non-tecnici.

### 💾 Backup Automation
Backup periodici di custom objects e configurazioni Salesforce.

### 🔍 Data Analysis
Estrazione dati per analisi batch con Python/R/Excel.

---

## Cosa Dimostra Questo Progetto

Dal punto di vista tecnico e business, questo progetto evidenzia:

### 🏗️ Software Architecture
- **Modularità**: Separazione chiara tra autenticazione, query engine, mapping, export
- **Configurabilità**: Zero hardcoding, tutto definibile via JSON/ENV
- **Estensibilità**: Facile aggiungere nuovi formati export o sorgenti dati
- **SOLID Principles**: Ogni modulo ha una singola responsabilità ben definita

### 🔐 Enterprise Security
- JWT authentication secondo best practices Salesforce
- Gestione sicura certificati privati (volume Docker read-only)
- Nessuna credenziale in codice o log
- Network isolation con Docker

### 🐳 DevOps & Containerization
- **Docker-first approach** per portabilità
- **Volume management** per persistenza dati
- **Health checks** e **graceful shutdown**
- **Automated deployment** ready

### 📚 Documentation-Driven Development
- **Documentazione bilingue** completa (IT/EN)
- **Esempi pratici** per ogni scenario
- **Troubleshooting guide** dettagliata
- **Architecture diagrams** e flow charts

### 💼 Commercial Software Development
- **Licensing model** proprietario ma source-available
- **Professional README** con badges e call-to-action
- **GitHub Issue Templates** per license requests
- **CHANGELOG** e **versioning** strutturato

### ⚙️ Production Readiness
- **Logging rotativi** per ambienti long-running
- **Error handling** robusto a ogni livello
- **Monitoring-friendly** (exit codes, structured logs)
- **Scriptable** per CI/CD integration

---

## Licenza Commerciale & Richieste

Questo è **software proprietario source-available**. Il codice è pubblico per trasparenza, ma l'uso richiede una licenza commerciale.

### 💼 Licenze Disponibili

**Individual License** - Singolo utente/organizzazione
**Team License** - Fino a 10 utenti
**Enterprise License** - Utenti illimitati + supporto dedicato
**Trial License** - 30 giorni gratuiti per valutazione

### 📧 Contatti per Licensing

**Email:** info@antoniotrento.net
**Website:** https://antoniotrento.net
**Developer:** Antonio Trento

**Richiedi una demo o un preventivo personalizzato.**

---

## Repository & Risorse

Il progetto è disponibile su GitHub con licenza proprietaria:

> **[🔗 Esplora il progetto su GitHub](https://github.com/antonio-backend-projects/salesforce-to-csv){: rel="nofollow"}**

**Risorse:**
- **[LICENSE](https://github.com/antonio-backend-projects/salesforce-to-csv/blob/main/LICENSE){: rel="nofollow"}** - Termini di licenza completi
- **[LICENSING.md](https://github.com/antonio-backend-projects/salesforce-to-csv/blob/main/LICENSING.md){: rel="nofollow"}** - Guida alle licenze disponibili
- **[CHANGELOG.md](https://github.com/antonio-backend-projects/salesforce-to-csv/blob/main/CHANGELOG.md){: rel="nofollow"}** - Cronologia versioni
- **[Docs (IT)](https://github.com/antonio-backend-projects/salesforce-to-csv/tree/main/docs){: rel="nofollow"}** - Documentazione italiana
- **[Docs (EN)](https://github.com/antonio-backend-projects/salesforce-to-csv/tree/main/docs-eng){: rel="nofollow"}** - Documentazione inglese

---

**© 2025 Antonio Trento. All Rights Reserved.**
*Questo progetto dimostra capacità di progettazione enterprise-grade, business acumen nel licensing, e attenzione alla qualità del codice production-ready.*
