
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

    # admin login
    is_admin = False

    with st.form("admin_login", clear_on_submit=True):
        with st.sidebar:

            st.header("Accedi")

            # credentials
            username = st.text_input(label="Username", key="username_input")
            password = st.text_input(label="Password", type="password", key="password_input")

            if st.form_submit_button("Login"):
                if admin.auth(username, password):
                    is_admin = True
                    logbook.log(f"Admin \"{username}\" logged in")
                else:
                    st.error("Credenziali errate!")
                    logbook.log(f"Login attempt with wrong credentials:   username: \"{username}\", password: \"{password}\"")

    # admin page
    if is_admin:

        st.sidebar.button("Logout")

        st.header("Console di amministrazione")
        st.markdown(" ")

        st.subheader("Prenotazioni")
        st.markdown(" ")

        # print prenotations
        df = db.get_df()
        st.dataframe(df)

        # occupied seats
        st.markdown(" ")
        st.markdown(f"**Numero di prenotazioni**: {df.shape[0]}")
        st.markdown(f"**Posti disponibili**: {parameters['seats'] - df.shape[0]}")
        st.markdown(f"**Capienza libera**: {1 - df.shape[0] / parameters['seats'] :.0%}")

        # convert df to csv
        @st.cache
        def get_csv(df: pd.DataFrame) -> str:
            return df.to_csv().encode("utf-8")

        # [BUG]
        # pressing download buttons logout admin automatically.
        # a form does not solve the problem because download buttons
        # can not be used in forms

        st.markdown(" ")

        # download df
        st.download_button(label="Scarica prenotazioni",
                           data=get_csv(df),
                           file_name=f"{helpers.time.format(helpers.time.now(), format='%Y-%m-%d_%H.%M.%S')}.csv",
                           on_click=logbook.log,
                           args=(f"Prenotations downloaded by admin \"{username}\"",),
                           key="prenotations_download_button"
                          )

        st.markdown(" ")

        st.subheader("Logbook")
        st.markdown(" ")

        # print logbook
        logs = logbook.read()
        st.text(logs)

        # download logbook
        st.download_button(label="Scarica logbook",
                           data=logs,
                           file_name=f"{helpers.time.format(helpers.time.now(), format='%Y-%m-%d_%H.%M.%S')}.log",
                           on_click=logbook.log,
                           args=(f"Logs downloaded by admin \"{username}\"",),
                           key="logs_download_button"
                          )

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
        if helpers.time.parse(parameters["members_opening"]) != helpers.time.parse(parameters["opening"]):
            st.markdown(f"**Apertura delle prenotazioni per i membri AISF**: {parameters['members_opening']}")
        st.markdown(f"**Apertura delle prenotazioni**: {parameters['opening']}")
        if helpers.time.parse(parameters["members_closure"]) != helpers.time.parse(parameters["closure"]):
            st.markdown(f"**Chiusura delle prenotazioni per i membri AISF**: {parameters['members_closure']}")
        st.markdown(f"**Chiusura delle prenotazioni**: {parameters['closure']}")
        st.markdown(" ")

        st.header("Prenotazione posto")
        st.markdown(" ")

        # prenotation form
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
                is_open = helpers.time.now() >= helpers.time.parse(parameters["opening"]) and helpers.time.now() < helpers.time.parse(parameters["closure"])
                is_open_members = helpers.time.now() >= helpers.time.parse(parameters["members_opening"]) and helpers.time.now() < helpers.time.parse(parameters["members_closure"])

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
