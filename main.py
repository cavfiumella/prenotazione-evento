
import helpers.User
import helpers.Admin
import helpers.time

import pandas as pd
import streamlit as st
import os
import sys
import traceback
import logging


def main(path: str = './prenotazioni.csv') -> None:

    # streamlit secrets
    parameters = st.secrets['parameters']
    credentials = st.secrets['credentials']
    members = st.secrets['members']['emails']

    # links
    aisf_link = 'http://ai-sf.it/perugia/'
    repo_link = 'https://github.com/cavfiumella/prenotazione-evento'
    aisf_email = 'perugia@ai-sf.it'
    aisf_policy = 'https://ai-sf.it/Informativa_Privacy_AISF.pdf'
    streamlit_policy = 'https://streamlit.io/privacy-policy'

    st.set_page_config(page_title=parameters['title'], initial_sidebar_state='collapsed',
                       menu_items={'About': f'[AISF Perugia]({aisf_link})',
                                   'Report a bug': os.path.join(repo_link, 'issues')
                                  }
                      )

    # init objects
    admin = helpers.Admin.Admin(credentials)
    user = helpers.User.User(path, parameters['seats'])

# main page

    st.title(parameters['title'])
    st.markdown(' ')

    st.subheader('Dettagli evento')
    st.markdown(' ')

    # event information
    st.markdown(parameters['description'])
    st.markdown(f'**Data**: {parameters["date"]}')
    st.markdown(f'**Luogo**: {parameters["place"]}')
    st.markdown(' ')

    # admin login
    is_admin = False

    with st.form('admin_login', clear_on_submit=True):
        with st.sidebar:

            st.header('Accedi')

            # credentials
            username = st.text_input(label='Username', key='username_input')
            password = st.text_input(label='Password', type='password', key='password_input')

            if st.form_submit_button('Login'):
                if admin.auth(username, password):
                    is_admin = True
                else:
                    st.error('Credenziali errate!')

    # admin page
    if is_admin:

        # show prenotations
        if os.path.exists(path):

            # print prenotations
            df = user.get_df()
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
                               file_name=f'{helpers.time.format(helpers.time.now(), format="%Y-%m-%d_%H.%M.%S")}.csv',
                               key='download_button'
                              )

        # no prenotation to show
        else:
            st.info('Non è stata registrata alcuna prenotazione ancora')

    # non-admin user page
    else:

        st.subheader('Prenotazione posto')
        st.markdown(' ')

        # prenotation form
        with st.form('prenotation_form'):

            col1, col2 = st.columns(2)
            with col1:
                user.name = st.text_input(label='Nome', key='name_input')
            with col2:
                user.surname = st.text_input(label='Cognome', key='surname_input')

            col1, col2 = st.columns(2)
            with col1:
                user.email = st.text_input(label='Email', key='email_input')

            user.seat = st.selectbox(label='Posto', options=user.get_available_seats(), key='seat_select')
            user.agree = st.checkbox(label=f'Acconsento al trattamento dei dati personali secondo le informative sotto riportate')

            if st.form_submit_button('Prenota'):

                # check if prenotation is open
                is_open = helpers.time.now() >= helpers.time.parse(parameters['opening'])
                is_open_members = helpers.time.now() >= helpers.time.parse(parameters['members_opening'])

                # check if email is registered as association's member
                is_member = user.email in members

                # prenotation is possible for user
                if is_open or (is_member and is_open_members):

                    response = user.save()

                    # save did not go well

                    if response == 'name' or response == 'surname':
                        st.error('Nome e cognome non sono validi')

                    elif response == 'email':
                        st.error('Inserire un indirizzo email valido')

                    elif response == 'seat':
                        st.error('Il posto scelto è già occupato')
                        st.info('Ricarica la pagina per aggiornare la lista dei posti disponibile')

                    elif response == 'agree':
                        st.error('Il consenso al trattamento dei dati personali è obbligatorio')

                    elif response == 'already':
                        st.error(f'E\' già presente una prenotazione con questo nome. Per recuperare il codice di prenotazione contatta [{aisf_email}](mailto:{aisf_email}).')

                    # prenotation registered
                    else:
                        st.info(f'**ATTENZIONE** - conserva il seguente codice di prenotazione: **{response}**')
                        st.success('Prenotazione correttamente registrata')

                # prenotation closed
                else:
                    st.error('Le prenotazione sono attualmente chiuse per te in questo momento.')

            st.markdown(f'**Informative sulla privacy**: [AISF]({aisf_policy}) e [Streamlit]({streamlit_policy})')

        ### prenotation_form ###

        st.markdown(' ')

        # footer: page information
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
    except Exception:
        logging.critical(traceback.format_exc())
        st.error('E\' stato riscontrato un error inaspettato. Provare a ricaricare la pagina. Ci scusiamo per il disagio.')
