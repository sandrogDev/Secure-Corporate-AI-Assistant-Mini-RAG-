import os
from dotenv import load_dotenv
from google import genai

# 1. Carichiamo le chiavi di sicurezza
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Error: API Key not found!")

client = genai.Client(api_key=API_KEY)

# 2. Carichiamo la Knowledge Base (Il file con le regole aziendali)
try:
    with open("company_policy.txt", "r", encoding="utf-8") as file:
        company_knowledge = file.read()
except FileNotFoundError:
    raise FileNotFoundError("Error: 'company_policy.txt' not found!")

# 3. IL PROMPT "ANTI-ALLUCINAZIONE" BLINDATO
system_prompt = f"""
You are an official Customer Support Agent for 'Global Tech Store'.

Here is the OFFICIAL COMPANY POLICY. You must rely EXCLUSIVELY on this text:
<policy>
{company_knowledge}
</policy>

INSTRUCTIONS:
1. Answer the customer's query using ONLY the information inside the <policy> tags.
2. If the policy contains the answer, provide it clearly. You are allowed to use basic logic (e.g., if the user asks about Sunday, you know Sunday is a weekend).
3. If the answer is NOT stated in the <policy> (e.g., specific products, prices not listed), you MUST decline and say exactly: "I'm sorry, but I don't have that information in my current guidelines."
4. FATAL RULE: DO NOT use outside knowledge. Do not invent generic e-commerce procedures like "calculated at checkout". If a price is in the policy, quote it exactly.
"""

print("Secure Corporate AI Assistant Booting Up...")
print("Type 'exit' or 'quit' to close the chat.\n")
print("-" * 50)

# 4. Creiamo il ciclo interattivo (La chat nel terminale)
while True:
    # Chiediamo all'utente (te) di scrivere una domanda
    user_question = input("Customer: ")
    
    # Se scrivi exit, il programma si ferma
    if user_question.lower() in ['exit', 'quit']:
        print("Assistant: Goodbye! Shutting down...")
        break
        
    # Uniamo il prompt di sistema (con le regole) alla domanda dell'utente
    full_prompt = f"{system_prompt}\n\nCustomer Question: {user_question}"
    
    try:
        # Invochiamo Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        # Stampiamo la risposta dell'AI
        print(f"Assistant: {response.text.strip()}\n")
        
    except Exception as e:
        print(f"Network Error: {e}\n")