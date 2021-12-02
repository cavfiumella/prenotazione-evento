
import helpers.Database
import helpers.User
import helpers.Admin
import helpers.time
import helpers.Logbook

import pandas as pd
import streamlit as st
import os
import sys
import traceback
import logging


def main(path: str = "./prenotazioni.csv") -> None:

    # streamlit secrets
    parameters = dict(st.secrets["parameters"])
    maintanance = dict(st.secrets["maintanance"])
    credentials = dict(st.secrets["credentials"])
    members = st.secrets["members"]["emails"]

    # links
    aisf_link = "http://ai-sf.it/perugia/"
    repo_link = "https://github.com/cavfiumella/prenotazione-evento"
    aisf_email = "perugia@ai-sf.it"
    aisf_policy = "https://ai-sf.it/Informativa_Privacy_AISF.pdf"
    streamlit_policy = "https://streamlit.io/privacy-policy"
    subscription_link = "https://ai-sf.it/iscrizione/"

    # utility dirs
    resources_path = "resources"

    st.set_page_config(page_title=parameters["title"], page_icon=os.path.join(resources_path, "perugia.png"),
                       initial_sidebar_state="collapsed",
                       menu_items={"About": f"[AISF Perugia]({aisf_link})",
                                   "Report a bug": os.path.join(repo_link, "issues")
                                  }
                      )

    # init objects
    db = helpers.Database.Database(path, parameters['seats'])
    admin = helpers.Admin.Admin(credentials)
    user = helpers.User.User()
    logbook = helpers.Logbook.Logbook()

# main page

    st.title(parameters["title"])
    st.markdown(" ")

    # maintanance mode
    if maintanance["active"]:
        st.info(maintanance["msg"])
        return

    # admin permissions
    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False

    # admin login
    with st.form("admin_login", clear_on_submit=True):
        with st.sidebar:

            st.header("Accedi")

            # credentials
            username = st.text_input(label="Username", key="username_input")
            password = st.text_input(label="Password", type="password", key="password_input")

            if st.form_submit_button("Login"):
                if admin.auth(username, password):
                    st.session_state["is_admin"] = True
                    st.session_state["admin_username"] = username
                    logbook.log(f"Admin \"{username}\" logged in")
                else:
                    st.error("Credenziali errate!")
                    logbook.log(f"Login attempt with wrong credentials:   username: \"{username}\", password: \"{password}\"")

            if st.session_state["is_admin"] and st.form_submit_button("Logout"):
                username = st.session_state["admin_username"]
                st.session_state["is_admin"] = False
                del st.session_state["admin_username"]
                logbook.log(f"Admin \"{username}\" logged out")

    # admin page
    if st.session_state["is_admin"]:

        st.header("Console di amministrazione")
        st.markdown(" ")

        st.subheader("Prenotazioni")
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
                           args=(f"Prenotations downloaded by admin \"{st.session_state['admin_username']}\"",),
                           key="prenotations_download_button"
                          )
        st.markdown(" ")

        # print prenotations
        st.dataframe(df)
        st.markdown(" ")

        # occupied seats
        st.markdown(f"**Numero di prenotazioni**: {df.shape[0]}")
        st.markdown(f"**Posti disponibili**: {parameters['seats'] - df.shape[0]}")
        st.markdown(f"**Capienza libera**: {1 - df.shape[0] / parameters['seats'] :.0%}")
        st.markdown(" ")

        # remove prenotation
        with st.form("remove_form"):

            st.markdown("**Rimuovi prenotazione**")
            st.markdown("**ATTENZIONE**: la rimozione di una prenotazione non è reversibile")

            ids = db.get_df().index.tolist()
            id = st.selectbox(label="ID prenotazione", options=ids, key="remove_select")

            if st.form_submit_button("Rimuovi"):
                if id == None:
                    st.error("Impossibile rimuovere la prenotazione.")
                else:
                    seat = db.get_df().loc[id].seat
                    db.remove(id)
                    st.success(f"Prenotazione **{id}** al posto **{seat}** correttamente eliminata.")
                    logbook.log(f"Prenotation {id} on seat {seat} removed.")
        st.markdown(" ")

        # logbook
        st.subheader("Logbook")
        st.markdown(" ")

        logs = logbook.read()

        # download logbook
        st.download_button(label="Scarica logbook",
                           data=logs,
                           file_name=f"{helpers.time.format(helpers.time.now(), format='%Y-%m-%d_%H.%M.%S')}.log",
                           on_click=logbook.log,
                           args=(f"Logs downloaded by admin \"{st.session_state['admin_username']}\"",),
                           key="logs_download_button"
                          )
        st.markdown(" ")

        # print logbook
        st.text(logs)
        st.markdown(" ")

    # non-admin user page
    else:

        st.image(os.path.join(resources_path, "perugia.png"), width=250)
        st.markdown(" ")

        st.header("Informazioni sull'evento")
        st.markdown(" ")

        # event information

        st.markdown(parameters["description"])
        st.markdown(f"**Data**: {parameters['date']}")
        st.markdown(f"**Luogo**: {parameters['place']}")

        # prenotations opening and closing time
        opening = helpers.time.parse(parameters["opening"])
        members_opening = helpers.time.parse(parameters["members_opening"])
        closing = helpers.time.parse(parameters["closing"])
        members_closing = helpers.time.parse(parameters["members_closing"])

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
        st.header("Prenotazione posto")
        st.markdown(" ")

        with st.form("prenotation_form", clear_on_submit=True):

            col1, col2 = st.columns(2)
            with col1:
                user.name = st.text_input(label="Nome", key="name_input")
            with col2:
                user.surname = st.text_input(label="Cognome", key="surname_input")

            col1, col2 = st.columns(2)
            with col1:
                user.email = st.text_input(label="Email", key="email_input")

            user.seat = st.selectbox(label="Posto", options=db.get_available_seats(), key="seat_select")
            user.agree = st.checkbox(label=f"Acconsento al trattamento dei dati personali secondo le informative sotto riportate")

            if st.form_submit_button("Prenota"):

                # check if prenotation is open
                now = helpers.time.now()
                is_open = now >= opening and now < closing
                is_open_members = now >= members_opening and now < members_closing

                # check if email is registered as association's member
                is_member = user.email in members

                # prenotation is possible for user
                if is_open or (is_member and is_open_members):

                    user.time = helpers.time.format(helpers.time.now())
                    id = db.register(user)

                    # registration did not go well

                    if id == "name" or id == "surname":
                        st.error("Nome e cognome non sono validi")

                    elif id == "email":
                        st.error("Inserire un indirizzo email valido")

                    elif id == "seat":
                        st.error("Il posto scelto è già occupato")
                        st.info("Ricarica la pagina per aggiornare la lista dei posti disponibile")

                    elif id == "agree":
                        st.error("Il consenso al trattamento dei dati personali è obbligatorio")

                    elif id == "already":
                        st.error(f"E' già presente una prenotazione con questo nome. Per recuperare il codice di prenotazione contatta [{aisf_email}](mailto:{aisf_email}).")

                    # prenotation registered
                    else:
                        st.info(f"**ATTENZIONE** - conserva il seguente codice di prenotazione: **{id}**")
                        st.success("Prenotazione correttamente registrata")

                # prenotation closed
                else:
                    st.error("Le prenotazione sono attualmente chiuse.")

            st.markdown(f"**Informative sulla privacy**: [AISF]({aisf_policy}) e [Streamlit]({streamlit_policy})")

        ### prenotation_form ###
        st.markdown(" ")

        # footer: page information
        st.header("Informazioni sulla pagina")
        st.markdown(" ")

        st.markdown(f"Questa pagina è stata realizzata dal [comitato locale AISF di Perugia]({aisf_link}).")
        st.markdown(f"Il **codice sorgente** è _open source_ e liberamente consultabile [qui]({repo_link}).")
        st.markdown(f"**Per maggiori informazioni** contattaci all'indirizzo email [{aisf_email}](mailto:{aisf_email}).")
        st.markdown(f"**[Iscriviti ad AISF Perugia]({subscription_link})**")

### main ###


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            main()
        else:
            main(path=sys.argv[1])
    except Exception:
        logging.critical(traceback.format_exc())
        st.error("E' stato riscontrato un error inaspettato. Provare a ricaricare la pagina. Ci scusiamo per il disagio.")
