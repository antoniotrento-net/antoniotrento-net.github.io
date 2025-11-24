---
layout: portfolio
title: "Corallo del crepuscolo"
date: 2024-06-28
description: "Acrilico su tela"
image: "/assets/images/portfolio/corallo-del-crepuscolo/corallo-del-crepuscolo-v1.jpg"
image-header:
image-paint: "/assets/images/portfolio/corallo-del-crepuscolo/image-paint-corallo-del-crepuscolo-v1.jpg"
slider:
  - "/assets/images/portfolio/corallo-del-crepuscolo/corallo-del-crepuscolo-slide-1.jpg"
  - "/assets/images/portfolio/corallo-del-crepuscolo/corallo-del-crepuscolo-slide-2.jpg"
---

> _“La natura non ha bisogno di gridare per essere ascoltata.”_

In questa composizione, Franco Trento evoca la forma effimera e ramificata di un **corallo immerso in un mare notturno** o forse di una creatura silenziosa che si dischiude alla luce fioca del tramonto. Le tonalità pesca si stagliano su uno sfondo scuro, quasi abissale, creando un effetto di rilievo e profondità che suggerisce movimento, vita, **una metamorfosi in atto**.

La materia pittorica è distribuita in tocchi densi e organici, come cellule in espansione, creando una **trama vivente** che pulsa sul confine tra astratto e figurativo.

Quest’opera parla di **fragilità luminosa**, di bellezza che si rivela solo a chi osserva con attenzione. Un richiamo al mondo naturale, che anche nell’ombra riesce a generare forme di meraviglia.





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

