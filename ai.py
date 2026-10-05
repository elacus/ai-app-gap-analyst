import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def analyse_app_idea(idea: str) -> str:
    prompt = f"""
    Du bist ein erfahrener KI-App-Produktexperte.

    Analysiere diese App-Idee:
    {idea}

    Gib eine kompakte Analyse mit:
    - Zielgruppe
    - Kernproblem
    - Vorhandene Wettbewerbsfeatures
    - Fehlende Features
    - MVP mit maximal fünf Features
    - Größte Risiken
    """
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    idee = input("Beschreibe deine App-Idee: ")
    print(analyse_app_idea(idee))