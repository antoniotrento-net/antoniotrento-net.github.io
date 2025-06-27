Perfetto, Antonio. Ecco una guida dettagliata per implementare un unico workflow n8n che gestisce i tre flussi principali dell’assistente vocale Vapi, integrato con il tuo calendario e con pianificazione appuntamenti reale.

⸻

🧠 Integrazione Vapi + Calendario + n8n

🔧 Guida completa per gestire:
	•	✅ Aggiornamento automatico della Knowledge Base
	•	✅ Verifica in tempo reale della disponibilità
	•	✅ Pianificazione appuntamenti al termine della chiamata

⸻

🎯 Obiettivo

Creare un singolo workflow n8n con 3 punti di ingresso distinti, ciascuno gestito da un Webhook node diverso, per:
	1.	update-availability: aggiornare ogni 12h la Knowledge Base di Vapi
	2.	check-availability: ricevere richieste assistant-request e rispondere dinamicamente
	3.	schedule-call: ricevere call.ended con i dati della conversazione, salvare o agire

⸻

🧩 PANORAMICA FLUSSI

Nome Webhook	Metodo	Attivazione	Cosa fa
/update-availability	POST	Ogni 12h via cron	Genera file .txt con slot liberi e lo carica su Vapi
/check-availability	POST	Evento assistant-request da Vapi	Analizza richiesta, controlla calendario, risponde
/schedule-call	POST	Evento call.ended da Vapi	Estrae dati, salva l’appuntamento, invia notifiche, ecc.


⸻

🔧 IMPOSTAZIONI SU VAPI

1. Imposta Server URL

Vai su Dashboard Vapi → Assistant → Settings → Server Settings e configura:

Campo	Valore
Server URL	https://TUO_DOMINIO/webhook/check-availability
Secret Token	(opzionale, usalo se vuoi validare le richieste)
Headers	(opzionali, ad esempio Authorization se vuoi firmare)

🔁 Vapi chiamerà check-availability ad ogni richiesta dell’utente all’agente.

⸻

2. Imposta eventi webhook per call.ended

Sempre in Server Settings, abilita:
	•	✅ call.ended tra gli eventi server
	•	Vapi invierà una richiesta a https://TUO_DOMINIO/webhook/schedule-call ogni volta che una chiamata termina

⸻

🏗️ STRUTTURA WORKFLOW n8n

🟡 1. Nodo Webhook: update-availability (manual trigger + cron)
	•	Metodo: POST
	•	URL: /webhook/update-availability
	•	Trigger secondario: Cron → ogni 12h
	•	Azioni:
	•	Google Calendar → Elenca eventi disponibili (es. titolo “Disponibile” o slot vuoti)
	•	Genera file .txt con i prossimi 3 slot in linguaggio naturale
	•	HTTP Request → API Vapi POST /files
	•	Headers: Authorization: Bearer <PRIVATE_API_KEY>
	•	Body: multipart/form-data con:
	•	file: contenuto testuale
	•	type: "knowledge"
	•	name: "disponibilita-settimanale"

⸻

🔵 2. Nodo Webhook: check-availability (assistant-request)
	•	Metodo: POST
	•	URL: /webhook/check-availability

Flusso:
	1.	Riceve payload con:

{
  "message": {
    "type": "assistant-request",
    "content": "Vorrei prenotare lunedì alle 10"
  }
}


	2.	Estrai data/ora dalla frase (ChatGPT, LangChain, Date & Time Parser)
	3.	Verifica disponibilità sul calendario
	4.	Rispondi con:

{
  "response": "Lunedì alle 10 non è disponibile. Ho disponibilità martedì alle 11 o mercoledì alle 18. Quale preferisci?"
}



⸻

🟢 3. Nodo Webhook: schedule-call (call.ended)
	•	Metodo: POST
	•	URL: /webhook/schedule-call

Flusso:
	1.	Riceve:

{
  "message": {
    "type": "call.ended",
    "call": {
      "transcript": "...",
      "startTime": "...",
      "endTime": "...",
      "assistant_id": "...",
      "phone": "+39...",
      "callId": "...",
      ...
    }
  }
}


	2.	Estrai dati da transcript o payload:
	•	Nome, email, orario scelto
	3.	Crea appuntamento nel calendario
	4.	Invia notifica (email, Telegram, CRM, database, ecc.)

⸻

📘 Prompt consigliato per l’agente Vapi

Ciao! Sono l’assistente vocale di Antonio Trento.
Antonio è disponibile per appuntamenti in orari limitati, che trovi nel documento “disponibilità settimanale”.

Posso proporti subito i prossimi slot liberi. Se preferisci un altro momento, chiedimelo pure e controllerò per te!


⸻

🔐 Sicurezza consigliata
	•	✅ Valida il Secret Token se configurato in Vapi (via header)
	•	✅ Aggiungi logging per debugging (es. transcript, errori calendario)
	•	✅ Usa Rate limit o Queue se temi troppe chiamate simultanee

⸻

🧪 Test suggeriti
	1.	Fai una chiamata e chiedi uno slot disponibile: → Vedi se risponde bene
	2.	Chiedi uno non disponibile: → Verifica che attivi check-availability
	3.	Completa una chiamata → Vedi se scatta schedule-call
	4.	Verifica aggiornamento automatico di update-availability da cron

⸻

🧩 Estensioni future possibili
	•	Sincronizzazione bidirezionale con Cal.com o Notion
	•	Salvataggio lead in un CRM (es. HubSpot, Airtable, Supabase)
	•	Invio link Google Meet/Zoom automatico
	•	Dashboard con tutte le chiamate effettuate + estrazione analytics

⸻

✅ Checklist finale

Cosa	Stato
Assistant Vapi configurato con webhook	⬜
Knowledge Base creata e collegata	⬜
Workflow n8n con 3 webhook configurati	⬜
Connessione a Google Calendar testata	⬜
Testato end-to-end con chiamata reale	⬜


⸻

🔗 Vuoi che ti generi anche lo YAML completo del workflow n8n?

Posso crearti il file workflow.json da importare direttamente. Mi basta sapere:
	•	Il tuo fuso orario
	•	Quali orari vuoi includere nei suggerimenti automatici
	•	Se preferisci salvare gli appuntamenti anche su file o database

Fammi sapere e lo creo subito per te ✅