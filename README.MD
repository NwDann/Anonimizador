1. pip install -r requirements.txt
2. python -m uvicorn api:app --reload
3. Abrir el html y cargar un PDF
4. Para generar un nuevo ejecutable:
   pyinstaller --noconfirm --onedir --windowed --collect-all spacy --collect-all es_core_news_lg --collect-all presidio_analyzer main.py
