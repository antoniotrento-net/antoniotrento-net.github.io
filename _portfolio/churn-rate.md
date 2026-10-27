---
layout: portfolio
title: "Churn Rate Calculator – Analisi e Predizione dell’Abbandono Clienti"
date: 2025-08-10
description: "Dal calcolo statistico di base a un sistema predittivo di AI: uno strumento completo per comprendere, analizzare e prevenire il churn nel settore energia e gas."
image: "/assets/images/portfolio/churn-rate/churn-rate.jpg"
image-header: "/assets/images/portfolio/churn-rate/churn-rate.jpg"
image-paint: "/assets/images/portfolio/churn-rate/churn-rate.jpg"
og_image: "og/churn-rate.jpg"
tags: [AI, MachineLearning, DataScience, Energy, Python, Analytics]
---

## 🌟 Panoramica del Progetto

Il **Churn Rate Calculator** è uno strumento sviluppato in **Python** per calcolare, analizzare e prevedere l’**abbandono clienti** (*customer churn*) nel settore **energia e gas**.  
Il progetto è nato inizialmente come **calcolatore statistico** semplice, ma si è rapidamente trasformato in una **piattaforma di analisi predittiva** grazie all’integrazione di tecniche di **Machine Learning**.

L’obiettivo principale è fornire un tool **leggero, veloce e altamente interpretabile** che permetta alle aziende di comprendere:

- **Chi sta abbandonando**
- **Quando è più probabile che accada**
- **Quali fattori influenzano maggiormente la decisione del cliente**

---

## 🔍 Contesto e Motivazioni

Il churn rate è un indicatore cruciale per qualunque business basato su contratti ricorrenti.  
Nel settore energia e gas, un churn elevato può comportare:

- **Perdita diretta di ricavi**
- **Aumento dei costi di acquisizione nuovi clienti**
- **Riduzione della stabilità finanziaria**

Questo progetto è stato pensato per **mettere la potenza dei dati nelle mani delle aziende**, riducendo il gap tra dati grezzi e decisioni strategiche.

---

## 📊 Funzionalità Chiave

### 1. Analisi Base
- Calcolo diretto del churn rate con formula:

```

(Clienti Persi / Clienti Totali) × 100

```
- Richiede solo due campi minimi: `customer_id` e `status`
- Risultato immediato e visualizzabile in pochi secondi

### 2. Analisi Avanzata con Machine Learning
- Calcolo del churn mensile e trimestrale
- Modello **RandomForestClassifier** ottimizzato
- Gestione dello **squilibrio delle classi** con tecniche di bilanciamento
- Predizione dei clienti a rischio in tempo reale
- **Esclusione automatica** di chi è già churned per risultati puliti
- Visualizzazioni grafiche: trend storici, variabili predittive, distribuzioni
- Report automatici con metriche:
- Accuracy
- Precision
- Recall
- Feature importance

---

## ⚖️ Confronto tra Versione Base e Avanzata ML

| Caratteristica                        | Base    | Avanzata ML                   |
| ------------------------------------- | ------- | ----------------------------- |
| Input richiesto                       | Minimo  | Esteso (variabili aggiuntive) |
| Accuratezza                           | ~80%    | 98%                           |
| Predizione clienti a rischio          | ❌       | ✅                             |
| Grafici e visualizzazioni             | ❌       | ✅                             |
| Tempo di calcolo                      | < 1s    | 1-3s                          |
| Training su nuovi dati                 | ❌       | ✅                             |
| Analisi trend temporali               | ❌       | ✅                             |
| Report PDF/HTML                       | ❌       | ✅                             |

---

## 🛠️ Architettura Tecnica

1. **Preprocessing dei Dati**
 - Pulizia e normalizzazione
 - Gestione dei valori mancanti
 - Encoding delle variabili categoriche

2. **Feature Engineering**
 - Creazione di nuove variabili derivate da quelle esistenti
 - Identificazione di pattern temporali (es. contratti in scadenza)

3. **Training del Modello**
 - Algoritmo: `RandomForestClassifier`
 - Ottimizzazione con `GridSearchCV`
 - Valutazione con *k-fold cross validation*

4. **Output e Visualizzazione**
 - Grafici di distribuzione churn/non churn
 - Importanza delle feature
 - Liste clienti a rischio

---

## 📈 Risultati e Performance

- **Accuratezza globale:** 98%
- **Precisione churners:** 100%
- **Recall churners:** 89%
- Variabile più predittiva: numero di contatti con il supporto negli ultimi 12 mesi
- Tempo medio di predizione: **<3 secondi**

---

## 🚀 Possibili Evoluzioni Future

- **Interfaccia Web** per utilizzo senza conoscenze di programmazione
- Integrazione con CRM e sistemi di ticketing
- Modelli di Deep Learning per pattern più complessi
- Automatizzazione report giornalieri via email
- Implementazione di dashboard interattive (Plotly, Dash)

---

📂 **Repository GitHub:** [https://github.com/antonio-backend-projects/churn-rate-test-qwen/](https://github.com/antonio-backend-projects/churn-rate-test-qwen/)  
💡 **Tecnologie:** Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
