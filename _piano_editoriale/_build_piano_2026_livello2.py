# -*- coding: utf-8 -*-
"""Secondo livello: stack/portfolio. Non è il piano traffico. Jekyll non lo monta."""
import csv
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).with_name("piano-editoriale-2026-livello2-stack.csv")

ARTICLE_RULES = """
IDENTITÀ
Scrivi in italiano come Antonio Trento, system architect e AI integrator (sito ufficiale https://antoniotrento.net).
Tono: diretto, concreto, un po' pungente. Parli a founder, CTO e responsabili IT di PMI italiane che vogliono stack sovrani, non slide.
Non sei un giornalista da magazine. Sei uno che monta Docker, n8n, Salesforce, RAG e agenti in produzione.

LUNGHEZZA (OBBLIGATORIA)
Minimo 4500 parole, target 5000–6000. Se sei sotto le 4500, allunga con: (a) un secondo walkthrough tecnico, (b) una sezione “cosa si rompe in produzione”, (c) una tabella comparativa, (d) 10 FAQ lunghe. Non diluire con ripetizioni.

FORMATO
Markdown. Niente YAML front matter (lo aggiunge la pipeline). Inizia con un H2, non ripetere il titolo come H1.
Usa H2 e H3 reali. Paragrafi corti. Elenchi. Almeno 2 blocchi di codice (yaml, python, bash o json) copiabili.
Almeno 1 tabella Markdown. Almeno 8 FAQ in fondo. Checklist operativa prima della conclusione.
Chiudi con un CTA sobrio verso https://antoniotrento.net e https://antoniotrento.net/biografia/ — niente hard sell.

SEO
Keyword principale da usare nel primo paragrafo, in almeno 2 H2, e in chiusura, in forma naturale (niente stuffing).
Keyword secondarie: spargi 4–6 occorrenze totali, variate.
Titoli H2 in stile long-tail, non “Introduzione / Conclusioni” nudi. La conclusione può chiamarsi come un verdetto.

VIETATO
- Frasi del tipo “nel mondo di oggi l’intelligenza artificiale sta rivoluzionando”.
- Elenco di settori (sanità, finance, agri, flotte, smart city) senza architettura.
- Promettere “AI che fa tutto da sola”.
- Inventare clienti, fatturati, loghi, o “ho implementato in Ferrari”.
- Tutorial da 800 parole spacchettato. Ogni sezione deve aggiungere un vincolo reale (GDPR, governor limit, GPU VRAM, pec, XML FatturaPA, rate limit, lock-in).
- Consigliere SaaS cloud come default. Default = self-hosted / Docker / dati in Italia o in UE sotto il controllo del cliente.

OBBLIGATORIO NEL TESTO
- Un’architettura di riferimento (componenti, confini, cosa NON tocca l’agente).
- Un percorso di implementazione a step numerati.
- Fallimenti tipici e come li riconosci dai log.
- Costi (ordine di grandezza in euro, token, VRAM, kWh) anche stimati e dichiarati come stime.
- Sezione “quando NON farlo”.
"""

IMAGE_SIZE = (1536, 1024)

IMAGE_RULES = (
    "Photorealistic editorial photograph, landscape 1536x1024 pixels (3:2), "
    "no text, no letters, no watermarks, no logos, no UI screenshots, no diagrams with labels. "
    "Dark professional lighting, shallow depth of field, cinematic but documentary. "
    "Suitable as a blog cover on a system-architect website. "
    "Do not depict a recognizable celebrity. Adult professional environment. "
)


def article_prompt(title, kw, kw2, angle, outline, must):
    bullets = "\n".join(f"- {x}" for x in outline)
    musts = "\n".join(f"- {x}" for x in must)
    return f"""{ARTICLE_RULES}

TITOLO DA RISPETTARE COME TEMA (non copiarlo come H1): {title}
KEYWORD PRINCIPALE: {kw}
KEYWORD SECONDARIE: {kw2}

ANGOLO EDITORIALE (non uscirne):
{angle}

OUTLINE OBBLIGATORIA (trasforma ogni punto in H2/H3, nell’ordine, approfondendo):
{bullets}

DEVI INCLUDERE NEL CORPO:
{musts}

Scrivi ora l’articolo completo in italiano, 5000–6000 parole, Markdown.
"""


def image_prompt(scene):
    return f"{IMAGE_RULES}{scene}"


POSTS = [
    dict(
        titolo="Perché il tuo workflow n8n con GPT-4o sta inviando i dati dei clienti a OpenAI (e come chiuderlo in Docker in 90 minuti)",
        kw="n8n self-hosted openai privacy",
        kw2="n8n docker, gdpr llm, dati clienti openai, workflow n8n produzione",
        descrizione="Post verticale su un errore da produzione: n8n self-hosted non è privacy se il nodo OpenAI manda body, file e PII in chiaro. Architettura per tenere i prompt in UE, proxy locale, redaction e kill-switch.",
        angle="Il clickbait è vero: self-hosting n8n non protegge nulla se l’LLM è cloud. Smonta il mito e mostra il recinto.",
        outline=[
            "Il malinteso: “è sul mio VPS quindi è GDPR-ok”",
            "Cosa esce davvero da un nodo OpenAI/Anthropic (body, header, retry, log del vendor)",
            "Mappa dei nodi n8n che esfiltrano senza che te ne accorga",
            "Redaction prima del modello: PII, IBAN, CF, pec, allegati",
            "Architettura chiusa: n8n + Ollama/vLLM + Postgres sulla stessa rete Docker",
            "Quando il cloud LLM è accettabile (contratto, DPA, regione, dati sintetici)",
            "Playbook 90 minuti: compose, credenziali, test con payload finto",
            "Come dimostrarlo a un DPO con log e diagramma dei confini",
        ],
        must=["docker-compose di n8n+postgres+ollama", "esempio di filtro PII in function node o sidecar Python", "checklist DPO"],
        scene="A dim server rack and a laptop in a small Italian office at night, ethernet cables, no screens readable, tense documentary mood.",
    ),
    dict(
        titolo="RAG su PostgreSQL con pgvector: come interrogare 10.000 fatture elettroniche italiane senza Pinecone e senza cloud",
        kw="rag pgvector fattura elettronica",
        kw2="postgresql pgvector, rag documenti italiani, fatturaPA xml, vector database self-hosted",
        descrizione="Guida lunga al RAG su fatture XML FatturaPA e PDF: chunking per IVA/linee, embedding, hybrid search BM25+vector, citazioni del file sorgente, zero Pinecone.",
        angle="Verticale italiano puro: FatturaPA, partita IVA, XML, non “document Q&A generico”.",
        outline=[
            "Perché un chatbot sui PDF delle fatture allucina numeri",
            "Anatomia FatturaPA: cosa chunkare (testata, linee, riepiloghi IVA) e cosa non spezzare",
            "Schema Postgres: documenti, chunks, embedding, tsvector italiano",
            "Hybrid search: BM25 + cosine e come pesare i due punteggi",
            "Citazioni obbligatorie: ogni importo deve puntare a file+xpath o pagina",
            "Pipeline ingest: SDI/XML, PDF scansionati, duplicati, revisioni",
            "Valutazione: 50 domande d’oro (totale documento, aliquota, scadenza)",
            "Costi VRAM vs API embedding e quando un 8GB basta",
        ],
        must=["SQL di esempio con pgvector", "snippet Python ingest XML", "tabella errori (importo sbagliato / fornitore confuso)"],
        scene="Close-up of stacked paper invoices and a blurred workstation with a database server case, warm desk lamp, no readable text on paper.",
    ),
    dict(
        titolo="MCP su Salesforce: perché un chatbot sul CRM non basta e come far eseguire l’agente senza bruciare i governor limits",
        kw="mcp salesforce agente produzione",
        kw2="model context protocol salesforce, governor limits, agente crm, salesforce api jwt",
        descrizione="Deep dive su MCP come strato d’azione su Salesforce: tool design, idempotenza, limiti API, JWT, cosa non far fare mai a un LLM (delete massivo, update senza filtro).",
        angle="Non “AI per le vendite”. È un pezzo di integrazione: protocollo, quote, permessi.",
        outline=[
            "Il chatbot che “legge gli opportunity” e non conclude nulla",
            "Cosa è MCP in pratica (tool, resources, auth) senza hype",
            "Mappa dei tool sicuri vs tool armi (update, delete, convertlead)",
            "Governor limits, concurrent API, bulk vs REST: numeri e strategie",
            "Idempotenza: idempotency key, dry-run, preview per l’umano",
            "JWT e utente di integrazione: minimo privilegio, non admin",
            "Osservabilità: ogni tool call è un audit trail",
            "Quando restare su Flow/Apex e non mettere l’LLM in mezzo",
        ],
        must=["esempio JSON di tool MCP", "tabella governor limits rilevanti", "kill-switch e coda di approvazione"],
        scene="A trader-like dual-monitor desk in a dark room, CRM-looking blur on screens, no readable UI text, professional cool light.",
    ),
    dict(
        titolo="Ollama in produzione è una trappola: quando serve vLLM (e come scegliere la GPU usata senza bruciare il budget)",
        kw="vllm vs ollama produzione",
        kw2="ollama produzione, vllm gpu, llm self-hosted pmi, throughput token",
        descrizione="Confronto brutale Ollama vs vLLM: latenza, batch, VRAM, quantizzazione, quando Ollama va bene (dev, un utente) e quando in produzione collassa.",
        angle="Benchmark e architettura, non recensione da YouTube.",
        outline=[
            "Cosa promette Ollama e dove smette di essere un server",
            "vLLM: paged attention, batch, OpenAI-compatible API",
            "VRAM: 8 / 12 / 24 GB e quali modelli italiani/EU reggono",
            "Quantizzazione GGUF vs AWQ/GPTQ: qualità vs velocità",
            "Un utente vs 15 dipendenti in contemporanea: code e timeout",
            "GPU usata (3090, 4090, A5000) vs cloud GPU: TCO 12 mesi",
            "Compose di produzione: healthcheck, reverse proxy, limiti",
            "Piano di rollback se il modello sbaglia i JSON",
        ],
        must=["tabella TCO", "compose vLLM o Ollama con limiti", "criterio di uscita da Ollama"],
        scene="A used gaming GPU on an anti-static mat next to a compact rack server, workshop lighting, no brand logos readable.",
    ),
    dict(
        titolo="Mettere ChatGPT nel CRM è un data leak: cosa dice il GDPR (e l’AI Act) se i prompt contengono clienti italiani",
        kw="gdpr chatgpt crm",
        kw2="ai act pmi, trasferimento dati openai, dpa llm, titolare responsabile trattamento",
        descrizione="Articolo giuridico-tecnico per PMI: titolare vs responsabile, trasferimenti extra-UE, istruzioni al modello, registri, cosa scrivere nel DPIA se usi LLM su anagrafiche.",
        angle="Paura vera + procedura. Non consulenza legale formale, ma checklist da portare al commercialista/DPO.",
        outline=[
            "Lo scenario classico: commerciale che incolla l’opportunity su ChatGPT",
            "Titolare, responsabile, sub-responsabile: chi è OpenAI nella tua filiera",
            "Trasferimenti extra-UE e perché “abbiamo il toggle EU” non chiude il tema",
            "Cosa deve finire nel registro e nel DPIA",
            "Misure tecniche: mascheramento, opt-out training, tenant, log minimi",
            "AI Act 2026: uso ad alto rischio vs uso interno di produttività",
            "Contratto con i dipendenti: policy, sanzioni interne, Shadow IT",
            "Alternativa sovrana: modello locale o vendor UE con DPA serio",
        ],
        must=["traccia di policy interna di 1 pagina", "elenco dati che non devono mai entrare in un prompt cloud", "riferimenti a principi GDPR (art. 5, 28, 32, 44) senza copiare norme per intero"],
        scene="A lawyer’s dark wooden desk with a closed laptop and a padlock in the foreground, blurred Italian office, no readable documents.",
    ),
    dict(
        titolo="Come costruire un agente IMAP che classifica PEC e fatture (senza Gmail API e senza dare la password a un SaaS)",
        kw="agente imap pec fatture",
        kw2="imap idle python, pec aruba, classificazione email ai, inbox agent self-hosted",
        descrizione="Architettura di un inbox agent: IMAP IDLE, cartelle, classificazione, estrazione XML, niente Google. Gestione PEC, quota, duplicati, errori di login.",
        angle="Verticale posta italiana (PEC), non “AI email assistant”.",
        outline=[
            "Perché Gmail API e Copilot sulla posta sono un non-starter per molte PMI",
            "IMAP vs Graph vs Gmail: cosa tieni in casa",
            "IDLE vs polling: CPU, ban del provider, backoff",
            "Tassonomia cartelle: da leggere, fatture, pec legale, spam, da umano",
            "Modello locale vs cloud sul solo body già redacted",
            "Allegati: XML FatturaPA, PDF, zip, virus",
            "Idempotenza: Message-ID, non riclassificare all’infinito",
            "Runbook: password app, fail2ban, backup delle regole",
        ],
        must=["snippet Python IMAP IDLE", "schema cartelle", "lista errori provider PEC"],
        scene="A physical mailbox slot in a modern office wall next to a small silent server, cool daylight, no logos.",
    ),
    dict(
        titolo="Stack Docker sovrano per PMI: ERP, BI e agenti AI sulla stessa compose (senza Microsoft 365 che ti tiene in ostaggio)",
        kw="docker pmi stack sovrano",
        kw2="self-hosted erp, docker compose produzione, vendor lock-in saas, bi postgres",
        descrizione="Piano di un ecosistema containerizzato per PMI: confini tra ERP, file, BI, n8n, LLM. Cosa mettere nello stesso compose e cosa isolare. Backup, update, chi ha le chiavi.",
        angle="Sovranità come architettura, non come slogan.",
        outline=[
            "Il conto Microsoft/Google a tre anni vs un rack o un VPS UE",
            "Cosa significa sovrano: dati, identità, DNS, backup, offboarding",
            "Mappa servizi: reverse proxy, IdP, DB, code, worker AI",
            "Un compose vs tanti compose: blast radius",
            "Backup: postgres dump, volumi, secret, test di restore mensile",
            "Aggiornamenti senza “lunedì morto”",
            "Permessi: l’agente AI non vede l’ERP intero",
            "Percorso di migrazione a scaglioni (posta, file, CRM, BI)",
        ],
        must=["diagramma testuale dei confini", "esempio di reti Docker interne", "checklist restore"],
        scene="A tidy homelab rack in a small business back office, blinking lights out of focus, documentary photography.",
    ),
    dict(
        titolo="LangGraph o n8n o uno script Python: quale orchestratore per un agente che deve davvero eseguire (non chiacchierare)",
        kw="langgraph vs n8n vs python",
        kw2="orchestrazione agenti, tool calling produzione, n8n limiti, langgraph stato",
        descrizione="Criteri di scelta per l’orchestrazione: stato, retry, UI per non-dev, test, versionamento. Tre architetture sullo stesso caso (prenotazione + scrittura CRM).",
        angle="Decision framework, non war of tools.",
        outline=[
            "Definizione: eseguire = side effect nel mondo reale",
            "n8n: veloce, visibile, debole su stato lungo e test",
            "LangGraph: stato, cicli, checkpoint, curva di debug",
            "Python crudo: massimo controllo, minimo teatro",
            "Stesso use case nei tre stack: pro e contro",
            "Osservabilità e replay",
            "Chi mantiene il sistema tra 12 mesi",
            "Regola pratica di scelta in una tabella",
        ],
        must=["tabella decisionale", "pseudo-grafo degli stati", "anti-pattern “metto tutto in un unico nodo LLM”"],
        scene="Three empty notebooks and a mechanical keyboard on a dark desk, top-down, no writing visible.",
    ),
    dict(
        titolo="Prompt injection in produzione: come un fornitore ti fa pagare due volte infilando istruzioni in una fattura PDF",
        kw="prompt injection documenti aziendali",
        kw2="prompt injection rag, pdf malevoli, tool calling sicurezza, indiretta injection",
        descrizione="Attacco reale su RAG/agenti che leggono PDF: istruzioni nascoste, jailbreak via XML, tool call indotta (invio SEPA, cambio IBAN). Difese: sandbox, allowlist, human confirm.",
        angle="Security engineering, esempi di payload, difese a strati.",
        outline=[
            "Injection diretta vs indiretta (il documento è l’attaccante)",
            "Casi: cambio IBAN, “ignora le policy”, esfiltrazione via HTTP tool",
            "Perché il system prompt non basta",
            "Separare “contesto da citare” e “istruzioni eseguibili”",
            "Allowlist tool, conferma umana sopra soglia (importo, IBAN)",
            "Scanner pre-RAG: testo invisibile, JS in PDF, xml:space",
            "Test suite rossa: 20 PDF cattivi",
            "Incident response se l’agente ha già scritto",
        ],
        must=["esempio di payload (innocuo, didattico)", "policy di conferma per pagamenti", "lista controlli sul PDF"],
        scene="A red USB stick on invoices beside a locked metal box, dramatic low light, no readable print.",
    ),
    dict(
        titolo="EU AI Act per chi monta agenti in PMI nel 2026: sei ad alto rischio o stai solo automatizzando l’inbox?",
        kw="eu ai act pmi agenti 2026",
        kw2="ai act classificazione rischio, obblighi gpt interni, trasparenza llm, registro usi ai",
        descrizione="Guida operativa all’AI Act per chi deploya agenti su inbox, CRM, HR screening, credito. Come classificare, cosa documentare, cosa non è “alto rischio”.",
        angle="Classificazione pratica + dossier minimo, non panico da LinkedIn.",
        outline=[
            "Cosa è in vigore nel 2026 per un deployer italiano",
            "Alto rischio vs uso interno di produttività: test sul tuo agente",
            "Obblighi di trasparenza se l’utente parla con un bot",
            "Documentazione tecnica minima che un auditor può capire",
            "Qualità dati di training vs RAG (non hai un foundation model tuo)",
            "Sorveglianza umana: non è un checkbox",
            "Sanzioni: ordini di grandezza e cosa succede prima (diffida)",
            "Template di registro degli usi AI in azienda",
        ],
        must=["albero decisionale alto rischio sì/no", "indice di un dossier da 10 pagine", "cosa NON fare (HR scraping selvaggio)"],
        scene="European parliament-like architecture out of focus behind a single person reviewing papers, blue hour, no flags sharp.",
    ),
    dict(
        titolo="Chunking di contratti italiani: perché spezzare ogni 500 token ti fa perdere clausole vessatorie e fori competenti",
        kw="chunking contratti italiani rag",
        kw2="clausole vessatorie nlp, rag legale, overlap chunk, recursive split pdf",
        descrizione="Tecnica di split per contratti (preliminari, NDA, SLA): articoli, commi, richiami incrociati, allegati. Come non tagliare “salvo quanto previsto all’art. 7”.",
        angle="NLP su testi giuridici italiani, molto verticale.",
        outline=[
            "Il contratto non è un blog post: struttura e rinvii",
            "Errori del splitter naive (500 token, markdown header inesistenti)",
            "Splitter per articoli/commi e overlap intelligente",
            "Metadata: parte, data, versione, firma, allegato",
            "Query tipiche: recesso, foro, penale, NDA durata",
            "Valutazione con avvocato in loop (gold set)",
            "Cosa non chiedere mai al RAG (parere legale sostitutivo)",
            "Pipeline da PDF scansito (OCR) vs digitale",
        ],
        must=["esempio di chunk buono vs cattivo", "schema metadata", "disclaimer ruolo dell’AI"],
        scene="Leather-bound contract folder on a steel table, shallow focus, no readable clauses.",
    ),
    dict(
        titolo="Kill switch per agenti che scrivono su Salesforce: dry-run, coda di approvazione e perché “conferma in chat” non è un controllo",
        kw="kill switch agente salesforce",
        kw2="human in the loop crm, dry-run llm, approvazione tool call, agente produzione sicurezza",
        descrizione="Design di un controllo reale: preview del payload, hash, scadenza, ruolo approvatore, freeze. Perché il “sì” in chat è bypassabile con injection.",
        angle="Control theory per side effect, non UX del bot.",
        outline=[
            "Side effect: la chat non è un log di audit",
            "Dry-run: l’agente propone, il sistema serializza il PATCH",
            "Coda: UI minima, Slack/email con link firmati, non “reply YES”",
            "Soglie: importo, numero record, campi protetti",
            "Freeze globale: feature flag, certificato, orario",
            "Replay e rollback Salesforce (non sempre possibile)",
            "Chi approva: separazione dei ruoli",
            "Test del kill switch (chaos: ignora il freeze)",
        ],
        must=["schema della coda (tabella)", "esempio payload firmato", "runbook freeze"],
        scene="A large physical emergency stop button in the foreground, blurred server room behind, red accent light.",
    ),
    dict(
        titolo="Cloudflare Tunnel su Raspberry Pi: esporre n8n e la dashboard senza aprire una porta (e senza farsi bannare l’IP di casa)",
        kw="cloudflare tunnel raspberry pi n8n",
        kw2="cloudflared docker, reverse proxy pmi, ip residenziale 403, zero trust tunnel",
        descrizione="Guida ops: cloudflared in Docker sul Pi, nomi interni, Access, cosa non esporre, rate limit, rinnovo. Lezione da IP residenziali che prendono 403.",
        angle="Ops da laboratorio/casa/ufficio piccolo, molto concreto.",
        outline=[
            "Perché il port forwarding sul modem è una pessima idea",
            "Tunnel vs VPN vs VPS: minaccia e latenza",
            "Installazione cloudflared in compose sul Pi",
            "Hostname pubblici vs hostname solo Access",
            "Cosa non tunnelare (Postgres, Redis, n8n editor in chiaro)",
            "IP residenziale, scrape e ban: non martellare API da casa",
            "Manutenzione: SD card, alimentazione, freeze",
            "Fallback se Cloudflare è down",
        ],
        must=["frammento compose cloudflared", "policy Access di esempio", "checklist hardening"],
        scene="A Raspberry Pi on a wood desk with a single ethernet cable, cozy night lamp, no screen text.",
    ),
    dict(
        titolo="Whisper API vs Parakeet/NeMo offline su Windows: quando la trascrizione in cloud ti costa più della GPU (e ti porta via le riunioni)",
        kw="trascrizione audio offline windows",
        kw2="whisper api costo, nvidia parakeet, meeting transcription gdpr, asr self-hosted",
        descrizione="Confronto costi, qualità IT, diarizzazione, SRT, hardware Windows. Perché le riunioni del CdA non devono finire in un vendor USA.",
        angle="ASR da prodotto, privacy e TCO.",
        outline=[
            "Cosa c’è in una registrazione: PII, strategia, numeri",
            "Whisper API: prezzo per ora, retry, retention",
            "Offline: Parakeet/NeMo, Whisper.cpp, VRAM",
            "Diarizzazione e parlato sovrapposto in italiano",
            "Pipeline: file → testo → riassunto locale → archivio",
            "Windows come runtime (non solo Linux server)",
            "Benchmark su 30 minuti di meeting reale (metrica WER dichiarata come metodo, non magia)",
            "Policy: consenso registrazione e cancellazione",
        ],
        must=["tabella costo per 20 ore/mese", "architettura cartelle e retention", "avvertenza sul riassunto LLM"],
        scene="A conference table with a single analog recorder and empty chairs, muted colors, no faces in focus.",
    ),
    dict(
        titolo="Fattura elettronica XML + vision OCR: come arrivare al 95% di campi giusti (e come misurarlo, non come raccontarlo)",
        kw="ocr fattura elettronica accuratezza",
        kw2="xml fatturapa vs pdf, ai vision documenti, evaluation estrazione dati, dataunchain",
        descrizione="Metodo di valutazione dell’estrazione: gold set, campi critici (IVA, totale, partita IVA), XML first vs vision sul PDF, errori costosi.",
        angle="Accuracy engineering. Niente “la nostra AI è al 99%”.",
        outline=[
            "XML è la fonte; il PDF è un fallback sporco",
            "Campi che fanno danni se sbagliati",
            "Gold set: 200 documenti, chi etichetta, accordo tra annotatori",
            "Metriche: exact match, tolleranza centesimi, partita IVA checksum",
            "Quando usare vision (scansioni, estero, non PA)",
            "Human review sopra soglia di incertezza",
            "Drift: nuovi tracciati, nuovo fornitore, nuovo layout",
            "Report settimanale che un amministrativo capisce",
        ],
        must=["definizione di accuratezza per campo", "flusso XML-first", "esempio di errore da un centesimo"],
        scene="A document scanner bed with a blank sheet, cool metal tones, no printed text visible.",
    ),
    dict(
        titolo="pgvector vs Qdrant vs Pinecone: il lock-in del vector DB ti costa più degli embedding (con numeri)",
        kw="pgvector vs qdrant vs pinecone",
        kw2="vector database lock-in, self-hosted qdrant, postgresql embedding, costo pinecone",
        descrizione="Confronto ops e prezzo: backup, filtri metadata, hybrid search, uscita dal vendor. Quando Postgres basta e quando Qdrant ha senso. Pinecone come anti-pattern per PMI sovrane.",
        angle="Procurement + ops, non benchmark da tweet.",
        outline=[
            "Cosa stai comprando: ANN, filtri, SLA, dati",
            "Postgres+pgvector: un sistema in meno, backup che già fai",
            "Qdrant self-host: quando il carico di query esplode",
            "Pinecone: velocità di start, prezzo a unità, uscita dolorosa",
            "Hybrid search e lingua italiana",
            "TCO 12 mesi su 1M chunk",
            "Migrazione: come non restare ostaggio degli ID",
            "Regola di default per PMI",
        ],
        must=["tabella TCO", "criteri di uscita", "esempio filtro metadata"],
        scene="Stacked hard drives and a small plant on a dark shelf, still life, no labels readable.",
    ),
    dict(
        titolo="Osservabilità degli LLM in produzione: tracce, costo per run, retry e perché “guarda la chat” non è un monitoraggio",
        kw="osservabilità llm produzione",
        kw2="tracing langfuse, costo token per agente, retry backoff openai, logging pii",
        descrizione="Come tracciare chiamate modello/tool senza loggare PII, attributire costi a un processo, allertare su loop e picchi. Stack: OpenTelemetry, Langfuse o Postgres casalingo.",
        angle="SRE per agenti.",
        outline=[
            "Cosa misurare: latenza, token, tool error, human override",
            "Traccia vs log: parent run, span tool, modello",
            "PII nei prompt: redaction prima dello storage",
            "Budget per agente e kill su sforamento",
            "Retry: idempotenza vs doppio pagamento",
            "Dashboard minime che un non-dev legge",
            "Allarmi: loop, 429, schema JSON rotto",
            "Retention e diritto all’oblio sui log",
        ],
        must=["schema tabella runs", "esempio di metriche", "policy retention"],
        scene="A dark operations room with out-of-focus graphs on a wall display, no numbers readable, blue ambient light.",
    ),
    dict(
        titolo="JSON Schema e tool calling: come impedire all’LLM di inventare un IBAN “perché sembrava plausibile”",
        kw="json schema tool calling iban",
        kw2="structured output llm, validazione iban, function calling affidabile, pydantic agente",
        descrizione="Contratto dati tra modello e tool: schema, validatori (IBAN, partita IVA, CF), reject+retry, niente stringhe libere su campi critici.",
        angle="Data contracts. Esempio IBAN/CF italiano.",
        outline=[
            "Allucinazione strutturata: peggio del testo libero",
            "JSON Schema / Pydantic come recinto",
            "Validatori di dominio: IBAN, CF, P.IVA, BIC",
            "Cosa fare se lo schema fallisce (retry, human, abort)",
            "Strict mode vs “modello che comunque chiacchiera”",
            "Test: 100 IBAN finti, 100 veri (dataset sintetico)",
            "Log del reject senza salvare l’IBAN in chiaro",
            "Quando non usare l’LLM (copia dal XML già parsato)",
        ],
        must=["schema JSON di esempio", "funzione di checksum IBAN (riferimento al metodo, codice semplificato)", "policy abort"],
        scene="A metal ruler and a rubber stamp on a ledger, macro photography, no digits readable.",
    ),
    dict(
        titolo="L’agente che gira in loop sulle tool call: come riconoscerlo dai log e come spezzarlo (senza spegnere tutto)",
        kw="tool calling loop infinito",
        kw2="agente llm retry loop, max iterations langgraph, circuit breaker ai, runaway agent",
        descrizione="Pattern di runaway agent: stessa tool, errore, retry, conto API. Circuit breaker, max step, backoff, “budget di azioni”.",
        angle="Incident da produzione.",
        outline=[
            "Sintomi: fattura OpenAI a tre zeri, CPU n8n a 100%, coda piena",
            "Cause: schema rotto, tool 500, prompt “insisti”",
            "Max iterations e perché 25 è già tanto",
            "Circuit breaker per tool (error budget)",
            "Dedup: non richiamare lo stesso GET 40 volte",
            "Watchdog esterno al grafo",
            "Postmortem: template",
            "Chaos test: tool che fallisce sempre",
        ],
        must=["contatore di step in pseudo-codice", "allarme su N tool/min", "checklist incident"],
        scene="A tangled ethernet cable knot in harsh light, abstract, no text.",
    ),
    dict(
        titolo="Smetti di seppellire i task dell’agente in ChatGPT: come far scrivere GitHub Issues (o GitLab) senza gh CLI e senza copincolla",
        kw="agente ai github issues",
        kw2="github api issues automazione, backlog agenti, vibeissue, tracker vs chat",
        descrizione="Perché il backlog in chat è debito. Design: l’agente apre issue con template, label, body riproducibile, idempotenza sul titolo.",
        angle="Processo engineering, API tracker.",
        outline=[
            "La chat non ha stato, assignee, SLA",
            "Issue come contratto: riproduzione, accettazione, log",
            "Auth: fine-grained token, least privilege, no PAT da admin",
            "Template body generato dal contesto (repo, file, errore)",
            "Idempotenza: non aprire 12 issue uguali",
            "Windows/macOS/Linux: niente dipendere da gh installato",
            "Review umana: label `needs-triage`",
            "Metrica: issue aperte vs chiuse vs duplicate",
        ],
        must=["esempio body markdown issue", "permessi token minimi", "regola anti-duplicato"],
        scene="A kanban board with blank sticky notes on glass, office bokeh, no writing.",
    ),
    dict(
        titolo="Export notturno Salesforce → CSV con JWT in Docker: field mapping, paginazione e perché l’utente “Administrator” è una bomba",
        kw="salesforce jwt export csv docker",
        kw2="salesforce connected app jwt, bulk api paginazione, field mapping crm, cron docker",
        descrizione="Ricetta di un exporter di produzione: Connected App, JWT, mapping campi, tipi, encoding, cron, secret, utente di integrazione non admin.",
        angle="Integrazione batch, non AI. Verticale CRM.",
        outline=[
            "Perché Data Loader a mano non è un processo",
            "JWT bearer: rotazione, orologio, audience",
            "Utente di integrazione e permessi per oggetto",
            "Paginazione e limite API: non farti throttle alle 3 di notte",
            "Mapping e formati data/valuta/booleani italiani",
            "CSV: encoding, separatore, escaping, PII",
            "Docker + cron: lock file, alert su fail",
            "Audit: chi ha scaricato cosa",
        ],
        must=["scheletro compose+cron", "esempio mapping JSON", "errori JWT comuni"],
        scene="A wall clock at 03:00 next to a closed laptop, night office, no screen glow with text.",
    ),
    dict(
        titolo="Reverse engineering su Oracle: come trovare la colonna IBAN senza schema (REPL, catalogo, e il rischio di fare damage in produzione)",
        kw="reverse engineering oracle iban",
        kw2="oracle data dictionary, sqlplus catalogo, ricerca colonne, replica read-only",
        descrizione="Metodo per esplorare DB Oracle legacy in sola lettura: dizionario dati, ricerca per nome/pattern, all_tab_columns, mai UPDATE. Replica e vincoli DBA.",
        angle="Legacy integration, cauto e professionale.",
        outline=[
            "Perché i legacy non hanno ERD aggiornato",
            "Read replica o utente SELECT-only: non toccare prod",
            "Catalogo: all_tab_columns, commenti, constraint",
            "Ricerca semantica: IBAN, SWIFT, “account”",
            "REPL e script batch, niente click a caso su GUI",
            "PII: come non esportare 8 milioni di clienti “per provare”",
            "Documentare lo schema trovato (markdown, non testa)",
            "Quando chiamare il DBA e fermarsi",
        ],
        must=["query di catalogo di esempio", "regole di engagement", "template documentazione schema"],
        scene="An old beige server in a dusty closet, documentary, no rack labels readable.",
    ),
    dict(
        titolo="Traefik vs Caddy vs Cloudflare Tunnel: quale reverse proxy per un’agentic app self-hosted (certificati, auth, e blast radius)",
        kw="traefik vs caddy vs cloudflare tunnel",
        kw2="reverse proxy docker, let’s encrypt self-hosted, zero trust, n8n https",
        descrizione="Scelta del fronte HTTPS per n8n, UI interne, API agenti. Confronti su ACME, middleware, SSO, cosa esporre. Tunnel quando non hai IP pubblico pulito.",
        angle="Networking da PMI, decisione.",
        outline=[
            "Cosa deve fare il fronte: TLS, auth, log, limiti",
            "Caddy: semplice, ACME, meno pezzi",
            "Traefik: labels Docker, dashboard, più fune",
            "Cloudflare Tunnel: niente porta 443 in ingresso",
            "Auth: Basic è insufficiente, Access/SSO, IP allowlist",
            "Blast radius se il proxy cade o è misconfigurato",
            "Log e GDPR (IP)",
            "Matrice di scelta",
        ],
        must=["matrice", "esempio Caddyfile o labels Traefik (uno dei due completo)", "errori certificato comuni"],
        scene="A concrete underpass with a single bright exit light, architectural, no signs with text.",
    ),
    dict(
        titolo="n8n in queue mode con Postgres: perché la tua automazione “ogni tanto non parte” (e come dimensionare i worker)",
        kw="n8n queue mode postgres",
        kw2="n8n worker docker, redis bull queue, webhook perso, scalare n8n",
        descrizione="Diagnosi della modalità queue: Redis/Bull, worker, webhook, esecuzioni orphan, DB che si riempie, UI lenta. Dimensionamento concreto.",
        angle="Ops n8n avanzato.",
        outline=[
            "Main vs worker: chi fa cosa",
            "Sintomi: webhook 200 ma niente run, coda che cresce",
            "Postgres: executions, pruning, vacuum",
            "Redis: persistenza, cosa succede se lo perdi",
            "Quanti worker: CPU, I/O LLM, concorrenza",
            "Idempotenza dei webhook",
            "Upgrade versioni senza perdere la coda",
            "Alerting sulle code",
        ],
        must=["variabili env rilevanti", "query/ pruning executions", "checklist “non parte”"],
        scene="A factory conveyor belt empty and still, industrial photography, no labels.",
    ),
    dict(
        titolo="Fine-tuning vs RAG per le FAQ aziendali in italiano: quando addestrare è spreco (e quando il retrieval non basta)",
        kw="fine tuning vs rag faq italiane",
        kw2="lora faq aziendali, retrieval vs weights, allucinazione policy interne, embeddings italiano",
        descrizione="Criteri: frequenza di aggiornamento policy, tono di voce, fatti vs stile. Costi LoRA vs pipeline RAG. Ibrido raro e onesto.",
        angle="Scelta di metodo, esempi di policy HR/IT italiane.",
        outline=[
            "FAQ che cambiano ogni mese: il fine-tune è già marcio",
            "Cosa il RAG non può fare (tono, formato, “siamo una banca”) ",
            "LoRA: dati, licenze, eval, GPU",
            "Ibrido: retrieval + piccolo adattamento di stile",
            "Dataset: ticket veri vs PDF ufficiali",
            "Rischio: il modello che “ricorda” uno stipendio",
            "Metrica: exact policy citation",
            "Default raccomandato per PMI",
        ],
        must=["albero decisionale", "esempio di domanda che il RAG deve citare", "costo ordine di grandezza"],
        scene="Two doors in a corridor, one lit one dark, architectural photography, no signs.",
    ),
    dict(
        titolo="Model Context Protocol spiegato senza hype: tool, resources, auth e perché non è “USB-C dell’AI” se il server è scritto male",
        kw="model context protocol spiegato",
        kw2="mcp server sicurezza, mcp vs openai functions, stdio sse mcp, tool poisoning",
        descrizione="Spec tecnica utile: transport, capability, permessi, poisoning dei tool, sandbox. Come scrivere un server MCP piccolo e onesto.",
        angle="Protocollo, rischi, implementazione minima.",
        outline=[
            "Cosa risolve MCP e cosa no",
            "Anatomy: tools, resources, prompts",
            "Transport: stdio vs HTTP/SSE",
            "Auth e chi può invocare cosa",
            "Tool poisoning e nomi ingannevoli",
            "Un server minimo (filesystem read-only) come esempio",
            "Come testarlo senza un client magico",
            "Quando restare su function calling classico",
        ],
        must=["elenco capability", "minaccia tool poisoning", "scheletro server (pseudo o python corto)"],
        scene="Exposed USB-C cables and a closed metal toolbox, still life, no logos.",
    ),
    dict(
        titolo="Assistente vocale in PMI: latenza, barge-in e GDPR (perché Vapi/Retell non sono “un centralino più furbo” se il audio va in USA)",
        kw="assistente vocale pmi gdpr latenza",
        kw2="barge-in voice ai, vapi self-hosted, stt tts privacy, centralino ai italiano",
        descrizione="Stack voce: STT, LLM, TTS, telefonía. Budget di latenza, interruzione dell’utente, dove gira l’audio, consenso, registrazione chiamate.",
        angle="Voice agents da produzione, privacy e UX acustica.",
        outline=[
            "Il silenzio di 2 secondi che fa riagganciare",
            "Catena STT→LLM→TTS: dove perdi i ms",
            "Barge-in: cosa spegnere quando l’umano parla",
            "Audio in transito: vendor, regioni, retention",
            "Script vs agente: prenotazione calendario è uno state machine",
            "Fallback umano e orari",
            "Obblighi di informativa sulla chiamata",
            "MVP onesto: FAQ + booking, niente diagnosi mediche",
        ],
        must=["budget di latenza in tabella", "flusso di stato prenotazione", "checklist informativa"],
        scene="An old analog telephone on a modern desk, side light, no brand marks.",
    ),
    dict(
        titolo="App desktop AI offline su Windows (Electron): come distribuire un modello locale senza che l’antivirus e il path da 260 caratteri ti distruggano il lancio",
        kw="electron ai offline windows",
        kw2="whisper.cpp windows, installer electron, path MAX_PATH, runtime llm desktop",
        descrizione="Lezioni da software desktop: pack del runtime, GPU opzionale, update, sandbox, size dell’installer, Windows Defender, permessi microfono.",
        angle="Shipping, non demo Colab.",
        outline=[
            "Perché “apri questo notebook” non è un prodotto",
            "Cosa mettere in Electron vs processo nativo",
            "Modelli: download al first run vs bundle",
            "MAX_PATH, spazi, utenti non admin",
            "GPU NVIDIA vs CPU fallback",
            "Firma, SmartScreen, aggiornamenti",
            "Privacy: niente telemetry di default",
            "Crash reporting senza mandare il file dell’utente",
        ],
        must=["architettura processi", "trappole Windows", "policy update"],
        scene="A Windows laptop closed on a kitchen table of a small office, morning light, no stickers readable.",
    ),
    dict(
        titolo="YAML come costituzione dell’agente: come definisci tono, divieti e canali (e perché un prompt da 12 pagine in chat non è governabile)",
        kw="yaml costituzione agente ai",
        kw2="agent constitution file, policy as code llm, prompt versioning, config agente",
        descrizione="Policy-as-code per agenti: file YAML versionato, validazione, hot reload pericoloso, audit. Tono, blacklist, tool ammessi, orari di pubblicazione.",
        angle="Governance, non “virtual influencer” da marketing.",
        outline=[
            "Il prompt in chat non ha diff né review",
            "Cosa va in YAML: identità, divieti, tool, budget",
            "Validazione schema e CI",
            "Segreto vs policy (token fuori dal YAML)",
            "Hot reload: blast radius",
            "Esempio di regola: “non dare consigli finanziari”",
            "Test: l’agente viola la costituzione?",
            "Chi approva una PR sulla costituzione",
        ],
        must=["esempio YAML (senza segreti)", "pipeline CI", "test di violazione"],
        scene="A printed constitution-like booklet out of focus next to a keyboard, warm library light, no readable letters.",
    ),
    dict(
        titolo="Il backtest del tuo bot di trading mente: walk-forward, overfitting e perché un Sharpe 2.4 in sample è quasi sempre spazzatura",
        kw="walk forward overfitting trading bot",
        kw2="validazione walk-forward, backtest bias, quantitative python, kill switch trading",
        descrizione="Metodo di validazione per bot (crypto o altro): walk-forward, costi, slippage, look-ahead, protocollo di rischio, kill switch. Niente segnali da vendere.",
        angle="Quant research onesto. Disclaimer: non è consulenza finanziaria.",
        outline=[
            "Disclaimer e cosa questo articolo non è",
            "Look-ahead e survivorship: come ti freghi da solo",
            "Walk-forward: finestre, embargo, rolling",
            "Costi: fee, funding, slippage realistico",
            "Overfitting: troppi parametri, troppi indicatori",
            "Risk protocol: cap, kill switch, no martingala",
            "Cosa loggare in paper trading",
            "Quando non automatizzare affatto",
        ],
        must=["schema walk-forward", "elenco bias", "kill switch concettuale"],
        scene="A blank candlestick chart on a distant monitor heavily blurred, dark room, no numbers or symbols readable.",
    ),
    dict(
        titolo="Margin debt FRED vs FINRA: perché il tuo dashboard “rischio contenuto” è un bug di aggregazione (non un mercato safe)",
        kw="margin debt fred vs finra",
        kw2="indicatore buffett household equity, proxy z1, dashboard rischio mercati, dati stale cape",
        descrizione="Lezione da data engineering su fonti macro: proxy diversi, YoY, stale, pesi. Come un aggregato può dare verde con Buffett estremo. Metodo: assi separati, as_of, disclaimer.",
        angle="Data quality per indicatori di mercato, non previsioni.",
        outline=[
            "Due numeri che non misurano la stessa cosa",
            "FINRA vs Z.1: metodologia e ritardi",
            "Stale: CAPE fermo, YoY che esplode o si azzera",
            "Pesi: un proxy debole che spegne un segnale forte",
            "Design: fragilità vs innesco, non un unico semaforo",
            "as_of e provenienza in UI",
            "Cosa non scrapare (403, ToS, IP residenziale)",
            "Come comunicare incertezza senza giallo da televideo",
        ],
        must=["tabella fonti vs ritardo", "esempio di aggregato fuorviante (metodologico)", "regole di visualizzazione as_of"],
        scene="A cracked green traffic light in fog, cinematic, no street signs readable.",
    ),
    dict(
        titolo="Hybrid search BM25 + embedding sull’italiano: come non far vincere sempre il cosine (e perdere “articolo 18”)",
        kw="hybrid search bm25 embedding italiano",
        kw2="postgresql full text italiano, rrf fusion, ricerca ibrida rag, tsvector italian",
        descrizione="Fusion BM25/vector per query giuridiche e tecniche italiane, tokenizzazione, stemmer, RRF, pesi, eval su query corte con numeri e articoli di legge.",
        angle="IR, lingua italiana.",
        outline=[
            "Query corte e numeriche: l’embedding da solo fallisce",
            "tsvector italian e limiti dello stemmer",
            "RRF vs somma pesata",
            "Filtri (anno, società, tipo doc) prima del ANN",
            "Eval: nDCG su 30 query reali",
            "Tuning dei pesi senza overfit",
            "Accenti, maiuscole, “n.” e “art.”",
            "Implementazione Postgres",
        ],
        must=["SQL ibrido di esempio", "lista query d’oro", "errori tipici italiani"],
        scene="Open dictionary pages blurred into bokeh, warm light, no readable words.",
    ),
    dict(
        titolo="Segreti degli agenti: perché il .env nel compose non è un vault (e come non far finire il token Salesforce nel log dell’LLM)",
        kw="secrets agenti llm vault",
        kw2="docker secrets vs env, infisical self-hosted, token salesforce log, redaction prompt",
        descrizione="Gestione secret per stack agentic: env, Docker secrets, vault, rotazione, redaction nei prompt e nei trace. Incident: token in chat history.",
        angle="Security ops.",
        outline=[
            "Superficie: .env, n8n credentials, LLM memory, crash dump",
            "Cosa può finire nel contesto del modello",
            "Docker secrets / systemd / vault a confronto",
            "Rotazione JWT e webhook",
            "Redaction in tracing",
            "Sviluppo vs prod: niente secret di prod sul laptop",
            "Incident: revoke, audit, postmortem",
            "Checklist prima del go-live",
        ],
        must=["matrice dove vivono i secret", "esempio redaction", "runbook leak"],
        scene="A bunch of unlabeled keys on a steel ring, macro, dark background.",
    ),
    dict(
        titolo="Human-in-the-loop che funziona: una coda di approvazione (non “scrivi OK in chat”) prima che l’agente spedisca PEC o SEPA",
        kw="human in the loop pec sepa",
        kw2="approvazione agente ai, coda review, dual control pagamenti, pec automatica rischi",
        descrizione="Design di dual control per azioni irreversibili: PEC, bonifici, publish social. UI, scadenze, deleghe, evidenza forense.",
        angle="Operazioni irreversibili in Italia.",
        outline=[
            "Irreversibile: PEC, SEPA, tweet, delete",
            "Perché il messaggio in chat non è dual control",
            "Coda: record immutabile, hash del payload",
            "Ruoli: proponente vs approvatore",
            "Timeout e cosa succede se nessuno clicca",
            "Mobile: approvazione da telefono con rischio phishing",
            "Forensics: cosa tieni 10 anni",
            "MVP: solo PEC e pagamenti sopra soglia",
        ],
        must=["stati della coda", "campi dell’audit log", "anti-phishing dell’approvazione"],
        scene="Two physical rubber stamps, one red one black, on a desk, still life.",
    ),
    dict(
        titolo="Quanto costa davvero GPT-4o vs un Qwen self-hosted su 100.000 documenti/mese (TCO con elettricità, persone e scrap)",
        kw="tco gpt-4o vs llm self hosted",
        kw2="costo token aziendale, qwen vllm, elettricità gpu, break even llm",
        descrizione="Modello di costo: input/output token, cache, failed calls, GPU, kWh Italia, ore umane di manutenzione. Break-even. Quando il cloud vince comunque.",
        angle="CFO + CTO, numeri stimati dichiarati.",
        outline=[
            "Unità: documento, pagina, token, run agente",
            "Cloud: listino, sconto, output cost, cached input",
            "Self-host: GPU, ammortamento, energia, raffreddamento",
            "Persone: chi rianima il box alle 2 di notte",
            "Scarti: retry, eval, gold set",
            "Scenario 100k doc/mese: foglio di calcolo narrato",
            "Quando restare sul cloud (picchi, qualità, time-to-first)",
            "Come rivedere il TCO ogni trimestre",
        ],
        must=["tabella TCO", "ipotesi esplicite", "sensibilità prezzo token"],
        scene="A household electricity meter out of focus next to a small PC, basement light, no digits sharp.",
    ),
    dict(
        titolo="Agente browser con Playwright: come non fargli cliccare “Elimina account” (allowlist di URL, snapshot e budget di azioni)",
        kw="playwright agente browser allowlist",
        kw2="browser automation llm, computer use rischi, playwright sandbox, agente web produzione",
        descrizione="Computer-use onesto: DOM snapshot vs screenshot, allowlist, deny “danger words”, timeout, evidenza video. Casi: scraping interno, non banking.",
        angle="Browser agents, sicurezza.",
        outline=[
            "Perché il DOM è meglio dello screenshot (quando c’è)",
            "Allowlist di host e path",
            "Blacklist azioni (delete, transfer, download exe)",
            "Budget di click e tempo",
            "Login: non mettere password nel prompt",
            "Evidenza: trace Playwright",
            "Cosa non automatizzare (home banking, SPID)",
            "Test su staging con trappole",
        ],
        must=["lista deny", "config allowlist", "nota legale scraping"],
        scene="A computer mouse on a red doormat, conceptual, no UI.",
    ),
    dict(
        titolo="Come valuti un agente (non un chatbot): task success, side-effect score e perché BLEU è inutile",
        kw="valutazione agenti llm produzione",
        kw2="agent eval task success, side effect score, golden traces, langsmith eval",
        descrizione="Framework di eval per agenti: successo del task, danni collaterali, costo, tempo, intervento umano. Golden traces. Online vs offline.",
        angle="Eval engineering.",
        outline=[
            "Chatbot vs agente: metriche diverse",
            "Task success binario è troppo rozzo: score a step",
            "Side-effect: ha scritto il campo sbagliato?",
            "Golden traces e replay",
            "Eval offline (CI) vs canary in prod",
            "Chi etichetta e quanto costa",
            "Dashboard settimanale",
            "Quando fermare il deploy",
        ],
        must=["scheda di uno scenario di eval", "metriche minime", "gate di release"],
        scene="A clipboard with a blank checklist and a red pen, desk overhead, no writing.",
    ),
    dict(
        titolo="Cache semantica sulle chiamate LLM: quando risparmi il 40% e quando servi la risposta sbagliata a un altro cliente",
        kw="cache semantica llm",
        kw2="semantic cache redis, embedding cache rischio, prompt cache openai, multi tenant cache",
        descrizione="Cache di prompt/risposta: similarità, tenant isolation, TTL, invalidazione. Il disastro del nearest-neighbor cross-cliente. Quando usare cache vendor.",
        angle="Performance vs isolamento.",
        outline=[
            "Due cache: exact hash vs nearest neighbor",
            "Il bug: similarità alta, cliente diverso",
            "Chiave: tenant_id obbligatorio",
            "TTL e invalidazione su cambio policy",
            "Redis vs Postgres",
            "Cache del vendor (prompt cache) e privacy",
            "Misura hit rate vs error rate",
            "Default sicuro: exact match + tenant",
        ],
        must=["schema chiave cache", "caso di leakage", "metriche"],
        scene="Two identical coffee mugs on opposite sides of a glass wall, conceptual, no logos.",
    ),
    dict(
        titolo="Multi-agente che si contraddice: orchestratore, blackboard e perché “più agenti” non è più intelligenza",
        kw="multi agente contraddizione orchestratore",
        kw2="multi agent orchestration, blackboard pattern, agent handoff, conflitto tool",
        descrizione="Fallimenti del multi-agent: handoff persi, double spend, policy diverse. Pattern blackboard, un solo writer su CRM, giudice umano.",
        angle="Architettura, scetticismo sul hype swarm.",
        outline=[
            "Il demo con 7 agenti e zero responsabilità",
            "Conflitti: due writer sullo stesso record",
            "Blackboard / stato condiviso versionato",
            "Un orchestratore stupido è meglio di 5 geni",
            "Handoff con contratto (schema)",
            "Timeout e ownership",
            "Quando un solo grafo batte lo swarm",
            "Test di contraddizione",
        ],
        must=["diagramma di ownership", "esempio di conflitto", "regola un writer"],
        scene="A chessboard with two kings facing each other, dramatic light, no letters on pieces if any.",
    ),
    dict(
        titolo="IMAP IDLE vs polling ogni 30 secondi: come non farti chiudere la PEC dal provider mentre l’agente “ascolta” la posta",
        kw="imap idle vs polling pec",
        kw2="imap connection limit, pec timeout, backoff email agent, aruba imap",
        descrizione="Dettaglio protocollo: IDLE, NOTIFY, limiti connessioni, reconnect, backoff, più caselle. Casi PEC italiane.",
        angle="Email ops, molto stretto.",
        outline=[
            "Cosa fa IDLE e quando il server lo taglia",
            "Polling: CPU, rate, ritardo di classificazione",
            "Limiti tipici dei provider PEC",
            "Reconnect e duplicati",
            "Più caselle: un processo vs pool",
            "Backoff e jitter (non martellare)",
            "Monitor: last_idle_at",
            "Scelta per 1 casella vs 40 caselle",
        ],
        must=["stato machine reconnect", "valori di timeout di esempio", "errori IMAP comuni"],
        scene="A waiting-room chair under a flickering fluorescent light, empty, cinematic.",
    ),
    dict(
        titolo="Backup e restore di uno stack Docker con Postgres, n8n e volumi LLM: il drill mensile che nessuno fa (finché perde le esecuzioni)",
        kw="backup docker postgres n8n",
        kw2="restore drill postgres, volumi docker backup, disaster recovery pmi, n8n executions",
        descrizione="DR reale: cosa backuppari, ordine di restore, secret, test su macchina vuota, RPO/RTO dichiarati. n8n senza backup è teatro.",
        angle="Disaster recovery, tono da runbook.",
        outline=[
            "RPO/RTO in italiano semplice",
            "Cosa è irriproducibile (DB, volumi, credenziali)",
            "Postgres: dump vs snapshot",
            "n8n: DB + encryption key",
            "Modelli LLM: si riseedano, non si backupano sempre",
            "Drill: restore su VPS vuoto ogni mese",
            "Offsite e 3-2-1 adattato a PMI",
            "Runbook da una pagina stampabile",
        ],
        must=["elenco artefatti", "ordine restore", "checklist drill"],
        scene="A fireproof box slightly open in a dark closet, documentary.",
    ),
    dict(
        titolo="L’agente non deve avere root sul server: user namespace, reti Docker interne e il giorno in cui un tool `rm` non è uno scherzo",
        kw="agente ai privilegi docker",
        kw2="least privilege llm, docker user namespace, sandbox tool, comando rm agente",
        descrizione="Hardening: l’LLM che può shellare è ransomware con UX. Drop cap, read-only rootfs, rete interna, allowlist binari, niente docker.sock.",
        angle="Container security per agenti.",
        outline=[
            "Threat model: prompt → tool → shell",
            "docker.sock: la fine del gioco",
            "User non-root, read-only, tmpfs",
            "Reti: l’agente non vede Postgres in chiaro",
            "Allowlist comandi vs “bash libero”",
            "seccomp / AppArmor cenni operativi",
            "Cosa loggare delle exec",
            "Audit prima del go-live",
        ],
        must=["compose con security_opt di esempio", "deny list", "test di fuga"],
        scene="A padlocked server cabinet, shallow depth, cold light, no brand.",
    ),
    dict(
        titolo="SPID, PEC e l’agente: cosa non automatizzare (e come preparare i dati per un umano che firma davvero)",
        kw="agente ai spid pec limiti",
        kw2="spid automazione vietata, pec valore legale, human signature workflow, identità digitale italia",
        descrizione="Confine legale/tecnico: SPID non si delega a un LLM. PEC ha valore. Design del dossier per l’umano: pacchetto, hash, checklist, non click automatico.",
        angle="Identità digitale italiana. Molto verticale.",
        outline=[
            "SPID: identità della persona, non del bot",
            "Cosa è automabile (preparazione) vs cosa no (autenticazione)",
            "PEC: invio automatico vs responsabilità",
            "Dossier: PDF, hash, elenco allegati",
            "UI per l’umano che firma",
            "Conservazione e opponibilità",
            "Rischi di “l’AI ha inviato la PEC”",
            "Architettura raccomandata",
        ],
        must=["matrice automabile/non", "contenuto del dossier", "disclaimer responsabilità"],
        scene="An Italian CIE-like card face-down on a table (no readable ID), next to a fountain pen.",
    ),
    dict(
        titolo="Rate limit delle API pubbliche (FRED, SEC, RSS): jitter, cache 24h e perché --force in loop dal PC di casa ti brucia l’IP",
        kw="rate limit api pubbliche cache",
        kw2="fred api rate limit, sec edgar educata, jitter cron, cache 24h",
        descrizione="Etiquette da data pipeline: 429, backoff, cache, UA onesta, niente scrape HTML se c’è API. Cron con jitter. IP residenziale vs VPS.",
        angle="Data engineering civile.",
        outline=[
            "Le API pubbliche non sono il tuo cluster",
            "FRED e simili: chiavi, limiti, cache",
            "SEC/RSS: rispetto e parsing robusto",
            "Jitter: non 50 job alle 00:00:00",
            "--force e i loop da laptop",
            "403 da HTML: smetti, cambia fonte",
            "Seed vs live: dichiaralo in UI",
            "Runbook 429",
        ],
        must=["politica di cache", "esempio backoff", "user-agent onesto"],
        scene="A traffic jam of identical cars from above, abstract, no plates readable.",
    ),
    dict(
        titolo="Come montare un “ChatGPT privato” su due GPU usate: modelli, coda, rete interna e cosa dire ai dipendenti al posto del divieto inutile",
        kw="chatgpt privato self hosted pmi",
        kw2="vllm dual gpu, llm interno azienda, alternativa chatgpt, policy shadow it",
        descrizione="Progetto interno: UI tipo chat, auth, modelli, coda, dati che restano in LAN. Change management: meglio un GPT interno che un divieto.",
        angle="Prodotto interno + policy.",
        outline=[
            "Il divieto di ChatGPT crea Shadow IT",
            "Requisiti: auth, audit, no training sui dati",
            "Due GPU: tensor parallel vs due modelli",
            "UI: Open WebUI o simile, dietro SSO",
            "Coda e fair share tra uffici",
            "Cosa è permesso incollare",
            "Formazione 45 minuti",
            "Metriche di adozione vs uso di ChatGPT personale",
        ],
        must=["architettura LAN", "policy di 10 regole", "hardware di esempio"],
        scene="Two compact PCs side by side in a locked cabinet, office, no logos.",
    ),
    dict(
        titolo="Salesforce Flow vs agente MCP: quando il clic automatico di Flow è più sicuro (e quando l’LLM serve davvero a leggere il disordine)",
        kw="salesforce flow vs agente mcp",
        kw2="flow orchestrator vs llm, automazione deterministica crm, eccezioni salesforce, tool llm",
        descrizione="Confine deterministico vs linguistico: Flow per se-allora, LLM per testo sporco e eccezioni. Pattern ibrido: Flow chiama un servizio di classificazione, non il contrario.",
        angle="Architettura CRM, anti-hype.",
        outline=[
            "Flow è codice visuale con contratti",
            "L’LLM è per testo e ambiguità, non per IVA al 22%",
            "Eccezioni: email libere, note, allegati",
            "Ibrido: classifica → campo → Flow",
            "Error handling e retry diversi",
            "Costi di manutenzione a 18 mesi",
            "Governance change set vs prompt",
            "Matrice di scelta per 10 automazioni tipiche",
        ],
        must=["matrice 10 casi", "schema ibrido", "anti-pattern LLM dentro ogni Flow"],
        scene="A mechanical lever next to a fountain pen, still life on steel, no text.",
    ),
    dict(
        titolo="Come misuri il 95% di accuratezza sull’estrazione documenti (e come ti accorgi che è un 95% sugli header e un 60% sugli importi)",
        kw="accuratezza estrazione documenti campi",
        kw2="field level accuracy ocr, gold set fatture, confusion importi, human review soglia",
        descrizione="Metriche per campo, micro/macro, costi dell’errore, campionamento. Perché l’accuracy globale mente. Dashboard per l’amministrativo.",
        angle="QA dati, continuazione verticale OCR ma distinta (metrica, non XML).",
        outline=[
            "Accuracy globale vs per campo",
            "Pesi: IBAN > indirizzo > CAP",
            "Intervalli di tolleranza",
            "Campione vs popolazione",
            "Confusion: fornitore A vs B con nomi simili",
            "Soglia di incertezza e coda umana",
            "Report che non è un F1 da paper",
            "Contratto con il fornitore AI interno/esterno",
        ],
        must=["tabella campi e pesi", "formula di score pesato", "esempio report settimanale"],
        scene="A jeweler’s loupe on a blank form, macro, no print.",
    ),
    dict(
        titolo="IBAN, codice fiscale e partita IVA: validatori prima dell’LLM (checksum, e il divieto di “completare” un identificativo mancante)",
        kw="validazione iban codice fiscale partita iva",
        kw2="checksum codice fiscale, partita iva algoritmo, llm allucinazione identificativi, validatori python",
        descrizione="Libreria di validazione italiana davanti al modello: CF, P.IVA, IBAN. Policy: mai inventare un identificativo. UX dell’errore.",
        angle="Dati anagrafici IT, ingegneria.",
        outline=[
            "Perché l’LLM completa i buchi con cifre plausibili",
            "Checksum CF e P.IVA: usa algoritmi, non il modello",
            "IBAN: struttura e modulo 97",
            "Pipeline: extract → validate → else human",
            "Test su dataset sintetico (non dati veri di clienti)",
            "UX: “campo illeggibile” ≠ “campo inventato”",
            "Log: non conservare CF in chiaro più del necessario",
            "Integrazione nei tool MCP/n8n",
        ],
        must=["ordine della pipeline", "riferimento agli algoritmi pubblici", "policy no-invent"],
        scene="A calculator and a blank ID sleeve, desk, no numbers visible.",
    ),
    dict(
        titolo="n8n credentials vs Infisical/Vault: quando il database delle credenziali di n8n diventa il tuo unico punto di fallimento",
        kw="n8n credentials vault infisical",
        kw2="n8n encryption key, secret management pmi, backup credenziali automazione, infisical docker",
        descrizione="Come n8n cifra le credenziali, cosa succede se perdi la encryption key, quando ha senso un vault esterno, come ruotare senza fermare i flow.",
        angle="Secret management specifico n8n.",
        outline=[
            "Dove stanno le credenziali e con quale chiave",
            "Perdere N8N_ENCRYPTION_KEY = perdere i flow",
            "Backup della chiave: procedure",
            "Vault esterno: quando il team cresce",
            "Rotazione token API nei nodi",
            "Ambienti: dev/staging/prod e credenziali miste",
            "Audit: chi ha visto il secret",
            "Procedura di disaster della chiave",
        ],
        must=["avvertenza encryption key", "modello a 3 ambienti", "runbook rotazione"],
        scene="A small safe with the door closed, hotel-room lighting, no brand.",
    ),
]


def dates_tue_thu(n, start=date(2026, 8, 18)):
    """n dates on Tue/Thu starting from start (must be a Tuesday)."""
    out = []
    d = start
    while len(out) < n:
        if d.weekday() in (1, 3):  # Tue, Thu
            out.append(d)
        d += timedelta(days=1)
    return out


def main():
    rows = []
    sched = dates_tue_thu(len(POSTS))
    for i, p in enumerate(POSTS):
        rows.append({
            "titolo": p["titolo"],
            "keyword_principale": p["kw"],
            "keyword_secondarie": p["kw2"],
            "descrizione": p["descrizione"],
            "prompt_articolo": article_prompt(
                p["titolo"], p["kw"], p["kw2"], p["angle"], p["outline"], p["must"]
            ).strip(),
            "prompt_immagine": image_prompt(p["scene"]),
            "larghezza_immagine": IMAGE_SIZE[0],
            "altezza_immagine": IMAGE_SIZE[1],
            "data_pubblicazione": f"{sched[i].isoformat()} 7:30",
        })

    fields = [
        "titolo",
        "keyword_principale",
        "keyword_secondarie",
        "descrizione",
        "prompt_articolo",
        "prompt_immagine",
        "larghezza_immagine",
        "altezza_immagine",
        "data_pubblicazione",
    ]
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=";", quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
