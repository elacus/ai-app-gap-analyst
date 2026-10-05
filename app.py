import time

import streamlit as st
from google import genai
from google.genai import errors

# Gemini-API-Key aus den Streamlit Cloud Secrets lesen
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Aktuell verfügbares Flash-Modell
MODEL = "gemini-3.5-flash"

# Nutzungslimit für den Beta-Test
MAX_REQUESTS_PER_SESSION = 5
WINDOW_SECONDS = 3600

client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(
    page_title="KI App Gap Analyst",
    page_icon="🧠",
)

st.title("🧠 KI App Gap Analyst")
st.caption(
    "Beta-Test: Analysiert App-Ideen, identifiziert Marktlücken "
    "und schlägt ein realistisches MVP vor."
)

# Session-basiertes Nutzungslimit
if "analysis_timestamps" not in st.session_state:
    st.session_state.analysis_timestamps = []

now = time.time()

st.session_state.analysis_timestamps = [
    timestamp
    for timestamp in st.session_state.analysis_timestamps
    if now - timestamp < WINDOW_SECONDS
]

remaining = MAX_REQUESTS_PER_SESSION - len(st.session_state.analysis_timestamps)

st.info(f"Verbleibende Analysen in dieser Session: {remaining}")

idea = st.text_area(
    "Beschreibe deine App-Idee",
    placeholder=(
        "Beispiel: Eine App für Studierende in Bremen mit "
        "Mensa-Speiseplänen, Stundenplan und Lerngruppen."
    ),
    height=160,
)

if st.button("App-Idee analysieren", type="primary"):
    if len(idea.strip()) < 20:
        st.warning("Bitte beschreibe deine App-Idee etwas ausführlicher.")

    elif len(idea) > 2000:
        st.warning("Bitte halte die Beschreibung unter 2.000 Zeichen.")

    elif remaining <= 0:
        st.warning(
            "Du hast das Testlimit erreicht. "
            "Bitte versuche es später erneut."
        )

    else:
        prompt = f"""
        Du bist ein erfahrener KI-App-Produktexperte.

        Analysiere diese App-Idee:
        {idea}

        Regeln:
        - Sei konkret, kritisch und praxisnah.
        - Maximal 300 Wörter.
        - Nenne mindestens drei konkrete Feature-Lücken.
        - Das MVP enthält maximal fünf Features.
        - Keine allgemeinen Floskeln.

        Antwortstruktur:
        ## Zielgruppe
        ## Kernproblem
        ## Vorhandene Wettbewerbsfeatures
        ## Fehlende Features
        ## MVP
        ## Risiken
        """

        with st.spinner("Gemini analysiert deine Idee ..."):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                )

                st.markdown(response.text)

                st.session_state.analysis_timestamps.append(time.time())

                st.download_button(
                    label="Analyse als Markdown speichern",
                    data=response.text,
                    file_name="app-gap-analyse.md",
                    mime="text/markdown",
                )

            except errors.ServerError as e:
                message = str(e)

                if "429" in message:
                    st.error(
                        "Das Nutzungslimit ist erreicht. "
                        "Bitte versuche es später erneut."
                    )

                elif "503" in message:
                    st.error(
                        "Das KI-Modell ist derzeit überlastet. "
                        "Bitte versuche es in wenigen Minuten erneut."
                    )

                else:
                    st.error(
                        "Die Analyse ist fehlgeschlagen. "
                        "Bitte versuche es erneut."
                    )

            except Exception:
                st.error(
                    "Es ist ein unerwarteter Fehler aufgetreten. "
                    "Bitte versuche es erneut."
                )