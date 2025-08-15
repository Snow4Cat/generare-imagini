# Generator de Imagini cu DALL·E 3

Această aplicație Streamlit folosește **OpenAI DALL·E 3** pentru a genera o singură imagine pe bază de prompt text.

## Caracteristici principale
- **Model:** DALL·E 3
- **Număr imagini:** 1 / request (limitat de API)
- **Dimensiuni suportate:** `1024x1024`, `1024x1792`, `1792x1024`
- **Calitate:** `standard` sau `hd`
- **Mock mode:** generează o imagine placeholder locală, fără apel la API
- **Fallback:** dacă API key lipsește/este invalidă → placeholder + mesaj
- **Persistența imaginii** până la o nouă generare

## Instalare locală
1. Clonează repository-ul:
```bash
git clone https://github.com/snow4cat/generare-imagini.git
cd generare-imagini
```
2. Instalează dependențele:
```bash
pip install -r requirements.txt
```
3. Adaugă cheia OpenAI în `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY="sk-..."
```
4. Rulează aplicația:
```bash
streamlit run app.py
```

## Deploy pe Streamlit Cloud
1. Publică proiectul pe GitHub.
2. În Streamlit Cloud → **New App**, selectează repo-ul.
3. În **Settings → Secrets**, adaugă:
```toml
OPENAI_API_KEY="sk-..."
```
4. Deploy.

## Utilizare
- Introdu promptul în câmpul de text.
- Selectează dimensiunea și calitatea dorită.
- Apasă **Generează**.
- Dacă Mock mode e activ sau API key lipsește/este invalidă, se generează un placeholder.
