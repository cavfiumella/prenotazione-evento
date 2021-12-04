
import helpers.Database
import helpers.Admin
import helpers.time
import helpers.Logbook
import helpers.Postman

import pandas as pd
import streamlit as st
import sys
import traceback
import logging
import locale


# timestamps locale
LOCALE = ("it_IT", "UTF-8")

try:
    helpers.time.set_locale(LOCALE)
except Exception:
    logging.error(f"unable to set locale \"{'.'.join(LOCALE)}\"")
    logging.error(traceback.format_exc())
    LOCALE = locale.getlocale(locale.LC_TIME)
    if LOCALE[0] == None: LOCALE = locale.getlocale() # LC_TIME not set
    logging.info(f"current locale is \"{'.'.join(LOCALE)}\"")


def main() -> None:

    st.set_page_config(page_title=st.secrets.event.title,
                       page_icon=st.secrets.resources.page_icon if "resources" in st.secrets and "page_icon" in st.secrets.resources else None,
                       initial_sidebar_state="collapsed",
                       menu_items={"About": f"[AISF Perugia]({st.secrets.links.local_aisf})",
                                   "Report a bug": st.secrets.links.bug
                                  }
                      )

    postman = helpers.Postman.Postman(st.secrets.mail.smtp_server, st.secrets.mail.sender_email, st.secrets.mail.password)
    logbook = helpers.Logbook.Logbook(st.secrets.resources.logbook if "resources" in st.secrets and "logbook" in st.secrets.resources else None)

# page header

    st.title(st.secrets.event.title)
    st.markdown(" ")

    # maintenance mode
    if st.secrets.maintenance.active:
        st.info(st.secrets.maintenance.message)
        return

# admin access

    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False

    with st.form("admin_login", clear_on_submit=True):
        with st.sidebar:

            st.header("Accedi \U0001F510")
            admin = helpers.Admin.Admin(dict(st.secrets.admins)) # access manager

            # credentials
            username = st.text_input(label="Username", key="username_input")
            password = st.text_input(label="Password", type="password", key="password_input")

            if st.form_submit_button("Login"):

                # logout previous authenticated user
                st.session_state.is_admin = False
                if "admin_username" in st.session_state:
                    del st.session_state.admin_username

                if admin.auth(username, password):
                    st.session_state.is_admin = True
                    st.session_state["admin_username"] = username
                    logbook.log(f"Admin \"{username}\" logged in.")
                else:
                    st.error("Credenziali errate!")
                    logbook.log(f"Login attempt with wrong credentials:   username: \"{username}\", password: \"{password}\".")

            if st.session_state.is_admin and st.form_submit_button("Logout"):
                username = st.session_state.admin_username
                st.session_state.is_admin = False
                del st.session_state.admin_username
                logbook.log(f"Admin \"{username}\" logged out.")

            del admin

# page content

    db = helpers.Database.Database(st.secrets.prenotations.seats,
                                   st.secrets.resources.prenotations if "resources" in st.secrets and "prenotations" in st.secrets.resources else None
                                  )

    # admin console
    if st.session_state.is_admin:

        st.header("\U0001F4CB Console di amministrazione")
        st.markdown(" ")

        st.subheader("\U0001F4DD Prenotazioni")
        st.markdown(" ")

        df = db.get_df()

        # download df

        # a complete function is defined to get df as csv to use streamlit cache feature
        @st.cache
        def get_csv(df: pd.DataFrame) -> str:
            return df.to_csv().encode("utf-8")

        st.download_button(label="Scarica prenotazioni",
                           data=get_csv(df),
                           file_name=f"{helpers.time.format(helpers.time.now(), format='%Y-%m-%d_%H.%M.%S')}.csv",
                           on_click=logbook.log,
                           args=(f"Prenotations downloaded by admin \"{st.session_state.admin_username}\".",),
                           key="prenotations_download_button"
                          )
        st.markdown(" ")

        # occupied seats
        occupied = df.shape[0]
        total = st.secrets.prenotations.seats
        st.markdown(f"**Numero di prenotazioni**: {occupied} / {total} ({occupied / total : .0%}).")
        st.markdown(" ")

        # print prenotations
        st.dataframe(df)
        st.markdown(" ")

        # remove prenotation
        with st.form("remove_form"):

            st.markdown("**Rimuovi prenotazione**")
            st.markdown("La rimozione di una prenotazione è un'operazione **irreversibile**.")

            ids = db.get_df().index.tolist()
            id = st.selectbox(label="ID prenotazione", options=ids, key="remove_select")

            if st.form_submit_button("Rimuovi"):

                if id == None:
                    st.error("Non ci sono prenotazioni da rimuovere.")

                else:

                    # ATTENTION: prenotation.name is the name of the pandas.Series (i.e. the ID) not the name field value
                    prenotation = db.get_df().loc[id]

                    db.remove(id)
                    st.success(f"Prenotazione **{prenotation.name}** al posto **{prenotation.seat}** correttamente eliminata.")
                    logbook.log(f"Prenotation {prenotation.name} on seat {prenotation.seat} removed.")

                    # send notification mail
                    if st.secrets.mail.active:

                        subject = "Cancellazione prenotazone MELT"
                        text = f"""\
Ciao {prenotation.loc["name"]}!

La seguente prenotazione è stata cancellata:

Codice di prenotazione: {prenotation.name}
Nome e Cognome: {prenotation.loc['name']} {prenotation.surname}
Email: {prenotation.email}
Posto: {prenotation.seat}

Speriamo di rivederti in futuro!
Alla prossima!

______________________________
{st.secrets.mail.signature}
Contattaci all'indirizzo: {st.secrets.contacts.local_aisf}"""

                        try:
                            postman.send(prenotation.email, subject, text)
                        except Exception:
                            logging.error(traceback.format_exc())
                            st.error(f"""**ATTENZIONE**: si è verificato un errore inatteso \
                            e non è stato possibile inviare una mail di conferma all'indirizzo \
                            {prenotation.email}. Si prega di **conservare il codice della prenotazione** scritto sopra. \
                            Ci scusiamo per il disagio.""")
        st.markdown(" ")

        # logbook
        st.subheader("\U0001F4C4 Logbook")
        st.markdown(" ")

        logs = logbook.read()

        # download logbook
        st.download_button(label="Scarica logbook",
                           data=logs,
                           file_name=f"{helpers.time.format(helpers.time.now(), format='%Y-%m-%d_%H.%M.%S')}.log",
                           on_click=logbook.log,
                           args=(f"Logs downloaded by admin \"{st.session_state.admin_username}\".",),
                           key="logs_download_button"
                          )
        st.markdown(" ")

        # print logbook
        st.text(logs)
        st.markdown(" ")

    # prenotation page
    else:

        if "resources" in st.secrets and "main_logo" in st.secrets.resources:
            st.image(st.secrets.resources.main_logo, width=250)
            st.markdown(" ")

        st.header("\U0001F4C5 Informazioni sull'evento")
        st.markdown(" ")

        # event information

        st.markdown(st.secrets.event.description)
        st.markdown(f"**Data**: {helpers.time.format(st.secrets.event.date, '%A %d %B %Y alle %H:%M')}")
        st.markdown(f"**Luogo**: {st.secrets.event.place}")

        # prenotations opening and closing time
        opening = helpers.time.parse(st.secrets.prenotations.opening)
        members_opening = helpers.time.parse(st.secrets.prenotations.members_opening)
        closing = helpers.time.parse(st.secrets.prenotations.closing)
        members_closing = helpers.time.parse(st.secrets.prenotations.members_closing)

        fmt = "%A %d %B %Y alle %H:%M" # format to print

        for x in [opening, members_opening, closing, members_closing]:
            if x.second != 0:
                fmt += ":%S"
                break

        if members_opening != opening:
            st.markdown(f"**Apertura delle prenotazioni per i membri AISF**: {helpers.time.format(members_opening, fmt)}")
        st.markdown(f"**Apertura delle prenotazioni**: {helpers.time.format(opening, fmt)}")

        if members_closing != closing:
            st.markdown(f"**Chiusura delle prenotazioni per i membri AISF**: {helpers.time.format(members_closing, fmt)}")
        st.markdown(f"**Chiusura delle prenotazioni**: {helpers.time.format(closing, fmt)}")

        st.markdown(" ")

        # prenotation
        st.header("\U0001F4DD Prenotazione posto")
        st.markdown(" ")

        with st.form("prenotation_form", clear_on_submit=True):

            prenotation = pd.Series({"name": "None",
                                     "surname": "None",
                                     "email": "None",
                                     "seat": -1,
                                     "agree": False,
                                     "time": "None"
                                   })

            col1, col2 = st.columns(2)
            with col1:
                prenotation.loc["name"] = st.text_input(label="Nome", key="name_input")
            with col2:
                prenotation.surname = st.text_input(label="Cognome", key="surname_input")

            col1, col2 = st.columns(2)
            with col1:
                prenotation.email = st.text_input(label="Email", key="email_input")

            prenotation.seat = st.selectbox(label="Posto", options=db.get_available_seats(), key="seat_select")
            prenotation.agree = st.checkbox(label=f"Acconsento al trattamento dei dati personali \
                                                    secondo le informative sotto riportate."
                                            )

            if st.form_submit_button("Prenota"):

                # check if prenotation is open
                now = helpers.time.now()
                is_open = now >= opening and now < closing
                is_open_members = now >= members_opening and now < members_closing

                # check if email is registered as association's member
                is_member = prenotation.email in st.secrets.members.emails

                # prenotation is possible for user
                if is_open or (is_member and is_open_members):

                    prenotation.time = helpers.time.format(helpers.time.now())
                    id = db.register(prenotation)

                    # registration did not go well

                    if id == "name" or id == "surname":
                        st.error("Nome e cognome non sono validi.")

                    elif id == "email":
                        st.error("Inserire un indirizzo email valido.")

                    elif id == "seat":
                        st.error("Il posto scelto è già occupato.")
                        st.info("Ricarica la pagina per aggiornare la lista dei posti disponibile.")

                    elif id == "agree":
                        st.error("Il consenso al trattamento dei dati personali è obbligatorio.")

                    elif id == "already":
                        st.error(f"E' già presente una prenotazione con questo nome. \
                                   Per recuperare il codice di prenotazione contatta \
                                   [{st.secrets.contacts.local_aisf}](mailto:{st.secrets.contacts.local_aisf})."
                                )

                    # prenotation registered
                    else:

                        # send confirmation mail
                        if st.secrets.mail.active:

                            subject = "Conferma prenotazone MELT"
                            text = f"""\
Ciao {prenotation.loc['name']}!

La tua prenotazione è stata correttamente registrata, eccone il riepilogo:

Codice di prenotazione: {prenotation.name}
Nome e Cognome: {prenotation.loc['name']} {prenotation.surname}
Email: {prenotation.email}
Posto: {prenotation.seat}

Se decidessi di non partecipare all'evento invia una mail a {st.secrets.contacts.local_aisf} per far cancellare \
la tua prenotazione.

Ci vediamo {helpers.time.format(st.secrets.event.date, '%A %d %B %Y alle %H:%M')} in {st.secrets.event.place}.
A presto!

______________________________
{st.secrets.mail.signature}
Contattaci all'indirizzo: {st.secrets.contacts.local_aisf}"""

                            try:
                                postman.send(prenotation.email, subject, text)
                            except Exception:
                                logging.error(traceback.format_exc())
                                st.error(f"**ATTENZIONE**: si è verificato un errore inatteso \
                                           e non è stato possibile inviare una mail di conferma all'indirizzo \
                                           {prenotation.email}. Si prega di **conservare il codice della prenotazione**. \
                                           Ci scusiamo per il disagio."
                                        )
                            else:
                                st.info(f"Ti abbiamo inviato una mail di riepilogo all'indirizzo **{prenotation.email}**. \
                                          Se non la trovi controlla la cartella della posta indesiderata."
                                       )

                        # no confirmation mail
                        else:
                            st.info("**Conserva il codice della prenotazione**.")

                        st.success(f"La tua prenotazione è stata correttamente registrata con il codice **{id}**.")


                # prenotation closed
                else:
                    st.error("Le prenotazioni sono **chiuse**.")

            st.markdown(f"**Informative sulla privacy**: [AISF]({st.secrets.links.aisf_policy}) e \
                          [Streamlit]({st.secrets.links.streamlit_policy})"
                       )

        ### prenotation_form ###
        st.markdown(" ")

        # footer: page information
        st.header("\U0001F310 Informazioni sulla pagina")
        st.markdown(" ")

        st.markdown(f"Questa pagina è stata realizzata dal [comitato locale AISF di Perugia]({st.secrets.links.local_aisf}).")
        st.markdown(f"Il **codice sorgente** è _open source_ e liberamente consultabile [qui]({st.secrets.links.repo}).")
        st.markdown(f"**Per maggiori informazioni** contattaci all'indirizzo email \
                      [{st.secrets.contacts.local_aisf}](mailto:{st.secrets.contacts.local_aisf})."
                   )
        st.markdown(f"**[Iscriviti ad AISF Perugia]({st.secrets.links.subscription})**")

    del db

    del logbook
    del postman

### main ###


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.critical(traceback.format_exc())
        st.error("E' stato riscontrato un error inaspettato. Provare a ricaricare la pagina. Ci scusiamo per il disagio.")
