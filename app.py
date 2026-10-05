import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

st.set_page_config(page_title="KI App Gap Analyst", page_icon="🧠")

st.title("🧠 KI App Gap Analyst")
st.write("Gib eine App-Idee ein und erhalte Zielgruppe, Feature-Lücken und MVP-Vorschläge.")

idea = st.text_area(
    "App-Idee",
    placeholder="Beispiel: Eine App für Studierende in Bremen mit Mensa-Speiseplänen, Stundenplan und Lerngruppen.",
    height=140,
)

if st.button("Analysieren", type="primary"):
    if not idea.strip():
        st.warning("Bitte gib zuerst eine App-Idee ein.")
    else:
        with st.spinner("Gemini analysiert deine Idee ..."):
            try:
                prompt = f"""
                Du bist ein erfahrener KI-App-Produktexperte.

                Analysiere diese App-Idee:
                {idea}

                Regeln:
                - Sei konkret und praxisnah.
                - Maximal 300 Wörter.
                - Nenne mindestens drei konkrete Feature-Lücken.
                - Das MVP enthält maximal fünf Features.
		- Verwende nur konkrete, überprüfbare Aussagen.
		- Nenne zu jeder Feature-Lücke ein praktisches Beispiel.
		- Erkläre kurz, warum jedes MVP-Feature wichtig ist.
		- Keine Wiederholungen.


                Antwortstruktur:
                ## Zielgruppe
                ## Kernproblem
                ## Vorhandene Wettbewerbsfeatures
                ## Fehlende Features
                ## MVP
                ## Risiken
                """
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt,
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Analyse fehlgeschlagen: {e}")

