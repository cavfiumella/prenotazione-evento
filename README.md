
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
[parameters]

title = "Titolo pagina"
description = "Descrizione generica dell'evento"
date = "data dell'evento"
place = "luogo dell'evento"
seats = <numero di posti a sedere (e.g. 40)>
members_opening = "2021-01-01 00:00:00"
opening = "2021-01-01 00:00:00"
members_closing = "2022-01-01 00:00:00"
closing = "2022-01-01 00:00:00"


[maintanance]

active = <true o false>
msg = "Messaggio informativo mostrato quando `active = true`"


[credentials]

username = ["username1", "username2", ...]
password = ["password1", "password2", ...]


[members]

emails = ["mario.rossi@gmail.com", ...]
```

La sezione `maintanance` attiva e disattiva la modalità manutenzione della pagina
che disabilita l'accesso al pubblico mostrando un messaggio informativo (i.e. `msg`).

La sezione `credentials` imposta le credenziali degli amministratori.

La sezione `members` contiene le email degli iscritti al comitato locale AISF.
Se non ci sono iscritti usare una lista vuota (i.e. `emails = []`).

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
