# -*- coding: utf-8 -*-
"""Terzo livello: query PMI/ops (n8n, GDPR, CRM). Non è il piano clienti. Jekyll non lo monta."""
import csv
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).with_name("piano-editoriale-2026-livello3-pmi-ops.csv")

ARTICLE_RULES = """
IDENTITÀ
Scrivi in italiano come Antonio Trento, system architect e AI integrator. Sito ufficiale: https://antoniotrento.net
Il lettore NON è uno sviluppatore che clona i tuoi repo. È un titolare, un responsabile, un founder o un IT di PMI italiana che ha cercato questo titolo su Google perché ha un problema concreto (costi, privacy, caos operativo, SaaS che non parla, dipendenti che usano ChatGPT sui clienti).
Tono: diretto, acchiappa-attenzione ma onesto. Dopo il gancio, consegni sostanza. Niente clickbait vuoto.

OBIETTIVO DEL PEZZO
1) Rispondere alla query in modo che Google e il lettore restino.
2) Far capire che il problema si risolve con integrazione, automazione e AI sotto il controllo dell’azienda (dati in casa / UE), non comprando “un altro software AI”.
3) Chiudere con un CTA sobrio a https://antoniotrento.net (portfolio e biografia). Non vendere un prodotto nominato. Non fare tour dei tuoi GitHub.

LUNGHEZZA
Minimo 4500 parole, target 5000–6000. Se sei corto: secondo caso d’uso, tabella costi, “cosa si rompe”, 10 FAQ. Niente ripetizioni.

FORMATO
Markdown, niente YAML front matter. Inizia con H2, non ripetere il titolo come H1.
H2/H3 long-tail. Paragrafi corti. Elenchi. Almeno 1 tabella. Almeno 8 FAQ. Checklist pratica.
Almeno 2 blocchi concreti (procedura numerata, esempio di policy, pseudo-flusso, snippet yaml/json SOLO se serve al lettore non-dev: spiegati riga per riga).

SEO
Keyword principale nel primo paragrafo, in 2 H2, in chiusura, naturale.
Keyword secondarie: 4–6 occorrenze variate.

VIETATO
- “Nel mondo di oggi l’AI sta rivoluzionando”.
- Articoli “AI per il settore X” da enciclopedia (agri, flotte, smart city, salute pubblica).
- Inventare clienti, brand, fatturati, “l’ho fatto in Ferrari”.
- Nominare progetti portfolio (Cloudetta, KineticMCP, DataUnchain, Qwibo, Vibeissue, Shotloom, SP500 monitor, Zirelia) e repo GitHub.
- Deep dive da maintainer (governor limits Salesforce pagina per pagina, walk-forward Sharpe, FINRA vs Z.1, path da 260 caratteri).
- Promettere automazione totale senza umani.
- Default SaaS USA. Default: controllo dei dati, self-hosted o vendor UE con contratto chiaro.

OBBLIGATORIO
- Un “è per te se / non è per te se”.
- Un percorso a 30/60/90 giorni in italiano semplice.
- Stime di costo in euro (dichiarate come stime).
- Sezione “quando NON farlo”.
- 3 errori da principiante che costano soldi o dati.
"""

IMAGE_SIZE = (1536, 1024)
IMAGE_RULES = (
    "Photorealistic editorial photograph, landscape 1536x1024 pixels (3:2), "
    "no text, no letters, no watermarks, no logos, no UI screenshots, no diagrams with labels. "
    "Dark professional lighting, shallow depth of field, cinematic but documentary. "
    "Italian small-business / office / workshop atmosphere. Adult professionals only, faces optional and anonymous. "
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

OUTLINE OBBLIGATORIA (ogni punto = H2/H3, nell’ordine):
{bullets}

DEVI INCLUDERE:
{musts}

Scrivi ora l’articolo completo in italiano, 5000–6000 parole, Markdown.
""".strip()


def image_prompt(scene):
    return f"{IMAGE_RULES}{scene}"


POSTS = [
    dict(
        titolo="I tuoi dipendenti usano ChatGPT sui clienti: cosa rischi in Italia e come dargli un’alternativa interna (senza divieti inutili)",
        kw="chatgpt dati aziendali gdpr",
        kw2="chatgpt in azienda italia, privacy dipendenti llm, alternativa chatgpt interna, shadow it openai",
        descrizione="Query da titolare spaventato: i commerciali incollano offerte e anagrafiche su ChatGPT. Rischi GDPR, policy, alternativa interna usabile, 30 giorni.",
        angle="Paura reale + soluzione usabile. Non un trattato legale. Non un tutorial Ollama da sysadmin.",
        outline=[
            "Lo scenario: il commerciale, l’offerta, il tasto incolla",
            "Cosa esce davvero dall’azienda (e perché “è solo un riassunto” non salva)",
            "GDPR in italiano semplice: titolare, responsabile, trasferimento",
            "Il divieto che nessuno rispetta (Shadow IT)",
            "Alternativa interna: chat in azienda, regole su cosa si può incollare",
            "Policy di 1 pagina che i dipendenti firmano",
            "Piano 30 giorni: inventory, blocco guidato, alternativa, audit leggero",
            "Quando serve un DPO e quando basta ordine interno",
        ],
        must=["tabella dati che non devono mai finire in un chatbot cloud", "bozza policy", "stima costi alternativa vs multa/reputazione"],
        scene="Open-plan Italian office, a worker hiding a laptop screen with a hand, documentary, no readable text.",
    ),
    dict(
        titolo="Zapier o Make a 400€ al mese: quando n8n self-hosted conviene (e quando stai solo spostando il problema sull’IT)",
        kw="n8n vs zapier vs make costi",
        kw2="n8n self hosted pmi, alternativa zapier italia, automazione no-code costi, make.com prezzo",
        descrizione="Confronto onesto dei tre: prezzo, lock-in, chi mantiene, privacy. Per PMI che pagano l’abbonamento e cercano “n8n italia”.",
        angle="Decision post da Google Ads mentale. Numeri. Niente compose da 40 righe.",
        outline=[
            "La bolletta no-code che cresce con i task",
            "Cosa stai comprando: connettori, run, persone",
            "Zapier/Make: veloci, cari, dati fuori",
            "n8n self-hosted: controllo, manutenzione, curva",
            "Chi lo tiene in vita se non hai un IT",
            "Tabella TCO 12 mesi su 3 scenari (piccola, media, picchi)",
            "Migrazione: da dove si parte senza spezzare i flow",
            "Quando restare su Make/Zapier senza vergogna",
        ],
        must=["tabella TCO", "lista 10 automazioni tipiche PMI", "criterio “non è per te se”"],
        scene="A receipt spike next to a small quiet home server, Italian SME back office, warm light.",
    ),
    dict(
        titolo="Perché il chatbot sul sito non porta appuntamenti (e cosa mettere al posto delle FAQ infinite)",
        kw="chatbot sito web non converte",
        kw2="chatbot aziendale lead, widget chat wordpress, prenotazione appuntamenti ai, alternativa chatbot faq",
        descrizione="Intent: il sito ha un bot e zero call. Perché fallisce, metriche, flusso verso calendario/WhatsApp/umano, quando un agente ha senso.",
        angle="Conversione, non NLP. Uccidi il widget pappagallo.",
        outline=[
            "Il bot che dice “ciao come posso aiutarti” e uccide il lead",
            "Cosa cerca chi arriva sul sito di un professionista/PMI",
            "FAQ vs prenotazione vs preventivo: tre mestieri diversi",
            "Metriche: avvio chat ≠ appuntamento in calendario",
            "Flussi che funzionano: 4 domande, slot, conferma umana",
            "WhatsApp, form, telefono: quando battono il widget",
            "Se usi l’AI: confini, fallback, orari",
            "Test A/B povero ma onesto in 14 giorni",
        ],
        must=["funnel in tabella", "script di 4 domande", "errori di copy del bot"],
        scene="An empty reception desk with a ringing phone and a dark computer, late afternoon, no logos.",
    ),
    dict(
        titolo="ChatGPT in azienda è legale in Italia nel 2026? Guida pratica per titolari (non da talk show)",
        kw="chatgpt legale in azienda italia",
        kw2="gdpr chatgpt 2026, ai act pmi italia, uso openai dipendenti, dpa chatgpt",
        descrizione="Query informazionale fortissima: legalità, DPA, AI Act, cosa scrivere nel registro, cosa vietare. Checklist stampabile.",
        angle="Chiarezza da “è legale sì/no” a “sotto quali condizioni”. Disclaimer: non è parere legale.",
        outline=[
            "La domanda sbagliata: “è legale?” vs “per quali dati?”",
            "Account personale vs account aziendale vs API",
            "Trasferimento extra-UE e DPA: cosa leggere davvero",
            "AI Act: uso interno vs sistemi che decidono sulle persone",
            "Registro dei trattamenti e informativa dipendenti",
            "Casi: marketing copy vs anagrafiche vs CV vs codice",
            "Checklist da stampare per il commercialista/DPO",
            "Alternative se la risposta è no",
        ],
        must=["checklist stampabile", "matrice sì/no per tipo di dato", "disclaimer non-parere"],
        scene="Italian small meeting room with a closed laptop and a printed checklist face-down, daylight.",
    ),
    dict(
        titolo="Come fare un ChatGPT interno per la PMI senza mandare i documenti in America",
        kw="chatgpt interno azienda self hosted",
        kw2="gpt aziendale privato, llm locale pmi, alternativa copilot 365, chat interna documenti",
        descrizione="Job-to-be-done: “voglio ChatGPT ma sui nostri file”. Architettura a blocchi per non-dev, costi, cosa può e non può, 60 giorni.",
        angle="Prodotto interno, linguaggio titolare. GPU solo come ordine di grandezza, non recensione vLLM.",
        outline=[
            "Cosa intendono i dipendenti per “un ChatGPT nostro”",
            "Due strati: chiacchiere vs documenti aziendali",
            "Dove stanno i file (NAS, Drive, gestionale) e chi li vede",
            "Cloud UE con contratto vs macchina in ufficio/VPS Italia",
            "Cosa sa fare bene (bozze, riassunti, Q&A citata) e cosa no (pareri, numeri da fattura senza fonte)",
            "Accessi: non tutti vedono gli stipendi",
            "Costi: 5 / 25 / 80 persone (stime)",
            "Piano 60 giorni e change management (il divieto non basta)",
        ],
        must=["architettura a scatole per non-tecnici", "tabella costi", "10 regole di utilizzo"],
        scene="A locked cabinet with two small PCs in a back office, Italian SME, no brand logos.",
    ),
    dict(
        titolo="AI che legge le fatture: 7 casi in cui sbaglia l’IVA (e come non farti fregare dal “99% di accuratezza”)",
        kw="ai lettura fatture errori",
        kw2="ocr fatture elettroniche, estrazione dati pdf fattura, intelligenza artificiale contabilità, fattura xml vs pdf",
        descrizione="Intent commerciale forte. Smonta il marketing OCR. XML vs PDF, errori IVA, come misurare, human review.",
        angle="Soldi e IVA, non vision model. Attrarre chi cerca automazione contabile.",
        outline=[
            "Il vendor che promette il 99%",
            "Fattura elettronica: il XML c’è già, il PDF è il piano B",
            "7 errori classici (split payment, reverse, bollo, arrotondamenti, fornitore omonimo, estero, allegato sbagliato)",
            "Cosa deve fare l’umano e sopra quale soglia",
            "Come misurare campo per campo (l’IVA vale più dell’indirizzo)",
            "Integrazione col gestionale: non un altro silos",
            "Costi: ore dell’amministrativo vs licenza vs errori",
            "Quando NON automatizzare (volume basso, caos totale)",
        ],
        must=["tabella 7 errori", "definizione onesta di accuratezza", "flusso XML-first spiegato a un amministrativo"],
        scene="A desk calculator and a stack of paper invoices out of focus, Italian accounting office.",
    ),
    dict(
        titolo="Automazione per PMI senza ufficio IT: da dove si parte in 30 giorni (senza comprare 4 software nuovi)",
        kw="automazione processi pmi da dove iniziare",
        kw2="digitalizzazione pmi italia, automazione senza it, workflow aziendali piccoli, n8n pmi",
        descrizione="Guida d’ingresso per chi cerca “automazione PMI”. Inventario processi, 3 quick win, cosa non toccare, chi coinvolgere.",
        angle="Onboarding del target. Sei la voce che mette ordine.",
        outline=[
            "Automazione non è “mettere l’AI su tutto”",
            "Mappa di una settimana: dove va il tempo (fatture, email, copy-paste, reminder)",
            "3 quick win tipici e 3 trappole",
            "Strumenti: fogli, gestionale, mail, calendario — collega prima di sostituire",
            "Chi è il referente interno (anche part-time)",
            "Piano 30 giorni settimana per settimana",
            "Budget onesto (stime)",
            "Come capire dopo 30 giorni se ha funzionato",
        ],
        must=["canvas inventario processi", "piano 30 giorni", "lista trappole software"],
        scene="A small Italian workshop office with a paper calendar and a single laptop, morning light.",
    ),
    dict(
        titolo="Salesforce è già caro: 4 automazioni sul CRM che servono prima di comprare Einstein (e il rischio di incollare i lead su ChatGPT)",
        kw="automazione salesforce pmi",
        kw2="salesforce einstein costi, crm ai italia, integrare salesforce senza einstein, lead scoring pmi",
        descrizione="Chi ha Salesforce e cerca AI. Automazioni deterministiche vs LLM sulle note. Privacy. Costo Einstein vs integrazione.",
        angle="CRM job, non MCP protocol. Attrarre chi paga Salesforce.",
        outline=[
            "Cosa la gente cerca: “AI su Salesforce”",
            "Einstein e add-on: cosa stai comprando",
            "4 automazioni prima dell’LLM (routing, reminder, igiene dati, sync)",
            "Dove l’LLM serve: note sporche, email, classificazione",
            "Perché incollare l’opportunity su ChatGPT è un leak",
            "Permessi: l’automazione non è l’admin di tutti",
            "Costi a confronto (stime)",
            "Quando il CRM è troppo caotico per qualsiasi AI",
        ],
        must=["tabella 4 automazioni vs Einstein", "regola dati che non escono dal CRM", "segnali di igiene dati"],
        scene="A sales desk with a blurred CRM-looking monitor, no UI text, Italian office.",
    ),
    dict(
        titolo="WhatsApp Business + AI per prenotazioni: come non regalare la rubrica dei clienti a un SaaS americano",
        kw="whatsapp business ai prenotazioni",
        kw2="chatbot whatsapp pmi, prenotazioni automatiche whatsapp, privacy whatsapp api, assistente whatsapp italia",
        descrizione="Query calda: bot WhatsApp. Official API vs non ufficiali, privacy, flusso booking, fallback umano, costi Meta.",
        angle="Canale che i clienti già usano. Sovranità sui contatti.",
        outline=[
            "Perché tutti vogliono il bot su WhatsApp",
            "API ufficiale vs tool grigi (ban, ToS)",
            "Cosa può fare: orari, slot, FAQ, pagamento? (confini)",
            "Rubrica e GDPR: chi è titolare dei numeri",
            "Flusso prenotazione con conferma umana",
            "Orari, ferie, handover al telefono",
            "Costi Meta + integratore vs segretaria",
            "Quando un form o una telefonata vincono",
        ],
        must=["flusso di prenotazione", "rischi account ban", "checklist privacy numeri"],
        scene="A smartphone face-down next to an appointment book, café-office, no screen content.",
    ),
    dict(
        titolo="9 cose che un commerciale non deve mai incollare su ChatGPT (con esempi di danni veri, non da film)",
        kw="cosa non incollare su chatgpt lavoro",
        kw2="chatgpt dati clienti, riservatezza offerte, nda e llm, formazione dipendenti ai",
        descrizione="Pezzo virale/formazione interna. Lista concreta, esempi, come addestrare il team in 45 minuti.",
        angle="Shareable + utile in azienda. Acchiappa click onesto.",
        outline=[
            "Perché “tanto lo usano tutti” non è una policy",
            "9 categorie: listini, NDA, CV, codice, password, sanitari, minori, strategie, dati fiscali",
            "Danno: fuga, contratto, reputazione, vantaggio al competitor nel modello",
            "Cosa SI può chiedere (testo anonimizzato, struttura, tono)",
            "Come anonimizzare in 2 minuti (e quando non basta)",
            "Workshop 45 minuti per il team commerciale",
            "Cosa mettere al posto: strumento interno o vendor con DPA",
            "Sanzioni interne proporzionate (senza teatro)",
        ],
        must=["tabella 9 cose", "script workshop", "esempio di anonimizzazione"],
        scene="A black marker redacting a document, macro, no readable words.",
    ),
    dict(
        titolo="Microsoft 365 vs stack self-hosted: quanto spendi in 3 anni (licenze, lock-in, e l’uscita che nessuno calcola)",
        kw="microsoft 365 vs self hosted costi",
        kw2="costo microsoft 365 pmi, vendor lock-in office 365, alternativa self hosted email, nextcloud vs sharepoint",
        descrizione="Intent economica. TCO 3 anni, dipendenza, Copilot che alza il prezzo, offboarding. Non guerra ideologica.",
        angle="CFO/titolare. Numeri e uscita.",
        outline=[
            "La licenza che “è solo 12 euro” per 20 persone",
            "Cosa è incluso e cosa diventa add-on (Copilot, storage, backup)",
            "Costo nascosto: tempo, integrazioni, “tanto è già lì”",
            "Self-hosted: email, file, identità — pezzi, non un mostro unico",
            "Uscita da 365: quanto costa davvero (mailbox, sharepoint, teams)",
            "Tabella 10 / 25 / 80 utenti su 36 mesi (stime)",
            "Ibrido: tieni 365, tira fuori i dati critici",
            "Quando 365 resta la scelta giusta",
        ],
        must=["tabella TCO", "elenco add-on", "criteri ibrido"],
        scene="A pile of identical software boxes blurred, next to a small NAS, office shelf.",
    ),
    dict(
        titolo="Knowledge base interna che i dipendenti usano davvero (non un Confluence aperto nel 2019 e mai più)",
        kw="knowledge base aziendale interna",
        kw2="wiki aziendale che funziona, ai su documenti interni, ricerca procedure pmi, onboarding knowledge base",
        descrizione="Perché le wiki muoiono, come farle vivere, ricerca, AI che cita la procedura, ownership.",
        angle="Intra-azienda, SEO “knowledge base”.",
        outline=[
            "La wiki fantasma e il WhatsApp del collega",
            "Cosa cercare: procedure, listini interni, how-to, non “tutto”",
            "Ownership: ogni pagina ha un padrone e una data",
            "Ricerca prima dell’AI (se non si trova, l’AI inventa)",
            "Q&A con citazione obbligatoria del documento",
            "Permessi: HR ≠ commerciale ≠ produzione",
            "Rituale mensile di pulizia (30 minuti)",
            "Metriche: ricerche a vuoto, ticket ripetuti",
        ],
        must=["template di una procedura", "regole di ownership", "metriche"],
        scene="Empty office shelves with a few labeled binders, labels unreadable, quiet.",
    ),
    dict(
        titolo="PEC, fatture e scadenze: come automatizzare uno studio (commercialista, consulente, agenzia) senza sostituire il professionista",
        kw="automazione studio commercialista pec",
        kw2="automazione studio professionale, pec automatica, scadenze fiscali software, ai per commercialisti",
        descrizione="Verticale JOB studio, non “AI per il legale”. Smistamento, reminder, dossier, cosa non automatizzare (firme, pareri).",
        angle="Target studi. Fiducia + automazione dei bordi.",
        outline=[
            "Lo studio annega in PEC e PDF, non in “mancanza di AI”",
            "Cosa si può smistare (fatture, scadenze, richieste ripetute)",
            "Cosa non si tocca: parere, firma, SPID, responsabilità",
            "Flusso: arrivo → classifica → cartella → reminder → umano",
            "Clienti e riservatezza",
            "Strumenti: gestionale dello studio prima di un chatbot",
            "Costi vs una segretaria part-time (stime oneste)",
            "Piano 60 giorni per uno studio da 3–10 persone",
        ],
        must=["matrice automabile/non", "flusso PEC", "stima tempi"],
        scene="A professional Italian studio waiting room, empty chairs, brass lamp, no diplomas readable.",
    ),
    dict(
        titolo="AI Act 2026 per la PMI italiana: la checklist da stampare (alto rischio o stai solo riassumendo le email?)",
        kw="ai act pmi italia checklist",
        kw2="regolamento ai unione europea aziende, obblighi ai 2026, chatbot trasparenza, titolare uso ai",
        descrizione="Query normativa. Albero sì/no, obblighi minimi, trasparenza bot, cosa fare lunedì. Disclaimer.",
        angle="Traffico da paura normativa, risposta operativa.",
        outline=[
            "Cosa è in vigore per chi USA i sistemi (non per chi li addestra a Mountain View)",
            "Alto rischio: esempi PMI (HR screening, credito) vs inbox",
            "Bot che parla al cliente: obblighi di dire che è una macchina",
            "Documenti minimi (registro usi, istruzioni, responsabile)",
            "Fornitori: cosa chiedere per iscritto",
            "Checklist stampabile in 12 punti",
            "Cosa succede se ignori (prima le lettere, poi le sanzioni — ordini di grandezza)",
            "Quando farti seguire da un legale",
        ],
        must=["albero decisionale", "checklist 12 punti", "disclaimer"],
        scene="A printer tray with a face-down document, EU-blue ambient light, no readable text.",
    ),
    dict(
        titolo="Trascrivere le riunioni senza mandarle sul cloud: quando serve, quanto costa, e il consenso che tutti saltano",
        kw="trascrizione riunioni privacy",
        kw2="trascrivere meeting senza cloud, whisper aziendale, verbale assemblea ai, gdpr registrazione audio",
        descrizione="Intent: meeting notes + privacy. Consenso, CdA, costi cloud vs locale, riassunto che allucina delibere.",
        angle="Ufficio direzione. Non benchmark ASR.",
        outline=[
            "Perché tutti vogliono il verbale automatico",
            "Consenso e registrazione in Italia (principio, non sentenza)",
            "Riunione commerciale vs CdA: due pesi",
            "Cloud (Otter, Whisper API, Meet) vs locale",
            "Il riassunto che inventa una decisione",
            "Flusso: audio → testo → bozza → approvazione umano",
            "Costi per 10 ore/mese (stime)",
            "Quando il taccuino vince",
        ],
        must=["policy consenso", "flusso approvazione verbale", "tabella costi"],
        scene="Empty boardroom table, one analog recorder, chairs pushed in, muted tones.",
    ),
    dict(
        titolo="Assistente vocale al posto del centralino: latenza, GDPR e quando è solo fuffa da vendor",
        kw="assistente vocale aziendale centralino",
        kw2="centralino ai italia, voicebot prenotazioni, ivr intelligente, segreteria telefonica ai",
        descrizione="Chi cerca di sostituire la segreteria. Latenza che fa riagganciare, audio in USA, booking, fallback.",
        angle="Telefono PMI. Esperienza utente + privacy.",
        outline=[
            "Il silenzio di 2 secondi e il cliente che riaggancia",
            "Cosa fa un centralino “furbo”: orari, trasferimento, prenotazione, FAQ",
            "Audio: dove va la voce, quanto resta, chi la sente",
            "Script vs “agente che improvvisa”",
            "Handover all’umano senza far ripetere tutto",
            "Settori dove è pericoloso (salute, legale, minori) — cenni, non enciclopedia",
            "Costi vs segreteria part-time",
            "MVP onesto in 45 giorni",
        ],
        must=["budget di latenza in parole povere", "checklist privacy chiamata", "criteri MVP"],
        scene="Vintage telephone on a modern reception desk, side light, no brand.",
    ),
    dict(
        titolo="Come estrarre dati dai PDF aziendali senza un software da 20.000 euro (e senza fidarti del “carica su questa AI”)",
        kw="estrarre dati da pdf aziendale",
        kw2="ai pdf documenti, ocr documenti pmi, automazione data entry, lettura contratti pdf",
        descrizione="Job: data entry da PDF. Cloud upload vs interno, tipi di PDF, human review, integrazione Excel/gestionale.",
        angle="Dolore universale data entry.",
        outline=[
            "Il PDF è un’immagine con le scarpe buone",
            "Tre tipi: nativo, scansito, misto",
            "Perché caricare 8.000 fatture su un sito AI è una pessima idea",
            "Cosa estrarre: campi, non “capire il documento”",
            "Validazione (numeri, date, partite IVA) prima del gestionale",
            "Coda umana sui dubbi",
            "Collegamento a Excel/ERP",
            "Quando il volume non paga l’automazione",
        ],
        must=["matrice tipi PDF", "regola no-upload di massa", "flusso campi+validazione"],
        scene="A document feeder scanner with blank paper, cool metal office.",
    ),
    dict(
        titolo="n8n per chi non programma: cosa puoi fare da solo e quando ti serve un integratore (lista onesta)",
        kw="n8n per principianti pmi",
        kw2="imparare n8n italiano, automazione no code, n8n tutorial azienda, quando assumere integratore",
        descrizione="Intent tutorial + decisione make-or-buy. Limiti del fai-da-te, template, quando chiamare qualcuno.",
        angle="Educazione che converte. Onesto sui limiti.",
        outline=[
            "n8n non è Magia: è Lego con i cavi",
            "5 automazioni che un non-dev porta a casa",
            "5 automazioni che sembrano facili e non lo sono (auth, pec, pdf, errori, idempotenza)",
            "Self-hosted vs cloud n8n: privacy e manutenzione",
            "Come non trasformare n8n in spaghetti",
            "Segnali che ti serve un integratore",
            "Come briefare (obiettivo, sistemi, volume, orari)",
            "Errori da corso YouTube in produzione",
        ],
        must=["due liste da 5", "template brief", "segnali make-or-buy"],
        scene="Colorful cable spaghetti on a desk, documentary, no screen text.",
    ),
    dict(
        titolo="Ransomware e backup per PMI: lo stack minimo che un titolare capisce (prima che sia tardi)",
        kw="backup ransomware pmi",
        kw2="backup 3-2-1 azienda, restore file pmi, nas backup, disaster recovery piccola impresa",
        descrizione="Intent paura alta, evergreen. 3-2-1 spiegato, test restore, email, gestionale, “il cloud di Microsoft non è backup”.",
        angle="Fiducia. Poi puoi parlare di automazione.",
        outline=[
            "Il backup che non è mai stato provato",
            "3-2-1 in italiano",
            "365/Google Drive non sono un backup",
            "Cosa salvare: file, mail, database gestionale, password",
            "Il drill: restore su un PC vuoto",
            "Ransomware: disconnettere, non pagare come piano A",
            "Costi minimi vs fermo di una settimana",
            "Checklist mensile da 20 minuti",
        ],
        must=["checklist mensile", "elenco cosa salvare", "stima fermo"],
        scene="A closed fireproof box in a closet, documentary photography.",
    ),
    dict(
        titolo="Gestionale, e-commerce e fatture che non si parlano: l’integrazione che fa risparmiare più di qualunque chatbot",
        kw="integrazione gestionale ecommerce fatture",
        kw2="sincronizzare magazzino ecommerce, fatturazione elettronica ecommerce, integrazione erp pmi, doppia digitazione",
        descrizione="Dolore classico PMI. Doppia digitazione, giacenze, fatture. Integrazione prima dell’AI.",
        angle="Soldi operativi. Target e-commerce+ERP.",
        outline=[
            "Il costo della doppia digitazione (ore e errori di giacenza)",
            "Mappa: sito, magazzino, gestionale, SDI",
            "Cosa sincronizzare per primo (SKU, prezzi, ordini, anagrafiche)",
            "Errori: ordine doppio, reso, IVA, corriere",
            "AI: dove entra DOPO l’integrazione (classificare, non “essere l’ERP”)",
            "Make/n8n/API del gestionale: criteri",
            "Piano a scaglioni",
            "KPI dopo 60 giorni",
        ],
        must=["mappa sistemi", "ordine di priorità sync", "KPI"],
        scene="Warehouse shelf blurred behind a small office desk, Italian SME.",
    ),
    dict(
        titolo="Quanto costa un agente AI in produzione (non l’abbonamento ChatGPT Plus da 20 dollari)",
        kw="costo agente ai azienda",
        kw2="prezzo automazione ai pmi, costo token openai aziendale, tco chatbot interno, quanto costa integratore ai",
        descrizione="Query prezzo. Scomponi: disegno, integrazione, token, errori, manutenzione. Range per 3 taglie.",
        angle="Intento commerciale diretto. Trasparenza.",
        outline=[
            "Plus da 20$ non è un agente",
            "Voci di costo: analisi, connettori, UI, modelli, persone, incidenti",
            "Tre taglie: classifica email / prenotazioni / agente che scrive sul CRM",
            "Token e scarti (retry, umani che correggono)",
            "Manutenzione annuale: il pezzo che i preventivi “dimenticano”",
            "Range in euro (stime, forchette larghe)",
            "Come leggere un preventivo (red flag)",
            "ROI: ore, errori, non “innovazione”",
        ],
        must=["tabella 3 taglie", "red flag preventivo", "esempio ROI semplice"],
        scene="A desk with scattered euro coins out of focus and a notebook, no amounts visible.",
    ),
    dict(
        titolo="Fine-tuning o “carico i PDF in chat”? Perché le FAQ aziendali non si addestrano (e cosa fare invece)",
        kw="fine tuning vs rag documenti aziendali",
        kw2="addestrare chatgpt sui documenti, faq aziendali ai, retrieval documenti, custom gpt vs rag",
        descrizione="Mito Custom GPT / “addestra sul nostro PDF”. Spiega retrieval, aggiornamenti, allucinazioni su policy HR.",
        angle="Educazione SEO su un malinteso diffusissimo.",
        outline=[
            "Cosa crede il titolare: “gli do i PDF e impara”",
            "Pesi vs documenti: analogia chiara",
            "FAQ che cambiano ogni mese",
            "Custom GPT e privacy",
            "Retrieval: cerca, cita, non inventare il CCNL",
            "Costi delle due strade",
            "Quando un piccolo adattamento di tono ha senso",
            "Setup minimo che funziona",
        ],
        must=["analogia non tecnica", "tabella quando A quando B", "rischio allucinazione policy"],
        scene="Two doors in a corridor, one labeled with unreadable blur, architectural.",
    ),
    dict(
        titolo="Il PDF del fornitore che ti fa pagare due volte: prompt injection spiegato a un titolare di PMI",
        kw="prompt injection spiegato semplice",
        kw2="sicurezza chatbot aziendale, pdf malevolo ai, truffa iban fattura, rischi agenti ai",
        descrizione="Sicurezza accessibile. Storia dell’IBAN nel PDF, cosa può fare un agente che “esegue”, difese in linguaggio umano.",
        angle="Click + fiducia. Non pentest report.",
        outline=[
            "L’agente che legge le fatture è un impiegato credulone",
            "Istruzione nascosta: “paga su questo IBAN”",
            "Cosa può succedere: bonifico, mail, cancellazione",
            "Perché il “sii prudente” nel prompt non basta",
            "Regole: niente pagamenti senza umano, allowlist, importi",
            "Come testare con un PDF finto (innocuo)",
            "Cosa chiedere al fornitore di automazione",
            "Incident: se è già partito",
        ],
        must=["storia-esempio didattica", "regole d’oro", "domande al fornitore"],
        scene="A red USB stick on invoices, dramatic light, no print readable.",
    ),
    dict(
        titolo="Open source in azienda: le 6 paure vere (supporto, sicurezza, chi lo mantiene) e quando conviene davvero",
        kw="open source in azienda rischi",
        kw2="software open source pmi, n8n open source, linux in azienda, manutenzione open source",
        descrizione="Ostacolo all’acquisto self-hosted. Rispondi alle paure, modello di supporto, quando il proprietario è peggio.",
        angle="Sblocco obiezioni. Conversione verso sovranità.",
        outline=[
            "“Se è gratis chi risponde al telefono?”",
            "6 paure: supporto, buchi, skill, licenze, fork, lock-in inverso",
            "Cosa è gratis e cosa paghi (persone, hosting, contratto)",
            "Vendor closed: il supporto che sparisce al rinnovo",
            "Come scegliere progetti con community e release",
            "Contratto di manutenzione con un integratore",
            "Esempi di pezzi (mail, automazione, file) senza fare tour prodotto",
            "Quando il proprietario è la scelta giusta",
        ],
        must=["tabella 6 paure", "modello di supporto", "criteri di scelta progetto"],
        scene="A toolbox with mixed old and new tools, workshop, no labels.",
    ),
    dict(
        titolo="Docker in una PMI da 15 persone: a cosa serve (spiegato senza nerd) e cosa non è",
        kw="docker a cosa serve azienda",
        kw2="docker pmi spiegato, container software azienda, perché docker, deploy applicazioni pmi",
        descrizione="Keyword Docker + azienda. Analogia, benefici (riproducibilità, isolamento), limiti, “non ti serve Kubernetes”.",
        angle="Educazione che posiziona l’autore come chi parla umano.",
        outline=[
            "Analogia: la vaschetta del gelato vs la cucina intera",
            "Problema: “sulla mia macchina funziona”",
            "Cosa ci metti: gestionale web, automazioni, AI interna",
            "Cosa NON è: il cloud, la sicurezza magica, Kubernetes",
            "Chi lo gestisce in 15 persone",
            "Backup e aggiornamenti in parole povere",
            "Costi VPS vs PC sotto la scrivania",
            "Quando è overkill",
        ],
        must=["analogia lunga e chiara", "quando sì quando no", "rischio PC sotto la scrivania"],
        scene="Stacked lunchboxes in a fridge, conceptual still life, no brands.",
    ),
    dict(
        titolo="Email che si smistano da sole: fatture, reclami, ordini (senza Gmail Gemini e senza dare la casella a un SaaS)",
        kw="classificare email aziendali automatico",
        kw2="smistamento pec e mail, automazione inbox pmi, ai email fatture, regole posta aziendale",
        descrizione="Inbox hell. Regole vs AI, PEC, cartelle, privacy, IMAP vs Google.",
        angle="Dolore quotidiano. Alto volume di ricerca.",
        outline=[
            "La casella che è il vero ERP dell’azienda",
            "Regole fisse vs modello che legge il testo",
            "Cartelle che un umano capisce",
            "Fatture, reclami, ordini, pec legale: priorità diverse",
            "Perché Gemini/Copilot sulla posta aziendale è un tema dati",
            "IMAP in casa vs Google Workspace",
            "Errori: mail nello spam sbagliato, doppia gestione",
            "KPI: tempo di prima risposta, mail arretrate",
        ],
        must=["tassonomia cartelle", "confronto regole vs AI", "KPI"],
        scene="Physical inbox tray overflowing, paper unreadable, office.",
    ),
    dict(
        titolo="Preventivi automatici con l’AI: il punto esatto in cui sbaglia i prezzi (e ti brucia il margine)",
        kw="preventivi automatici ai",
        kw2="ai preventivi aziendali, configuratore prezzi, chatbot preventivo, errore listino llm",
        descrizione="Chi vuole il bot che fa preventivi. Listini, eccezioni, approvazione, allucinazione prezzi.",
        angle="Soldi. Titolare commerciale.",
        outline=[
            "Il sogno: “il bot manda il preventivo da solo”",
            "Listino, sconti, eccezioni, urgenza: dove l’AI inventa",
            "Fonte di verità: ERP/foglio, non la memoria del modello",
            "Soglia: sotto X euro auto, sopra umano",
            "Tono del preventivo vs numeri",
            "Tracciabilità: quale listino, quale data",
            "Integrazione CRM",
            "Quando un configuratore classico batte l’LLM",
        ],
        must=["regola soglia", "esempio di errore di margine", "fonte di verità"],
        scene="A price gun and a blank quote folder, warehouse office.",
    ),
    dict(
        titolo="Shadow IT: Slack + ChatGPT + fogli Google. Come chiuderlo senza divieti che nessuno rispetta",
        kw="shadow it chatgpt azienda",
        kw2="dipendenti usano ai di nascosto, governance ai pmi, strumenti non autorizzati, rischio dati slack",
        descrizione="Governance. Inventario, alternative, comunicazione, eccezioni. Non polizia.",
        angle="Management. Condivide su LinkedIn.",
        outline=[
            "Perché nasce lo Shadow IT (il tool ufficiale è lento o assente)",
            "Mappa: messaggi, file, AI, fogli",
            "Rischi reali vs paranoia",
            "Inventario senza caccia alle streghe",
            "Offrire un binario ufficiale più comodo",
            "Eccezioni documentate",
            "Formazione 45 minuti",
            "Indicatori: ticket, usi, incidenti",
        ],
        must=["script comunicazione interna", "matrice rischi", "piano 45 minuti"],
        scene="Sticky notes covering a monitor, office chaos, writing unreadable.",
    ),
    dict(
        titolo="Come scegliere chi ti integra l’AI: 11 red flag (e 7 domande da fare al primo call)",
        kw="come scegliere integratore ai",
        kw2="consulente intelligenza artificiale pmi, preventivo automazione, system integrator ai, fuffa ai vendor",
        descrizione="Intent commerciale altissimo. Insegna a comprare. Posiziona Antonio come anti-fuffa.",
        angle="Buyer’s guide. Conversione naturale.",
        outline=[
            "Il mercato pieno di demo ChatGPT incollate",
            "11 red flag (nessun confine dati, niente manutenzione, “AI proprietaria” magica, lock-in, ecc.)",
            "7 domande al primo call",
            "Come leggere un SOW",
            "Proprietà di codice, prompt, workflow",
            "Cosa deve restare tuo se cambi fornitore",
            "Pilot da 30 giorni vs progetto da 80k subito",
            "Come usare questa guida (anche con altri, non solo con me)",
        ],
        must=["lista 11 + 7", "cosa deve restare tuo", "struttura pilot"],
        scene="Two empty chairs across a table, negotiation room, daylight.",
    ),
    dict(
        titolo="Dati in Italia o cloud USA: guida pratica per decidere (senza ideologia e senza “tanto è tutto cloud”)",
        kw="dati in italia vs cloud usa",
        kw2="server in italia pmi, sovranità dati, gdpr trasferimento extra ue, vps italia vs aws",
        descrizione="Decisione infrastrutturale in linguaggio titolare. Latenza, legge, costi, ibrido.",
        angle="Sovranità come scelta, keyword forti.",
        outline=[
            "Cosa significa “i dati stanno in America” in pratica",
            "Email, file, CRM, backup, AI: cinque risposte diverse",
            "GDPR e trasferimenti: versione operativa",
            "VPS Italia / UE vs hyperscaler",
            "Ibrido intelligente",
            "Costi e competenze",
            "Cosa chiedere per iscritto al vendor",
            "Tabella decisionale",
        ],
        must=["tabella per tipo di dato", "domande al vendor", "scenario ibrido"],
        scene="A map of Europe on a wall out of focus, office, no country names sharp.",
    ),
    dict(
        titolo="Copilot sui documenti di lavoro: cosa finisce in Microsoft e cosa puoi (davvero) bloccare",
        kw="microsoft copilot privacy documenti",
        kw2="copilot 365 dati aziendali, disattivare copilot, rischio copilot pmi, training dati microsoft",
        descrizione="Chi ha 365 e paura di Copilot. Impostazioni, tenant, cosa non è un opt-out. Alternative.",
        angle="Query di prodotto Microsoft, risposta da integratore indipendente.",
        outline=[
            "Copilot non è “un ChatGPT a lato”: è dentro Word/Excel/Teams",
            "Cosa può vedere (permessi file = permessi modello, in soldoni)",
            "Cosa si può disattivare a livello tenant (e cosa resta)",
            "Il mito “non usano i nostri dati per addestrare” — come leggerlo",
            "Casi: legale interno, HR, listini",
            "Formazione: quando NON premere il bottone",
            "Alternative per chi vuole AI ma non su tutto il tenant",
            "Checklist admin + titolare",
        ],
        must=["checklist", "casi sì/no", "nota che le UI Microsoft cambiano — principi non click-by-click eterno"],
        scene="A Microsoft-like office window light on a closed laptop, no logos.",
    ),
    dict(
        titolo="Onboarding dipendenti in PMI: account, accessi, policy AI — la checklist (e 4 automazioni) senza un HR-tech da 50.000€",
        kw="onboarding dipendenti pmi checklist",
        kw2="automazione onboarding, accessi nuovi assunti, policy ai dipendenti, offboarding pmi",
        descrizione="HR piccolo. Checklist, offboarding (più importante), automazioni mail/account.",
        angle="HR operativo. Include policy AI come gancio attuale.",
        outline=[
            "L’assunto senza email e con tutti i drive aperti",
            "Checklist giorno 0 / 7 / 30",
            "Offboarding: il buco di sicurezza n.1",
            "4 automazioni: account, cartelle, welcome, reminder",
            "Policy AI nel pacchetto di benvenuto",
            "Chi approva gli accessi",
            "Strumenti che hai già (Google/365/gestionale)",
            "Errori: accessi eterni, shared password",
        ],
        must=["checklist on/off", "4 automazioni", "nota sicurezza"],
        scene="A new empty desk with a plant and an unopened laptop, office.",
    ),
    dict(
        titolo="5 automazioni su magazzino e ordini prima di comprare un WMS “con l’AI”",
        kw="automazione magazzino pmi",
        kw2="gestione ordini ecommerce, sottoscorta automatico, integrazione corriere gestionale, wms costi",
        descrizione="Logistica piccola. Quick win prima del software pesante.",
        angle="Soldi e errori di picking, non robotica.",
        outline=[
            "Il WMS da fiera che non ti serve (ancora)",
            "5 automazioni: sottoscorta, tracking, etichette, reso, alert rottura",
            "Dati sporchi: SKU doppi, barcode",
            "AI: previsione domanda solo con storico pulito",
            "Integrazione corriere e e-commerce",
            "Costi WMS vs n8n+gestionale",
            "KPI: stockout, tempo ordine",
            "Quando il WMS diventa obbligatorio",
        ],
        must=["lista 5", "KPI", "criterio WMS"],
        scene="Small warehouse aisle, cardboard boxes unbranded, documentary.",
    ),
    dict(
        titolo="Il sito ha visite e zero lead: form, WhatsApp o agente? Come scegliere il contatto (senza un altro widget)",
        kw="sito visite zero lead",
        kw2="convertire traffico sito pmi, whatsapp o form contatto, call to action sito, lead generation b2b",
        descrizione="Intent marketing del sito stesso. CTA, attrito, mobile, orari. Antoniotrento.net come esempio di principio non di vanity.",
        angle="Conversione del traffico che stai cercando di comprare/attrarre.",
        outline=[
            "Visite vanitose vs richiesta vera",
            "Mobile: il form da 12 campi",
            "WhatsApp vs form vs telefono vs calendario",
            "Promessa del bottone (appuntamento, preventivo, urgenza)",
            "Orari e risposta: l’AI che prende i dati, l’umano che chiude",
            "Tracciamento semplice (senza 14 tag)",
            "Test in 14 giorni",
            "Cosa non fare: chatbot che blocca lo schermo",
        ],
        must=["matrice canali", "esempio CTA", "piano 14 giorni"],
        scene="A shop door with an open/closed sign blurred, street, no shop name.",
    ),
    dict(
        titolo="Cercare nei contratti e negli NDA dell’azienda senza un avvocato in chat 24/7 (e senza farsi dare pareri dall’AI)",
        kw="cercare nei contratti aziendali ai",
        kw2="rag contratti, clausole recesso software, nda azienda ricerca, assistente documenti legali",
        descrizione="Legal ops povero. Ricerca e citazione vs parere. Rischi.",
        angle="Utilità + disclaimer forte.",
        outline=[
            "Trovare la clausola ≠ interpretarla",
            "Archivio: versioni, firme, cartelle",
            "Ricerca per articolo, foro, recesso, penale",
            "L’AI che “spiega” e sbaglia il foro competente",
            "Citazione obbligatoria del pezzo di testo",
            "Ruolo dell’avvocato (conferma, non sostituito)",
            "Permessi: non tutti vedono tutti i contratti",
            "Quando il volume non giustifica lo strumento",
        ],
        must=["disclaimer", "esempi di query utili vs pericolose", "regola citazione"],
        scene="Leather folder closed on a steel table, law-office mood, no text.",
    ),
    dict(
        titolo="Quando NON automatizzare: 10 processi che l’AI peggiora (e ti costano clienti)",
        kw="quando non automatizzare processi",
        kw2="limiti automazione aziendale, ai che peggiora il servizio, processi da lasciare umani, fuffa automazione",
        descrizione="Contrarian click. Fiducia. Elenco processi (reclami seri, prezzi su misura, prima vendita, crisi).",
        angle="Anti-hype. Posiziona come adulto.",
        outline=[
            "L’automazione come status symbol",
            "10 processi: reclamo serio, primo cliente, prezzo su misura, licenziamento, crisi stampa, eccezione VIP, negoziazione, salute/legale, minori, bonifici",
            "Segnali che stai automatizzando per moda",
            "Ibrido: l’AI prepara, l’umano decide",
            "Come dire di no a un vendor",
            "Cosa automatizzare al posto (il bordero ripetitivo)",
            "Metriche di qualità del servizio",
            "Checklist “meritiamo l’umano”",
        ],
        must=["lista 10", "script no al vendor", "ibrido"],
        scene="A human handshake in the foreground, office bokeh, faces not identifiable.",
    ),
    dict(
        titolo="Il costo nascosto di HubSpot e Salesforce “con l’AI”: crediti, limiti, e il giorno in cui il rinnovo raddoppia",
        kw="costo nascosto hubspot salesforce ai",
        kw2="hubspot credits ai, salesforce einstein prezzo, lock-in crm, rinnovo licenze crm",
        descrizione="Intent pricing CRM. Crediti, seats, oggetti, AI pack. Lock-in.",
        angle="Procurement. Target chi sta per firmare.",
        outline=[
            "Il listino e la fattura vera dopo 8 mesi",
            "Seats, oggetti, marketing contacts, API",
            "Pacchetti AI e crediti che finiscono",
            "Integrazioni che paghi due volte",
            "Uscita: esportare non è migrare",
            "Domande da fare al sales prima della firma",
            "Ibrido: CRM magro + automazione tua",
            "Red flag contrattuali",
        ],
        must=["lista domande al sales", "voci di costo", "nota lock-in"],
        scene="A contract unsigned with a pen, table, text unreadable.",
    ),
    dict(
        titolo="Assistente AI per l’amministrazione: prima nota, solleciti, riconciliazione — dove può aiutare e dove combina pasticci",
        kw="ai amministrazione aziendale",
        kw2="automazione solleciti fatture, riconciliazione bancaria ai, prima nota automatica, ai per ufficio amministrativo",
        descrizione="Target ufficio amm. Confini, SEPA, human, errori.",
        angle="Back office. Traffico da “AI contabilità” senza essere un settore-enciclopedia.",
        outline=[
            "L’amministrazione non è un chatbot",
            "Solleciti: tono, scadenze, eccezioni (cliente grosso, lite)",
            "Riconciliazione: matching vs invenzione",
            "Prima nota: il sogno e il piano dei conti",
            "Bonifici: mai l’agente da solo",
            "Integrazione banca/gestionale",
            "Cosa misurare (giorni crediti, errori)",
            "Piano a strati",
        ],
        must=["matrice compiti", "divieto SEPA autonoma", "KPI"],
        scene="Italian accounting stamps and a ledger closed, desk, no numbers.",
    ),
    dict(
        titolo="Come misurare se un’automazione ha funzionato dopo 90 giorni (ore, errori, soldi — non “abbiamo fatto l’AI”)",
        kw="misurare roi automazione aziendale",
        kw2="kpi automazione processi, ore risparmiate workflow, errori dopo n8n, baseline processi",
        descrizione="Intent post-acquisto. Baseline, KPI, trappole delle ore “risparmiate”.",
        angle="Serietà. Converte chi ha già speso o sta per spendere.",
        outline=[
            "Senza baseline è folklore",
            "Cosa misurare: tempo, errori, lead time, fermo, token",
            "Come prendere la foto del “prima” in una settimana",
            "90 giorni: cosa è rumore, cosa è segnale",
            "Il risparmio che non si vede in busta paga (ma c’è)",
            "Dashboard da una pagina per il titolare",
            "Quando spegnere l’automazione",
            "Come scrivere l’obiettivo nel contratto con l’integratore",
        ],
        must=["template baseline", "dashboard 1 pagina", "clausola obiettivo"],
        scene="A wall calendar on day 90, empty office, no writing sharp.",
    ),
    dict(
        titolo="Modelli AI europei vs GPT: qualità dell’italiano, privacy, e cosa scegliere in una PMI nel 2026",
        kw="llm europei vs chatgpt pmi",
        kw2="modelli ai italia europa, mistral vs gpt azienda, privacy llm ue, scegliere modello linguistico",
        descrizione="Scelta modello per non-ML. Lingua, privacy, costo, quando GPT resta meglio.",
        angle="Query 2026. Decision helper.",
        outline=[
            "Non stai scegliendo un tifoso, stai scegliendo un fornitore di testo",
            "Italiano: dove i modelli ancora inciampano",
            "Privacy e dove gira l’inferenza",
            "Costo e stabilità API",
            "Usi: bozze vs numeri vs tool",
            "Ibrido: cloud per il grezzo, locale per i dati sensibili",
            "Come fare una prova su 20 documenti tuoi",
            "Tabella di scelta",
        ],
        must=["tabella", "protocollo prova 20 doc", "ibrido"],
        scene="Two coffee cups on opposite sides of a table, European window light.",
    ),
    dict(
        titolo="Fattura elettronica e AI: il XML c’è già (quello che i vendor di OCR non ti dicono)",
        kw="fattura elettronica xml ai",
        kw2="fatturapa vs ocr, sdi fatture automatiche, leggere xml fattura, data entry fatture pa",
        descrizione="Educazione FatturaPA. Taglia il mercato OCR inutile. Posiziona competenza Italia.",
        angle="Search “fattura elettronica automazione”.",
        outline=[
            "La PA ti manda già i campi",
            "Cosa c’è nell’XML (in parole)",
            "Quando il PDF resta (estero, scansioni, allegati)",
            "Come entra nel gestionale senza AI",
            "Dove l’AI aiuta comunque (email, PDF sporchi, matching fornitore)",
            "Errori di mapping campi",
            "Cosa chiedere al commercialista/software house",
            "Risparmio vs teatro OCR",
        ],
        must=["spiegazione XML non nerd", "quando serve ancora l’OCR", "domande alla software house"],
        scene="A USB stick labeled with unreadable blur next to a tax folder, desk.",
    ),
    dict(
        titolo="Se l’agente “può cliccare” sul computer: cosa deve poter fare e cosa no (guida per chi firma i permessi)",
        kw="rischi agente ai che usa il computer",
        kw2="automazione browser aziendale, permessi agenti ai, computer use sicurezza, ai che clicca",
        descrizione="Computer-use hype. Permessi, allowlist, banking, delete. Per titolari.",
        angle="Paura + regole. Traffico da news computer-use.",
        outline=[
            "Un agente con il mouse è un stagista con i privilegi sbagliati",
            "Cosa può andare storto in 10 minuti",
            "Allowlist di siti e azioni",
            "Mai: home banking, SPID, delete, download eseguibili",
            "Budget di click e timeout",
            "Log: cosa tenere per capire cosa ha fatto",
            "Cosa chiedere al vendor di “AI che usa il PC”",
            "Alternativa: API e integrazioni, non il mouse",
        ],
        must=["lista never", "domande vendor", "preferenza API"],
        scene="A computer mouse on a red doormat, conceptual.",
    ),
    dict(
        titolo="Dal foglio Excel al processo: 4 integrazioni che valgono più di un chatbot in homepage",
        kw="integrare excel gestionale pmi",
        kw2="excel come database rischi, sincronizzare fogli google, automazione excel azienda, uscire da excel",
        descrizione="Excel hell. 4 integrazioni concrete. Chatbot come anti-pattern.",
        angle="Realtà PMI. Altissimo riconoscimento.",
        outline=[
            "Excel è il vero software dell’Italia",
            "Quando Excel va bene e quando è un incidente",
            "4 integrazioni: listini, presenze, magazzino, scadenze",
            "Google Sheet condiviso: permessi e disastri",
            "Come non “migrare tutto in un mese”",
            "Il chatbot che risponde sui numeri sbagliati del foglio",
            "Passi di uscita graduale",
            "KPI: versioni, errori, chi ha il file “vero”",
        ],
        must=["4 integrazioni", "segnali di pericolo Excel", "piano graduale"],
        scene="Printed spreadsheet pages stacked, numbers blurred, desk lamp.",
    ),
    dict(
        titolo="Cosa scrivere nella privacy policy se usi l’AI sui ticket dei clienti (senza copiare un template americano)",
        kw="privacy policy chatbot ai",
        kw2="informativa ai clienti, gdpr assistente virtuale, trasparenza bot, trattamento dati llm",
        descrizione="Intent compliance + implementazione. Informativa, base giuridica, fornitori, tempi. Disclaimer.",
        angle="Query precisa. Utile e indicizzabile.",
        outline=[
            "Perché il template USA non calza",
            "Cosa deve capire il cliente in 8 righe",
            "Fornitori (modello, hosting, email)",
            "Finalità: assistenza, non profilazione selvaggia",
            "Tempi di conservazione delle chat",
            "Diritti: accesso, cancellazione, limiti tecnici",
            "Trasparenza “parli con una macchina”",
            "Allineare policy, cookie, script del bot",
        ],
        must=["traccia di 8 righe in italiano", "elenco fornitori da nominare", "disclaimer legale"],
        scene="A website footer out of focus on a monitor, no readable policy text.",
    ),
    dict(
        titolo="Quanto tempo ci vuole a mettere in produzione un agente AI (timeline onesta: 2 settimane, 2 mesi, 6 mesi)",
        kw="quanto tempo serve agente ai produzione",
        kw2="tempi progetto automazione, mvp agente ai, roadmap integrazione sistemi, go live chatbot aziendale",
        descrizione="Intent aspettative. Tre fasce, dipendenze (dati sporchi, accessi, legale), cosa succede se “lo voglio lunedì”.",
        angle="Qualifica i lead. Filtra chi vuole magia.",
        outline=[
            "Perché “lunedì è live” è una bugia utile solo al vendor",
            "2 settimane: classifica, bozza, niente side effect",
            "2 mesi: un processo con umano in mezzo",
            "6 mesi: più sistemi, permessi, audit",
            "Dipendenze: accessi, dati, chi decide, DPO",
            "Cosa blocca (Salesforce admin in ferie, PEC, listini)",
            "Come si vede un progetto sano a metà strada",
            "Cosa chiedere in un kickoff",
        ],
        must=["tre fasce", "lista dipendenze", "agenda kickoff"],
        scene="A project Gantt chart completely out of focus on a wall, office.",
    ),
    dict(
        titolo="Self-hosted in pratica: VPS in Italia, NAS in ufficio o Raspberry — cosa sta a casa e cosa no",
        kw="self hosted pmi vps nas",
        kw2="server in ufficio vs cloud, nas aziendale, raspberry pi azienda, vps italia pmi",
        descrizione="Scelta dove gira lo stack. Corrente, backup, IP, chi riavvia. Per titolari che hanno sentito “mettiamo un Pi”.",
        angle="Ops in linguaggio umano. Non tunnel Cloudflare da 4000 parole nerd.",
        outline=[
            "Tre scatole: ufficio, armadio casa, datacenter",
            "Cosa può stare su NAS (file, backup)",
            "Cosa vuole un VPS (servizi 24/7, IP, corrente)",
            "Raspberry: laboratorio, non il fatturato",
            "Chi viene di notte se si spegne",
            "Costi 12 mesi (stime)",
            "Ibrido: backup in ufficio, app sul VPS",
            "Errori: aprire le porte del modem",
        ],
        must=["tabella tre opzioni", "cosa non mettere sul Pi", "ibrido"],
        scene="A NAS next to a router with lights, small office shelf, no logos readable.",
    ),
    dict(
        titolo="Chatbot “legale” o “fiscale”: perché è pericoloso e come fare un assistente che cita i documenti (senza spacciare pareri)",
        kw="chatbot legale fiscale rischi",
        kw2="ai pareri fiscali, assistente documenti studio, allucinazione normativa, chatbot avvocato",
        descrizione="Query da studi e da titolari che vogliono “l’AI che sa la legge”. Confine parere vs ricerca.",
        angle="E-E-A-T e traffico da nicchia professionale.",
        outline=[
            "La domanda “posso scaricare questo costo?” non è una ricerca",
            "Allucinazioni su norme e sentenze",
            "Assistente che trova e cita il PDF interno dello studio",
            "Disclaimer, logging, chi è responsabile",
            "Cosa mostrare al cliente finale (di solito niente bot fiscale)",
            "Uso interno vs uso pubblico",
            "Assicurazione e deontologia (cenni, non consulenza)",
            "Architettura onesta",
        ],
        must=["confine parere/ricerca", "disclaimer", "uso interno vs pubblico"],
        scene="Law books stacked, gold lettering unreadable, moody library light.",
    ),
    dict(
        titolo="Integrare TeamSystem, Zucchetti o il gestionale che hai già: senza rifare l’ERP (e senza un altro “modulo AI” da listino)",
        kw="integrazione gestionale teamsystem zucchetti",
        kw2="api gestionale pmi, collegare erp ecommerce, modulo ai erp costi, system integrator gestionale",
        descrizione="Intent altissimo in Italia. API, CSV, middleware, modulo vendor. Rabbia da listino.",
        angle="Mercato italiano reale. Non nominare un tuo prodotto.",
        outline=[
            "Il gestionale è il centro, l’AI è un satellite",
            "Modulo AI del vendor: pro e lock-in",
            "API, export CSV, database (quando il DBA dice no)",
            "Cosa integrare prima: anagrafiche, documenti, magazzino",
            "Middleware (n8n o simile) come cassetto",
            "Errori di mapping IVA/codici",
            "Chi deve stare al tavolo (software house, commercialista, tu)",
            "Come scrivere la richiesta alla software house",
        ],
        must=["lettera/richiesta tipo alla software house", "ordine di integrazione", "rischio modulo listino"],
        scene="Italian SME server closet with a tower PC, documentary, no brand.",
    ),
    dict(
        titolo="Sequenze email e LinkedIn automatiche che non sembrano spam (GDPR, consenso, e quando l’AI scrive troppo “americano”)",
        kw="email automatiche gdpr pmi",
        kw2="sequenze linkedin automazione, cold email italia, consenso marketing, tono ai italiano",
        descrizione="Lead gen B2B. GDPR, tono, limiti automazione social. Non growth-hacking illegale.",
        angle="Marketing PMI. Filtra chi vuole spam.",
        outline=[
            "Automazione ≠ spam a 10.000 P.IVA",
            "Consenso, legittimo interesse, liste comprate (no)",
            "LinkedIn: ToS e reputazione del profilo",
            "L’AI che scrive in corporatese americano",
            "Sequenza corta, utile, con uscita",
            "CRM: non perdere chi dice no",
            "Metriche: risposta, non solo invii",
            "Quando chiamare è più rispettoso",
        ],
        must=["principi GDPR operativi", "esempio tono IT vs USA", "metriche"],
        scene="A closed mailbox on an apartment door, European street bokeh.",
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
