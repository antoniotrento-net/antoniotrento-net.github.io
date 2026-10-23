---
layout: portfolio
title: "Nesso"
date: 2026-10-23
description: "Motore fra un sistema esterno e EspoCRM. Canale, scheda, campi. Solo le API di Espo. Repository pubblico e sito del prodotto."
image: "/assets/images/portfolio/nesso/nesso.jpg"
image-header: "/assets/images/portfolio/nesso/nesso.jpg"
image-paint: "/assets/images/portfolio/nesso/nesso.jpg"
tags: [EspoCRM, Integrazione, Python, Docker, API, Jekyll, Open Source]
---

**Repository:** [github.com/nessocrm/nessocrm](https://github.com/nessocrm/nessocrm){: target="_blank"}

**Sito:** [nessocrm.github.io](https://nessocrm.github.io/it/){: target="_blank"}

Nesso porta i record fra un sistema esterno e EspoCRM. Si scelgono il canale, la scheda e l'abbinamento dei campi. Da lì lo stesso motore sposta i record. Il passaggio verso Espo usa solo le API HTTP di Espo. Non è un secondo CRM e non ha il nome di un gestionale scritto nel codice.

Questa pagina è il caso, non la brochure. Il sito del prodotto spiega le decisioni a chi arriva da fuori. Il manuale, nella cartella `docs` del repository, cambia insieme al codice ed è la fonte se una frase di qui e una frase di là divergono. Qui racconto perché il confine è fatto così, che cosa un giro di notte fa davvero, e che cosa ho lasciato spento di proposito.

---

## Il problema che vale la pena di risolvere

In un'azienda che ha già Espo, le anagrafiche non nascono nel CRM. Nascono in un file di notte, in una tabella di un altro database, in un webhook di un sito, in un PDF il cui nome contiene il codice dell'azienda. Qualcuno, di solito con uno script scritto una volta e mai più riletto, le copia dentro Espo. La prima notte lo script funziona. Il comando esce con codice zero. Il lunedì il file ha una riga in meno, una cella svuotata e una nota che il commerciale ha scritto venerdì sul record. Lo script non sa niente di quella nota. La svuota, oppure lascia il record orfano, e nessuno sa più quale dei due testi è quello vero.

L'alternativa peggiore è la query sulle tabelle di Espo. È veloce, salta i team, la storia e gli hook, e il giorno in cui Espo cambia uno schema si rompe in silenzio: la colonna c'è ancora, il significato no. L'alternativa comoda è un secondo prodotto che tiene le anagrafiche «di qua» e poi le rincorre «di là». La verità si sdoppia. Il lunedì mattina si sceglie a sentimento.

Nesso è il rifiuto di queste tre scorciatoie. Espo sta sempre da una parte. Dall'altra c'è un canale. In mezzo ci sono due oggetti, non uno: il collegamento e l'integrazione. Il collegamento è il canale, con il suo indirizzo e il suo modo di autenticarsi. L'integrazione è la regola: quale scheda, quale colonna è l'identità, quale campo finisce dove, di chi è il padrone di quel campo, ogni quanto parte il giro. Un'integrazione ha un solo collegamento. Un collegamento può averne più d'una. Due file sulla stessa scheda Account non si mescolano, perché la chiave contiene l'identità dell'integrazione.

Il nome del sistema esterno non entra nel codice. Se entrasse, ogni cliente nuovo sarebbe una modifica del programma. Invece ogni cliente nuovo è una configurazione. Il canale può essere un CSV, un Excel, un SFTP, un FTPS, un webhook, una SELECT in sola lettura, un PDF, un documento, oppure un HTTP in uscita. MySQL, MariaDB, Postgres, SQL Server e Oracle sono letture, non scritture sulle tabelle di Espo. La direzione segue il canale. Un collegamento HTTP esce da Espo. Gli altri entrano. Cambiare direzione significa cambiare collegamento, non spuntare una casella nascosta.

## Due oggetti, e perché non basta uno

Ho tenuto separati collegamento e integrazione perché un file di anagrafiche e un file di sedi sono due mestieri anche quando arrivano dalla stessa cartella. Se finissero nella stessa regola, la colonna identità sarebbe una sola: un codice sede verrebbe letto come un codice cliente, o il contrario. Con due integrazioni, la chiave dell'anagrafica contiene l'id della prima, la chiave della sede contiene l'id della seconda. Entrambe possono vivere su Account. Non si sovrascrivono, perché la chiave intera è diversa anche quando, per caso, il valore esterno è la stessa stringa.

Il collegamento può essere lo stesso, se i due file arrivano dallo stesso SFTP. Può essere diverso, se le anagrafiche arrivano da un CSV e le sedi da una SELECT. L'integrazione non eredita la direzione da un'opinione: la eredita dal collegamento a cui è attaccata. Attaccare l'integrazione delle sedi a un collegamento HTTP la farebbe uscire da Espo, non entrare. È un errore di configurazione visibile, non una sorpresa scritta in un commento.

Chi installa le accende una alla volta. Prima le anagrafiche, con l'anteprima. Poi le sedi, con l'anteprima. Il numero in home, quello delle anagrafiche allineate, conta i giri in ingresso verso Account. Un successo delle sedi non va scambiato per il successo del file clienti, e un fallimento del file clienti non va coperto da un giro di sedi andato a buon fine la stessa mattina. Il numero è uno. I giri sono tanti. Il numero ha il diritto di comparire solo se il giro di oggi verso Account, in ingresso, è riuscito. Un successo di ieri non viene presentato come oggi.

## Il file di stanotte, come filo di tutto il caso

Per non parlare a vuoto uso lo stesso file in tutto il racconto. È un CSV di anagrafiche. Ha una colonna con il codice esterno, una con il nome, una con la città, una con la partita IVA, una con una nota. Il codice esterno è l'identità. Nome, città e partita IVA sono campi della sorgente. La nota, in questa integrazione, ha come padrone Espo, perché una persona del commerciale la scrive sul record e il file di notte non deve cancellarla.

Nel file di questa notte ci sono tre casi che bastano a vedere il giro, più un quarto che il file non mostra e che è il più importante.

La riga del codice C014 è identica all'ultima volta. L'hash della riga è già quello salvato. Espo non viene richiamato. Non c'è un aggiornamento da fare e non c'è un motivo per toccare il record. Un secondo invio identico non duplica e non riscrive. Questo è il comportamento che uno script non ha: lo script riscrive anche ciò che non è cambiato, e chiama Espo per niente.

La riga del codice C001 non c'è ancora su Espo. Il giro la prepara come un Account nuovo. Nel racconto il nome è Nord Est e la città è Trieste. La chiave che nascerà sulla scheda standard è fatta dall'id dell'integrazione, due punti, e C001. Sulle schede che Espo ha già, il campo si chiama `cExternalKey`. Sulle schede create da Nesso si chiama `externalKey`. La nota, in creazione, si scrive lo stesso se il file la porta: il record non esiste ancora, e non c'è una nota di una persona da proteggere. Dal giro successivo il padrone conta.

Una riga, la diciottesima del racconto, non ha una colonna obbligatoria. Il file non si sposta fra gli elaborati. Lo scarto è uno solo, di file, non una coda di righe. Le altre righe non vengono fatte passare a metà. Manca invece una cella, e la colonna c'è: si scarta quella riga, e le altre proseguono. Sono due errori diversi. Il primo dice che il file non è quello atteso. Il secondo dice che una riga è incompleta. Trattarli allo stesso modo farebbe o bloccare tutto per una cella, o caricare un file troncato come se fosse intero.

Il quarto caso è la riga che ieri c'era e stanotte non c'è più. Il record su Espo si chiude e resta nello storico. Non si cancella. Non è l'oblio. La prima volta che un giro chiuderebbe dei record, chiede conferma: un file troncato non chiude l'elenco da solo, senza che qualcuno lo veda. Se la riga torna, il record si può riaprire. Chiudere è un gesto di stato. Cancellare è un altro mestiere, e non è questo.

## La chiave, l'hash e il cursore

L'identità è una convenzione unica: id dell'integrazione, due punti, valore esterno. Due integrazioni sulla stessa scheda non si pestano i piedi, perché la chiave contiene l'integrazione. Sulle schede standard il campo è `cExternalKey`. Se la scheda non esiste, Nesso può crearla via API. Si indicano il singolare e il plurale. Espo mette il prefisso C. I campi della scheda nuova non ricevono un secondo prefisso. La chiave, lì, si chiama `externalKey`. Una scheda creata qui è una scheda Espo. La vede chi ha il team. Non è un archivio parallelo.

In ingresso il sistema esterno consegna una riga: una chiamata, una SELECT, un file. Se l'hash è già quello salvato, Espo non viene richiamato. Se la chiave c'è già, è un aggiornamento. Se non c'è, è una creazione. L'hash è la memoria dell'ingresso. Serve a non riscrivere il mondo ogni notte.

In uscita il cursore ricorda l'ultimo `modifiedAt` e l'id Espo. Il giro legge pagine da cinquanta e manda solo i campi abbinati. Il cursore avanza solo dopo i POST riusciti. Se manca la chiave esterna, il pull si ferma: i record dopo non escono. Sono due memorie diverse. Confonderle è il modo in cui un caricamento riscrive tutto, o un'uscita rimanda gli stessi record all'infinito. Un secondo giro in uscita, se in Espo nessuno ha toccato quei record, esporta zero. È il segno che il cursore ha capito.

La cadenza è a mano, cinque minuti, quindici, un'ora, o un orario fisso, per esempio le 02:10. Un'integrazione in pausa viene saltata dal pianificatore e dal webhook. Esegui ora no: quello parte perché una persona lo ha chiesto. I quindici minuti sono provati con un orologio finto: un secondo prima non parte, allo scadere parte una volta, e non riparte nello stesso minuto. Non è un quarto d'ora osservato sul contenitore.

La stessa integrazione non parte due volte. La seconda riceve che un'esecuzione è già in corso. Due integrazioni diverse possono girare insieme. Se una è già in corso, il pianificatore la salta e non scrive un errore ogni trenta secondi. Dopo un errore l'orologio si aggiorna e si aspetta l'intervallo intero. Solo con `retry_failed` acceso l'orologio resta fermo, e il giro può ripresentarsi prima. Il default è l'attesa intera. Un errore non è un invito a martellare Espo.

In home, un file atteso entro un'ora accende il bordo se quell'ora passa senza un giro riuscito. Un file già in elaborati non viene riletto. Un avviso di giro fallito si accende una volta, con il nome dell'integrazione. Il giornale resta nella lingua del giro. La pagina può essere in italiano o in inglese. Il giornale no: è il verbale di quell'esecuzione, non una brochure da riallineare.

Se Espo rifiuta perché esiste già un record simile con un'altra chiave, la riga viene scartata. Si può dire all'integrazione di adottare quel record. Non è il default. Una data illeggibile non inventa un giorno. Le date si leggono in tre formati. Un elenco, se il campo nuovo è un elenco, deve avere almeno un valore. Un telefono italiano diventa `+39`. L'errore di Espo, se nomina un campo, riporta quel nome.

## La cella vuota e il padrone del campo

Di default vince la sorgente, anche se la cella arriva vuota. Se il file di stanotte porta la città vuota, la città su Espo diventa vuota. È fastidioso ed è corretto. Lo svuotamento non è un effetto collaterale su tutta la scheda. Vale sui campi che la sorgente possiede. Un campo non abbinato non viene toccato.

Si può dire che un campo è di Espo. Una nota scritta da una persona resta. Se il file porta un valore diverso, quel valore finisce in una coda da guardare. Il campo su Espo non cambia. La coda non è un secondo CRM e non scade in una scrittura automatica. È un contrasto, su un campo, per una chiave. Chi la apre vede che cosa c'è oggi e che cosa è arrivato. Una cella vuota sulla nota, se il padrone è Espo, non alimenta quella coda: il vuoto è già stato deciso, e non va confermato al mattino per salvare la frase.

In creazione il campo di Espo si scrive lo stesso. Non esiste ancora una nota da proteggere. Dal giro dopo, il padrone conta. Il badge sul record dice chi ha scritto per ultimo. Non è una cronologia legale. È il segno dell'ultimo giro che ha toccato il record, utile a chi deve capire se la riga è ancora quella del file o se qualcuno in Espo l'ha corretta.

La visibilità è una regola di Espo: questa riga è del team Vendite, assegnata a questa persona. Il team e la persona arrivano da una colonna o da un team fisso. Nesso non inventa un permesso fuori da Espo. Gli utenti di Espo non si creano da un'anagrafica. Una colonna di nomi non diventa un elenco di login. Creare un utente è un gesto di amministrazione, con una password e un ruolo. Un file di clienti non ha quel gesto dentro.

## Chi legge lo stesso giro

Quattro persone guardano lo stesso file e non cercano la stessa cosa. Non sono personaggi di una brochure. Sono i ruoli che, in un'azienda con Espo e un altro sistema, devono dire sì.

Chi tiene il numero guarda la home. Vuole un solo numero: le anagrafiche allineate oggi, e il saldo se c'è un importo. Vale solo se il giro di oggi è riuscito. È un controllo. Non scrive.

Chi ha la nota è la persona del commerciale. Il campo della nota ha come padrone Espo, così il file di notte non la svuota. Il badge dice chi ha scritto per ultimo.

Chi controlla apre l'anteprima. Vede una partita IVA già presente prima che il giro scriva. Può annullare quello che il giro ha scritto. La prima chiusura dei record spariti chiede conferma proprio qui: un file troncato non chiude l'elenco da solo.

Chi installa fa quattro passi: collegamento, scheda, abbinamento, giro. La ricetta è un punto di partenza da rivedere, non un connettore certificato. Il piano di accensione dice che cosa resta spento. La pagina di consegna non contiene le password.

## Quello che esiste e resta spento

La scrittura di ritorno è spenta finché non la si accende. Accesa, scrive solo le colonne nominate. Non riscrive il file intero e non inventa colonne. Non è il cursore HTTP. Il cursore manda i campi abbinati a un endpoint. La scrittura di ritorno scrive sulla sorgente da cui la riga è arrivata. Tenerla spenta è la scelta di default, perché il ritorno non deciso è il modo in cui un caricamento diventa, senza che nessuno l'abbia detto, una scrittura sul gestionale.

La coda di ritento è spenta. L'uscita HTTP ha già i suoi tentativi nel cursore, e non va rimessa in coda. Accesa, la coda riguarda solo una riga in ingresso che ha un'identità esterna, e non nello stesso giro: la prossima volta è almeno un minuto dopo. Un'identità vuota è uno scarto di file e non entra in coda. Se un tentativo fallisce, i tentativi aumentano e l'attesa cresce, con un tetto di un giorno, e dopo otto tentativi quella riga di coda diventa scarto. Il default spento significa una cosa pratica: il ciclo che scarta non scrive una seconda volta attraverso la coda. `retry_failed` è un altro interruttore, e riguarda l'orologio dell'integrazione intera dopo un errore del giro. Accendere l'uno non accende l'altro.

Il filtro del portale è spento. Non chiama le API dei ruoli del portale e non crea utenti del portale. Acceso, in uscita salta i record di altri team. Una chiave mancante ferma il pull lo stesso. Spento, la select e l'elenco dei record non cambiano. Il portale di Espo non si amministra da qui.

Senza la variabile `NESSO_SECRET_KEY` la password del collegamento resta in chiaro nel volume SQLite del motore. La prova non imposta la variabile. Con la variabile, un salvataggio nuovo viene sigillato, con il prefisso `enc1:`. Una riga vecchia in chiaro si apre ancora. Togliere la variabile dopo il sigillo significa che quel collegamento non si apre finché la password non viene riscritta. I segreti non entrano nella vista pubblica del collegamento e non entrano nello scarico della configurazione. Non ho migrato da solo le righe già salvate: un sigillo silenzioso all'avvio sarebbe stata una sorpresa, non una protezione.

L'anteprima mostra che cosa nascerebbe e che cosa cambierebbe, senza chiamare la scrittura. La modalità lettura e l'interruttore generale fermano le scritture. Un giro in lettura legge, confronta, e non manda il POST. Sono i freni. Stanno spenti nel senso che non cambiano un giro che già funziona, finché qualcuno non decide altrimenti. La prova pubblica non accende né la coda, né il portale, né il sigillo, né la scrittura di ritorno.

## Il modello, le ricette, e ciò che non passa di qui

Proponi l'abbinamento legge i nomi delle colonne, nella lingua della pagina, e propone il campo Espo, compresa la partita IVA se la scheda ha un campo fiscale. Una colonna non riconosciuta resta vuota, da compilare a mano. I sinonimi sono un elenco per lingua. Non escono in rete. Non salvano l'integrazione. La persona rivede e poi salva.

Completa le colonne vuote chiama un modello solo se un indirizzo è impostato. Riempie le colonne ancora vuote, fra i campi che la scheda conosce. Non tocca una colonna già abbinata. Non salva. La chiamata manda i nomi delle colonne, al massimo tre celle corte, e il nome del campo. Non manda la password del collegamento. L'indirizzo del modello non entra nello scarico. Senza indirizzo non parte nessuna chiamata, e la proposta per sinonimi resta. Il modello non sceglie il canale, non crea le schede, non accende la scrittura di ritorno. Non riscrive il giornale.

Le ricette di anagrafiche, contatti, sedi e listino sono quattro punti di partenza. Ognuna nomina una scheda e delle colonne. Non scrivono da sole e non certificano il sistema dall'altra parte. Il listino punta a Product. Se questa installazione non ha la scheda, i campi restano vuoti. La ricetta non inventa il catalogo. Meglio un abbinamento vuoto, visibile, che un Product fantasma creato per far tornare i conti di una slide.

La posta del CRM resta in Espo. Nesso non legge la casella e non spedisce. L'Advanced Pack non viene riscritto e non sta nel repository. Se qualcuno lo ha in locale, resta locale. I dump di produzione non si importano nell'Espo di prova. Non si montano, non si copiano gli allegati. Un Espo vuoto è la prova. Un dump è un'altra cosa: contiene persone, note e file che non hanno chiesto di finire su un portatile.

Non esiste un giro senza Espo. Il prodotto non è un ponte generico fra due sistemi qualsiasi. Togliere Espo da una parte e mettere qualunque cosa dall'altra farebbe un altro programma. Il canale può cambiare. Il lato Espo no.

## Come è fatto, senza aprire le tabelle

Il motore è Python, libreria standard più il driver per leggere il database esterno. Parla con Espo solo via HTTP, con l'header di autorizzazione che Espo si aspetta. La sua memoria sta in un file SQLite: collegamenti, integrazioni, hash, cursore, giornale. Quel file non è un secondo CRM. Le schede stanno in Espo. Lì, nel volume, vive il ricordo di quale riga è già stata vista e di quale record è già stato mandato.

La prova si alza con Docker Compose: il database, un Espo vuoto, il motore. Non c'è un installer e non c'è una lista d'attesa. Il repository è pubblico. Il sito non raccoglie email. Il contatto è il repository. La demo descritta nel manuale, il Gruppo Meridia, è la prova di un giro. Non è un secondo prodotto e non è un cliente pubblicato sul sito di Nesso. I quattro flussi da cui è nata l'idea — il sito, i file di notte, le anagrafiche, i lavori — non sono quattro programmi dentro Nesso. Diventano, se servono, delle configurazioni.

Il sito, su GitHub Pages, è un Jekyll bilingue. L'italiano e l'inglese dicono gli stessi fatti. Il diario ha quattro capitoli sullo stesso giro: il confine, la chiave, la cella vuota, gli interruttori spenti. Non sono storie di clienti. Sono il ragionamento delle decisioni già nel motore. Le figure sono WebP piccole. Il segno è quattro quadrati, i colori del tema, e in pagina si muovono: si spostano, spariscono, cambiano colore, tornano in quadrato. Sulla home il file entra da sinistra, passa dal segno, e a destra nasce il record.

## I canali, uno per uno

Un CSV entra. Si sceglie il separatore, si legge l'intestazione, si abbina. Un Excel entra allo stesso modo, foglio per foglio solo se il foglio è quello nominato. Un file già spostato fra gli elaborati non viene riletto: la cartella di arrivo non è un archivio da ripassare ogni quarto d'ora. SFTP e FTPS sono la stessa idea su un altro trasporto. Il file arriva, si legge, e se il giro riesce esce dalla coda di arrivo. Un file atteso che non arriva accende il bordo. Non inventa un file vuoto per far quadrare l'orologio.

Un webhook entra quando il sistema esterno chiama. L'integrazione in pausa viene saltata anche dal webhook: la pausa non è solo un'etichetta del pianificatore. Una SELECT entra in sola lettura. Il driver parla con MySQL, MariaDB, Postgres, SQL Server o Oracle, e legge. Non scrive su quelle tabelle e non scrive sulle tabelle di Espo. La frase «database» nel collegamento non autorizza un UPDATE. Un PDF entra se il nome del file contiene la chiave dell'azienda. Non è un lettore magico di ogni scansione: è un ingresso il cui contratto è il nome. Un documento segue la stessa logica di ingresso.

HTTP esce. Il cursore ricorda l'ultimo `modifiedAt` e l'id, pagina da cinquanta, e avanza solo dopo i POST riusciti. Manca la chiave esterna: il pull si ferma, e i record dopo non escono. Non è un buco da saltare. È il segnale che l'identità, da quel punto, non è più affidabile, e mandare il resto sarebbe mandare record senza nome.

Due canali non si mescolano in un'integrazione. Se le anagrafiche arrivano da SFTP e le sedi da una SELECT, sono due collegamenti e due integrazioni, anche se entrambi finiscono su Account. La chiave contiene l'integrazione. Il nome «Account» da solo non è un'identità.

## La prova, senza il dump

La prova è Compose. Tre servizi: il database, Espo, il motore. Espo parte vuoto. Non c'è un'anagrafica di un cliente vero, non c'è un allegato di produzione, non c'è un utente copiato da un'altra installazione. Admin e porte stanno nel manuale del repository, non in questa pagina, perché una pagina di portfolio non è il posto in cui si pubblicano credenziali, anche se sono quelle di un contenitore locale.

Il codice del motore non è montato come cartella viva nel contenitore. Una modifica al programma chiede una ricostruzione dell'immagine. È scomodo per chi sviluppa e giusto per chi prova: quello che gira è quello che è stato costruito, non un file cambiato a metà e dimenticato sul disco.

La suite di test sta nel repository, accanto al motore. Copre il carico, il giro, le frasi. Non sostituisce un clic sulla pagina. Un test verde dice che la chiave, l'hash, il cursore, la cella vuota, la chiusura, gli interruttori spenti e il sigillo si comportano come il manuale. Un test verde non dice che ogni etichetta della pagina sia già al posto giusto. Il manuale lo scrive. La pagina, quando mente, va corretta. Non si corregge il manuale per far tornare una slide.

Sul sito pubblico non c'è un modulo. Non c'è una lista d'attesa. Non c'è un'email di contatto del prodotto. Chi vuole il codice apre il repository. Chi vuole leggere apre il sito. La prova la alza chi ha Docker, dal compose che sta nel repo. Non ho messo un attore di prova già acceso, con gli interruttori della coda, del portale e del sigillo, perché quegli interruttori spenti sono parte del prodotto, non un'omissione da riempire prima della demo.

## Il sito, e perché non è il manuale

Il sito è un Jekyll su GitHub Pages, italiano e inglese, con gli stessi URL di funzione dall'altra parte della lingua. Le pagine dicono le decisioni: come funziona, i canali, le ricette, l'architettura, il confine, i termini. Il diario ha quattro capitoli, oltre le quattromila parole l'uno in ciascuna lingua, sullo stesso giro di questa pagina. Non sono casi cliente. Se un capitolo e il manuale divergono, vale il manuale.

Le figure del diario sono WebP, 1280 per 720 e una versione a 640, perché una pagina di lettura non deve scaricare un PNG da diversi megabyte. Il segno è quattro quadrati. In testata si muovono: escono, spariscono, tornano con un altro colore, rientrano. Sulla home il file sta a sinistra, i quadrati al centro, il record a destra. Un gettone con il codice attraversa il segno. Il record compare quando il gettone è arrivato. Chi riduce il movimento vede il record fermo, senza l'attraversamento. L'animazione precedente, un terminale che non diceva che cosa fa il prodotto, è stata tolta dalla home e lasciata nel repository come archivio, non in pagina.

Il footer dice la stessa cosa del confine, in una riga con lo stesso corpo delle altre: non è un connettore certificato, è il motore, e da lì si arriva al confine e ai termini. La prima versione di quella frase stava fuori dallo stile. È stata chiusa nel riquadro. Un testo vero, messo nel posto sbagliato, sembra un bug anche quando la frase è giusta.

## Che cosa non ho scritto nel prodotto

Non ho scritto il nome di un gestionale nel codice, oltre a Espo, che è il lato fisso. Non ho scritto un connettore «certificato» per un'anagrafica tipo. Le ricette sono mappe da rivedere. Non ho scritto la creazione degli utenti a partire da una colonna. Non ho scritto la cancellazione come risposta a una riga sparita. Non ho scritto l'oblio. Non ho scritto la posta. Non ho portato l'Advanced Pack nel repository. Non ho acceso, nella prova, la scrittura di ritorno, la coda, il filtro del portale, il sigillo. Non ho messo un modulo sul sito.

Ognuna di queste assenze è una decisione, non un buco dimenticato a metà. Si può accendere ciò che ha un interruttore. Non si può, da questa pagina, far diventare Nesso un ponte fra due sistemi qualunque, né un lettore di casella, né un amministratore del portale. Chi cerca quello cerca un altro programma. Meglio dirlo qui, nel caso, che scoprirlo dopo aver clonato il repository.

## Il lunedì, che è il vero test

Uno script e Nesso si assomigliano la prima sera: le righe nuove diventano record. Il lunedì il file ha una riga in meno, una cella svuotata, una nota scritta a mano, e una persona che chiede se il sistema ha aggiornato. La risposta, con questo confine, è lunga e utile. I campi della sorgente sono quelli del file di stanotte, compresi i vuoti. I campi il cui padrone è Espo sono quelli lasciati dalla persona. I record la cui riga non c'è più sono chiusi, se qualcuno ha confermato la prima chiusura, e restano nello storico. Il file già elaborato non viene riletto. Il file atteso che non è arrivato ha acceso il bordo, e il numero in home non mente sull'ora.

Nessuna di queste risposte richiede di aprire le tabelle di Espo. Si leggono dal giornale, dall'anteprima, dal badge. Il confine è anche questo: il lunedì si ragiona su oggetti che una persona può nominare.

Il codice sta su [github.com/nessocrm/nessocrm](https://github.com/nessocrm/nessocrm){: target="_blank"}. Il sito sta su [nessocrm.github.io](https://nessocrm.github.io/it/){: target="_blank"}. Il manuale è la cartella `docs` del repository, in italiano e in inglese. Se questa pagina e il manuale divergono, vale il manuale: è il testo che cambia insieme al codice.
