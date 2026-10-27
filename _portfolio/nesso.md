---
layout: portfolio
title: "Nesso"
date: 2026-10-23
description: "Integrazione tra EspoCRM e sistemi aziendali: un motore Python per configurare trasferimenti, regole sui campi e controlli prima degli aggiornamenti."
image: "/assets/images/portfolio/nesso/nesso.jpg"
image-header: "/assets/images/portfolio/nesso/nesso.jpg"
image-paint: "/assets/images/portfolio/nesso/nesso.jpg"
og_image: "og/nesso.jpg"
tags: [EspoCRM, Integrazione, Python, Docker, API, Jekyll, Open Source]
---

# Nesso: collegare EspoCRM ai sistemi aziendali

**Nesso è uno strumento di integrazione che automatizza il trasferimento dei dati tra EspoCRM, gestionali, siti web e file aziendali.** Dall’interfaccia si configurano le sorgenti, si associano i campi e si verificano le modifiche prima di applicarle al CRM.

Ho progettato il prodotto attorno a un’esigenza precisa: mantenere aggiornate le informazioni provenienti dai sistemi esterni, conservando quelle che le persone gestiscono direttamente in EspoCRM. Un indirizzo amministrativo e una nota commerciale possono appartenere alla stessa anagrafica, ma richiedono regole diverse.

Il progetto comprende il motore Python, l’interfaccia di configurazione, l’ambiente dimostrativo Docker, il manuale bilingue e il sito di presentazione.

- **Sito del prodotto:** [scopri Nesso](https://nessocrm.github.io/it/).
- **Codice e istruzioni:** [repository Nesso su GitHub](https://github.com/nessocrm/nessocrm).
- **Ambito:** integrazione dei dati, automazione dei processi e progettazione di prodotto.

---

## Il problema: informazioni distribuite, aggiornamenti da governare

Un’azienda può usare EspoCRM per le relazioni commerciali e affidare ad altri strumenti la gestione di clienti, documenti, commesse o fatture. Le informazioni raggiungono il CRM attraverso esportazioni periodiche, interrogazioni al database e richieste dal sito web.

Il trasferimento iniziale è solo una parte del problema. Occorre decidere anche cosa fare quando un dato cambia, un campo arriva vuoto o un cliente non compare più nel file. Senza regole esplicite, un’importazione può sovrascrivere una nota utile o lasciare nel CRM informazioni non più aggiornate.

Per questo ho concentrato il lavoro su tre obiettivi:

1. **Configurare i flussi dall’interfaccia**, separando l’accesso alla sorgente dalle regole sui dati.
2. **Controllare gli aggiornamenti per singolo campo**, distinguendo le informazioni del gestionale da quelle curate nel CRM.
3. **Rendere verificabile ogni elaborazione**, dall’anteprima ai risultati e agli errori.

## La soluzione: collegamenti e regole separati

Nesso organizza la configurazione in due elementi. Il **collegamento** definisce come comunicare con il sistema esterno: indirizzo, canale e autenticazione. L’**integrazione** stabilisce quali dati trasferire, in quale scheda di EspoCRM e con quale frequenza.

La separazione permette di riutilizzare uno stesso collegamento per flussi diversi. Un sito, per esempio, può alimentare Lead e Contatti attraverso due integrazioni, ciascuna con i propri identificativi e abbinamenti.

I canali disponibili coprono situazioni operative differenti:

- **Webhook**, per ricevere dati inviati da siti e applicazioni.
- **Database**, per leggere dati con query SELECT da MySQL, MariaDB, PostgreSQL, SQL Server e Oracle.
- **CSV ed Excel**, per importazioni periodiche da cartelle locali o server SFTP e FTPS.
- **HTTP e trasferimenti file supportati**, per inviare informazioni ai sistemi destinatari.
- **Documenti e PDF**, con la possibilità di associare un PDF all’azienda quando il nome contiene la sua chiave identificativa completa.

La compatibilità dipende dai formati e dalle interfacce del sistema da collegare. I modelli di configurazione per anagrafiche, contatti, sedi e listini preparano gli abbinamenti più comuni, da verificare sul caso specifico.

## Un esempio: aggiornare un cliente e conservare la nota commerciale

Consideriamo un’importazione periodica delle anagrafiche dal gestionale. Il file contiene codice cliente, ragione sociale, città e nota; nel frattempo, il commerciale ha aggiornato la nota direttamente in EspoCRM.

Durante la configurazione si stabilisce che ragione sociale e città vengono aggiornate dal gestionale, mentre la nota resta sotto il controllo del CRM.

| Informazione ricevuta | Regola configurata | Risultato previsto |
|---|---|---|
| Ragione sociale modificata | Priorità alla sorgente | Aggiornamento del valore nel CRM |
| Città vuota | Priorità alla sorgente | Svuotamento del campo nel CRM |
| Nota diversa da quella esistente | Priorità a EspoCRM | Conservazione della nota e raccolta della differenza per verifica |
| Dati identici a quelli già elaborati | Confronto dei valori da scrivere | Record riconosciuto come invariato |

**Un valore vuoto è quindi una decisione da gestire, non un dettaglio da ignorare.** Se prevale la sorgente, può svuotare il campo; se il campo è gestito in EspoCRM, l’aggiornamento conserva il valore esistente. Alla creazione di un nuovo record, il valore iniziale può comunque provenire dalla sorgente.

L’assenza di un’intera anagrafica viene trattata separatamente. Quando la gestione delle assenze è configurata e la scheda dispone di uno stato compatibile, Nesso può chiudere il record mantenendolo nello storico. La prima chiusura richiede conferma.

## Dalla configurazione all’attivazione

L’interfaccia accompagna la preparazione di un’integrazione in quattro passaggi:

1. **Collegamento:** scelta del canale e delle impostazioni di accesso.
2. **Scheda:** selezione dell’entità di EspoCRM da utilizzare.
3. **Abbinamento:** associazione delle colonne ai campi, trasformazioni e priorità di aggiornamento.
4. **Pianificazione:** frequenza, dipendenze e riepilogo della configurazione.

Prima dell’attivazione, l’anteprima mostra l’impatto previsto sui record. La prova a secco permette di esaminare un campione senza scrivere su EspoCRM. Sono disponibili anche una modalità di sola lettura per integrazione e un blocco generale delle scritture verso il CRM.

La schermata Attività raccoglie esiti, righe scartate e conflitti. Il monitoraggio mostra l’ultimo successo, l’ultimo errore e la prossima esecuzione. Si possono inoltre definire orari entro cui attendere un file e soglie di inattività da segnalare nell’applicazione.

Per chi configura il sistema e poi lo consegna al cliente, una pagina dedicata riepiloga integrazioni, orari e regole dei campi, senza includere password o token.

---

## Le scelte tecniche principali

### EspoCRM accessibile attraverso le API

Nesso legge e scrive nel CRM tramite le API HTTP di EspoCRM. Anche la creazione di schede, campi e relazioni utilizza le API. Il database del CRM resta gestito da EspoCRM; le query dei collegamenti database riguardano invece le sorgenti esterne.

Questa scelta mantiene un’interfaccia di integrazione definita e separa la logica del trasferimento dalla struttura interna delle tabelle del CRM.

### Identificare i record e riconoscere le modifiche

In ingresso, l’identità combina l’integrazione con il codice esterno del record. Quando serve, la chiave può comprendere più colonne: codice società e codice cliente, per esempio, distinguono anagrafiche di società diverse con lo stesso codice cliente.

Il confronto tramite hash riconosce i dati già elaborati ed evita di ripetere aggiornamenti identici. Le eventuali corrispondenze con record preesistenti seguono la politica sui duplicati configurata.

In uscita, un cursore registra l’avanzamento delle esportazioni. Negli invii HTTP viene aggiornato dopo le consegne riuscite, così i record non consegnati possono essere ripresi nelle esecuzioni successive.

### Adattarsi alle schede disponibili

Nesso legge da EspoCRM le schede e i campi utilizzabili. La configurazione può quindi lavorare con Aziende, Contatti e Lead, ma anche con le schede personalizzate della specifica installazione.

Quando il processo lo richiede, si possono creare nuove schede e campi tramite le API. Restano elementi di EspoCRM, con il suo modello di dati e i suoi permessi.

### Assistenza all’abbinamento, con conferma

La proposta di abbinamento riconosce nomi e sinonimi delle colonne in italiano e inglese e suggerisce i campi corrispondenti. Questa funzione lavora localmente.

Un modello esterno, se configurato, può aiutare a completare gli abbinamenti mancanti. La richiesta può includere nomi di colonne e campioni di celle, ma esclude le password del collegamento. Le proposte vanno sempre riviste prima di salvare l’integrazione.

## Stack e organizzazione del progetto

| Componente | Tecnologia e funzione |
|---|---|
| Motore di integrazione | Python, API HTTP, elaborazione dei dati e pianificazione |
| Stato operativo | SQLite per configurazioni, identificativi, avanzamento e registro delle attività |
| CRM | EspoCRM, interrogato e aggiornato tramite API |
| Ambiente di prova | Docker Compose con Nesso, EspoCRM, daemon del CRM e MariaDB |
| Documentazione | MkDocs, con manuale in italiano e inglese |
| Sito del prodotto | Jekyll su GitHub Pages, con pagine italiane e inglesi |

Il repository comprende test dedicati a importazioni, esportazioni, regole sui campi e comportamento delle integrazioni. La documentazione descrive funzioni e limiti della versione e viene aggiornata insieme al prodotto.

## La demo: un contesto aziendale da esplorare

L’ambiente locale installa EspoCRM e carica la demo **Gruppo Meridia**, un’impresa industriale immaginaria. I dati fittizi comprendono aziende, contatti, richieste, offerte, contratti, commesse, interventi, fatture e ticket.

La demo permette di seguire relazioni e trasferimenti in un contesto coerente: un cliente ha contatti e sedi, un’offerta può essere collegata a un contratto, una commessa può avere interventi e fatture. È un ambiente di valutazione tecnica, distinto da un caso cliente reale.

Per riprodurre gli scenari occorre verificare i requisiti descritti nel manuale. Le estensioni commerciali di EspoCRM, come l’Advanced Pack, non sono distribuite nel repository.

## Stato del prodotto e aspetti da configurare

Nesso è alla prima versione. Prima dell’adozione, occorre validare identificativi, regole sui campi, permessi e compatibilità dei flussi nell’ambiente di destinazione.

Alcune opzioni richiedono una scelta esplicita:

- **Scrittura di ritorno al database esterno:** da abilitare sulla singola integrazione, limitandola alle colonne indicate.
- **Nuovi tentativi e filtri per team:** da configurare secondo il processo operativo.
- **Protezione delle credenziali salvate:** richiede `NESSO_SECRET_KEY`. La demo non imposta la variabile, quindi le credenziali nel volume locale restano in chiaro.

Gli avvisi del motore sono consultabili nell’applicazione; l’invio di notifiche email non è attualmente disponibile.

## Cosa dimostra questo progetto

Nesso raccoglie un lavoro di **integrazione dei sistemi e progettazione del prodotto**: definizione dei flussi, gestione dell’identità dei record, controllo delle modifiche e strumenti per chi deve configurare e mantenere il collegamento.

La parte tecnica è accompagnata da un percorso di utilizzo verificabile: configurazione guidata, anteprima, attivazione progressiva, monitoraggio e consegna. Manuale, demo e sito permettono di esaminare le stesse funzioni da prospettive diverse.

> Il punto centrale del progetto è rendere esplicite le regole con cui i sistemi si scambiano le informazioni, così che chi usa il CRM possa capire cosa viene aggiornato e chi gestisce l’integrazione possa verificarne l’esito.

Per esplorare il prodotto, visita il [sito di Nesso](https://nessocrm.github.io/it/). Il [repository pubblico](https://github.com/nessocrm/nessocrm) contiene codice, istruzioni di avvio e manuale bilingue.
