
import helpers.User
import helpers.Admin

import pandas as pd
import streamlit as st
import os
import sys
import logging


def main(path: str = './prenotazioni.csv') -> None:

    # streamlit secrets
    parameters = st.secrets['parameters']
    credentials = st.secrets['credentials']

    aisf_link = 'http://ai-sf.it/perugia/'
    repo_link = 'https://github.com/cavfiumella/prenotazione-evento'
    aisf_email = 'perugia@ai-sf.it'

    st.set_page_config(page_title=parameters['title'], initial_sidebar_state='collapsed',
                       menu_items={'About': f'[AISF Perugia]({aisf_link})',
                                   'Report a bug': os.path.join(repo_link, 'issues')
                                  }
                      )

# admin login

    # init Admin
    admin = helpers.Admin.Admin(credentials)
    admin = False

    st.sidebar.header('Accedi')
    username = st.sidebar.text_input(label='Username', key='username_input')
    password = st.sidebar.text_input(label='Password', type='password', key='password_input')

# main page

    st.title(parameters['title'])
    st.markdown(' ')

    st.subheader('Dettagli evento')
    st.markdown(' ')

    # event information
    st.markdown(parameters['event'])
    st.markdown(f'**Data**: {parameters["date"]}')
    st.markdown(f'**Luogo**: {parameters["place"]}')
    st.markdown(' ')

    st.subheader('Prenotazione posto')
    st.markdown(' ')

    if st.sidebar.button('Login', key='login_button'):

        if not admin.auth(username, password):
            st.sidebar.error('Credenziali errate!')

        else:

            # show logout button
            st.sidebar.button('Logout')

            # show prenotations
            if os.path.exists(path):

                # print prenotations
                df = pd.read_csv(path, index_col='id')
                st.dataframe(df)

                # convert df to csv
                @st.cache
                def get_csv(df: pd.DataFrame) -> str:
                    return df.to_csv().encode('utf-8')

                # download df

                # [BUG]
                # pressing download button logout admin automatically.
                # a form does not solve the problem because download buttons
                # can not be used in forms

                st.download_button(label='Download',
                                   data=get_csv(df),
                                   file_name=f'{pd.Timestamp.utcnow().tz_convert("Europe/Rome").strftime("%Y-%m-%d_%H.%M.%S")}.csv',
                                   key='download_button'
                                  )

            # no prenotation to show
            else:
                st.info('Non è stata registrata alcuna prenotazione ancora')

    # non-admin user
    else:

        with st.form('main_form'):

            user = helpers.User.User(path, parameters['seats'])

            col1, col2 = st.columns(2)
            with col1:
                user.name = st.text_input(label='Nome', key='name_input')
            with col2:
                user.surname = st.text_input(label='Cognome', key='surname_input')

            col1, col2 = st.columns(2)
            with col1:
                user.email = st.text_input(label='Email', key='email_input')
            with col2:
                user.phone = st.text_input(label='Numero di telefono', key='phone_input')

            user.seat = st.selectbox(label='Posto', options=user.get_available_seats(), key='seat_select')
            user.agree = st.checkbox(label='Consenso al trattamento dei dati')

            if st.form_submit_button('Prenota'):

                response = user.save()

                # save did not go well

                if response == 'name' or response == 'surname':
                    st.error('Nome e cognome non sono validi')

                elif response == 'email':
                    st.error('Inserire un indirizzo email valido')

                elif response == 'phone':
                    st.error('Inserire un numero di telefono valido')

                elif response == 'seat':
                    st.error('Il posto scelto è già occupato')
                    st.info('Ricarica la pagina per aggiornare la lista dei posti disponibile')

                elif response == 'agree':
                    st.error('Il consenso al trattamento dei dati personali è obbligatorio')
                # prenotation registered
                else:
                    st.success('Prenotazione correttamente registrata')

        st.markdown(' ')

        # footer
        st.subheader('Informazioni sulla pagina')
        st.markdown(' ')

        with st.expander('Espandi'):
            st.markdown(f'Questa pagina è stata realizzata dal [comitato locale AISF di Perugia]({aisf_link}).')
            st.markdown(f'Il **codice sorgente** è _open source_ e liberamente consultabile [qui]({repo_link}).')
            st.markdown(f'**Per maggiori informazioni** contattaci all\'indirizzo email [{aisf_email}](mailto:{aisf_email}).')

### main ###


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            main()
        else:
            main(path=sys.argv[1])
    except Exception as ex:
        logging.critical(f'{type(ex)}: {ex}')
        st.error('E\' stato riscontrato un error inaspettato. Provare a ricaricare la pagina. Ci scusiamo per il disagio.')
