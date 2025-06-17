# Merel's AI Appointment Assistant

## 💡 Wat dit script doet:
- Leest automatisch de laatste ongelezen e-mail
- Genereert met GPT-4 een vriendelijk antwoord
- Stuurt het antwoord automatisch terug via Gmail

## ▶️ Zo start je:
1. Zorg dat Python geïnstalleerd is
2. Zet je `.env` file in de hoofdmap (met je Gmail + API-sleutel)
3. Activeer de omgeving (optioneel):
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Installeer dependencies:
```bash
pip install openai python-dotenv
```
5. Run:
```bash
python main.py
```

✅ De assistent controleert je inbox en stuurt automatisch antwoord.
