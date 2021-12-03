
# Prenotazione evento
## AISF - comitato locale di Perugia


### Distribuzione pagina

Fare il fork della repository
[cavfiumella/prenotazione-evento](https://github.com/cavfiumella/prenotazione-evento)
con il proprio account Github.
Poi collegarsi al sito [share.streamlit.io](https://share.streamlit.io),
eseguire l'accesso con il proprio account Github in modo da poter visualizzare
le proprie repository e creare una nuova app.
Scegliere la forked repository e impostare i vari parametri,
quindi aprire le impostazioni avanzate ed eseguire le seguenti azioni:
- selezionare come interprete **Python 3.9**
- impostare i **segreti** come segue:

```
[event]

title = "Titolo dell'evento"
description = "Descrizione dell'evento"
date = "2021-01-01 17:00:00"
place = "Aula A - Dipartimento di Fisica"


[prenotations]

seats = 40
members_opening = "2021-01-01 00:00:00"
opening = "2021-01-01 00:00:00"
members_closing = "2022-01-01 00:00:00"
closing = "2022-01-01 00:00:00"


[maintenance]

active = false
message = "Il sito web è attualmente in manutenzione. Per maggiori informazioni contatta [webmaster@email.com](mailto:webmaster@email.com)"


[admins]

username = ["master"]
password = ["master_password"]


[members]

emails = []


[mail]

active = true
smtp_server = "smtp.gmail.com"
sender_email = "sender@gmail.com"
password = "sender_email_password"


[resources]

page_icon = "resources/page_icon.png"
main_logo = "resources/logo.png"
prenotations = "prenotations.csv"
logbook = "logbook"


[links]

local_aisf = "http://ai-sf.it/perugia/"
repo = "https://github.com/cavfiumella/prenotazione-evento"
aisf_policy = "https://ai-sf.it/Informativa_Privacy_AISF.pdf"
streamlit_policy = "https://streamlit.io/privacy-policy"
subscription = "https://ai-sf.it/iscrizione/"


[contacts]

local_aisf = "perugia@ai-sf.it"
```

I segreti sono utili ad impostare parametri variabili dell'app a seconda delle necessità
specifiche dell'evento o del comitato.
I parametri sono così strutturati:
- la sezione `event` contiene le informazioni sull'evento;
- la sezione `prenotations` contiene informazioni riguardanti le prenotazioni,
quali il numero di posti a sedere, gli orari di apertura e chiusura delle prenotazioni per i membri AISF e non;
- la sezione `maintenance` attiva e disattiva la modalità manutenzione della pagina
in cui l'accesso al pubblico viene disabilitato e mostra un messaggio informativo;
- la sezione `admins` contiene le credenziali degli utenti con privilegi di amministrazione
della pagina;
- la sezione `members` contiene gli indirizzi email degli iscritti AISF;
- la sezione `mail` attiva o disattiva l'invio di email riepilogative sulla prenotazione
effettuata agli utenti che prenotano un posto;
- la sezione `resources` specifica la posizione delle immagini da usare come icona della pagina
e come logo nel form di prenotazione e dei file dove salvare le prenotazioni e il logbook;
- la sezione `links` contiene link utili;
- la sezione `contacts` contiene contatti utili.

Tutti i parametri sono obbligatori ad eccezione della sezione `resources` che può essere omessa.

I segreti possono essere modificati anche dopo aver avviato l'app dalle sue impostazioni.

Una volta attivata la pagina è accessibile al link `share.streamlit.io/username/reponame/main/main.py`
dove `username` e `reponame` sono i nomi dell'utente proprietario della forked repository Github e della repository stessa.


### Amministratori

Gli amministratori, dopo aver eseguito il login nel menù in alto a sinistra,
possono visualizzare e scaricare le prenotazioni espresse fino a quel momento e il logbook
con le operazioni eseguite dagli amministratori di sistema.
Possono inoltre rimuovere una prenotazione dall'elenco.


### Link utili

- [Profilo Github sviluppatore](https://github.com/cavfiumella)
- [Repository del progetto](https://github.com/cavfiumella/prenotazione-evento)
- [Comitato locale AISF di Perugia](http://ai-sf.it/perugia/)
- [Email comitato locale](mailto:perugia@ai-sf.it)
