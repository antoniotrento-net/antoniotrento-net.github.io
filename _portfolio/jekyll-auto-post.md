---
layout: portfolio
title: "Jekyll Auto Post – Workflow AI per Generazione e Pubblicazione Automatica"
date: 2025-07-19
description: "Sistema automatico che genera e pubblica articoli in un sito Jekyll partendo da un CSV, con contenuti scritti da AI e commit su GitHub, integrato con automazioni n8n."
image: "/assets/images/portfolio/jekyll-auto-post/jekyll-auto-post.jpg"
image-header: "/assets/images/portfolio/jekyll-auto-post/jekyll-auto-post.jpg"
image-paint: "/assets/images/portfolio/jekyll-auto-post/jekyll-auto-post.jpg"
---

**Jekyll Auto Post** è un progetto backend sviluppato per **automatizzare completamente la creazione, generazione e pubblicazione di articoli** su siti web statici Jekyll. Il sistema è progettato per ricevere input da un file CSV e orchestrare l'intero flusso di pubblicazione grazie a un workflow intelligente in n8n.

---

### Caratteristiche principali

- **Integrazione con AI generativa**: tramite modelli GPT-4o-mini, il sistema genera automaticamente testi editoriali coerenti e ottimizzati per SEO a partire da un semplice input testuale.
- **Pipeline n8n completamente automatizzata**: il CSV viene letto in automatico, vengono scelti gli articoli ancora da pubblicare, trasformati in file Markdown compatibili con Jekyll e inviati su GitHub tramite commit diretto su `main`.
- **Gestione immagini e SEO**: il sistema può anche generare immagini di copertina personalizzate (tramite OpenAI Image API o Sora) e includerle nel frontmatter, ottimizzando i contenuti per la condivisione social.
- **Pubblicazione multi-piattaforma**: ogni articolo può essere automaticamente condiviso su social media come Twitter/X, LinkedIn o Facebook, ed eventualmente inoltrato a una newsletter.

---

### Utilizzo reale

Il sistema **è già utilizzato in produzione su vari siti attivi** come:

- 🔗 [antoniotrento.net](https://antoniotrento.net) — sito personale e portfolio tecnico
- 🔗 [audely.github.io](https://audely.github.io) — progetto di receptionist AI vocale automatica
- 🔗 [fomofoto.net](https://fomofoto.net) — esperimento editoriale di pubblicazione visuale e fotografica

Questo conferma l'affidabilità del sistema in scenari eterogenei, dalla pubblicazione tecnica all'editoria multimediale.

---

### Tecnologie usate

- **Jekyll** per la generazione del sito statico
- **n8n** per l’automazione backend low-code
- **GitHub API** per versioning e deploy continuo
- **OpenAI GPT-4o-mini** per la scrittura dei contenuti
- **Image AI (DALL·E / Sora)** per le immagini automatiche
- **Docker** per l’ambiente di esecuzione
- **CSV** come input e sistema di stato semplificato

---

### Vantaggi strategici

Questo progetto è una dimostrazione pratica di come AI e automazione possano ridurre drasticamente il tempo, il costo e la complessità nella gestione di contenuti digitali. Il sistema consente la **scalabilità editoriale** con intervento umano quasi nullo, mantenendo **alta qualità e coerenza visiva**.

Grazie alla sua architettura modulare, può essere adattato ad altri casi d’uso come:

- redazioni digitali
- knowledge base tecniche
- marketplace di contenuti
- siti multilingua con pubblicazione automatica

---

### Codice e demo

🔧 Codice sorgente disponibile su GitHub:  
**[github.com/antonio-backend-projects/jekyll-recipe-ai](https://github.com/antonio-backend-projects/jekyll-recipe-ai)**

🌐 Demo pubblica:  
**[antonio-backend-projects.github.io/jekyll-recipe-ai](https://antonio-backend-projects.github.io/jekyll-recipe-ai)**

---

Jekyll Auto Post è un perfetto esempio di orchestrazione intelligente tra AI, automazione e strumenti open-source. Rappresenta una **soluzione scalabile, robusta e già testata sul campo**, pensata per creator, aziende, e sviluppatori che vogliono un sistema editoriale automatico sempre attivo.

