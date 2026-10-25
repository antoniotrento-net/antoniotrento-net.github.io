---
layout: portfolio
title: "Telario — aprire i mockup, riprendere il lavoro"
date: 2026-10-25
description: "Editor per file Balsamiq .bmpr: React, TypeScript, SQLite e WebAssembly nel browser, prova online senza login e uso locale con Docker. Applicazione Electron pianificata per una futura evoluzione."
image: "/assets/images/portfolio/telario/telario-index.jpg"
image-header: "/assets/images/portfolio/telario/telario-cover.jpg"
image-paint: "/assets/images/portfolio/telario/telario-cover.jpg"
og_image: "portfolio/telario/telario-index.jpg"
tags: [React, TypeScript, WebAssembly, SQLite, Docker, SVG, Wireframe, Product Engineering]
---

# Telario: il mockup c’è, il PNG no, la licenza neanche

**Telario è un editor indipendente per aprire, esplorare e modificare file `.bmpr` nel browser.** Nasce da un problema molto concreto del mio lavoro: il mio capo prepara i mockup con Balsamiq, io devo svilupparli, ma non ho a disposizione la stessa licenza. Quando arriva soltanto il progetto e manca l’esportazione in immagine, il lavoro si ferma su una domanda apparentemente piccola: come leggo quello che devo realizzare?

La soluzione organizzativa sarebbe chiedere il PNG. Poi ricordarlo. Poi ricordarlo con una formulazione leggermente più diplomatica. Ho preferito affiancare a quella conversazione uno strumento: un’app che restituisce accesso al contenuto, permette correzioni essenziali e produce esportazioni utilizzabili. Il requisito iniziale non era rivoluzionare i wireframe. Era cominciare a lavorare senza aspettare un altro allegato.

Oggi il progetto comprende un editor web funzionante, una prova pubblica senza account, l’avvio locale con Docker, un’identità visiva originale e un sito bilingue. **La versione desktop Electron è una proposta futura documentata: non è ancora sviluppata e non esiste un installer da scaricare.** L’uso locale è già disponibile con gli strumenti attuali; Electron dovrà renderlo più immediato per chi non vuole usare un terminale.

- **Prova l’app:** [telario.antoniotrento.net](https://telario.antoniotrento.net/).
- **Sito del progetto:** [Telario, versione italiana](https://telario.github.io/it/).
- **Codice e istruzioni:** [repository pubblico su GitHub](https://github.com/telario/telario).
- **Evoluzione desktop:** [roadmap Electron archiviata nel progetto](https://github.com/telario/telario/blob/main/docs/roadmap/desktop-electron.md).

## Il problema: ricevere un file non significa poterlo usare

Un passaggio di consegne può risultare completo per chi lo prepara e incompleto per chi lo riceve. L’autore vede schermate, testi e relazioni. Il destinatario vede un’estensione che richiede uno strumento non disponibile. Nel mezzo c’è una dipendenza: una licenza, una conversione o una persona che deve trovare il tempo di esportare il documento.

Questa asimmetria produce un costo che non compare nella dimensione del file. Si perde tempo a ricostruire il contesto, si interrompono altre attività e si rinvia una decisione che avrebbe richiesto pochi minuti. Quando l’immagine arriva, spesso serve ricordare quale dettaglio volevamo verificare. La scadenza, invece, è rimasta perfettamente accessibile dall’inizio.

Ho trattato questa situazione come un problema di prodotto: quale azione minima permette al destinatario di proseguire? La prima risposta è leggere il documento. La seconda è estrarre ciò che serve. Solo dopo viene l’editing. Questo ordine ha guidato il perimetro dell’app e impedito che una necessità personale diventasse subito il tentativo di ricostruire ogni funzione del programma originale.

## Un progetto personale con un perimetro verificabile

Telario non è affiliato a Balsamiq e non fornisce una licenza per il prodotto originale. Interpreta in modo indipendente dati di progetto e li rappresenta con un proprio sistema grafico. Il valore sta nella possibilità di consultare il contenuto e compiere alcune operazioni utili, sapendo quali dettagli richiedono ancora confronto e verifica.

Ho scelto di presentarlo come prima versione funzionante. Alcuni controlli sono approssimati, certe strutture avanzate rimangono segnaposto e il salvataggio nel formato `.bmpr` è sperimentale. Queste informazioni non sono nascoste in una nota marginale: fanno parte delle istruzioni, del sito e del percorso di utilizzo. Un piccolo strumento è più utile quando la fiducia che chiede è proporzionata alle prove disponibili.

Il repository è pubblico e permette di leggere il codice e la documentazione. Questo non equivale automaticamente ad assegnare al progetto una licenza generale già scelta. Le dipendenze mantengono le proprie condizioni e attribuzioni; la distribuzione dell’applicazione richiede una decisione separata. Anche questa distinzione rientra nel lavoro: rendere consultabile un progetto e descriverne correttamente lo stato sono responsabilità collegate.

## Dal database alla pagina: leggere il contenitore prima dei pixel

Il `.bmpr` viene trattato come un archivio SQLite. L’app legge informazioni di formato, risorse e dati delle pagine, poi interpreta i controlli necessari a costruire una rappresentazione. Il wireframe visualizzato è il risultato di questa interpretazione: non è semplicemente un’immagine estratta da un contenitore con un altro nome.

Questa struttura rende importante conservare più informazione di quella immediatamente utilizzata dall’interfaccia. Il lettore mantiene i byte originali e i JSON grezzi. Se una proprietà non è gestita dal pannello di modifica, non significa che debba sparire dall’archivio. Il modello conosciuto dall’app è un sottoinsieme del documento, non una dichiarazione che tutto il resto sia inutile.

Gli schemi osservati includono le versioni 1.2 e 2.0. La compatibilità con un archivio concreto va comunque provata, soprattutto quando contiene simboli, varianti o controlli avanzati. Il limite di apertura è 100 MB: una soglia d’ingresso, non una garanzia che ogni progetto vicino a quella dimensione sia altrettanto fluido su ogni macchina. Lettura, interpretazione e prestazioni restano domande distinte.

## SQLite e WebAssembly nel browser

Il cuore della lettura usa sql.js e il relativo modulo WebAssembly. Il browser riceve l’applicazione, inizializza SQLite e apre il database in memoria. Non serve un server di database dedicato, né una connessione a un servizio remoto incaricato di convertire il progetto. Le query e la costruzione del modello avvengono nell’ambiente che l’utente sta già usando.

L’architettura ha una conseguenza precisa: il contenuto del file selezionato non viene inviato dall’editor al server. Questo vale anche nella prova online. Il server consegna HTML, JavaScript, CSS e WebAssembly; il documento viene letto sul dispositivo del visitatore. Le schede mantengono progetti indipendenti e non esiste un archivio condiviso fra utenti della demo pubblica.

Locale non significa però privo di costi o automaticamente persistente. Database, modello e cronologia occupano memoria sulla macchina dell’utente. La scheda può mostrare tutte le modifiche e non averne conservato una copia durevole. Per questo il prodotto distingue elaborazione locale, cronologia della sessione ed esportazione. L’utente deve poter capire dove lavora il programma e dove si trova effettivamente il risultato che potrà riaprire domani.

## Una base React con responsabilità separate

L’interfaccia è sviluppata con React e TypeScript. Ho separato lettura e scrittura del formato, modello dei dati, geometria, rendering, cronologia, esportazioni e interazioni. La divisione serve a rendere più controllabili i cambiamenti: aggiungere una corrispondenza per un’icona non dovrebbe alterare il writer, così come cambiare un pannello non dovrebbe riscrivere la geometria del progetto.

| Area | Responsabilità |
| --- | --- |
| `src/io` | Lettura, copia e salvataggio dell’archivio SQLite |
| `src/model` | Pagine, controlli, proprietà e trasformazioni geometriche |
| `src/render` | Rappresentazione SVG e stile sketch |
| `src/editor` | Cronologia delle operazioni e undo/redo |
| `src/export` | Produzione dei formati di uscita |
| `src/ui` | Canvas, selezione, pannelli e comandi |

Non considero questa struttura una garanzia automatica contro le regressioni. È un modo per localizzare responsabilità e scegliere controlli pertinenti. Quando un risultato cambia, posso chiedere se la differenza nasce dai dati letti, dalla trasformazione, dal disegno o dall’esportazione. La stessa domanda diventa poi utile nel supporto: una segnalazione precisa può isolare un caso piccolo invece di trascinare con sé un intero progetto aziendale.

## Il canvas SVG e la scelta di una grafica indipendente

I controlli vengono disegnati in SVG, con coordinate e trasformazioni riferite alla pagina. Questo rende leggibili gli elementi e permette di riutilizzare la rappresentazione per l’esportazione vettoriale. Lo stile sketch opzionale è affidato a rough.js. La modalità visiva non cambia la natura del documento e non pretende di riprodurre esattamente il tratto del software originale.

Font di sistema e forme indipendenti comportano differenze possibili nella composizione. Una variazione di spaziatura può essere irrilevante quando devo recuperare un’etichetta e importante quando sto discutendo l’allineamento di una schermata. La validità della vista dipende anche dalla domanda che sto cercando di risolvere. Ho quindi reso esplicita la distinzione fra leggibilità del contenuto e fedeltà grafica.

I gruppi sono spostabili e ridimensionabili come blocchi, ma i singoli figli non sono modificabili dall’interfaccia. Tabelle, testo ricco, curve e controlli complessi possono avere una resa approssimata. Quando una struttura non è risolta, il segnaposto deve restare riconoscibile. Mostrare un dubbio è preferibile a disegnare una forma plausibile che invita l’utente a fidarsi di un’interpretazione non verificata.

## Editing essenziale, pensato per rimettere in moto il lavoro

Il percorso operativo comincia dal selettore file o dal trascinamento del progetto. L’utente può esplorare le pagine, rinominarle, crearne di nuove e gestire il cestino reversibile. Sul canvas sono disponibili selezione singola, selezione multipla con Maiusc e rettangolo di selezione. Il pannello proprietà e il doppio clic sui testi permettono modifiche senza dover manipolare direttamente i dati grezzi.

Spostamento, ridimensionamento con otto maniglie, duplicazione, eliminazione, copia e incolla interni, allineamento e ordine di sovrapposizione coprono le correzioni più frequenti. La cronologia supporta annulla e ripeti fino a cento operazioni. Zoom, adattamento della pagina e spostamento della vista aiutano a orientarsi, soprattutto quando un diagramma supera lo spazio visibile iniziale.

L’obiettivo non è riempire la schermata di comandi. È permettere una proposta concreta: cambiare una parola, riposizionare un elemento o esportare una vista da discutere. Il fatto che una correzione sia facile non la rende automaticamente una revisione approvata. Per questo il flusso deve distinguere il documento ricevuto, la proposta locale e la copia verificata che viene eventualmente restituita all’autore.

## Le icone: dal punto interrogativo a un catalogo documentato

Una delle prime prove reali ha mostrato piccoli riquadri con un punto interrogativo. Non erano contenuti creati dall’autore: il renderer iniziale riconosceva soltanto poche icone. I dati contenevano nomi validi, ma l’app non aveva ancora un tracciato per rappresentarli. Il problema era nella copertura grafica, non necessariamente nell’integrità del documento.

Ho verificato la raccolta d’origine e integrato 2.060 varianti di Font Awesome Free 6.7.2, con alias e corrispondenze storiche. L’integrazione usa i metadati ufficiali e conserva licenze e attribuzioni. Non include il catalogo Pro. Un nome moderno esatto ha precedenza sugli alias, perché una regola storica troppo generica potrebbe trasformare un identificativo già corretto in un simbolo diverso.

Alcune richieste di stile vengono sostituite con una variante Free dello stesso soggetto. Per esempio, `database-regular` viene rappresentato con `database-solid`. Il valore originale del documento rimane invariato. Questa scelta aumenta l’utilità nella lettura senza dichiarare un’identità visiva inesistente. Il catalogo risolve molti casi, ma non garantisce ogni icona personalizzata o ogni variante usata in qualunque versione del prodotto originale.

## Sei esportazioni, sei destinazioni del lavoro

Una consegna utile non richiede sempre un nuovo archivio editabile. SVG e PNG permettono di condividere la pagina come immagine; Markdown recupera i testi di tutte le pagine; JSON rende disponibili i dati per l’ispezione. Mermaid e draw.io cercano di ricostruire una struttura di diagramma da portare in altri strumenti. Le uscite rispondono a esigenze diverse e non sono copie equivalenti del progetto.

I collegamenti di Mermaid e draw.io vengono dedotti dalla vicinanza degli estremi e vanno controllati. Un rapporto visivo fra forme e frecce non coincide sempre con un collegamento semantico esplicito. Il PNG viene limitato a 8192 pixel per lato e circa trentadue megapixel, con possibile riduzione delle pagine molto grandi. La verifica deve quindi riguardare il file prodotto, non soltanto il successo del download.

Per chi sviluppa, la scelta più utile può essere molto semplice: esportare una schermata, indicare il testo da confermare e proseguire. Per un’analisi del diagramma serve un confronto più attento. Il formato di uscita va scelto dal passo successivo, non dal desiderio di usare tutte le opzioni disponibili. Un buon export riduce il lavoro del destinatario invece di aggiungere un’altra conversione da comprendere.

## Salvataggio .bmpr: conservazione prima delle promesse

Il writer restituisce gli stessi byte originali quando non ci sono modifiche. Quando il progetto cambia, lavora su una copia in memoria, aggiorna le pagine interessate in una transazione e controlla l’integrità SQLite. Risorse, campi sconosciuti e strutture non modificate non vengono ricostruiti indiscriminatamente a partire da ciò che l’interfaccia comprende.

Questo comportamento offre criteri concreti di verifica, ma non certifica automaticamente la riapertura in ogni versione di Balsamiq. Un database integro è un contenitore coerente; la compatibilità applicativa richiede anche che il programma destinatario interpreti correttamente le risorse. Le miniature incorporate vengono conservate senza essere rigenerate e possono mostrare uno stato precedente. Per alcuni schemi con colonne obbligatorie sconosciute, il writer preferisce rifiutare una nuova pagina anziché inventare valori.

Il download della copia richiede l’attivazione esplicita del salvataggio sperimentale. L’originale deve essere conservato e la copia verificata prima di entrare nel flusso condiviso. Non considero questa cautela un ostacolo all’utilità: consultare, correggere una proposta ed esportare immagini restano attività preziose anche quando la scrittura nel formato originale richiede ancora ulteriori prove.

## La prova pubblica e l’alternativa locale

L’app è disponibile su [telario.antoniotrento.net](https://telario.antoniotrento.net/) senza registrazione. Il dominio raggiunge un tunnel Cloudflare dedicato e quindi il container Nginx che serve l’applicazione. Il sito di presentazione vive invece su GitHub Pages. Separare i due ambienti permette di aggiornare il racconto del progetto senza confonderlo con il servizio che esegue l’editor.

Il percorso pubblico è comodo per una prima prova: aprire la demo sintetica, navigare fra le pagine e verificare i comandi. Non introduce collaborazione o salvataggio remoto. Ogni scheda mantiene il proprio stato e i file selezionati vengono elaborati dal browser. Il servizio dipende dalla disponibilità della macchina che lo ospita e può essere temporaneamente indisponibile durante manutenzione o riavvii.

Per l’uso locale è già possibile avviare Docker Compose e aprire l’app su `localhost:8080`. In alternativa esiste l’ambiente di sviluppo Node e Vite. Dopo il build, l’editor non richiede CDN o servizi esterni per elaborare i documenti. La scelta fra prova pubblica e avvio locale riguarda la distribuzione degli asset; non cambia l’obiettivo di mantenere l’elaborazione del progetto sul dispositivo dell’utente.

## Test e qualità: misurare il comportamento che conta

Ho affiancato test del modello, regressioni del renderer e prove browser sulle interazioni principali. I controlli coprono geometria, cronologia, duplicazione, pagine, esportazioni e percorsi di salvataggio con documenti sintetici. Per le icone, ogni variante inclusa viene confrontata con la propria geometria, insieme ai casi di alias e sostituzione. La presenza di un tracciato, da sola, non prova che sia quello giusto.

La prova pubblica è stata verificata con una sessione anonima: apertura della demo, modifica di testo, esportazioni SVG e PNG e nuova scheda indipendente. Nel percorso osservato non sono emerse richieste di scrittura del documento o errori JavaScript. Le verifiche su archivi reali rimangono locali: un problema tecnico non richiede di pubblicare il mockup del cliente che lo ha fatto emergere.

Questi risultati sono evidenze su percorsi definiti, non una garanzia assoluta sull’assenza di regressioni. Il documento di validazione raccoglie anche i limiti. Per una nuova struttura cerco il caso minimo riproducibile, con dati sintetici quando possibile. Una buona segnalazione distingue ciò che il file contiene, ciò che l’app mostra e ciò che l’esportazione produce. Questo rende la manutenzione più precisa e meno dipendente dal ricordo di una sessione particolare.

## Identità visiva e sito del progetto

Il marchio Telario riprende una finestra e una griglia, con un elemento arancio che si stacca dalla struttura. Il petrolio `#173D4D` dà continuità al sistema, l’arancio `#F47847` introduce il gesto operativo. Il nome richiama un telaio: elementi diversi che vengono tenuti insieme per rendere leggibile una struttura. La grafica accompagna il problema senza appoggiarsi all’identità del prodotto con cui viene confrontata.

Il sito presenta il progetto in italiano e inglese, con tema chiaro e scuro, preferenza memorizzata e rispetto della scelta di sistema al primo accesso. Comprende funzionamento, compatibilità, avvio e un taccuino con quattro approfondimenti per lingua. Le copertine editoriali condividono palette e materiali visivi; le schermate tecniche pubblicate usano la demo sintetica, non documenti aziendali.

Per questa pagina portfolio ho mantenuto il logo ufficiale a colori su fondo chiaro, con proporzioni e margini pensati per anteprima e copertina. Non serve ridisegnare il simbolo a ogni pubblicazione. Il lavoro sull’identità consiste anche nel preservarne la riconoscibilità fra app, sito e presentazione personale, lasciando alle immagini abbastanza spazio perché il marchio non sembri né minuscolo né schiacciato ai bordi.

## Evoluzione futura: Telario Desktop con Electron

La prossima evoluzione proposta è un’app desktop Electron. **È una direzione archiviata per il futuro, non una funzione disponibile oggi.** Non ho aggiunto dipendenze Electron, creato un processo principale o preparato un installer. Ho registrato obiettivi, perimetro e criteri di accettazione nel repository, così il lavoro potrà ripartire da una base esplicita anziché da una promessa lasciata nel testo del sito.

L’obiettivo è usare Telario localmente senza installare Docker o Node e senza dipendere dal dominio della prova pubblica. La build dell’editor, WebAssembly, icone e altre risorse dovranno essere incluse nel pacchetto. Aprire una finestra che carica semplicemente il sito remoto non soddisferebbe il requisito: il prodotto desktop dovrà essere provato anche senza rete dopo l’installazione.

La base React e il motore dei documenti dovranno rimanere condivisi. Il livello desktop potrà gestire finestre, dialoghi e ciclo di vita, evitando di duplicare parser, renderer e writer. L’accesso nativo ai file richiederà un confine ristretto e verificabile: l’interfaccia non deve ottenere accesso generico al filesystem o alla shell soltanto perché ora gira dentro un programma installato.

La prima piattaforma proposta è Windows, coerente con l’ambiente di lavoro attuale, ma la scelta andrà confermata alla ripresa. Anche packaging, firma e canale di distribuzione restano decisioni future. La prima prova dovrà dimostrare avvio offline, caricamento corretto di SQLite e degli asset e comportamento coerente delle esportazioni. Solo dopo avrà senso estendere il percorso a dialoghi nativi e installer.

Electron non renderà automaticamente più fedele il formato `.bmpr`, né aggiungerà autosalvataggio persistente o collaborazione. Queste capacità richiederebbero evolutive separate. La promessa del desktop è semplificare accesso e distribuzione mantenendo i confini già dichiarati. Quando esisterà un pacchetto verificato, la documentazione potrà presentarlo come risultato. Fino ad allora resta una roadmap concreta, con una distinzione netta fra ciò che funziona e ciò che voglio costruire.

## Cosa dimostra Telario nel mio lavoro

Questo progetto raccoglie lettura di formati strutturati, interfacce interattive, rendering vettoriale, conservazione dei dati e distribuzione di un’applicazione. Il punto di partenza personale non ha ridotto l’attenzione tecnica: l’ha resa più mirata. Una funzione deve giustificarsi rispetto a un blocco reale e avere un comportamento che posso spiegare, ripetere e confrontare.

Mi interessa in particolare il confine fra capacità disponibile e aspettativa dell’utente. Un file che si apre non certifica il salvataggio; un catalogo ampio non equivale a ogni variante possibile; una scheda con undo non è un archivio permanente. Rendere visibili queste differenze è una parte della progettazione, non soltanto un’aggiunta alla documentazione. È ciò che permette a una persona di usare lo strumento per il compito adatto senza affidargli implicitamente altro.

Telario mostra anche un percorso completo di prodotto: problema, perimetro, implementazione, identità, prove, istruzioni e presentazione. Il sito e questa pagina portfolio non sostituiscono il codice; aiutano a capire perché esiste e dove guardare per valutarlo. La futura evoluzione desktop nasce dallo stesso criterio: rimuovere un ulteriore attrito, questa volta nell’installazione, senza scambiare il packaging per una nuova applicazione già realizzata.

## Provarlo con un obiettivo preciso

Il modo più semplice di iniziare è [aprire l’app online](https://telario.antoniotrento.net/) e scegliere la demo. Sposta un elemento, cambia un testo e scarica un’immagine. Poi confronta il risultato fuori dall’editor. È una prova breve che mostra il percorso principale senza coinvolgere documenti privati o chiederti di fidarti di una descrizione astratta.

Per un progetto reale, conserva l’originale e controlla una pagina conosciuta prima di proseguire. Leggi i [limiti di compatibilità](https://telario.github.io/it/compatibilita/) e scegli l’esportazione in base alla consegna che devi preparare. Il [repository](https://github.com/telario/telario) contiene istruzioni, struttura del codice e risultati delle verifiche; la [roadmap desktop](https://github.com/telario/telario/blob/main/docs/roadmap/desktop-electron.md) conserva separatamente la proposta Electron.

Il risultato che cerco rimane molto concreto: il documento si apre, il contenuto diventa leggibile e posso tornare al lavoro. Il PNG può ancora arrivare dopo. Nel frattempo, finalmente, non è l’unico modo per andare avanti.
