---
layout: portfolio
title: "Ecosistema HelmsmanTrading – Motore MCP, Backend SaaS, App Desktop e Sito"
date: 2026-09-02
description: "Un ecosistema completo per il trading assistito da LLM, progettato e sviluppato end-to-end: il motore MCP a 5 livelli (HelmsmanTrading), il backend SaaS License/Data API con Stripe e PostgreSQL (Helmsman-saas), il Control Panel Electron zero-knowledge (Helmsman-desktop), il sito di branding bilingue (HelmsmanTrading.github.io) e la versione open-core pianificata (helmsman-lite). Un caso di studio sulle scelte tecniche e architetturali, non un pitch di vendita."
image: "/assets/images/portfolio/helmsman-trading/helmsman-trading.jpg"
image-header: "/assets/images/portfolio/helmsman-trading/helmsman-trading.jpg"
image-paint: "/assets/images/portfolio/helmsman-trading/helmsman-trading.jpg"
tags: [MCP, Trading Assistant, LLM, Python, FastAPI, PostgreSQL, Redis, Stripe, Electron, React, TypeScript, Risk Management, Multi-Broker, Backtesting, Data Engineering, Docker, Jekyll]
---

> *"Un modello linguistico è un consulente brillante e un esecutore pessimo. Sa argomentare una tesi di mercato meglio di molti analisti, ma se gli lasci in mano la size, lo stop e il bottone 'invia ordine' prima o poi ti fa saltare il conto — non per malizia, ma perché allucina un numero con la stessa sicurezza con cui ne azzecca dieci. HelmsmanTrading nasce da questa consapevolezza: separare in modo chirurgico il **giudizio** (l'LLM) dall'**esecuzione** (un motore deterministico che non improvvisa mai)."*

**HelmsmanTrading** è un motore di trading assistito da intelligenza artificiale costruito attorno a un principio non negoziabile: **l'LLM propone, il codice dispone, l'umano decide.** Non è un "bot che fa soldi mentre dormi" e non pretende di esserlo. È un'infrastruttura di ingegneria — disciplina, gestione del rischio, sicurezza dell'esecuzione — dentro cui un modello linguistico può ragionare sui mercati senza avere il potere di combinare disastri irreversibili.

Il progetto è la dimostrazione pratica di una tesi: nel trading algoritmico assistito da AI, il vantaggio competitivo non è il "segnale magico", ma **il motore che rende sicuro, misurabile e ripetibile qualsiasi segnale**. Le strategie sono contenuto modulare e sostituibile; l'impianto che le imbriglia è ciò che ha davvero valore.

---

## 1. Il problema: perché mettere un LLM nel loop del trading è pericoloso

Chiunque abbia provato a collegare un modello linguistico a un conto reale si è scontrato con tre muri.

Il primo è l'**allucinazione dei dati**. Un LLM, richiesto di un prezzo o di un indicatore, può inventare un valore plausibile e sbagliato. Nel trading un dato stantio o inventato non è un fastidio: è la premessa di una perdita. Serve una garanzia deterministica che il modello non decida mai su dati vecchi o falsi.

Il secondo è l'**allucinazione dell'esecuzione**. Chiedere a un LLM di calcolare quante azioni comprare, dove mettere lo stop e con che ordine, significa affidare aritmetica critica a un sistema probabilistico. La size di una posizione non può essere "quasi giusta". Deve uscire da una formula, non da una previsione di token.

Il terzo è la **mancanza di freni**. Un agente autonomo che sbaglia in un ciclo può ripetere l'errore a raffica: dieci ordini invece di uno, una posizione aperta e riaperta, un conto svuotato in un loop. Servono interruttori hardware, non buoni propositi nel prompt.

HelmsmanTrading risponde a questi tre muri con un'architettura stratificata in cui **ogni responsabilità critica è tolta all'LLM** e affidata a codice deterministico e verificabile. Il modello resta dov'è insostituibile — leggere il contesto, spiegare una tesi, dialogare con l'umano — e viene escluso da tutto ciò che deve essere esatto.

---

## 2. L'architettura a 5 livelli

Il cuore del sistema è una separazione netta in cinque strati, ognuno con un contratto formale e un confine invalicabile. Nessuno strato "scavalca" quello sotto: i dati salgono, gli ordini scendono, e ogni passaggio è tipizzato.

- **L1 – Data Feed**: procura i dati di mercato e ne garantisce la freschezza.
- **L2 – Skills**: le strategie, come regole deterministiche interrogabili.
- **L3 – Orchestrator**: l'LLM, che dialoga col sistema esclusivamente tramite strumenti (tool) esposti via protocollo MCP.
- **L4 – Risk Engine**: il "giudice supremo" che dimensiona, valida e può bloccare qualsiasi operazione.
- **L5 – Broker Adapters**: l'esecuzione reale sui broker, dietro un'interfaccia astratta e intercambiabile.

Questa non è un'astrazione accademica: è ciò che permette di sostituire una strategia, aggiungere un broker o cambiare fonte dati **senza toccare il resto del sistema**, e soprattutto senza indebolire le garanzie di sicurezza.

---

## 3. L1 – Il livello dati: niente decisioni su dati stantii

Il primo livello ha un compito apparentemente banale e in realtà fondamentale: fornire dati **freschi, coerenti e ricchi**, oppure fermarsi.

### La guardia di freschezza (anti-allucinazione)

Ogni pacchetto di dati di mercato porta con sé un timestamp. Prima che qualsiasi strategia venga valutata, un controllo deterministico verifica che il dato non sia più vecchio di una soglia di sicurezza. Se lo è, il sistema solleva un'eccezione esplicita (`StaleDataError`) e **si ferma**, invece di procedere su informazioni obsolete. La soglia è consapevole della sessione: durante le ore di contrattazione pretende dati recenti; a mercato chiuso accetta l'ultima chiusura, come è giusto nei weekend e nei festivi. È la prima linea contro l'allucinazione: un LLM non può ragionare su un prezzo di ieri credendolo di oggi, perché a quel prezzo non arriva nemmeno.

### Un registro modulare di indicatori

Il livello dati calcola una libreria estesa di oltre quaranta indicatori tecnici — medie mobili (SMA, EMA, WMA, HMA, KAMA), oscillatori (RSI a più periodi, MACD, stocastico, CCI, Williams %R, Ultimate Oscillator), misure di volatilità (ATR, bande di Bollinger, canali di Keltner, Donchian), volume (OBV, MFI, CMF, Chaikin), trend (ADX, Aroon, Supertrend, PSAR, Vortex, Ichimoku) e altro. Ogni indicatore è una funzione registrata in modo dichiarativo: aggiungerne uno significa scrivere una funzione decorata, non modificare i feed. Un indicatore che fallisce non blocca gli altri — resta semplicemente assente, mai inventato.

### Multi-timeframe e coerenza orizzonte/timeframe

Uno degli errori più insidiosi nel trading sistematico è valutare una strategia sul timeframe sbagliato: una regola pensata per operare su più giorni non deve essere giudicata su barre orarie, altrimenti si sta misurando un'altra strategia. Il motore risolve il problema alla radice: ogni skill **dichiara** il proprio timeframe, coerente con il proprio orizzonte, e legge gli indicatori dal timeframe corretto (con fallback prudente quando il dato di quel timeframe non è disponibile). Le strategie pluri-giornaliere vengono quindi valutate su barre daily reali, non su rumore intraday.

### Il data-lake e il disaccoppiamento dal broker

I prezzi non arrivano necessariamente dal broker su cui si esegue: la fonte dati è **disaccoppiata** dall'esecuzione. Un data-lake ordinato — organizzato per fonte, timeframe e ticker — funge da sorgente unica, con cache locale e sincronizzazione opzionale su object storage (Cloudflare R2). Questo permette di alimentare tutte le istanze del motore da un'unica fonte consolidata, calcolare un VWAP affidabile da dati a volume consolidato, e mantenere una separazione pulita tra "dove prendo i prezzi" e "dove mando gli ordini".

---

## 4. L2 – Le Skills: le strategie come contratto, non come scatola nera

Nel livello L2 vivono le strategie, chiamate **skill**. Ma non sono blocchi opachi che sputano "compra" o "vendi": sono oggetti con un **contratto formale** che l'LLM può interrogare in modo trasparente.

Ogni skill dichiara un identificativo, un orizzonte temporale, le direzioni ammesse (long, short o entrambe), gli indicatori e i timeframe da cui dipende. Espone due metodi chiave che il resto del sistema usa senza conoscerne l'interno: `explain()`, che restituisce non un verdetto ma **le ragioni e le evidenze** dell'applicabilità (i predicati soddisfatti, i valori che li giustificano), e le funzioni che definiscono la distanza dello stop-loss e dell'eventuale take-profit — perché è la strategia a sapere *quanto* è lontano lo stop giusto per la propria tesi, mentre sarà il Risk Engine a decidere *quante* azioni.

Questa separazione — la skill definisce la *distanza* del rischio, il motore definisce la *quantità* — è uno dei perni dell'intero sistema. La strategia non conosce il capitale, non conosce la size: conosce solo la propria logica di mercato. Il capitale è sacro e vive altrove.

Le skill incluse coprono famiglie diverse e complementari: rottura di volatilità in trend (ATR-Breakout), mean-reversion di breve su ipervenduto dentro un trend (Connors), compressione di volatilità (Volatility Squeeze), acquisto contrarian su nomi di qualità profondamente ipervenduti (Quality Dip), e un retest su VWAP ancorato. Sono, dichiaratamente, **contenuto di partenza**: modulari, sostituibili, ampliabili. Il loro valore non sta nell'essere il Sacro Graal — non lo sono, e il progetto è onesto su questo — ma nell'essere espresse in una forma che il motore può eseguire in sicurezza e, come vedremo, **misurare senza illudersi**.

---

## 5. L3 – L'Orchestrator e il protocollo MCP

Il terzo livello è dove entra l'LLM, ma con un guinzaglio preciso. Il modello non ha accesso diretto ai broker, ai calcoli di rischio o ai dati grezzi: interagisce con il sistema **solo** attraverso un insieme di strumenti (tool) esposti tramite il **Model Context Protocol (MCP)**, implementato con FastMCP.

Il server MCP è progettato per due modalità di trasporto. In locale gira su **stdio**: nessuna porta aperta, nessun HTTPS, il motore vive sulla macchina dell'utente e nessun dato sensibile transita altrove. In remoto — per esempio su un VPS — può esporre un trasporto HTTP a streaming, gestito come servizio di sistema dietro un reverse proxy. La stessa base di codice serve entrambi gli scenari.

Gli strumenti esposti all'LLM sono verbi chiari e circoscritti: recuperare i dati correnti di un titolo, valutare quali strategie sono applicabili, scansionare un intero universo alla ricerca di opportunità, richiedere un *preventivo* di trade, confermarlo, aumentare un'esposizione esistente, leggere lo stato del conto e le performance. Ogni tool è un confine: l'LLM può chiedere, ma non può calcolare al posto del motore né eseguire scavalcando il rischio.

---

## 6. Il gate umano a due fasi: preview → confirm

Il meccanismo di sicurezza più visibile è il **gate umano a due fasi**. Nessun ordine nasce da un singolo comando dell'LLM.

Nella prima fase (`preview`), il modello invia la propria *intenzione* di trade: la strategia scelta, il sottostante, la direzione, il livello di convinzione. Il Risk Engine prende questa intenzione e calcola **tutto ciò che conta** — la size esatta, il prezzo di stop, l'eventuale take-profit — restituendo un preventivo con un identificativo univoco. Nessun ordine è stato inviato.

Nella seconda fase (`confirm`), l'operazione viene eseguita **solo** presentando quell'identificativo, cioè dopo un'approvazione esplicita. Fra le due fasi il sistema gestisce anche lo scenario reale della volatilità: se tra il preventivo e la conferma il prezzo si è mosso al punto da alterare in modo significativo la size (e quindi il rischio), il motore **richiede una nuova conferma** invece di eseguire silenziosamente qualcosa di diverso da quanto approvato. Un piccolo scostamento a rischio invariato passa; uno scostamento che cambia il profilo di rischio no.

A protezione dell'idempotenza, ogni ordine porta un identificativo deterministico derivato dal preventivo: se un messaggio viene ripetuto per errore o per un ritentativo di rete, il broker non apre due posizioni. È il tipo di dettaglio che non si nota finché non ti salva.

---

## 7. L4 – Il Risk Engine: il giudice supremo deterministico

Se c'è un componente che incarna la filosofia del progetto, è il Risk Engine. Qui **non entra nessuna probabilità linguistica**: solo aritmetica e regole invalicabili.

### Dimensionamento per rischio, non per capriccio

La size non è mai decisa dall'LLM. È calcolata da una formula: dato un budget di rischio per operazione (una frazione del capitale) e la distanza dello stop fornita dalla skill, il numero di unità è il rapporto tra i due. In altre parole, si rischia sempre lo stesso importo predefinito, indipendentemente da quanto "convinto" sia il modello. La convinzione dell'LLM può modulare entro limiti, ma non può far esplodere l'esposizione.

### Tetti di esposizione ("heat") e di potere d'acquisto

Sopra la singola operazione vegliano tetti di portafoglio. Un tetto di **heat lorda** limita il rischio aperto complessivo (posizioni esistenti più la nuova) come frazione dell'equity: oltre quella soglia, nessun nuovo trade, per quanto valida sia la tesi. Un tetto di **potere d'acquisto** impedisce di impegnare più di quanto il conto consenta. Sono limiti hard, non suggerimenti.

### Il floor anti-sweep sullo stop

Uno stop troppo stretto è un modo elegante di regalare soldi al rumore di mercato: viene "spazzato via" (*stop hunting*) e la posizione chiusa in perdita un attimo prima che il prezzo vada dove doveva. Il motore impone un **pavimento** alla distanza dello stop — mai più stretto di una percentuale minima né di un multiplo dell'ATR corrente — proteggendo l'operazione da uscite premature causate dalla volatilità normale.

### Il kill-switch di sessione

Al di sopra di tutto c'è un interruttore. Se il drawdown intraday supera una soglia, o se si accumulano troppi errori consecutivi del broker, il sistema **arma un kill-switch** che blocca l'apertura di nuovi ordini. Non è una variabile nel prompt: è uno stato persistente che va rimosso manualmente dall'umano. Un agente in loop non può "convincersi" di disarmarlo.

### Aumento di esposizione controllato

Aggiungere a una posizione vincente è legittimo, ma pericoloso se improvvisato. Il motore prevede un percorso dedicato e deliberato per **incrementare** un'esposizione esistente, che riusa le stesse regole di heat e potere d'acquisto: si può crescere su una tesi che funziona, ma sempre dentro i tetti di rischio, mai a caso.

---

## 8. L5 – Broker Adapters: un core broker-agnostic

L'esecuzione reale vive nel livello L5, ma il resto del sistema **non sa quale broker sta usando**. Questo è deliberato e difeso con rigore.

Il core dialoga esclusivamente con un'interfaccia astratta (`BaseBrokerAdapter`) e con oggetti di trasferimento dati tipizzati (stato del conto, posizioni, ordini, fill, trade chiusi, performance). Ogni broker concreto — Alpaca, Tradier, IG Markets, Interactive Brokers, oltre a un simulatore *paper* completamente offline — implementa quel contratto. Aggiungere un broker significa scrivere un nuovo adapter che rispetta l'interfaccia, senza toccare orchestratore, rischio o strategie.

Gli adapter non sono banali wrapper: incapsulano le idiosincrasie di ciascuna piattaforma. Interactive Brokers, per esempio, è integrato sulla Client Portal Web API, con la gestione dei suoi identificativi di contratto, degli ordini bracket padre-figlio, del particolare uso del prezzo ausiliario per gli stop e del ciclo di conferme richiesto. IG lavora sui suoi "epic" con una mappatura curata dei simboli e il riuso della sessione autenticata. Ognuno parla la propria lingua verso l'esterno, ma la stessa lingua — pulita e tipizzata — verso l'interno.

A garanzia che questa astrazione non sia "finta modularità", esiste una **suite di conformità**: una batteria di test che ogni adapter deve superare, verificando che rispetti il contratto allo stesso modo degli altri. È ciò che rende credibile la promessa "cambi broker senza cambiare il motore".

---

## 9. Backtest e validazione onesta: il vero fiore all'occhiello

Qui il progetto prende una posizione che lo distingue nettamente dai venditori di segnali: **misura le proprie strategie con brutale onestà, e pubblica il risultato anche quando è scomodo.**

### Un harness separato e sicuro

Il backtest gira su uno store dati **completamente separato** dal data-lake operativo: non lo tocca, non lo intacca, non ne condivide il codice. È, per progettazione, **solo misura**: non disabilita né altera alcuna strategia, anche quando ne dimostra la debolezza. Produce un report; la decisione resta all'umano.

### Nessun look-ahead, per costruzione

Il difetto classico dei backtest è guardare, anche involontariamente, dati futuri. L'harness lo previene alla radice: gli indicatori sono causali (il valore alla barra `t` dipende solo dai dati fino a `t`), l'ingresso avviene all'apertura della barra successiva al segnale, e l'uscita guarda solo le barre seguenti. Gli indicatori sono calcolati in forma vettorizzata una sola volta per titolo — con un test di fedeltà che verifica la coincidenza con il motore reale — rendendo l'analisi ordini di grandezza più veloce senza sacrificare correttezza. Costi e slippage sono modellati su entrambi i lati, per non cadere nell'ottimismo.

### La prova che separa alfa da beta

Un risultato positivo, da solo, non dimostra niente: su un mercato in salita quasi ogni regola che compra guadagna. Per distinguere la **bravura della regola** (alfa) dalla **semplice esposizione al mercato** (beta), l'harness include il test più severo: il **benchmark a ingresso casuale**. Si tengono le stesse strategie, gli stessi stop e take, ma si entra in giorni scelti a caso invece che sui segnali. Se il caso rende quanto il segnale, la regola d'ingresso non aggiunge nulla.

Applicato a un paniere di titoli tecnologici ad alta liquidità, il verdetto è stato onesto e istruttivo: **una sola strategia** ha battuto in modo statisticamente significativo l'ingresso casuale (oltre due deviazioni standard), mentre le altre, pur positive nel periodo, si sono rivelate in gran parte esposizione al mercato toro. La stessa analisi, isolata su un anno ribassista, ha mostrato perdite su tutte le regole — come è realistico attendersi.

Questa trasparenza **è** il prodotto. In un settore pieno di curve di equity gonfiate e promesse di rendimento, un motore che ti dice "questa strategia ha un edge misurato, quest'altra è solo il mercato" costruisce l'unica cosa che conta davvero: **fiducia**.

---

## 10. Il ponte SaaS zero-knowledge

Attorno al motore è progettata un'architettura di commercializzazione che non tradisce i principi tecnici. Il modello è un **ponte locale ↔ SaaS a conoscenza zero**: le chiavi dei broker, le impostazioni di trading e l'esecuzione degli ordini restano **sul client dell'utente**; il server centrale gestisce solo licenza, dati, fatturazione e CRM. Il fornitore non vede mai le credenziali di trading né esegue ordini per conto del cliente.

Il "lucchetto" che protegge il servizio non è una barriera aggirabile lato client, ma il **confine dei dati**: il motore, quando opera in modalità licenziata, ottiene i dati tramite URL firmati a breve scadenza rilasciati solo a fronte di una licenza attiva. Senza licenza, niente dati; con licenza scaduta o piano insufficiente, il sistema **degrada con grazia** spiegando all'utente il motivo, invece di crashare. I piani determinano in modo trasparente quali titoli, quali strategie e quali broker sono disponibili, e il motore rispetta quell'allowlist già in locale, comunicando in chat, con tono amichevole e mai invadente, quando un piano superiore sbloccherebbe più opportunità.

L'infrastruttura di supporto è pensata per essere solida e non giocattolo: database PostgreSQL, gestione idempotente dei webhook di pagamento, sincronizzazione con un CRM tramite servizi di integrazione scritti come codice (non tramite connettori "no-code" da principianti), programmi di referral e affiliazione, e una gestione dei dati orientata alla robustezza e alla continuità del servizio.

---

## 11. Qualità del codice, testing e metodo

Un sistema che tocca soldi veri vive o muore sulla disciplina di ingegneria. Il progetto è coperto da una suite di **centinaia di test automatici** — unitari, di integrazione, di conformità dei broker — che accompagnano ogni modifica: si parte sempre da una baseline verde, si lavora in modo atomico, si rilancia l'intera suite, si controlla il *diff*, si committa citando l'attività tracciata. La regola aurea è **zero regressioni**: una nuova funzionalità non ha il diritto di indebolire ciò che già funziona.

La tracciabilità del lavoro passa da un flusso basato su issue come fonte di verità, con un piccolo strumento a riga di comando che integra il tracker direttamente nel ciclo di sviluppo. Ogni scelta architetturale rilevante — dal disaccoppiamento dati/broker alla coerenza timeframe/orizzonte, dalla validazione dell'edge al posizionamento di prodotto — è documentata, motivata e messa in discussione, non calata dall'alto.

---

## 12. Lo stack tecnologico in sintesi

- **Linguaggio e core**: Python, con modelli dati tipizzati (Pydantic) come contratto tra i livelli.
- **Protocollo agente**: Model Context Protocol via FastMCP, trasporti stdio (locale) e HTTP a streaming (remoto/VPS).
- **Dati e indicatori**: pandas e librerie di analisi tecnica, registro modulare di 40+ indicatori, VWAP da volume consolidato, data-lake su Cloudflare R2 con cache locale.
- **Broker**: Alpaca, Tradier, IG Markets, Interactive Brokers (Client Portal Web API), simulatore paper offline; possibilità di estensione all'universo MetaTrader tramite un modello "bring-your-own-key".
- **Rischio**: motore deterministico con sizing per rischio, tetti di heat e potere d'acquisto, floor anti-sweep, kill-switch persistente, gate umano a due fasi e idempotenza degli ordini.
- **Validazione**: harness di backtest walk-forward senza look-ahead, benchmark a ingresso casuale, confronto buy-and-hold, stress su regimi ribassisti.
- **SaaS**: architettura zero-knowledge, License/Data API con URL firmati, entitlement guidati dai dati, PostgreSQL, pagamenti con webhook idempotenti, CRM via scripting.
- **Qualità**: centinaia di test automatici, suite di conformità dei broker, sviluppo issue-driven, commit atomici.

---

## 13. La filosofia di prodotto: uno strumento per trader, non un oracolo

HelmsmanTrading è, dichiaratamente, uno **strumento per trader**, non un prodotto d'investimento e non una promessa di rendimento. Il suo valore è il **motore**: la disciplina del rischio, il controllo umano, la sicurezza dell'esecuzione, la trasparenza della misurazione. La profittabilità dipende dalle scelte di chi lo usa — è il trader a decidere al gate, non un algoritmo a garantire guadagni.

È una posizione onesta e, paradossalmente, più forte di mille curve di equity truccate. In un mercato dove tutti promettono "segnali che fanno soldi", offrire invece un impianto rigoroso che protegge il capitale, misura senza illudersi e mette l'essere umano nella cabina di comando è ciò che costruisce un rapporto duraturo. Le strategie di oggi sono la base; il motore che le rende sicure ed espandibili è l'investimento che dura.

---

## 14. L'ecosistema completo: cinque repository, un'unica architettura

Tutto ciò che ho descritto finora riguarda il **motore** — ma il motore è solo il primo di **cinque componenti** che ho progettato e sviluppato end-to-end. HelmsmanTrading non è un singolo programma: è un ecosistema in cui ogni pezzo ha un ruolo tecnico preciso e un confine netto verso gli altri. Vale la pena descriverli uno per uno, perché la parte interessante — dal punto di vista ingegneristico — è proprio **come i confini sono stati disegnati**.

La mappa è questa: un **motore MCP** che gira sul computer dell'utente; un **backend SaaS** che gestisce licenze, dati, pagamenti e comunicazioni; un'**app desktop** che fa da collante locale e custodisce i segreti; un **sito** bilingue per la comunicazione e il brand; e una **versione open-core** pianificata. Il filo conduttore di tutte le scelte è la *conoscenza zero*: le credenziali di trading e l'esecuzione non lasciano mai la macchina dell'utente.

### 14.1 Il motore MCP — `HelmsmanTrading`

È il componente descritto in dettaglio in tutte le sezioni precedenti: l'architettura a 5 livelli, il Risk Engine, gli adapter multi-broker, il gate umano, l'harness di backtest. Nel disegno dell'ecosistema ha un doppio ruolo: è il **primo server MCP** — nato come banco di prova dell'intera architettura — ed è la **base che verrà incorporata nell'app desktop** come motore di esecuzione locale. È scritto in Python, gira come server MCP (FastMCP) in modalità stdio sulla macchina dell'utente, ed è coperto da centinaia di test automatici. È il cuore attorno a cui ruota tutto il resto.

### 14.2 Il backend SaaS — `Helmsman-saas`

È il server che rende l'ecosistema commercializzabile senza mai vedere un segreto di trading. Costruito in **Python con FastAPI**, usa **PostgreSQL** via SQLAlchemy 2.0 (con migrazioni Alembic), **Redis** per validazioni sub-millisecondo e conteggio delle quote, autenticazione con **bcrypt e JWT**, e integrazioni con **Stripe** (SDK ufficiale) e **Cloudflare R2** (via boto3). L'API è organizzata in router chiari: `health`, `auth`, `account`, `billing`, `downloads`, `engine` e `webhooks`.

Il suo compito centrale è la **License/Data API**, la stessa a cui si connette il motore: `GET /api/license/validate` fa da heartbeat della licenza (restituendo tier, quote ed entitlement), mentre `GET /api/data/{ticker}/{tf}` rilascia un **URL firmato** verso R2, valido pochi decine di secondi, solo se la licenza è attiva e il piano lo consente. Questo è l'enforcement reale del modello: **senza licenza attiva non escono i dati** — un binario copiato senza abbonamento è un guscio vuoto, perché il "lucchetto" non è nel client ma al confine dei dati.

Il resto del backend è l'infrastruttura che serve a un vero prodotto: la gestione dei pagamenti con **webhook Stripe idempotenti** che sincronizzano lo stato della licenza (attiva, insoluta, cancellata) ed emettono o revocano le chiavi; un sistema di **entitlement guidato dai dati** (piani, feature, associazioni piano-feature) invece che da `if` sparsi nel codice; le **quote e il rate limiting** applicati lato server su Redis; un layer di **email transazionali** su SMTP con template e preset (verifica, reset password, OTP, comunicazioni di billing); un **pattern outbox** con un worker dedicato che consegna gli eventi a un **CRM EspoCRM** via REST — integrazione scritta come codice, non con connettori no-code; e i meccanismi di **crescita** (referral e affiliazione). C'è anche una **dashboard** utente separata, costruita con Vite, React e Tailwind, e un deployment containerizzato (Docker Compose per sviluppo, VPS di test e produzione, con Caddy come reverse proxy). In coerenza con l'intero progetto, **nessuna chiave broker entra mai in questo repository**.

### 14.3 L'app desktop — `Helmsman-desktop`

È il collante locale, ed è dove la "conoscenza zero" diventa concreta. È un'applicazione **Electron** (con **React 19**, **Vite** e **TypeScript**, impacchettata con electron-builder) il cui compito è installare e configurare il motore MCP sulla macchina dell'utente **senza mai esporre segreti**.

Il flusso tecnico è elegante: l'utente fa login al SaaS e la license key viene salvata nel **keychain del sistema operativo** (Windows Credential Manager o macOS Keychain, tramite la libreria keytar); le chiavi dei broker finiscono nello stesso keychain, mai in file di testo; il rischio e le impostazioni vivono in un `config.toml` locale; e le skill disponibili vengono intersecate con il tier della licenza. Il pezzo più ingegnoso è come l'app si integra con il client LLM: scrive un `claude_desktop_config.json` che contiene **solo un comando**, zero credenziali. Quando l'app viene lanciata con il flag `--mcp`, **non apre alcuna interfaccia**: legge il keychain e la configurazione, avvia il server MCP Python e cede i propri stdin/stdout al client, facendo da ponte trasparente. I moduli del processo principale (`main.ts`, `preload.ts` per il bridge IPC sicuro, `vault.ts` per il keychain, `claude.ts` per la scrittura della configurazione) riflettono questa separazione netta tra UI, segreti e orchestrazione.

Allo stato attuale è alla versione 0.1.0 ed è in **sviluppo iniziale**: l'impianto del processo principale, la gestione del vault e la logica di configurazione ci sono e sono coerenti con la specifica; l'interfaccia React è ancora abbozzata. È deliberatamente l'ultimo tassello, perché ha senso rifinirlo solo quando motore e SaaS sono stabili — ed è destinato a **inglobare il motore** trasformandolo da progetto Python a prodotto installabile con un doppio clic.

### 14.4 Il sito e il sistema di brand — `HelmsmanTrading.github.io`

È il frontend pubblico, tenuto **volutamente separato** dalla documentazione tecnica del motore: questo sito parla a chi fa trading, non a chi clona un framework. È costruito con **Jekyll su GitHub Pages**, completamente **bilingue** (italiano in `/it/`, inglese in `/en/`), con un'architettura a contenuti ricca — pagine su architettura, broker supportati, confronti, coperture, download, blog — e un flusso di **pre-registrazione** per l'early access.

L'aspetto che lo rende più di una semplice landing è il **sistema di brand versionato nel repository**: una cartella dedicata contiene un vero *brand book*, un file di **design token** (`tokens.yml`) e un set di creatività pubblicitarie. I contenuti strutturati (l'elenco dei broker, l'universo dei titoli, la navigazione) vivono in **file di dati YAML** invece che essere cablati nell'HTML, così il sito resta coerente e manutenibile e le stesse informazioni possono alimentare più pagine. È l'infrastruttura di comunicazione dell'ecosistema, trattata con lo stesso rigore del codice.

### 14.5 La versione open-core — `helmsman-lite` (pianificata)

Per onestà: **questo repository non è ancora stato creato.** È la prossima tappa prevista dell'ecosistema, e la includo perché fa parte del disegno complessivo. L'idea è un **open-core**: un sottoinsieme pubblico del motore — presumibilmente i livelli dati, skill e rischio con il simulatore *paper* offline, senza il ponte licenza — pensato come vetrina tecnica verificabile e per l'adozione da parte di chi vuole studiare o estendere l'architettura, mentre le funzionalità legate alla distribuzione dei dati e alla parte commerciale restano nel motore completo abbinato al SaaS. È la classica separazione "core aperto, servizi a valore aggiunto chiusi", ma va detto chiaramente che oggi è **sulla carta**, non nel codice.

### 14.6 Come i pezzi comunicano

Il valore architetturale sta nell'insieme. All'avvio, l'**app desktop** legge dal keychain la license key e le chiavi broker, scrive la configurazione del client LLM e lancia il **motore MCP** in locale via stdio. Il motore, quando serve dati di mercato, chiama la **License/Data API del SaaS**: si valida e riceve URL firmati per scaricare i parquet da R2, il tutto filtrato dagli entitlement del piano. Il **SaaS**, a sua volta, orchestra Stripe per i pagamenti, aggiorna lo stato delle licenze, emette le comunicazioni transazionali e sincronizza il CRM. Il **sito** porta gli utenti nel funnel di registrazione. In tutto questo, le credenziali dei broker e l'esecuzione degli ordini **non lasciano mai il computer dell'utente**: il server non le vede, non le custodisce, non le usa. È una decisione architetturale, non una promessa di marketing — ed è verificabile leggendo i confini tra i repository.

## In conclusione

HelmsmanTrading è la sintesi di un'idea precisa: **l'intelligenza artificiale nel trading va imbrigliata, non liberata.** Un LLM è straordinario nel ragionare e disastroso nell'eseguire; questo progetto costruisce, strato dopo strato, l'infrastruttura che tiene il modello dove è bravo e lo esclude da dove sarebbe pericoloso. Dati che non mentono, strategie come contratti trasparenti, un motore di rischio inflessibile, adapter broker intercambiabili, un gate umano invalicabile e un backtest che ha il coraggio di dire la verità sui propri numeri.

È il tipo di sistema che si costruisce quando si è capito che, nei mercati, sopravvivere è la precondizione di ogni profitto — e che la sopravvivenza è una questione di ingegneria, non di fortuna.
