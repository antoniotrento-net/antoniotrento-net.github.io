# -*- coding: utf-8 -*-
"""Piano PRIMARIO: verticali che vendono progetti (dati, prodotto, app, LLM). Jekyll non lo monta."""
import csv
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).with_name("piano-editoriale-2026-clienti.csv")

ARTICLE_RULES = """
IDENTITÀ
Scrivi in italiano come Antonio Trento. Sito: https://antoniotrento.net
Non sei un blogger tecnico. Sei chi progetta e costruisce prodotti digitali end-to-end: dati, backend, interfaccia, automazione, LLM. Il lettore è chi PAGA: titolare, founder, direttore commerciale, responsabile operations, titolare di studio, founder di agenzia. Ha un problema che gli costa soldi, tempo o clienti. Non cerca un tutorial.

OBIETTIVO
Far partire una conversazione di vendita. Ogni pezzo deve far dire: “questo è il mio problema” e “questa persona lo costruisce, non vende un plugin”.
Chiudi con CTA sobrio a https://antoniotrento.net e https://antoniotrento.net/portfolio/ — niente hard sell, niente listino inventato.

LUNGHEZZA
Minimo 4500 parole, target 5000–6000. Allunga con: casi (anonimi, architetturali, non clienti inventati con nome), calcolo del costo dell’inerzia, obiezioni, FAQ da buyer, cosa include un progetto vs cosa è fuffa.

FORMATO
Markdown, niente YAML. Inizia con H2. Linguaggio da riunione col titolare, non da documentazione.
Vietato: docker-compose, snippet Python lunghi, n8n nodi, governor limits, comandi bash, recensioni di librerie.
Consentito: tabelle di costo, timeline, “cosa vedi a schermo”, flussi in italiano, mock di schermate descritti a parole, checklist da stampare.

SEO
Keyword principale nel primo paragrafo, in 2 H2, in chiusura.
Keyword secondarie 4–6 volte, naturali.

VIETATO
- Tutorial stack (Docker, n8n, LangGraph, pgvector, MCP, Ollama, Traefik).
- GDPR articolo per articolo, AI Act da commercialista.
- “AI per il settore X” da enciclopedia (agri, flotte, smart city, salute pubblica).
- Nominare repo e prodotti portfolio (Cloudetta, KineticMCP, DataUnchain, Qwibo, Shotloom, Zirelia, Vibeissue, SP500…).
- Inventare clienti, brand, fatturati (“l’ho fatto per Ferrari”).
- Promettere magia, 99% accuracy, “in una settimana live”.

OBBLIGATORIO
- Costo dell’inerzia in euro o ore (stime dichiarate).
- Cosa ottiene il cliente (schermata, report, app, portale) in linguaggio visivo.
- Perché il SaaS / l’agenzia sito / il no-code si fermano all’80%.
- Perché serve qualcuno che fa DATI + BACKEND + FRONTEND + LLM, non tre fornitori che si incolpano.
- “È per te se / non è per te se”.
- Timeline onesta (settimane/mesi) e cosa succede dopo il go-live (manutenzione).
- 8 FAQ da chi sta per firmare.
"""

IMAGE_SIZE = (1536, 1024)
IMAGE_RULES = (
    "Photorealistic editorial photograph, landscape 1536x1024 (3:2), "
    "no text, no letters, no watermarks, no logos, no UI. "
    "Cinematic, wealthy-but-real Italian business mood (not a server rack, not a homelab). "
    "Adult professionals, faces optional and anonymous. Shallow depth of field. "
)


def article_prompt(title, kw, kw2, angle, outline, must):
    bullets = "\n".join(f"- {x}" for x in outline)
    musts = "\n".join(f"- {x}" for x in must)
    return f"""{ARTICLE_RULES}

TITOLO (tema, non copiarlo come H1): {title}
KEYWORD PRINCIPALE: {kw}
KEYWORD SECONDARIE: {kw2}

ANGOLO DI VENDITA:
{angle}

OUTLINE (H2/H3, ordine):
{bullets}

INCLUDERE:
{musts}

Scrivi l’articolo in italiano, 5000–6000 parole, Markdown.
""".strip()


def image_prompt(scene):
    return f"{IMAGE_RULES}{scene}"


POSTS = [
    dict(
        titolo="Stai decidendo a naso perché i numeri sono in 6 software: quanto ti costa al mese (e come avere UN cruscotto che il titolare apre davvero)",
        kw="cruscotto aziendale titolare",
        kw2="dashboard vendite pmi, dati in tanti software, business intelligence piccola impresa, numeri del giorno prima",
        descrizione="Buyer: titolare cieco sui numeri. Vendi un prodotto dati+UI, non Power BI da corso.",
        angle="Dolore del ‘quanto abbiamo venduto ieri’. Prodotto: una schermata, non un file Excel.",
        outline=[
            "Il lunedì mattina in cui nessuno sa rispondere",
            "Dove sono finiti i numeri (gestionale, e-commerce, fogli, ads, banca)",
            "Il costo dell’inerzia: decisioni sbagliate, scorte, assunzioni",
            "Perché Power BI ‘ce l’abbiamo’ e non lo apre nessuno",
            "Cosa deve vedere il titolare in 20 secondi (la schermata)",
            "Chi costruisce i dati sotto e chi disegna l’interfaccia: se sono due fornitori, fallisce",
            "Timeline e cosa non è incluso (non è magia sui dati sporchi)",
            "È per te se / non è per te se",
        ],
        must=["calcolo ore/euro di inerzia", "descrizione della schermata", "obiezione ‘abbiamo già Excel’"],
        scene="A CEO at a dark conference table looking at a blank wall, empty chairs, morning light, no screens readable.",
    ),
    dict(
        titolo="Il report arriva il 20 del mese: come avere i numeri del giorno prima senza assumere un ufficio data",
        kw="report vendite in ritardo",
        kw2="reporting automatico aziendale, data analyst esterno, report mensile pmi, kpi giornalieri",
        descrizione="Buyer che aspetta il file del controller. Vendi pipeline+prodotto, non ‘assumere un junior’.",
        angle="Velocità di decisione vs headcount.",
        outline=[
            "Decidere a mese inoltrato è decidere sul passato",
            "Cosa c’è dietro un report ‘manuale’ (la persona, non lo strumento)",
            "Assumere un analyst junior non sistema le fonti",
            "Il prodotto: aggiornamento, allarmi, non 40 slide",
            "Cosa deve essere vero nei dati (definizioni: vendita, reso, IVA)",
            "Quanto tempo ci vuole sul serio",
            "Manutenzione: i report muoiono se nessuno li possiede",
            "Segnali che stai comprando fuffa (dashboard da template)",
        ],
        must=["confronto costo junior vs progetto", "definizioni da mettere per iscritto", "red flag template"],
        scene="A wall calendar showing mid-month, empty office, late afternoon.",
    ),
    dict(
        titolo="Vuoi vendere un prodotto AI ai tuoi clienti: da ChatGPT in demo a un software che si paga ogni mese",
        kw="lanciare prodotto ai white label",
        kw2="saas ai per agenzie, productizzare intelligenza artificiale, mvp ai da vendere, software ai per i tuoi clienti",
        descrizione="Buyer: agenzia, software house, consulente che vuole un prodotto. Vendi build end-to-end.",
        angle="Da ore a prodotto. Margine.",
        outline=[
            "La demo che fa ‘wow’ e non si fattura",
            "Cosa comprano i TUOI clienti (risultato, non un modello)",
            "Interfaccia: se sembra una chat, pagano due spicci",
            "Dati, permessi, log: il pezzo che la demo non ha",
            "Prezzo: progetto vs canone, cosa includere",
            "90 giorni: cosa può essere un MVP onesto",
            "Cosa resta tuo (codice, infrastruttura, marchio)",
            "Quando NON productizzare (un solo cliente, un solo flusso)",
        ],
        must=["distinzione demo vs prodotto", "scheletro offerta commerciale", "90 giorni onesti"],
        scene="A product box mockup out of focus on a dark desk, premium lighting, no logos.",
    ),
    dict(
        titolo="L’agenzia ti ha consegnato il sito. Il ‘backend’ è un Google Form. Perché non hai un prodotto (e i clienti se ne accorgono)",
        kw="sito vetrina vs prodotto digitale",
        kw2="agenzia web senza backend, app su misura vs wordpress, prodotto digitale pmi, form al posto del gestionale",
        descrizione="Buyer deluso dall’agenzia. Vendi full-stack vero: UI+logica+dati.",
        angle="Contrapposizione agenzia vs chi costruisce software.",
        outline=[
            "Il sito bello che non tiene uno stato",
            "Cosa manca: utenti, permessi, storico, pagamenti, file",
            "Il cliente che torna e i dati non ci sono",
            "No-code e Form: l’80% e poi il muro",
            "Cosa vedi in un prodotto vero (login, elenco, dettaglio, azione)",
            "Quanto costa rifare vs rattoppare",
            "Come briefare chi deve costruirlo (non ‘fammi un sito’)",
            "È per te se stai perdendo operazioni, non se ti serve solo brochure",
        ],
        must=["checklist prodotto vs vetrina", "brief da una pagina", "muro del no-code"],
        scene="A beautiful shop window at night, empty interior dark, street reflection.",
    ),
    dict(
        titolo="200 copia-incolla al giorno: il costo vero del ‘tanto lo fa Maria’ (e l’app interna che Maria odierà se è fatta male)",
        kw="app interna aziendale copia incolla",
        kw2="software gestionale su misura, automazione data entry, costo ore amministrative, tool interno ux",
        descrizione="Operations. Vendi app interna usabile, dati puliti, non macro Excel.",
        angle="Maria è il sistema. Il prodotto deve farle risparmiare, non aggiungere un login.",
        outline=[
            "Maria come infrastruttura critica",
            "Calcolo: 200 azioni × giorni × costo orario",
            "Perché Excel e WhatsApp vincono sui software brutti",
            "L’app interna: 5 schermate, non 50",
            "Dati sotto: se sbagli il modello, Maria torna al foglio",
            "Coinvolgere chi lavora (altrimenti boicottaggio)",
            "Go-live e le due settimane di odio",
            "Manutenzione: chi risponde quando cambia una regola",
        ],
        must=["calcolo euro/anno", "5 schermate tipo", "errore UX da fornitore"],
        scene="A tired office worker at a cluttered desk, documentary, no screen text.",
    ),
    dict(
        titolo="Il cliente chiede un portale B2B e tu gli mandi un Excel: quanto fatturato stai lasciando sul tavolo",
        kw="portale b2b clienti",
        kw2="area riservata rivenditori, listini per cliente, ecommerce b2b su misura, self service ordini",
        descrizione="Wholesale/B2B. Vendi portale: listini, ordini, stato, UX.",
        angle="Self-service che fa ricavo, non ‘un login sul sito’.",
        outline=[
            "L’Excel con i prezzi ‘non girarlo’",
            "Cosa vuole il rivenditore alle 22",
            "Listini, sconti, disponibilità, storico",
            "Perché Shopify/Woo sembrano la via e poi no",
            "Schermate che fanno chiudere l’ordine",
            "Integrazione col gestionale: se non c’è, è teatro",
            "Chi paga il progetto (tu o il margine nuovo)",
            "Timeline e rollout per fasce di clienti",
        ],
        must=["descrizione portale", "obiezione ‘facciamo un PDF’", "rollout"],
        scene="A closed wholesale counter at night, catalog blurred, industrial warm light.",
    ),
    dict(
        titolo="I commerciali hanno il pipeline in testa: come avere UN numero (senza comprare un CRM da 400€ a utente e lasciarlo vuoto)",
        kw="pipeline commerciale unica",
        kw2="crm che i commerciali usano, forecast vendite pmi, lead che muoiono, cruscotto direzione commerciale",
        descrizione="Direttore commerciale. Vendi CRM+UI+dati usabili, non licenze.",
        angle="Adozione. Il software vuoto è il nemico.",
        outline=[
            "Il forecast che è un sentimento",
            "Perché i CRM enterprise restano vuoti",
            "Cosa deve inserire un commerciale in 40 secondi",
            "Il numero unico: definizione di ‘won’",
            "Interfaccia mobile vs maschere da anni ’90",
            "AI: solo dove pulisce note, non dove inventa il close date",
            "Direzione: la dashboard che non umilia il team",
            "Cambio di processo, non solo di tool",
        ],
        must=["definizione pipeline", "maschera da 40 secondi", "perché Salesforce vuoto fallisce"],
        scene="A sales floor after hours, empty chairs, one lamp, no screens.",
    ),
    dict(
        titolo="Hai speso decine di migliaia in un PoC di AI finito in un cassetto. Come (non) rifarlo",
        kw="poc intelligenza artificiale fallito",
        kw2="progetto ai cassetto, proof of concept vs produzione, budget ai sprecato, go live agente ai",
        descrizione="Buyer bruciato. Vendi produzione: UI, dati, ownership. Smonta il PoC da slides.",
        angle="Terapia post-fregatura + offerta seria.",
        outline=[
            "Il workshop da 40k e il notebook che nessuno apre",
            "PoC vs prodotto: utenti, permessi, errori, orari",
            "Chi ha venduto la demo (modello, non processo)",
            "Come valutare un secondo tentativo senza bruciare altro",
            "Cosa deve essere vero prima di scrivere una riga",
            "MVP che un operatore usa il martedì",
            "Contratto: proprietà, manutenzione, criteri di uscita",
            "Quando è meglio fermarsi",
        ],
        must=["lista cause di morte del PoC", "criteri secondo tentativo", "clausole da pretendere"],
        scene="A drawer slightly open with a forgotten USB stick, office, moody.",
    ),
    dict(
        titolo="Prenotazioni, no-show e WhatsApp: il buco nel calendario che non vedi (e l’app che te lo fa fatturare)",
        kw="ridurre no show prenotazioni",
        kw2="software prenotazioni su misura, whatsapp conferme appuntamenti, calendario che fattura, clinica studio no-show",
        descrizione="Chi vende tempo (studi, cliniche, consulenti, saloni). Vendi prodotto booking+reminders+UI.",
        angle="Ricavo perso per buchi. Non ‘bot WhatsApp tutorial’.",
        outline=[
            "Il no-show come sconto invisibile",
            "WhatsApp non è un sistema, è un cavo",
            "Cosa deve fare il prodotto: slot, conferma, lista d’attesa, pagamento caparra",
            "Interfaccia cliente vs interfaccia segreteria",
            "Dati: storico, abituali, chi salta sempre",
            "Quando un SaaS da 29€/mese basta",
            "Quando ti serve su misura (regole strane, più sedi, più operatori)",
            "ROI in 90 giorni (stima)",
        ],
        must=["calcolo no-show", "due interfacce", "quando SaaS basta"],
        scene="An empty waiting-room chair, clock on the wall out of focus, clinic mood, no logos.",
    ),
    dict(
        titolo="8.000 SKU e un prezzo diverso per ogni cliente: il listino PDF è una perdita di margine",
        kw="listini personalizzati b2b software",
        kw2="prezzi per cliente gestionale, catalogo 8000 sku, configuratore prezzi, app listini agenti",
        descrizione="Agenti/rappresentanti. Vendi catalogo+prezzi+app.",
        angle="Margine e errori di prezzo.",
        outline=[
            "Lo sconto ‘a voce’ che non torna in fattura",
            "PDF e WhatsApp: due fonti, zero verità",
            "Cosa deve vedere l’agente in visita",
            "Regole di prezzo: il motore, non la chat AI",
            "Frontend: ricerca, disponibilità, ordine",
            "Sincronizzazione col gestionale",
            "Offline in zona senza rete (quando serve)",
            "Errore da 2% sul listino × volume",
        ],
        must=["stima errore listino", "schermata agente", "AI vs motore prezzi"],
        scene="A sales rep bag and a closed price book, car interior blurred, no text.",
    ),
    dict(
        titolo="Il tuo software interno è un Access del 2008: quando conviene riscriverlo (e quando è un suicidio)",
        kw="riscrivere software gestionale legacy",
        kw2="migrare access, applicazione obsoleta azienda, modernizzare gestionale, costo rewrite software",
        descrizione="Legacy. Vendi rewrite selettivo, dati, UI nuova.",
        angle="Paura e opportunità. Onestà sul rewrite.",
        outline=[
            "Il file .mdb che tiene in piedi l’azienda",
            "Sintomi: un solo PC, una sola persona, backup ‘sulla chiavetta’",
            "Rewrite totale vs strappare un pezzo",
            "Cosa conservare: regole di business, non le maschere grigie",
            "Interfaccia nuova che gli operatori accettano",
            "Costo e tempo (forchette oneste)",
            "Il suicidio: riscrivere tutto mentre si lavora come prima, senza cutover",
            "Piano a strati",
        ],
        must=["sintomi da rewrite", "strati", "forchette tempo/costo qualitative"],
        scene="An old beige PC in a dusty corner, documentary, no brand.",
    ),
    dict(
        titolo="Il tecnico in giro perde due interventi al giorno: l’app sul telefono che (non) gli hai dato",
        kw="app tecnici sul campo",
        kw2="field service software, interventi assistenza app, ordini di lavoro mobile, tecnico senza carta",
        descrizione="Field service. Vendi mobile+backend+dati.",
        angle="Produttività in strada.",
        outline=[
            "La chiamata ‘dove sei / che pezzo ti manca’",
            "Cosa deve fare l’app in 4 tap",
            "Foto, firma, ricambi, orari: dati che oggi spariscono",
            "Perché un PDF via mail non è un’app",
            "Ufficio: la coda interventi che si vede",
            "Offline e copertura",
            "Integrazione magazzino/gestionale",
            "ROI: interventi in più, non ‘digitalizzazione’",
        ],
        must=["4 tap", "coda ufficio", "ROI interventi"],
        scene="A service van dashboard at dusk, phone face-down, no map text.",
    ),
    dict(
        titolo="Pratiche ferme tre settimane in una casella: il software che fa muovere i dossier (non un’altra email)",
        kw="software gestione pratiche",
        kw2="dossier clienti fermo, workflow pratiche, broker assicurativo software, stato pratica visibile",
        descrizione="Broker, CAF, studi, assicurazioni. Vendi stato+UI+scadenze.",
        angle="Tempo ciclo = soldi e clienti persi.",
        outline=[
            "‘A che punto è la mia pratica?’ e nessuno sa",
            "Email come database: il disastro",
            "Stati, responsabili, scadenze, allegati",
            "Portale cliente vs telefono ogni giorno",
            "LLM: classificare e estrarre, non decidere",
            "Cosa vede il titolare: colli di bottiglia",
            "Go-live per team, non big bang",
            "Quando un CRM generico basta (raro)",
        ],
        must=["macchina a stati in italiano", "portale cliente", "colli di bottiglia"],
        scene="A stack of file folders in a metal tray, insurance-office mood, labels unreadable.",
    ),
    dict(
        titolo="Vuoi un MVP in 90 giorni che non sia una slide: cosa si può (davvero) consegnare e cosa stai sognando",
        kw="mvp software 90 giorni",
        kw2="sviluppare mvp founder, app su misura tempi, prototipo vs prodotto, budget mvp italia",
        descrizione="Founder. Vendi build onesto. Full-stack come promessa di completezza, non come stack.",
        angle="Aspettative. Qualifica i lead.",
        outline=[
            "MVP non è il brand e tre schermate su Figma",
            "Cosa sta in 90 giorni (un flusso, utenti veri, dati veri)",
            "Cosa non sta (marketplace, AI magica, dieci integrazioni)",
            "Frontend senza backend: il tradimento",
            "Dati: se non sai la fonte, non c’è MVP",
            "Come si lavora settimana per settimana (visibile)",
            "Budget: forchette, non un numero magico",
            "Cosa succede al giorno 91",
        ],
        must=["in/out 90 giorni", "ritmo settimanale", "giorno 91"],
        scene="A foam core prototype and a coffee, startup table, no logos.",
    ),
    dict(
        titolo="Assumere un data analyst non sistema le fonti: perché i KPI restano una rissa (e serve una pipeline, non una persona sola)",
        kw="data analyst non basta",
        kw2="pipeline dati aziendale, fonti dati sporche, kpi non allineati, team data pmi",
        descrizione="Chi sta per assumere. Vendi architettura dati + prodotto, non headcount.",
        angle="Headcount vs sistema.",
        outline=[
            "L’annuncio ‘cerchiamo un data analyst junior’",
            "Il primo mese: pulizia, non insight",
            "Rissa sui KPI: due vendite diverse",
            "Pipeline: contratti sui numeri, non grafici",
            "Chi deve stare al tavolo (commerciale, amm, IT)",
            "Cosa fa una persona vs cosa fa un sistema",
            "Quando assumere DOPO",
            "Deliverable che un titolare firma",
        ],
        must=["rissa KPI esempio", "tavolo ruoli", "quando assumere"],
        scene="Two people arguing over papers, faces not clear, meeting room.",
    ),
    dict(
        titolo="Non ti serve ‘un modello’. Ti serve un processo che produce un output che il cliente paga",
        kw="prodotto llm vs chatbot",
        kw2="usare llm in un software, ai che produce documenti, processo ai aziendale, output pagabile intelligenza artificiale",
        descrizione="Chi ha visto ChatGPT e vuole ‘metterlo in azienda’. Vendi processo+UI+qualità.",
        angle="Output pagabile, non chat.",
        outline=[
            "La chat è un giocattolo, il processo è un prodotto",
            "Esempi di output: dossier, classificazione, bozza, estratto — con umano",
            "Qualità: come si rifiuta un output",
            "Interfaccia: coda, stato, responsabile",
            "Dati in ingresso: spazzatura in, spazzatura out",
            "Prezzo al cliente finale vs costo di produzione",
            "Errori da ‘mettiamo GPT sulla inbox’",
            "Come si parte da UN output",
        ],
        must=["un output esempio", "coda/stato", "rifiuto qualità"],
        scene="A finished printed report folder on a desk, premium, no readable title.",
    ),
    dict(
        titolo="Il sito è bello e al secondo click si rompe: perché i clienti se ne vanno (e non è ‘un problema di hosting’)",
        kw="sito lento errori utenti",
        kw2="ux che perde clienti, frontend backend disallineati, app instabile, conversione sito rotto",
        descrizione="Buyer con sito/app che perde gente. Vendi qualità full-stack.",
        angle="Conversione persa. Non Lighthouse tutorial.",
        outline=[
            "Il secondo click: login, carrello, prenota, paga",
            "Bello ≠ funzionante",
            "Sintomi: timeout, doppi invii, dati spariti",
            "Tre fornitori (grafica, wordpress, ‘lo sviluppatore’) e nessuno è padrone",
            "Cosa si misura (funnel, errori) prima di ridisegnare",
            "Riparare vs rifare",
            "Chi deve essere un unico responsabile tecnico",
            "Cosa chiedere in un audit di una settimana",
        ],
        must=["sintomi", "audit 1 settimana", "un responsabile"],
        scene="A person walking away from a shop door, dusk, motion, no signs readable.",
    ),
    dict(
        titolo="Il titolare chiede ‘quanto abbiamo venduto ieri’ e in 10 minuti nessuno risponde: questo è il tuo vero software mancante",
        kw="quanto abbiamo venduto ieri",
        kw2="vendite giornaliere pmi, cruscotto titolare, dati in tempo reale piccola impresa, report vendite quotidiano",
        descrizione="Headline da ricerca parlata. Stesso cluster cruscotto, angolo più punch.",
        angle="Domanda letterale da Google vocale / titolare.",
        outline=[
            "La domanda più costosa dell’azienda",
            "Perché 10 minuti sono già troppi",
            "Cosa deve entrare nella definizione di ‘venduto’",
            "Canali: negozio, web, rappresentanti, marketplace",
            "La schermata da telefono in macchina",
            "Allarmi: ieri anomalo",
            "Chi mantiene le definizioni",
            "Piccolo vs medio: due profondità di progetto",
        ],
        must=["definizione venduto", "schermata mobile", "allarme"],
        scene="A car interior, phone in a holder showing a dark screen, dawn, no UI.",
    ),
    dict(
        titolo="Tre magazzini, un e-commerce, i rappresentanti: tre ‘verità’ sul residuo e ordini che non puoi evadere",
        kw="giacenze magazzino disallineate",
        kw2="multimagazzino ecommerce, scorte errate, software magazzino pmi, disponibilità prodotti",
        descrizione="Ops+commerce. Vendi verità unica su stock + UI.",
        angle="Vendite che non puoi consegnare.",
        outline=[
            "Hai venduto quello che non c’è",
            "Tre sistemi, tre residui",
            "Cosa deve vedere il sito vs l’agente vs il magazzino",
            "Resi, trasferimenti, impegno ordine",
            "Perché un WMS da fiera è prematuro (spesso)",
            "Prodotto: disponibilità onesta in ogni canale",
            "Rollout per magazzino",
            "KPI: stockout e overselling",
        ],
        must=["tre verità", "impegno ordine", "KPI"],
        scene="Warehouse aisles diverging, split light, cardboard unbranded.",
    ),
    dict(
        titolo="Ferie, turni e presenze ancora su WhatsApp: l’app HR minima che toglie il caos (senza un software da multinazionale)",
        kw="app ferie turni pmi",
        kw2="gestione presenze piccola impresa, sostituzioni turni, software hr semplice, richiesta ferie app",
        descrizione="HR PMI. Vendi app semplice, non SAP HR.",
        angle="Caos turni = straordinari e liti.",
        outline=[
            "Il gruppo WhatsApp ‘turni’",
            "Cosa serve davvero: richiesta, approvazione, calendario, saldo",
            "Cosa non serve (talent, OKR, social interno)",
            "Interfaccia da telefono per chi sta in produzione",
            "Regole: chi approva, scadenze, sovrapposizioni",
            "Dati per paga: export, non un altro silos",
            "Quando il modulo del gestionale basta",
            "Go-live in un mese (se le regole sono chiare)",
        ],
        must=["minimo prodotto", "quando gestionale basta", "export paga"],
        scene="A factory break room whiteboard with unreadable shift grid, documentary.",
    ),
    dict(
        titolo="40 ticket uguali al giorno: il customer care che non ha una knowledge (e l’AI che copia le risposte sbagliate)",
        kw="customer care ticket ripetuti",
        kw2="knowledge base assistenza, ai helpdesk rischi, software ticket pmi, risposte standard clienti",
        descrizione="Supporto. Vendi knowledge+coda+UI, AI con citazione.",
        angle="Qualità vs volume. Paura AI che sbaglia.",
        outline=[
            "Il copia-incolla delle risposte vecchie",
            "Prima la knowledge, poi qualunque AI",
            "Ticket: stati, SLA, chi è il cliente",
            "AI che cita la procedura, non che inventa il rimborso",
            "Interfaccia agente vs portale cliente",
            "Quando sei troppo piccoli per un helpdesk enterprise",
            "Metriche: ripetuti, tempo, escalation",
            "Errori che ti fanno perdere un cliente grosso",
        ],
        must=["citazione obbligatoria", "metriche", "errore rimborso"],
        scene="A headset on an empty support desk, muted office, no screens.",
    ),
    dict(
        titolo="2.000 PDF in una cartella e zero ricerca: stai pagando l’affitto della conoscenza che non usi",
        kw="ricerca documenti aziendali pdf",
        kw2="archivio pdf non cercabile, knowledge documenti, trovare contratti vecchi, area documenti interna",
        descrizione="Documenti. Vendi prodotto ricerca+permessi+UI, non ‘RAG tutorial’.",
        angle="Conoscenza morta = ore e rischi.",
        outline=[
            "Il file ‘definitivo_ver3_FINALE’",
            "Cercare non è avere Drive",
            "Permessi: non tutti vedono gli stipendi",
            "Cosa esce a schermo: pezzo, file, data, responsabile",
            "LLM: riassume solo ciò che ha trovato",
            "Chi carica, chi archivia, chi butta",
            "Progetto a strati (contratti prima, tutto dopo)",
            "Quando un bravo filenaming basta (raro ma onesto)",
        ],
        must=["schermata risultato", "permessi", "strati"],
        scene="Cardboard archive boxes in a corridor, institutional, labels blurred.",
    ),
    dict(
        titolo="Overbooking e canali che non si parlano: l’ospitalità perde soldi tra Booking, sito e telefono",
        kw="overbooking canali prenotazione",
        kw2="gestione canali hotel, software b&b prenotazioni, calendario unico ospitalità, sito vs ota",
        descrizione="Hospitality. Vendi calendario unico + sito/portale.",
        angle="Ricavo e recensioni. Verticale che vende.",
        outline=[
            "La camera venduta due volte",
            "OTA, sito, walk-in, WhatsApp",
            "Calendario unico: non è un foglio",
            "Cosa vede il cliente sul TUO sito (disponibilità vera)",
            "Prezzi e restrizioni: se sono a mano, sbagli",
            "Quando un channel manager basta",
            "Quando ti serve un pezzo su misura (esperienze, più strutture, B2B)",
            "Recensioni e no-show: il cerchio",
        ],
        must=["canali", "quando SaaS basta", "sito con disponibilità vera"],
        scene="A hotel hallway with a cart, warm lamps, no signage readable.",
    ),
    dict(
        titolo="Ordini di produzione ancora su carta: la piccola manifattura che non sa se è in ritardo (finché il cliente chiama)",
        kw="ordini produzione digitale pmi",
        kw2="mes piccola manifattura, avanzamento commessa, software officina, ritardi produzione",
        descrizione="Manifattura piccola. Vendi avanzamento commessa + schermate reparto.",
        angle="Ritardo = penale e reputazione.",
        outline=[
            "Il foglio in officina e l’Excel in ufficio",
            "Cosa deve vedere il capo reparto vs il titolare",
            "Stati della commessa, fermi, ricambi",
            "Non è un SAP: è un flusso",
            "Dati che servono al commerciale per non over-promettere",
            "Go-live in un reparto pilota",
            "Integrazione gestionale/scorta",
            "KPI: rispetto data, code",
        ],
        must=["due schermate", "pilota", "over-promessa commerciale"],
        scene="A small machine shop, empty, paper traveler hanging unreadable, industrial light.",
    ),
    dict(
        titolo="Hai già i clienti: ti manca l’area riservata (corsi, file, rinnovi) e stai lasciando soldi a Teachable e compagnia",
        kw="area riservata clienti su misura",
        kw2="membership sito, accademia aziendale, vendere corsi senza saas usa, portale clienti esistente",
        descrizione="Chi ha audience. Vendi membership/portale, pagamenti, contenuti.",
        angle="Margine vs piattaforma USA.",
        outline=[
            "I clienti ci sono, il prodotto digitale no",
            "Cosa fa un’area riservata vera (utenti, accessi, scadenza, file)",
            "Perché le piattaforme ready-made si prendono il margine e i dati",
            "UX: se è brutta non rinnovano",
            "Contenuti, video, PDF: peso e permessi",
            "Rinnovi e solleciti: processo, non spam",
            "Quando restare su una piattaforma",
            "Migrazione: il terrore degli account",
        ],
        must=["confronto margine", "feature minime", "migrazione"],
        scene="A velvet rope and an empty doorway, club mood, no logos.",
    ),
    dict(
        titolo="No-code ti porta all’80% e poi ti blocca: quando (e come) chiamare chi sviluppa sul serio",
        kw="limiti no code azienda",
        kw2="bubble webflow limiti, passare da no-code a codice, app no-code lenta, vendor lock-in no code",
        descrizione="Founder bloccato. Vendi uscita/rebuild selettivo.",
        angle="Muro dell’80%. Vendita del rebuild.",
        outline=[
            "L’80% che sembra successo",
            "Sintomi del muro: permessi, performance, un’integrazione, un pdf",
            "Lock-in: i tuoi dati in un tool che non esporti davvero",
            "Strappare il pezzo critico vs rifare tutto",
            "Cosa conservare (design, copy, apprendimenti)",
            "Come non fermare il business durante il passaggio",
            "Costi: hai già pagato l’80%, ora paghi il 100%",
            "Quando il no-code resta (interni, volume basso)",
        ],
        must=["sintomi muro", "strappo vs rewrite", "continuità"],
        scene="A road that ends at a wall, cinematic, dusk, no signs.",
    ),
    dict(
        titolo="Il costo di NON avere l’app: ore, errori, clienti persi — una stima che puoi fare lunedì mattina",
        kw="costo non digitalizzare processi",
        kw2="roi software su misura, spreco ore manuali, errori data entry costo, perdere clienti per processo",
        descrizione="Pezzo calcolatrice. Vende urgenza. Qualsiasi verticale.",
        angle="Inerzia in euro.",
        outline=[
            "L’inerzia sembra gratis",
            "Tre voci: ore, errori, clienti che non tornano",
            "Come misurare le ore in 3 giorni (metodo)",
            "Errori: un reso, una fattura, un appuntamento",
            "Clienti persi: il silenzio che non vedi nel P&L",
            "Foglio di stima (spiegato, non un Excel da scaricare obbligatorio)",
            "Quando il numero NON giustifica un progetto",
            "Come usare la stima in un confronto con un fornitore",
        ],
        must=["metodo 3 giorni", "tre voci", "quando non fare il progetto"],
        scene="An empty cash register drawer, shop, moody, no currency sharp.",
    ),
    dict(
        titolo="Schede immobile su 5 portali a mano: l’agenzia immobiliare che lavora per gli annunci, non per le visite",
        kw="pubblicare annunci immobiliari automatico",
        kw2="software agenzia immobiliare, multilisting, scheda immobile unica, crm visite immobiliari",
        descrizione="Real estate. Vendi scheda unica + canali + CRM visite.",
        angle="Tempo agente = visite, non data entry.",
        outline=[
            "L’agente fotografo-copywriter-data entry",
            "Una scheda, molti portali",
            "Foto, planimetrie, disponibilità, prezzo",
            "Visite, feedback, proposta: il CRM vero",
            "Sito proprio vs solo portali",
            "Quando un software verticale di categoria basta",
            "Quando le regole della tua rete richiedono su misura",
            "KPI: tempo scheda vs visite",
        ],
        must=["scheda unica", "KPI", "quando SaaS verticale basta"],
        scene="An empty apartment with a window, real-estate mood, no flyers readable.",
    ),
    dict(
        titolo="Lead che arrivano e muoiono in 48 ore: ti manca il cruscotto, non ‘più ads’",
        kw="lead che non vengono lavorati",
        kw2="tempo di risposta lead, crm marketing pmi, lead ads sprecati, follow up commerciale",
        descrizione="Marketing+sales. Vendi velocità+assegnazione+UI.",
        angle="Ads senza operations = soldi bruciati.",
        outline=[
            "Il form che cade in una mail",
            "SLA: chi tocca il lead in 5 minuti",
            "Assegnazione, stato, esito",
            "Cruscotto: lead vecchi, orfani, duplicati",
            "AI: riassumere il messaggio, non ‘chiudere la vendita’",
            "Ads: spegni le campagne se il follow-up non c’è",
            "Integrazione form/WhatsApp/telefono",
            "Metrica unica: tempo al primo contatto",
        ],
        must=["SLA", "metrica unica", "spegnere ads"],
        scene="A ringing phone on an empty desk, after hours, no caller ID readable.",
    ),
    dict(
        titolo="Stai ottimizzando la metrica sbagliata: il KPI che ti fa perdere soldi (mentre la dashboard è ‘verde’)",
        kw="kpi sbagliati azienda",
        kw2="vanity metrics, dashboard fuorviante, indicatori titolare, ottimizzare metrica sbagliata",
        descrizione="Data storytelling commerciale. Vendi definizioni+prodotto numeri.",
        angle="Verde ≠ sano. Molto vendibile.",
        outline=[
            "Il semaforo verde e il conto in rosso",
            "Vanity: visite, messaggi, ‘engagement’",
            "Esempi: scontrino medio vs margine, ticket chiusi vs clienti persi, occupancy vs rev",
            "Chi sceglie i KPI (non l’IT da solo)",
            "Una dashboard, poche metriche, un owner",
            "Cosa nascondono i filtri",
            "Come rifare le definizioni in un workshop",
            "Dopo: il prodotto che le rispetta",
        ],
        must=["esempi vanity vs soldi", "workshop definizioni", "pochi KPI"],
        scene="A green traffic light in fog, cinematic, no street names.",
    ),
    dict(
        titolo="Rinnovi, scadenze e ‘chi non ha pagato’: il software che ti ricorda i soldi (non un altro foglio scadenziario)",
        kw="software rinnovi scadenze clienti",
        kw2="solleciti automatici professionali, contratti in scadenza, recuring revenue pmi, chi non ha pagato",
        descrizione="Recurring. Vendi scadenze+solleciti+stato pagamenti+UI.",
        angle="Cassa. Verticale servizi/abbonamenti.",
        outline=[
            "Il rinnovo che scopri quando il cliente è già andato",
            "Contratti, canoni, pec, fatture: un filo",
            "Cosa deve vedere amministrazione vs commerciale",
            "Tono dei solleciti: se è brutto, perdi il cliente",
            "Dati banca/gestionale: matching, non speranza",
            "Quando un gestionale ‘ha già le scadenze’ (e nessuno le usa)",
            "Progetto piccolo, impatto cassa",
            "GDPR e toni: cenni da titolare, non trattato",
        ],
        must=["due viste", "tono solleciti", "impatto cassa"],
        scene="A wall of hanging keys, some missing, still life, no numbers.",
    ),
    dict(
        titolo="UX che fa abbandonare la prenotazione (o il carrello): non ti serve ‘più traffico’, ti serve un flusso che si chiude",
        kw="abbandono prenotazione carrello",
        kw2="ux checkout, form troppo lunghi, conversione mobile, rifare interfaccia prodotto",
        descrizione="Conversion UX. Vendi frontend serio legato a backend vero.",
        angle="Traffico sprecato. Full-stack implicito.",
        outline=[
            "Paghi le ads e perdi al form",
            "Mobile: il dito, la tastiera, i 12 campi",
            "Passi: cosa è obbligatorio ora vs dopo",
            "Errori: ‘qualcosa è andato storto’",
            "Backend che rifiuta e frontend che non spiega",
            "Test: 5 utenti veri battono 50 opinioni interne",
            "Quando ridisegnare vs quando sistemare 3 ostacoli",
            "Come si misura il chiusura del flusso",
        ],
        must=["ostacoli classici", "5 utenti", "misura chiusura"],
        scene="A shopping bag left on a sidewalk, dusk, no logos.",
    ),
    dict(
        titolo="Chi vende tempo (consulenti, cliniche, saloni): il calendario è il tuo ERP. Se è un Google Calendar condiviso, stai improvvisando",
        kw="calendario professionale multi operatore",
        kw2="prenotazioni più professionisti, agenda studio, software appuntamenti, risorse e sale",
        descrizione="Multi-operatore. Vendi scheduling come prodotto.",
        angle="Agenda = fatturato.",
        outline=[
            "Google Calendar non sa i tuoi vincoli",
            "Operatori, sale, attrezzature, pause, tragitto",
            "Cliente: prenota la persona giusta",
            "No-show, lista attesa, spostamenti",
            "Pagamenti e pacchetti sedute",
            "SaaS verticale vs su misura (regole strane)",
            "Dati: chi rende, quali slot restano vuoti",
            "Cosa vede il titolare il venerdì",
        ],
        must=["vincoli", "venerdì titolare", "SaaS vs su misura"],
        scene="A salon chair empty, mirrors, warm light, no brand.",
    ),
    dict(
        titolo="Software house senza frontend: stai consegnando API e il cliente vede un deserto. Perché ti serve qualcuno che chiude il prodotto",
        kw="frontend per software house",
        kw2="ui ux per backend team, consegnare prodotto completo, app interfaccia cliente, partnership sviluppo",
        descrizione="B2B verso software house. Vendi partnership frontend+prodotto.",
        angle="Loro backend, manca la faccia. Collaborazione.",
        outline=[
            "L’API ‘è pronta’ e il cliente non sa dove cliccare",
            "Prodotto = contratto visibile",
            "Cosa fa un frontend serio (stati, errori, vuoti, permessi)",
            "Design system vs pagina bella una tantum",
            "Come si lavora in due team senza rimpalli",
            "Dati e contratti API: se cambiano ogni giorno, l’UI muore",
            "White-label per i LORO clienti",
            "Modello di collaborazione",
        ],
        must=["definizione prodotto visibile", "modello collaborazione", "errori/vuoti"],
        scene="An unfinished building facade with scaffolding, architectural, dusk.",
    ),
    dict(
        titolo="Hai un’idea di app e stai per bruciare il budget sul prototipo sbagliato: le 8 domande prima di spendere",
        kw="prima di sviluppare un app",
        kw2="validare idea app, budget sviluppo founder, domande al developer, evitare spreco mvp",
        descrizione="Founder pre-spend. Vendi discovery onesta (che poi può diventare build).",
        angle="Qualifica. Fiducia.",
        outline=[
            "L’idea non è il perimetro",
            "8 domande: chi, frequenza, dato, pagamento, offline, ruoli, rischio, analoghi",
            "Cosa NON chiedere a ChatGPT (il competitor ‘facile’)",
            "Figma non è un test di mercato",
            "Quanto tenere per il dopo-MVP",
            "Come capire se l’interlocutore è uno sviluppatore o un venditore di slide",
            "Deliverable di una discovery (che resta tua)",
            "Quando NON partire",
        ],
        must=["8 domande", "deliverable discovery", "segnale venditore slide"],
        scene="A napkin sketch out of focus and a closed wallet, café table.",
    ),
    dict(
        titolo="Multi-sede: 3 filiali, 3 Excel, un titolare che non sa quale punto vende. Il cruscotto di gruppo che manca",
        kw="cruscotto multi sede",
        kw2="filiali dati unificati, report catena negozi, confronto punti vendita, direzione rete",
        descrizione="Reti. Vendi consolidato+permessi per sede.",
        angle="Confronto sedi = potere.",
        outline=[
            "Ogni sede ha la sua verità",
            "Consolidare non è sommare Excel",
            "Permessi: il responsabile vede solo la sua",
            "Definizioni comuni (scontrino, reso, ore)",
            "Schermata direzione vs schermata store manager",
            "Rollout sede per sede",
            "Resistenza: ‘i nostri numeri sono diversi’",
            "Cosa fare con i dati prima del software",
        ],
        must=["due schermate", "definizioni comuni", "resistenza"],
        scene="Three storefronts in a row at night, lights, no shop names readable.",
    ),
    dict(
        titolo="Cosa stai comprando quando firmi uno sviluppo su misura (e cosa non è ‘un sito da 3.000 euro’)",
        kw="cosa include software su misura",
        kw2="preventivo sviluppo applicativo, differenza sito e software, manutenzione applicativa, proprietà codice",
        descrizione="Educazione all’acquisto. Vende progetti veri. Trasparenza.",
        angle="Buyer’s guide al tuo mestiere.",
        outline=[
            "Sito, e-commerce, gestionale, app: quattro mestieri",
            "Cosa c’è in un preventivo serio (analisi, UI, dati, go-live, garanzia)",
            "Cosa manca nei preventivi da 3k",
            "Proprietà: codice, grafica, account, dati",
            "Manutenzione: il 15–25% che nessuno vuole sentire",
            "Come si paga (sal, non ‘tutto all’inizio’)",
            "Red flag",
            "Come usare questa pagina mentre parli con chiunque (me compreso)",
        ],
        must=["quattro mestieri", "voci preventivo", "manutenzione"],
        scene="A fountain pen over a contract, text unreadable, wood desk.",
    ),
    dict(
        titolo="Il progetto ‘finito’ che muore in sei mesi: manutenzione, piccole modifiche, e perché il fornitore sparisce",
        kw="manutenzione software dopo go live",
        kw2="software morto dopo rilascio, contratto manutenzione applicativa, chi aggiorna l app, fornitore sparito",
        descrizione="Post-vendita honesty. Vende retainer. Paura del ghosting.",
        angle="Go-live non è la fine.",
        outline=[
            "Il giorno dopo il go-live inizia il vero uso",
            "Piccole modifiche: IVA, un campo, un export",
            "Chi ha le chiavi (hosting, store, DNS, backup)",
            "Contratto di manutenzione: ore, SLA, cosa è extra",
            "Il fornitore che sparisce (codice sul PC suo)",
            "Cosa pretendere in consegna (repo, accessi, documentazione viva)",
            "Costo del fermo vs canone",
            "Come cambiare cavallo senza morire",
        ],
        must=["lista consegna", "SLA in parole", "chiavi"],
        scene="Abandoned reception with a withered plant, office, daylight.",
    ),
    dict(
        titolo="Dossier di credito e pratiche che viaggiano per email: il portale che fa chiudere (invece di inseguire allegati)",
        kw="portale dossier credito",
        kw2="istruttoria documentale software, allegati clienti, pratica finanziamento stato, area upload documenti",
        descrizione="Credito/finanza/intermediari. Vendi portale documentale+stati.",
        angle="Tempo istruttoria = margine.",
        outline=[
            "L’allegato che manca sempre",
            "Portale: checklist, upload, stato, scaduto",
            "Permessi: cliente, ufficio, partner",
            "LLM: controllo completezza, non delibera",
            "Audit: chi ha visto cosa",
            "Integrazione con chi eroga",
            "UX del cliente ansioso",
            "Quando un drive condiviso è negligenza",
        ],
        must=["checklist upload", "confine LLM", "Drive = negligenza"],
        scene="A metal briefcase closed on a table, bank-office cold light, no logos.",
    ),
    dict(
        titolo="Comande, magazzino e fatture: il locale che perde margine tra sala e amministrazione",
        kw="software locale ristorazione magazzino",
        kw2="costo del venduto ristorante, giacenze cucina, integrazione cassa fatture, food cost",
        descrizione="HoReCa. Vendi filo cassa-magazzino-amm, non un’altra cassa.",
        angle="Food cost. Verticale che paga.",
        outline=[
            "Lo scontrino c’è, il food cost no",
            "Sala, cucina, magazzino, commercialista: quattro mondi",
            "Cosa deve tornare: ricetta, scarico, fattura fornitore",
            "Perché il gestionale ‘ce l’abbiamo’ e i numeri no",
            "Interfaccia che un cameriere/cuoco usa",
            "Dati per il titolare: piatto che perde",
            "Integrazione cassa: non rifare la cassa se funziona",
            "Piccolo locale vs catena",
        ],
        must=["filo ricetta-scarico", "piatto che perde", "non rifare la cassa"],
        scene="Empty restaurant after close, chairs up, warm residual light.",
    ),
    dict(
        titolo="Soci, rinnovi, comunicazioni: l’associazione che vive di Excel e perde quote ogni anno",
        kw="gestione soci associazione software",
        kw2="rinnovo quote associative, anagrafica soci, comunicazioni soci, software asd no profit",
        descrizione="Nonprofit/ASD. Vendi anagrafica+rinnovi+comunicazioni.",
        angle="Quote perse. Budget piccolo ma reale.",
        outline=[
            "Il tesoriere con il foglio",
            "Anagrafica unica, privacy, consensi",
            "Rinnovi: solleciti umani, non spam",
            "Eventi e comunicazioni segmentate",
            "Pagamenti: se è un casino, non rinnovano",
            "Volontari: UX semplicissima",
            "Costo vs quote recuperate",
            "Quando un tool da 10€/mese basta",
        ],
        must=["quote recuperate", "UX volontari", "quando tool basta"],
        scene="A community hall with stacked chairs, evening, no banners readable.",
    ),
    dict(
        titolo="Catalogo, preventivo, ordine, fattura: il buco tra commerciale e amministrazione che ti mangia il margine",
        kw="dal preventivo alla fattura software",
        kw2="configuratore preventivi, ordine cliente flusso, allineamento commerciale amministrazione, margine perso preventivo",
        descrizione="Commerciale-amm. Vendi flusso unico, numeri coerenti.",
        angle="Preventivo ≠ fattura. Soldi.",
        outline=[
            "Il preventivo vinto e la fattura diversa",
            "Un documento, molti stati",
            "Regole di prezzo e approvazione sconti",
            "Cosa vede il commerciale vs l’amministrazione",
            "AI: bozza descrittiva, non il totale",
            "Integrazione gestionale",
            "Errori classici di mapping",
            "KPI: delta preventivo-fattura",
        ],
        must=["stati documento", "AI non tocca il totale", "KPI delta"],
        scene="Two documents side by side on a desk, text unreadable, one slightly offset.",
    ),
    dict(
        titolo="Formazione interna: i video e i PDF che nessuno trova (e i nuovi assunti che chiedono sempre le stesse cose)",
        kw="piattaforma formazione interna",
        kw2="lms piccola azienda, onboarding video, cercare procedure, accademia interna",
        descrizione="L&D PMI. Vendi LMS leggero+ricerca.",
        angle="Onboarding ripetuto = costo.",
        outline=[
            "Il drive ‘formazione’ cimitero",
            "Cosa deve trovare un assunto al giorno 2",
            "Video, PDF, quiz: il minimo",
            "Chi aggiorna quando cambia una procedura",
            "AI: ‘dov’è il pezzo’ con citazione, non un corso inventato",
            "Permessi per ruolo",
            "Metrica: domande ripetute allo desk",
            "Quando basta Notion (e quando no)",
        ],
        must=["giorno 2", "citazione", "Notion sì/no"],
        scene="An empty training room, chairs, projector off, no slides.",
    ),
    dict(
        titolo="White-label per la tua agenzia: vendi AI e software ai clienti senza rimontare tutto ogni volta",
        kw="white label software agenzia",
        kw2="prodotto da rivendere ai clienti, piattaforma white label, margine agenzia digitale, software ripetibile",
        descrizione="Agenzie. Vendi piattaforma ripetibile + UI brandizzabile.",
        angle="Margine e scala. Molto commerciale.",
        outline=[
            "Ogni cliente un progetto da zero: il margine muore",
            "Cosa è white-label (brand, domini, dati separati)",
            "Cosa è un pasticcio (stesso database, stessi log)",
            "Un core, tante pelli, regole per tenant",
            "Chi fa il supporto L1 (tu) e L2 (chi costruisce)",
            "Prezzo al tuo cliente vs tuo costo",
            "Contratto: responsabilità, uptime, dati",
            "Quando NON fare white-label (un solo verticale che non ripeti)",
        ],
        must=["tenant/dati", "L1/L2", "quando no"],
        scene="Identical shop windows with different colored blinds, street, no names.",
    ),
    dict(
        titolo="L’RFI del cliente grosso: cosa deve saper fare il tuo software (e come non firmare un suicidio in 40 pagine)",
        kw="rfi software come rispondere",
        kw2="gara fornitura software, requisiti cliente enterprise, scope creep, contratto sviluppo",
        descrizione="Chi risponde a gare. Vendi lucidità di perimetro + capacità full-stack.",
        angle="Non perdere / non suicidarti.",
        outline=[
            "L’RFI scritto per spaventare",
            "Cosa è requisito, cosa è desiderio, cosa è teatro",
            "Sicurezza, backup, ruoli: risposte da adulto senza overclaim",
            "Cosa NON promettere (AI, integrazioni infinite, date)",
            "Come spezzare lo scope",
            "Chi deve scrivere la risposta (non solo commerciale)",
            "Red flag nella gara",
            "Quando ritirarsi è vincere",
        ],
        must=["requisito vs teatro", "spezzare scope", "quando ritirarsi"],
        scene="A thick anonymous binder on a boardroom table, overhead light, no title.",
    ),
    dict(
        titolo="Da vendere ore a vendere un prodotto: quando il freelancer (o la piccola software house) deve smettere di fatturare giornate",
        kw="passare da consulenza a prodotto",
        kw2="productizzare servizi, smettere di vendere ore, margine software vs time material, founder developer",
        descrizione="Meta per chi è simile ad Antonio ma anche buyer di prodotto. Posiziona il passaggio.",
        angle="Modello di ricavo. Attrare chi vuole un prodotto costruito.",
        outline=[
            "Le ore hanno un tetto, il prodotto no",
            "Sintomi che è ora (stesse job, stessi flussi)",
            "Cosa productizzare senza tradire i clienti attuali",
            "UI e dati: se resti ‘script e call’, non è un prodotto",
            "Prezzo, onboarding, supporto",
            "Il primo cliente del prodotto (spesso uno vecchio)",
            "Rischi: due mestieri in parallelo",
            "90 giorni di prova del nuovo modello",
        ],
        must=["sintomi", "primo cliente", "due mestieri"],
        scene="A timesheet book closed next to a small product box, desk, no text.",
    ),
    dict(
        titolo="Il commerciale promette una feature che il software non ha: come chiudere il buco (processo + prodotto) prima che ti costi un cliente",
        kw="feature promessa non esiste",
        kw2="scope commerciale vs prodotto, customizzazione pericolosa, dire no al cliente, roadmap software",
        descrizione="Product ops. Vendi allineamento commerciale-prodotto, a volte un modulo.",
        angle="Vendite vs delivery. Dolore da software house e PMI con sw interno.",
        outline=[
            "La mail ‘sì lo facciamo’",
            "Costo di una custom per un solo cliente",
            "Processo: come si dice no / come si mette in roadmap",
            "Quando la feature è davvero il prodotto (e va costruita bene)",
            "Frontend: aspettative vs realtà",
            "Dati e casi limite che il commerciale non vede",
            "Contratto: change request",
            "Cruscotto: promesse vs backlog",
        ],
        must=["dire no", "change request", "un solo cliente"],
        scene="A handshake in the foreground, contract unsigned behind, faces unclear.",
    ),
    dict(
        titolo="Area appuntamenti + pagamenti + fascicolo: lo studio (medico, tecnico, legale) che sembra un’azienda del 1998",
        kw="software studio professionale completo",
        kw2="fascicolo cliente studio, pagamenti e agenda, portale paziente cliente, digitalizzare studio",
        descrizione="Studi. Vendi trio agenda-pagamenti-fascicolo, UX.",
        angle="Uno studio = un prodotto, non tre SaaS staccati.",
        outline=[
            "Tre tool che non si parlano",
            "Il fascicolo: documenti, consensi, storico",
            "Agenda e cassa: se non tornano, è caos",
            "Portale: il cliente che non chiama per un PDF",
            "Cosa è delicato (dati sanitari/legali) in parole da titolare",
            "Cosa può fare l’AI (bozze, classifica) e cosa no",
            "SaaS di categoria vs su misura",
            "Piano a pezzi per non fermare lo studio",
        ],
        must=["tre pezzi", "portale PDF", "piano a pezzi"],
        scene="A professional studio corridor, closed doors, brass plate unreadable.",
    ),
    dict(
        titolo="Hai i dati. Non hai le domande. Il motivo per cui le dashboard non fanno fatturare (e un analyst che costruisce prodotto sì)",
        kw="dashboard che non si usano",
        kw2="data product aziendale, domande di business, analyst che costruisce, self service bi fallisce",
        descrizione="Posiziona data analyst come product builder, non reportificio.",
        angle="Domande → prodotto dati. Vendita consulenza alta.",
        outline=[
            "Self-service BI: il mito",
            "Senza domande sono grafici",
            "Come si tirano fuori le domande (workshop)",
            "Ogni domanda ha un owner e una frequenza",
            "Dal notebook alla schermata usata",
            "LLM sui dati: pericoloso se le definizioni ballano",
            "Cosa consegnare (prodotto, non file)",
            "Segnali di fallimento a 60 giorni",
        ],
        must=["workshop domande", "owner/frequenza", "60 giorni"],
        scene="A blank projector screen in a meeting room, chairs, daylight.",
    ),
]


def dates_tue_thu(n, start=date(2026, 8, 18)):
    out = []
    d = start
    while len(out) < n:
        if d.weekday() in (1, 3):
            out.append(d)
        d += timedelta(days=1)
    return out


def main():
    sched = dates_tue_thu(len(POSTS))
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
    rows = []
    for i, p in enumerate(POSTS):
        rows.append({
            "titolo": p["titolo"],
            "keyword_principale": p["kw"],
            "keyword_secondarie": p["kw2"],
            "descrizione": p["descrizione"],
            "prompt_articolo": article_prompt(
                p["titolo"], p["kw"], p["kw2"], p["angle"], p["outline"], p["must"]
            ),
            "prompt_immagine": image_prompt(p["scene"]),
            "larghezza_immagine": IMAGE_SIZE[0],
            "altezza_immagine": IMAGE_SIZE[1],
            "data_pubblicazione": f"{sched[i].isoformat()} 7:30",
        })
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=";", quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
