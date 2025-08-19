---
layout: portfolio
title: "oracle-shell – Reverse engineering per DB Oracle"
date: 2025-08-19
description: "Shell interattiva per esplorare e fare reverse engineering su database Oracle: REPL, comandi meta, ricerca colonne (es. IBAN), esecuzione batch e config via .env"
image: "/assets/images/portfolio/oracle-shell/oracle-shell.jpg"
image-header: "/assets/images/portfolio/oracle-shell/oracle-shell.jpg"
image-paint: "/assets/images/portfolio/oracle-shell/oracle-shell.jpg"
tags: [python, shell, backend, tools]
---

## Panoramica

**oracle-shell** è una utility da terminale pensata per **fare reverse engineering su database Oracle** quando la documentazione è scarsa o nulla. Consente di scoprire velocemente **dove vivono davvero i dati**, mappare tabelle/colonne e verificare flussi applicativi con ricerche mirate (es. *IBAN*).

> Progetto portfolio di **Antonio Trento**.

## Problema

In molti contesti enterprise il database è ampio, storico e poco omogeneo. Serviva uno strumento **leggero e immediato** per:

* esplorare schemi e tabelle senza IDE pesanti,
* cercare **campi chiave** (es. IBAN) in tutto il DB,
* lanciare query in sequenza con **sicurezza su DML** (commit/rollback espliciti).

## Soluzione

* **REPL SQL**: esecuzione quando termini con `;`, multi-riga, messaggistica chiara.
* **Comandi meta**:

  * `\schemas`, `\tables [pattern]`, `\d owner.tabella`, `\find %TESTO%`.
* **Ricerca rapida “investigativa”**: pattern su dizionari Oracle per trovare colonne candidate (es. tutte quelle che contengono “IBAN”), con snippet pronti per verifiche record-level.
* **Batch mode**: `--file` per script `.sql` separati da `;`.
* **Config via `.env`**: nessuna credenziale hardcoded; pronto per ambienti diversi.

## Come viene usato

Un caso tipico è il **tracciamento end-to-end**:

1. si inserisce un **valore fittizio** dal frontend (es. un IBAN di test),
2. con `\find %IBAN%` si individuano le colonne candidate,
3. si lancia una **ricerca normalizzata** (maiuscolo, senza spazi/trattini) per capire **quali tabelle** vengono realmente aggiornate,
4. si procede a verifiche/patch scriptate con DML e **commit controllato**.

## Stack & dettagli

* **Python** + `oracledb` (Instant Client)
* Output tabellare leggibile, **limite righe** configurabile (`--limit`)
* Supporto Windows; encoding UTF-8 e fallback compatibili con prompt datati

## Risultato

Riduce drasticamente il tempo di discovery: da “giorni a colpi di SELECT casuali” a **minuti** con un flusso guidato. Ideale per **migrazioni**, **refactoring di integrazioni** e **audit**.

## Codice sorgente

* GitHub: **[antonio-backend-projects/oracle-shell](https://github.com/antonio-backend-projects/oracle-shell)**


