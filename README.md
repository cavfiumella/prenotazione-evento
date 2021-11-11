
# Prenotazione evento
## AISF - comitato locale di Perugia


### Distribuzione pagina

Collegarsi al sito [share.streamlit.io](https://share.streamlit.io), accedere con il proprio account
e creare una nuova app.

Scegliere la repository contenente l'app e impostare i vari parametri, quindi aprire le impostazioni
avanzate:
- selezionare come interprete **Python 3.9**
- impostare i **segreti** come segue:
```
[parameters]

title = "Titolo pagina"
description = "Descrizione generica dell'evento"
date = "data dell'evento"
place = "luogo dell'evento"
seats = <numero di posti a sedere (e.g. 40)>


[credentials]

username = ["username1", "username2", ...]
password = ["password1", "password2", ...]


[members]

emails = ["mario.rossi@gmail.com", ...]
```

La sezione `credentials` dei segreti imposta le credenziali degli amministratori.

La sezione `members` contiene le email degli iscritti al comitato locale AISF.
Se non ci sono iscritti usare una lista vuota (i.e. `emails = []`).

I segreti possono essere modificati anche dopo aver avviato l'app.

Una volta attivata la pagina è accessibile al link `share.streamlit.io/username/reponame/main/main.py`
dove `username` e `reponame` sono i nomi dell'utente proprietario della repository Github e della repository stessa.


### Amministratori

Gli amministratori, dopo essersi loggati nel menù in alto a sinistra,
possono visualizzare e scaricare le prenotazioni espresse fino a quel momento e il logbook
con le operazioni eseguite dagli amministratori di sistema.


## Link utili

- [Comitato locale AISF di Perugia](http://ai-sf.it/perugia/)
- [Email comitato locale](mailto:perugia@ai-sf.it)
