---
layout: portfolio
title: "DataUnchain – AI Privata per l'Estrazione Dati Aziendali"
date: 2026-03-12
description: "Motore di estrazione dati da documenti aziendali (fatture, DDT, contratti, buste paga) con AI Vision 100% offline. 95.5% di accuratezza su 219 documenti reali, $0.002/documento, senza cloud."
image: "/assets/images/portfolio/dataunchain/dataunchain-cover.jpg"
image-header: "/assets/images/portfolio/dataunchain/dataunchain-cover.jpg"
image-paint: "/assets/images/portfolio/dataunchain/dataunchain-cover.jpg"
tags: [AI, Python, Docker, FastAPI, Ollama, Qwen, VLM, On-Premise, Data Extraction, OCR, Automazione, ERP Integration]
---

> *"Il problema non era la tecnologia — era convincere l'AI a leggere fatture in italiano con timbri, rotazioni e qualità da scanner da ufficio. Ci ho messo tre mesi a costruire una pipeline che lo fa in 32 secondi."*

**DataUnchain** è un'AI Appliance per l'automazione del data entry documentale: trasforma PDF, immagini e scansioni in JSON strutturato e li inserisce direttamente nel gestionale ERP aziendale, senza cloud e senza condividere dati con terzi.

Il progetto nasce dall'osservazione diretta di un problema che affligge migliaia di uffici amministrativi italiani: il data entry manuale. Un impiegato amministrativo trascorre in media 2-3 ore al giorno ad aprire documenti — fatture di acquisto, DDT, ordini, buste paga — e a copiare i valori nel gestionale uno per uno. È un lavoro ripetitivo, soggetto a errori, impossibile da delegare completamente senza rischiare inserimenti errati nel sistema contabile. Moltiplicato per decine o centinaia di fornitori diversi, ciascuno con il proprio layout di documento, il problema scala in modo non lineare.

Le soluzioni cloud esistono: Amazon Textract, Azure Document Intelligence, Google Document AI sono prodotti maturi e precisi. Ma hanno un limite fondamentale per molte aziende: i documenti — fatture, contratti, buste paga, estratti conto — contengono dati altamente sensibili. Trasmetterli a infrastrutture di terzi viola le policy interne di molte aziende manifatturiere, studi professionali e strutture sanitarie, e in alcuni casi è in contrasto con il GDPR o con clausole contrattuali di riservatezza.

DataUnchain risolve il problema alla radice: l'AI gira completamente on-premise, dentro l'infrastruttura aziendale, senza che un singolo byte di dato esca mai verso internet.

---

## Il Contesto: Perché il Data Entry È Ancora un Problema nel 2026

Può sembrare strano che nel 2026, con l'AI ovunque, il data entry manuale sia ancora uno dei colli di bottiglia più comuni nelle PMI italiane. La ragione è strutturale.

La fatturazione elettronica SDI ha standardizzato il formato delle fatture attive — quelle emesse dall'azienda verso i clienti. Ma le **fatture passive** — quelle ricevute dai fornitori — arrivano ancora in PDF libero, spesso come scansioni, con layout completamente diversi da fornitore a fornitore. Un'azienda con 200 fornitori ha 200 layout diversi da gestire. I software OCR tradizionali basati su template richiedono di configurare manualmente ogni template: coordianate esatte dei campi, regioni di interesse, mappature. È un lavoro che può richiedere giorni per fornitore, e si rompe ogni volta che il fornitore cambia anche solo marginalmente il layout della propria fattura.

I DDT (Documenti di Trasporto) sono ancora più eterogenei: ogni spedizioniere ha il proprio modulo, spesso compilato a mano o con scritte sovrapposte a timbri. Le buste paga cambiano formato a seconda del software paghe usato dall'azienda (Zucchetti, TeamSystem, Wolters Kluwer, Paghe.web) e il medesimo campo — il lordo, per esempio — si chiama in modi diversi a seconda del CCNL applicato.

Il modello AI Vision (VLM) risolve questo problema in modo radicalmente diverso: non si configura per layout, **comprende il documento come lo farebbe un essere umano**. Vede l'immagine e capisce che il numero dopo "Totale fattura" o dopo "Importo da pagare" o dopo "Tot. IVA inclusa" è sempre lo stesso tipo di dato, indipendentemente da dove appare nella pagina.

---

## Il Problema Tecnico: Cosa Rende Difficile Questo Problema

Estrarre dati strutturati da documenti aziendali italiani reali è significativamente più difficile di quanto appaia in una demo:

### 1. Varianza di formato illimitata

Ogni fornitore impagina la fattura come vuole. Il totale può essere in alto a destra, in basso al centro, o in una cella di una tabella a metà pagina. La P.IVA del fornitore può essere nell'intestazione, nel footer, o in un campo separato. Un sistema basato su coordinate o template fallisce al primo documento fuori standard. Un VLM no.

### 2. Qualità documentale degradata

Il 70% dei documenti che arrivano nelle aziende non sono PDF nativi puliti: sono fotografie fatte con lo smartphone appoggiando la fattura sul tavolo, scansioni con scanner da ufficio anni Novanta, fotocopie di fotocopie. In pratica: rumore, rotazione, contrasto ridotto, JPEG artifacts, timbri sovrapposti al testo, macchie di caffè, angoli tagliati.

Per replicare questa condizione nel benchmark, ogni documento sintetico del corpus è stato degradato con trasformazioni controllate: rumore gaussiano, rotazione casuale ±3°, compressione JPEG a qualità 60–85, sovrapposizione di timbri opachi. Il risultato: **nessuna differenza di accuratezza tra documenti degradati e PDF nativi** — il VLM è robusto alla degradazione visiva al punto da rendere la distinzione statisticamente irrilevante.

### 3. Verifica della correttezza, non solo dell'estrazione

Estrarre un numero è necessario, ma non sufficiente. Una fattura dove l'imponibile estratto è corretto ma l'IVA è sbagliata non deve entrare nel gestionale senza segnalazione — l'operatore deve verificarla manualmente. Il problema è che un sistema puramente AI non sa fare questa distinzione: restituisce i valori estratti e non verifica se tornano.

DataUnchain introduce un layer di verifica Python separato dal modello AI. Questo layer conosce le regole matematiche di ogni tipo di documento:
- Fattura: `imponibile + iva = totale` (tolleranza ±€0.50 per arrotondamenti)
- Busta paga: `lordo - trattenute = netto`
- Estratto conto: `saldo_iniziale + accrediti - addebiti = saldo_finale`

Se il check fallisce, il documento va in `NEEDS_REVIEW` e l'operatore viene notificato. Non viene mai inserito silenziosamente nel gestionale con dati potenzialmente errati.

### 4. Privacy assoluta

Buste paga, contratti, estratti conto bancari — sono dati che per molte aziende non possono fisicamente uscire dall'infrastruttura interna, né per policy aziendale, né per contratto con i dipendenti, né per vincoli normativi. DataUnchain non richiede connessione internet: tutto il modello AI, tutta la pipeline di processing, tutta la storage dei dati è on-premise, dentro un Docker Compose che gira su un server aziendale.

### 5. Integrazione con gestionali legacy

Il mercato dei gestionali italiani è frammentato: Zucchetti, TeamSystem, Mexal, Passepartout, Profis, Danea Easyfatt, e decine di altri. Ciascuno accetta input in formati diversi. DataUnchain implementa un sistema di adapter: ogni sistema gestionale ha il proprio adapter che prende il JSON strutturato e lo traduce nel formato nativo del gestionale.

---

## La Pipeline: Come Funziona in Dettaglio

### Ingestion — Come Arrivano i Documenti

DataUnchain supporta più canali di input:

- **Cartella monitorata (watchdog):** il canale più semplice. L'operatore trascina il documento in una cartella, la pipeline lo processa automaticamente entro pochi secondi.
- **Email monitor:** monitora una casella email dedicata (es. `fatture@azienda.it`), scarica gli allegati PDF e li mette in coda.
- **SDI monitor:** si collega al canale di ricezione FatturaPA per intercettare le fatture elettroniche passive direttamente dallo SDI.
- **API REST:** endpoint FastAPI per integrazioni programmatiche da altri sistemi.
- **Bot Telegram:** per operatori in mobilità che ricevono documenti su smartphone.

### Step 1 — Classificazione del Documento

Prima di estrarre qualsiasi campo, il sistema deve sapere con quale tipo di documento ha a che fare. La classificazione non è banale: una nota di credito può sembrare una fattura, un DDT può avere campi numerici simili a un ordine di acquisto.

Il primo step è una chiamata al VLM con un prompt specializzato per la classificazione: al modello viene mostrata l'immagine del documento e viene chiesto di identificarne il tipo tra quelli supportati, con un grado di confidence. Questo step è veloce (2-4 secondi) perché non richiede l'estrazione di ogni campo.

Il risultato della classificazione determina quale prompt di estrazione verrà usato nel passo successivo. Avere prompt specifici per tipo — invece di un unico prompt generico — aumenta significativamente la precisione: il modello sa esattamente quali campi cercare, come si chiamano tipicamente, e quale formato ci si aspetta.

### Step 2 — Estrazione Strutturata

Questa è la chiamata principale al VLM. Il prompt di estrazione per ogni tipo di documento è costruito con:

1. **Descrizione dei campi da estrarre** con nome, tipo (stringa, numero, data), e varianti di etichetta note
2. **Formato di output atteso** (JSON schema con i tipi corretti)
3. **Istruzioni di fallback** per campi non trovati (restituire `null` invece di inventare un valore)
4. **Istruzioni di normalizzazione** (date sempre in formato ISO 8601, importi sempre come float con punto decimale)

Il modello restituisce un JSON. Se il JSON non è valido o mancano campi obbligatori, il sistema ritenta con temperatura ridotta prima di passare il documento a `NEEDS_REVIEW`.

### Step 3 — Verifica e Confidence

Il layer Python verifica:

- **Coerenza matematica:** le formule specifiche per tipo di documento (vedi sopra)
- **Formato dei campi:** P.IVA con checksum Luhn, codice fiscale con algoritmo di controllo, IBAN con mod-97, date nel range plausibile
- **Completezza:** presenza di tutti i campi obbligatori per quel tipo di documento

A ogni documento viene assegnato un livello di confidence:
- **HIGH:** estrazione completa, math check superato, tutti i campi validati
- **MEDIUM:** estrazione completa ma uno o più campi opzionali mancanti o fuori formato
- **LOW → NEEDS_REVIEW:** math check fallito, campi obbligatori mancanti, o risposta del modello non parsabile

Nel benchmark, il 92.2% dei documenti è finito in HIGH, il 5.9% in LOW (tutti estratti conto con crash GGML per limite hardware).

### Step 4 — Output e Integrazione

Il JSON validato viene passato al router degli output, che instrada il documento verso l'adapter configurato per quella tipologia:

- **webhook:** POST verso qualsiasi endpoint HTTP esterno
- **CSV/Excel:** file compatibili con import manuale nei gestionali
- **FatturaPA:** generazione XML XSD-conforme per import SDI
- **Zucchetti:** CSV nel tracciato Ad Hoc Revolution o chiamata REST API
- **TeamSystem:** CSV nativo o Digital Hub API
- **Mexal:** tracciato ASCII a 375 caratteri codifica latin-1 (formato legacy ancora in uso in molte aziende)
- **Google Sheets:** push diretto su foglio Google via API
- **RPA Playwright:** per gestionali senza API, automazione dell'interfaccia web tramite browser controllato

---

## Stack Tecnologico Completo

| Componente | Tecnologia | Ruolo |
|---|---|---|
| **AI Vision** | Qwen2.5-VL 7B via Ollama | Classificazione + estrazione campi |
| **Document processing** | pdf2image + Pillow | Conversione PDF → immagine |
| **File watching** | watchdog (Python) | Monitoraggio cartella input |
| **Validation layer** | Python 3.11 | Math check, validazione formati |
| **API** | FastAPI + Pydantic | Endpoint REST + validazione schema |
| **Dashboard** | Streamlit | Monitoring risultati in tempo reale |
| **Orchestrazione** | Docker Compose | Stack multi-servizio self-hosted |
| **Email input** | imaplib (Python) | Monitor casella fatture@azienda |
| **Telegram input** | python-telegram-bot | Bot per documenti da mobile |
| **Output — generico** | httpx | Webhook HTTP |
| **Output — ERP** | Adapter specifici per sistema | CSV, REST, tracciati ASCII |
| **Output — Google** | google-api-python-client | Sheets API v4 |
| **Output — RPA** | Playwright (Python) | Automazione browser per gestionali legacy |

### Perché Qwen2.5-VL e non altri modelli

La scelta del modello è stata l'aspetto più critico del progetto. Ho testato diverse famiglie di modelli VLM open weight su questo corpus specifico prima di convergere su Qwen2.5-VL 7B:

- **LLaVA 1.6 (Mistral 7B):** ottimo per descrizioni di immagini generali, insufficiente per estrazione strutturata di dati numerici — tendenza a parafrasare invece di estrarre
- **InternVL2 8B:** risultati promettenti ma instabile con documenti degradati ad alta compressione JPEG
- **Qwen2.5-VL 7B:** migliore equilibrio tra precisione sull'estrazione strutturata, robustezza visiva e velocità su hardware consumer. Eccellente comprensione del testo in italiano e dei formati numerici europei (virgola come separatore decimale, punti come separatori delle migliaia)

Un aspetto non banale: i modelli americani hanno tendenza a interpretare "1.234,56" come una sequenza di caratteri invece di un numero, mentre "1,234.56" viene gestito correttamente. Per documenti italiani questo è critico — Qwen2.5-VL gestisce entrambi i formati in modo affidabile.

---

## Risultati del Benchmark: Analisi Dettagliata

Il benchmark è stato costruito per testare le condizioni reali, non quelle ottimali. Il corpus di 219 documenti è stato generato sinteticamente con un seed fisso (per garantire la riproducibilità) ma con una distribuzione realistica di tipologie e con degradazione controllata che replica le condizioni dei documenti reali.

### Hardware del test

| Componente | Specifiche |
|---|---|
| GPU | NVIDIA RTX 2000 Ada Generation — 16 GB VRAM GDDR6 |
| CPU | Intel Xeon E-2386G — 6 core / 12 thread |
| RAM | 46 GB DDR4 |
| OS | Ubuntu 22.04.3 LTS |
| Modello | Qwen2.5-VL 7B via Ollama 0.6.x |
| Costo cloud | $0.24/ora (RunPod Community Cloud) |
| Durata benchmark | ~3.3 ore per 219 documenti |
| Costo totale | ~$0.80 |

### Accuratezza campo per campo

| Campo | Accuratezza | Su |
|---|---|---|
| Classificazione tipo documento | **100.0%** | 206/206 |
| P.IVA / Codice Fiscale | **100.0%** | 206/206 |
| Data emissione (YYYY-MM-DD) | **100.0%** | 144/144 |
| Imponibile (±€0.50) | **100.0%** | 94/94 |
| IVA (±€0.50) | **100.0%** | 94/94 |
| Totale fattura (±€0.50) | **100.0%** | 94/94 |
| Netto busta paga (±€0.50) | **100.0%** | 35/35 |
| Saldo finale estratto conto (±€0.50) | **100.0%** | 7/7 |
| Numero documento di riferimento | **96.6%** | 199/206 |
| Math check interno (±€0.10) | **100.0%** | 120/120 |
| Lordo busta paga (±€0.50) | **54.3%** ⚠️ | 19/35 |

### Distribuzione confidence

| Livello | Documenti | % |
|---|---|---|
| HIGH | 202 | 92.2% |
| MEDIUM | 4 | 1.8% |
| LOW | 13 | 5.9% |

I 13 documenti LOW sono tutti estratti conto con crash GGML — non vengono inseriti nel gestionale ma messi in coda NEEDS_REVIEW per revisione manuale.

### Velocità per tipologia

| Tipo | Velocità media |
|---|---|
| Contratto | 26s |
| Nota di Credito | 31s |
| Busta Paga | 31s |
| DDT | 32s |
| Fattura | 36s |
| Ordine Acquisto | 37s |
| Estratto Conto | 48s |

Gli estratti conto sono più lenti perché le tabelle di movimenti dense generano contesti più lunghi per il modello.

### La scoperta principale: SCAN = CLEAN

Il risultato più significativo del benchmark non è l'accuratezza complessiva, ma il fatto che **i documenti degradati hanno performance identiche ai PDF nativi su ogni metrica**. Classificazione, P.IVA, importi, math check — zero differenza statisticamente rilevabile tra i 60 PDF nativi e i 146 documenti con rumore, rotazione e timbri.

Questo è il punto che distingue un approccio VLM da un OCR tradizionale: l'OCR tradizionale degrada linearmente con la qualità dell'immagine. Il VLM è addestrato su immagini reali del mondo — incluse fotografie sfocate, testi sovrapposti, illuminazione non uniforme — e mantiene robustezza visiva anche in condizioni difficili.

### I Due Limiti Identificati

**Limite 1 — Crash GGML sugli estratti conto (13/20)**

Gli estratti conto con tabelle di movimenti dense (15+ righe) producono un crash interno nel backend GGML di Ollama quando si supera un certo limite dimensionale di tensori su 16 GB VRAM. Questo non è un bug del codice della pipeline — è un limite fisico dell'hardware nel configurazione testata. I 7 estratti conto con meno righe elaborati correttamente ottengono il 100% su tutti i campi. Fix pianificato: DPI adattivo (se le righe superano 12, riduzione da 200 a 150 DPI) o migrazione a GPU 24 GB VRAM.

**Limite 2 — Lordo busta paga: 54.3%**

Il netto busta paga viene estratto al 100% — l'etichetta "NETTO IN BUSTA" è standardizzata. Il lordo al 54.3% perché i software paghe italiani usano etichette diverse per lo stesso campo: Zucchetti usa "RETRIBUZIONE LORDA", TeamSystem usa "IMPONIBILE LORDO", Wolters Kluwer usa "TOTALE COMPETENZE". Il numero viene sempre letto correttamente quando trovato — il problema è il riconoscimento dell'etichetta. Fix pianificato: lista esplicita di tutte le varianti nel prompt busta paga. Target: >90%.

---

## Risorse GPU durante il Benchmark

| Metrica | Valore |
|---|---|
| GPU Utilization | 87–100% (media ~94%) |
| VRAM utilizzata | 13.3 GB / 16 GB |
| Power draw | ~68 W (6 W in idle) |
| Temperatura GPU | 65–70°C (26°C in idle) |
| CPU Load | ~4% |
| RAM sistema | ~35 GB |

La pipeline è 100% GPU-bound. Il 4% di CPU load significa che il processore attende la GPU ad ogni inferenza. Investire in GPU più potente — o in una GPU con 24 GB VRAM — produce miglioramenti lineari nelle performance. Aggiornare la CPU non cambia nulla.

---

## Architettura del Sistema: Servizi Docker

DataUnchain gira come stack Docker Compose con quattro servizi principali e profili opzionali per i canali di input meno comuni:

```
┌─────────────────────────────────────────────────────┐
│                   Docker Network                    │
│                                                     │
│  ┌──────────┐   ┌───────────┐   ┌───────────────┐  │
│  │  ollama  │◄──│ processor │──►│     api       │  │
│  │ :11434   │   │ (watchdog │   │  FastAPI      │  │
│  │ Qwen2.5  │   │ +extract) │   │  :8000        │  │
│  └──────────┘   └─────┬─────┘   └───────────────┘  │
│                       │                             │
│                  ┌────▼──────┐   ┌───────────────┐  │
│                  │  outputs  │   │  dashboard    │  │
│                  │  router   │   │  Streamlit    │  │
│                  │ +adapters │   │  :8501        │  │
│                  └───────────┘   └───────────────┘  │
└─────────────────────────────────────────────────────┘
```

**Profili opzionali** (attivabili via `--profile`):
- `telegram` — bot Telegram per input da mobile
- `email` — monitor casella email fatture
- `sdi` — monitor SDI per FatturaPA passive

La separazione in profili permette di deployare solo i canali necessari, riducendo la superficie d'attacco e il consumo di risorse.

---

## Confronto con le Alternative

| Soluzione | Privacy | Costo/doc | Accuratezza | Setup |
|---|---|---|---|---|
| **DataUnchain** | 100% on-premise | $0.002 | 95.5% | Docker Compose |
| Amazon Textract | Cloud AWS | $0.015 | ~95% | API key |
| Azure Document Intelligence | Cloud Microsoft | $0.010 | ~95% | API key |
| Google Document AI | Cloud Google | $0.010 | ~94% | API key |
| OCR tradizionale + template | On-premise | ~$0 | 60-80%* | Config per fornitore |

*L'OCR tradizionale con template raggiunge alta accuratezza sui documenti configurati, ma crolla su documenti fuori template e su scansioni degradate.

Il posizionamento di DataUnchain è preciso: stessa classe di accuratezza dei servizi cloud enterprise, a un quinto del costo per documento, senza trasferire i dati. Per aziende con vincoli di privacy reali — studi legali, aziende farmaceutiche, strutture sanitarie, aziende con NDA stretti sui dati contabili — questa non è un'ottimizzazione di costo, è un requisito non negoziabile.

---

## Competenze Dimostrate

Lo sviluppo di DataUnchain ha richiesto la convergenza di competenze che raramente si trovano nello stesso profilo:

### AI Engineering e MLOps
Integrazione di modelli VLM multimodali (Qwen2.5-VL) in pipeline di produzione. Prompt engineering avanzato per estrazione strutturata: gestione del format output, fallback su campi non trovati, normalizzazione dei valori, varianti linguistiche dello stesso campo. Valutazione comparativa di modelli su task specifici. Comprensione dei limiti fisici (VRAM, context length, tensori GGML) e progettazione di workaround.

### Architettura Software
Progettazione di pipeline event-driven: watchdog → classify → extract → validate → route. Implementazione del pattern adapter per disaccoppiare la logica di estrazione dai sistemi di destinazione. Gestione degli stati documento (QUEUED, PROCESSING, VALIDATED, NEEDS_REVIEW, FAILED) con transizioni deterministiche. API REST con FastAPI e validazione schema Pydantic.

### Benchmark Engineering
Costruzione di un corpus sintetico con ground truth matematicamente verificata. Ogni documento del corpus è generato con valori interni coerenti: la somma torna al centesimo, le date sono plausibili, le P.IVA passano il checksum. Questo permette di misurare non solo l'estrazione dei valori ma la capacità del sistema di rilevare errori aritmetici interni. Degradazione controllata dei documenti con parametri fissi (seed, livelli di compressione, intensità rumore) per garantire riproducibilità del benchmark.

### DevOps e Containerizzazione
Stack Docker Compose multi-servizio con networking interno, volumi persistenti, healthcheck, variabili di ambiente tramite `.env`. Profili opzionali per servizi aggiuntivi. Configurazione per deployment su hardware consumer (workstation aziendale con GPU) senza dipendenza da cloud.

### Dominio Business e Contabilità Italiana
Comprensione del flusso contabile italiano: P.IVA con algoritmo di checksum, Codice Fiscale, IVA 22%/10%/4%, Note di Credito come reverse di fattura, FatturaPA con XSD SDI. Conoscenza dei formati gestionali italiani: tracciato Zucchetti Ad Hoc Revolution, tracciato Mexal a 375 caratteri latin-1, Digital Hub TeamSystem. Comprensione delle varianti di CCNL nelle buste paga. Questo dominio specifico è raro tra gli AI engineer generici e cruciale per costruire un prodotto utilizzabile da aziende italiane reali.

### Integrazione di Sistemi Legacy
Sviluppo di adapter per sistemi con interfacce datate: tracciati ASCII a larghezza fissa, encoding latin-1, formati CSV con separatori non standard. Automazione browser con Playwright per gestionali senza API pubblica. Capacità di reverse engineering di formati di input non documentati analizzando esempi di file di import.

---

## Stato del Progetto e Prossimi Step

DataUnchain è un prodotto commerciale in fase di validazione con i primi clienti. Non è open source.

Il benchmark pubblicato rappresenta lo stato della versione 2.0 della pipeline. Le prossime fasi di sviluppo includono:

- **v2.1:** DPI adattivo per estratti conto (risolve il crash GGML), lista varianti etichette buste paga (target >90% sul lordo)
- **Benchmark v3:** 300 documenti su 10 tipologie, confronto diretto con Amazon Textract, Azure Document Intelligence e Google Document AI sullo stesso corpus
- **Learning progressivo:** sistema di feedback che impara i pattern ricorrenti dei fornitori specifici di ogni cliente
- **Connettori ERP aggiuntivi:** Passepartout, Profis, Danea Easyfatt

---

## Il Processo di Sviluppo: Dalla Prova di Concetto al Prodotto

### Fase 1 — Prova di Concetto (4 settimane)

Il punto di partenza era semplice: riuscire a estrarre la P.IVA e il totale da una fattura PDF con un VLM locale. Ho iniziato con LLaVA su un MacBook M1, con prompt elementari. I risultati erano incoraggianti per i PDF nativi puliti, ma crollavano su qualsiasi documento degradato o con layout non standard.

La prima scoperta importante: il modello non è il collo di bottiglia. Il problema principale era la **conversione del documento in immagine** — la qualità, la risoluzione, il DPI, il modo in cui le pagine multiple venivano gestite. Ho iterato su pdf2image con parametri diversi fino a trovare la configurazione ottimale: 200 DPI, formato PNG, una pagina alla volta, con pre-processing Pillow per aumentare il contrasto.

### Fase 2 — Prompt Engineering Sistematico (6 settimane)

La differenza tra un prompt che funziona sul 60% dei documenti e uno che funziona sul 95% sta in dettagli non intuitivi. Ho costruito un set di test con 30 documenti diversi per tipologia e iterato sui prompt tenendo traccia di ogni variazione e del suo impatto sull'accuratezza.

Le scoperte principali:
- **Separare classificazione ed estrazione** aumenta l'accuratezza di circa 12 punti percentuali rispetto a un prompt unico
- **Specificare le varianti di etichetta** per ogni campo (non solo "VAT number" ma "P.IVA", "Partita IVA", "C.F./P.IVA", "Cod. IVA") riduce i missed fields del 40%
- **Fornire esempi di formato atteso** nel prompt (es. "data nel formato YYYY-MM-DD, esempio: 2025-03-15") riduce gli errori di normalizzazione quasi a zero
- **Istruire esplicitamente il modello a restituire null** per campi non trovati invece di inferire un valore plausibile elimina le allucinazioni sui campi numerici

### Fase 3 — Architettura della Pipeline (4 settimane)

Superata la fase di prompt engineering, il problema successivo era trasformare il prototipo in una pipeline robusta che potesse girare in modo autonomo e non supervisionato. I requisiti:
- Nessun timeout fisso: documenti diversi hanno tempi di processing molto variabili (26-48s)
- Gestione degli errori: crash GGML, risposta malformata, timeout di rete — tutto deve produrre uno stato documentale esplicito, non un'eccezione non gestita
- Idempotenza: se il sistema si riavvia nel mezzo di un processing, il documento deve essere processabile di nuovo senza duplicati

Il sistema di stati documento (QUEUED → PROCESSING → VALIDATED / NEEDS_REVIEW / FAILED) con transizioni atomiche è stato il componente più lungo da progettare correttamente. Un documento non può mai "sparire" tra stati — la transizione è sempre esplicita e loggata.

### Fase 4 — Adapter e Integrazione ERP (5 settimane)

Gli adapter ERP sono stati la parte più sorprendente per complessità. Ogni sistema gestionale ha le sue idiosincrasie:
- Mexal usa un tracciato ASCII a larghezza fissa di 375 caratteri, encoding latin-1, con campi posizionali che cambiano a seconda della versione del software
- Zucchetti Ad Hoc Revolution accetta CSV con separatore punto e virgola, ma la colonna P.IVA deve essere preceduta da apostrofo per evitare che Excel la interpreti come numero
- TeamSystem Digital Hub richiede autenticazione OAuth2 con token a scadenza di 1 ora e gestione del refresh

Ogni adapter ha richiesto l'analisi di file di import di esempio forniti da clienti o trovati nei forum di supporto dei gestionali. Non esiste documentazione pubblica completa per nessuno di questi formati.

### Fase 5 — Benchmark e Validazione (3 settimane)

La costruzione del benchmark è stata una fase di progetto a sé stante. Generare 219 documenti sintetici che siano realistici, matematicamente coerenti e abbastanza diversi da testare robustezza non è banale.

Il generatore usa un seed fisso per riproducibilità. Ogni documento viene generato con:
- Valori numerici casuali ma coerenti (l'IVA è calcolata dal codice, non inserita casualmente)
- Layout scelto da un set di template che copre la varianza reale dei fornitori
- Degradazione applicata con parametri casuali ma controllati (il seed determina il livello di rumore, l'angolo di rotazione, il livello di compressione JPEG)

La ground truth è una struttura JSON per ogni documento con i valori esatti — generata dallo stesso script che ha generato il documento, quindi matematicamente garantita. Questo permette di misurare l'accuratezza in modo completamente automatizzato: confronto JSON estratto vs JSON ground truth con tolleranza ±€0.50 sugli importi.

---

## Riflessioni Tecniche: Cosa Ho Imparato

### I VLM non sono tutti uguali per task specifici

Il mercato tende a valutare i modelli VLM su benchmark generici (VQA, OCR su documenti di testo semplice, descrizione di immagini naturali). Queste valutazioni non predicono bene le performance su un task specifico come l'estrazione strutturata da documenti aziendali degradati. La valutazione corretta è sempre empirica: costruisci un corpus rappresentativo del tuo caso d'uso e misura.

### La verifica matematica vale più dell'accuratezza del modello

Un sistema con 95% di accuratezza che inserisce silenziosamente il 5% di dati sbagliati nel gestionale è peggio di un sistema con 90% di accuratezza che manda in NEEDS_REVIEW tutto ciò che non riesce a verificare. Il math check non aumenta l'accuratezza dell'estrazione — aumenta la fiducia nei dati che entrano nel gestionale. Questa distinzione è fondamentale per convincere un CFO ad adottare il sistema.

### Il dominio specifico è un vantaggio difendibile

Un AI engineer generico può costruire una pipeline di estrazione in poche settimane. Ma conoscere le varianti di etichetta delle buste paga italiane, i formati di import di Mexal e Zucchetti, le regole di calcolo dell'IVA sui beni in reverse charge, il formato del codice alfanumerico SDI per le FatturaPA — questo richiede mesi di esposizione al dominio. È il tipo di conoscenza che non si trova facilmente online e che differenzia un prodotto generico da uno che funziona davvero per le aziende italiane.

### On-premise non significa "vecchio"

C'è un pregiudizio nel settore tech secondo cui "cloud = moderno" e "on-premise = legacy". DataUnchain dimostra il contrario: un sistema on-premise nel 2026, basato su Docker Compose, con un VLM locale via Ollama, è più moderno e più capace di molti sistemi cloud di dieci anni fa. La scelta on-premise non è una limitazione tecnica — è una scelta architetturale motivata da requisiti reali di privacy e sovranità del dato.

--- Non una demo su documenti puliti — una pipeline che gira su scansioni storte, fatture con timbri sovrapposti e buste paga con etichette non standard. Questo è il tipo di engineering che trovo interessante: quando la differenza tra il 60% e il 95% di accuratezza sta nei dettagli del prompt, nella tolleranza matematica di ±€0.50, e nella scelta di far fallire esplicitamente invece di inserire dati sbagliati in silenzio.*

---

📩 **Vuoi valutare un pilot per la tua azienda?** [Contattami](mailto:info@antoniotrento.net)
