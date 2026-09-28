import json
import requests
from pydantic import BaseModel, Field
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

JAVA_API_URL = "http://localhost:8080/api/soap-notes"

class SOAPNote(BaseModel):

    patientId: str = Field(
        default="",
        description="Patient ID mentioned in the conversation."
    )

    transcript: str = Field(
        default="",
        description="Original doctor-patient conversation."
    )

    subjective: str = Field(
        default="",
        description="Symptoms and information reported by the patient."
    )

    objective: str = Field(
        default="",
        description="Observable or measurable clinical information."
    )

    assessment: str = Field(
        default="",
        description="Doctor's assessment or possible condition."
    )

    plan: str = Field(
        default="",
        description="Treatment, medication, tests, or follow-up plan."
    )

transcript = """
Doctor: What brings you in today?

Patient: I have been having a cough for two days.

Doctor: Do you have any other problems?

Patient: No, I don't have any other problems.

Doctor: Any throat discomfort?

Patient: Yes, I have some throat discomfort.

Doctor: Okay. I will provide treatment for your throat and cough.
"""
prompt = f"""
You are a clinical documentation assistant.

Convert the following doctor-patient conversation into a structured SOAP note.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

patientId
transcript
subjective
objective
assessment
plan

If patient ID is not mentioned, use an empty string.

Do not invent medical information.

Doctor-patient conversation:

{transcript}
"""
print("Sending transcript to Ollama...")

try:

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=120
    )

    response.raise_for_status()

    ollama_result = response.json()

    generated_text = ollama_result.get("response", "")

    print("\nOllama response:")
    print(generated_text)


except requests.exceptions.RequestException as e:

    print("Error connecting to Ollama:")
    print(e)

    exit()

try:

    soap_data = json.loads(generated_text)

    soap_note = SOAPNote(**soap_data)

except Exception as e:

    print("\nError converting Ollama response to SOAP JSON:")
    print(e)

    print("\nReceived response:")
    print(generated_text)

    exit()

print("\nStructured SOAP Note:")
print(json.dumps(
    soap_note.model_dump(),
    indent=4
))

print("\nSending SOAP note to Java Spring Boot...")

try:

    java_response = requests.post(
        JAVA_API_URL,
        json=soap_note.model_dump(),
        timeout=30
    )

    java_response.raise_for_status()

    print("\nSOAP note successfully saved!")

    print("\nJava response:")
    print(json.dumps(
        java_response.json(),
        indent=4
    ))


except requests.exceptions.RequestException as e:

    print("\nError sending SOAP note to Java:")

    if hasattr(e, "response") and e.response is not None:
        print("Status:", e.response.status_code)
        print("Response:", e.response.text)

    else:
        print(e)