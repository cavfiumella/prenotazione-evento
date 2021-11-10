
import helpers.Answer

import pandas as pd
import streamlit as st
import sys
import logging


TITLE = 'Prenotazione evento'
N_SEATS = 43


def main(path: str = './prenotazioni.csv') -> None:

    st.set_page_config(page_title=TITLE)

    st.title(TITLE)
    st.markdown(' ')

    with st.form('main_form'):

        answer = helpers.Answer.Answer(path, N_SEATS)

        col1, col2 = st.columns(2)
        with col1:
            answer.name = st.text_input(label='Nome', key='name_input')
        with col2:
            answer.surname = st.text_input(label='Cognome', key='surname_input')

        col1, col2 = st.columns(2)
        with col1:
            answer.email = st.text_input(label='Email', key='email_input')
        with col2:
            answer.phone = st.text_input(label='Numero di telefono', key='phone_input')

        answer.seat = st.selectbox(label='Posto', options=answer.get_available_seats(), key='seat_select')
        answer.agree = st.checkbox(label='Consenso al trattamento dei dati')

        if st.form_submit_button('Prenota'):

            response = answer.save()

            if type(response) == str:
                # some field is not valid
                if response == 'name' or response == 'surname':
                    st.error('Nome e cognome non sono validi')
                if response == 'email':
                    st.error('Inserire un indirizzo email valido')
                if response == 'phone':
                    st.error('Inserire un numero di telefono valido')
                if response == 'seat':
                    st.error('Il posto scelto è già occupato')
                    st.info('Ricarica la pagina per aggiornare la lista dei posti disponibile')
                if response == 'agree':
                    st.error('Il consenso al trattamento dei dati personali è obbligatorio')
            else:
                st.success('Prenotazione correttamente registrata')

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
