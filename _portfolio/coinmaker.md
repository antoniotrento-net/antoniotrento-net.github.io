---
layout: portfolio
title: "Coinmaker – MWFormation & Smart Money Suite"
date: 2025-12-06
description: "Motore di trading algoritmico multi-strategia (MWFormation + Smart Money), con backtest di un anno, gestione del rischio integrata e pipeline end-to-end verso broker, storage dati e monitoring. Il repository è privato e pensato per un utilizzo professionale."
image: "/assets/images/portfolio/coinmaker/coinmaker.jpg"
image-header: "/assets/images/portfolio/coinmaker/coinmaker.jpg"
image-paint: "/assets/images/portfolio/coinmaker/coinmaker.jpg"
tags: [Trading Bot, Algorithmic Trading, Python, Backtesting, Risk Management, Broker API, Docker, Quantitative Strategy, Automation]
---


> *"Non mi interessava fare l’ennesimo bot da retail. Volevo un motore serio, backtestato, estendibile, che potesse diventare un prodotto vendibile a trader professionali e desk quantitativi."*

**Coinmaker – MWFormation & Smart Money Suite** è un progetto di trading algoritmico completo:
un motore multi-strategia scritto in Python, containerizzato, con backtest di un anno e integrazione end-to-end con broker, data feed, storage e sistemi di notifica.

Il repository è **privato**: il codice non è pubblico, perché le strategie sono **profittevoli** (MWFormation mostra un gain di circa **+12% su un anno di backtest** nel setup attuale).
L’accesso al sorgente è valutato **solo su richiesta** e solo in ottica di collaborazione/uso professionale, non per curiosi o utilizzo “plug & play” retail.

---

## Panoramica strategica

Il motore espone due famiglie di strategie indipendenti ma orchestrate dallo stesso framework:

### 1. MWFormation

Strategia discrezionale codificata attorno alle classiche figure **“M” e “W”** (doppio massimo / doppio minimo), ma implementata con un motore di **pattern recognition** robusto:

* Identificazione automatica di **swing high / swing low** su serie OHLC.
* Riconoscimento di pattern M/W con:

  * vincoli su profondità e distanza temporale fra i pivot,
  * filtri di simmetria e “pulizia” del pattern,
  * conferme su chiusure e volumetria.
* Filtri di **contesto di mercato**:

  * trend di fondo (medie mobili multi-timeframe),
  * livelli chiave (high/low settimanali/mensili, livelli di range),
  * volatilità (ATR) per adattare distanza di stop e target.
* Logica di **entry/exit** parametrizzabile:

  * entry su breakout/ritest del neckline,
  * stop dinamici (ATR, struttura) e partial take-profit,
  * gestione RR target (es. 1:2 / 1:3) e trailing opzionale.

La strategia è pensata per timeframe operativi swing/intraday (es. H1–H4), con regole completamente deterministiche e backtestabili.

---

### 2. Smart Money Strategy

Una seconda famiglia di strategie ispirata ai concetti di **Smart Money Concepts**:

* Ricostruzione della **market structure**:

  * identificazione automatica di BOS/CHOCH (Break of Structure / Change of Character),
  * definizione di trend attivo e zone di interesse.
* Rilevazione di:

  * **liquidity grab / stop hunt** sopra/sotto massimi e minimi chiave,
  * **order block** e zone di supply/demand,
  * compressioni di prezzo seguite da espansioni impulsive.
* Filtri multi-livello:

  * sessioni orarie operative (esclusione di fasce illiquide),
  * filtri di spread/commissione del broker,
  * regime di volatilità (no entry in condizioni estreme o in “chop”).
* Modulo di **position building**:

  * ingressi parziali su più livelli,
  * scaling-out su target intermedi,
  * gestione diaria/max-drawdown per protezione del conto.

Questa parte del motore è strutturata per poter ospitare in futuro ulteriori varianti Smart Money sulla stessa infrastruttura di backtest ed execution.

---

## Architettura tecnica

Il progetto è organizzato come un **motore di trading generalizzato**, non come un singolo script:

* **`core/engine.py`**
  Loop principale, gestione degli eventi (nuova candela, segnale, ordine eseguito), orchestrazione delle strategie registrate.

* **`data/`**
  Moduli per il caricamento e l’aggiornamento di dati storici e real-time:

  * connettori verso API REST/WebSocket del broker/exchange,
  * normalizzazione OHLCV,
  * salvataggio su storage locale/DB per riuso nei backtest.

* **`strategies/mwformation.py`**
  Implementa:

  * motore di detection M/W,
  * generazione segnali long/short,
  * interfaccia standardizzata verso il motore (metodi `on_bar`, `on_signal`, ecc.).

* **`strategies/smart_money.py`**
  Modulo che ricostruisce la market structure, calcola order block, liquidity sweep e genera i setup Smart Money.

* **`risk/risk_manager.py`**
  Layer trasversale che decide:

  * size della posizione (percentuale di equity, fixed-fraction, ecc.),
  * max rischio per trade, max perdita giornaliera,
  * blocco dell’operatività in caso di drawdown.

* **`backtesting/`**
  Motore di simulazione che riusa gli stessi moduli di strategia:

  * ingest dei dati storici,
  * simulazione tick-by-tick o bar-by-bar,
  * applicazione di spread, commissioni e slippage,
  * calcolo delle metriche finali.

* **`config/` (YAML + `.env`)**
  Tutta la parametrizzazione è esterna al codice:

  * coppie/trading universe,
  * timeframe, orari operativi,
  * parametri delle strategie (pattern, filtri, RR),
  * credenziali broker, chiavi API, endpoint.

Il motore è pensato per essere **estendibile**: aggiungere una nuova strategia significa creare un modulo che implementa una semplice interfaccia e registrarlo nel core.

---

## Motore di backtesting

Uno dei punti chiave del progetto è il **backtester proprietario**, progettato per ridurre al minimo il gap fra test e operatività reale:

* Simulazione **bar-based** con gestione esplicita di:

  * apertura/chiusura ordini,
  * esecuzione di stop/target entro la stessa candela,
  * gap e buchi di mercato.
* Supporto multi-strumento e multi-strategia:

  * più strategie attive in parallelo sullo stesso asset,
  * controllo di conflitti (es. limitare l’esposizione totale).
* Calcolo automatico di:

  * equity curve,
  * drawdown assoluto e relativo,
  * sharpe/ sortino ratio,
  * distribuzione dei trade,
  * analisi per fascia oraria / giorno della settimana.

Nel setup attuale, la strategia **MWFormation**, backtestata su un anno di dati, mostra un gain intorno al **+12%** (al netto di costi modellati).
Naturalmente si tratta di risultati storici, **non** di garanzie di performance future.

---

## Gestione del rischio e controllo esposizione

La parte di **risk management** non è un’aggiunta cosmetica, ma un layer centrale:

* sizing dinamico basato su:

  * rischio per trade (% equity),
  * volatilità del sottostante (ATR-based),
  * plafond giornalieri/settimanali;
* limiti globali:

  * max numero di posizioni aperte,
  * max esposizione in leva,
  * kill-switch automatico oltre una certa soglia di drawdown;
* log dettagliati di:

  * ogni decisione del risk manager,
  * motivazione di riduzioni/stop dell’operatività.

Questo rende il motore adatto a contesti in cui il **controllo del rischio** è tanto importante quanto il setup di ingresso.

---

## Integrazione, deployment e automazione

Il progetto dimostra anche la capacità di integrare più componenti in un ecosistema unico:

* **Containerizzazione Docker**
  L’intero motore gira in un container dedicato:

  * facile deployment su VPS, server on-prem o cloud,
  * separation of concerns rispetto ad altri servizi.

* **Integrazione broker/API**
  Il motore comunica con il broker tramite API REST/WebSocket:

  * invio ordini market/limit/stop,
  * polling o streaming delle esecuzioni,
  * riconciliazione dello stato interno con quello del conto.

* **Logging & monitoring**
  Logging strutturato (JSON) e rotazione log per:

  * segnali generati,
  * ordini inviati, modificati, cancellati,
  * interventi del risk manager.

* **Notifiche**
  Hook per notifiche (es. Telegram / email) per:

  * nuovi trade aperti/chiusi,
  * superamento soglie di rischio,
  * errori di connessione o problemi con il broker.

Il risultato è un sistema **automatizzato ma osservabile**, adatto a essere monitorato nel tempo e a scalare su più strategie.

---

## Accesso al progetto & posizione commerciale

Questo progetto non è pensato come “repo open source per smanettare”.

* Il codice risiede in un **repository privato**, con:

  * strategie MWFormation & Smart Money,
  * motore di backtesting,
  * infrastruttura di execution completa.
* L’accesso è valutato **solo per collaborazioni serie**:

  * desk di trading,
  * gestori,
  * team quant che cercano un punto di partenza solido da estendere.

Non viene fornito supporto a chi cerca un “bot magico” da collegare al proprio conto personale senza competenze tecniche o di rischio.

> Se sei interessato a valutare **collaborazioni professionali** o un utilizzo commerciale del motore (licenza, customizzazione, integrazione sul tuo stack), puoi contattarmi per una demo privata.
> L’equity curve, i risultati di backtest e l’architettura interna vengono condivisi solo in questo contesto.
