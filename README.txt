SESION 06 - RETRIEVAL AVANZADO

Continuidad del proyecto: parsing, OCR, chunks e indice vectorial existentes.
Ejecuta los comandos desde esta carpeta. Usa Python 3.11 o superior.

PREPARACION ANTES DE CLASE
1. Activa el entorno: source .venv/bin/activate
2. Instala dependencias: python -m pip install -r requirements.txt
3. La configuracion se carga desde .env o variables de entorno. Se requiere
   OPENAI_API_KEY para embeddings, OCR y transformaciones con el LLM.
   OPENAI_MODEL, OPENAI_EMBEDDING_MODEL y OPENAI_VISION_MODEL son opcionales.
   No muestres ni compartas la clave en clase.
4. Pre-descarga el reranker:
   python -c "from retrieval_advanced import load_reranker; load_reranker(); print('reranker OK')"
5. Genera los PDFs sinteticos del guion:
   python 00b_generar_docs_retrieval.py
6. Reconstruye el indice con los documentos nuevos:
   python 07_indexar_documentos.py
   Este paso reemplaza data/indice/vector_store.json, procesa TODOS los PDFs
   y usa OpenAI para embeddings y OCR del escaneado. Hazlo antes de clase.
   Usa el mismo modelo de embeddings para indexar y consultar. El JSON anterior
   no registra el nombre del modelo; la dimension por si sola no lo identifica.
7. Comprueba continuidad:
   python 08_consultar_indice.py --query "cuantos dias de vacaciones tengo" --top-k 3
8. Pruebas locales, sin llamadas externas:
   python -m unittest -v

SECUENCIA DE CLASE (120 MINUTOS)
0-5: Apertura: retrieval selecciona evidencia; aun no genera una respuesta RAG.
5-15: python 08_consultar_indice.py --query "Error F110-031 SAP" --top-k 5
15-30: python 09_busqueda_bm25.py --query "F110-031" --top-k 5
       python 09_busqueda_bm25.py --query "como recuperar acceso a mi cuenta"
30-45: python 10_busqueda_hibrida.py --query "Error F110-031 SAP"
45-57: python 11_rrf.py --query "Error F110-031 SAP" --candidate-k 10
57-72: python 12_reranking.py --query "Error F110-031 SAP" --candidate-k 20 --top-k 5
72-84: python 13_query_rewriting.py
84-95: python 14_multi_query.py
95-106: python 15_hyde.py --query "Por que puede fallar un proceso automatico de pagos"
106-116: python 16_retrieval_avanzado.py --query "Error F110-031 SAP" --candidate-k 20 --top-k 5
         python 16_retrieval_avanzado.py --query "Por que fallo lo de ayer" --history "Revisamos SAP F110 del 2026-09-03 y aparecio F110-031"
116-120: Reconstruir la arquitectura y explicar cada responsabilidad.

COMPARACIONES Y DIFERENCIAS RESPECTO AL GUION
- retrieval_advanced.py concentra las funciones para recorrerlas por bloques.
- 10 muestra rankings separados; 11 los fusiona por posiciones, no scores crudos.
- Se conserva chunk_id para deduplicar: el proyecto ya dispone de ese campo.
- BM25 conserva acentos y codigos; omite documentos sin terminos compartidos.
- candidate-k es un maximo: un corpus pequeno puede entregar menos candidatos.
- 14 usa SAP, presente en el corpus, e incluye fusion RRF y deduplicacion.
  --query permite probar otra pregunta; --n controla las variantes solicitadas.
- 15 distingue texto hipotetico de evidencia real; no entrega una respuesta RAG.
- 16 permite --no-rewrite para comparar con/sin reformulacion.
- El reranker se carga una vez por proceso; la primera descarga requiere red.
- Los ejemplos SAP son sinteticos del guion, no instrucciones operativas oficiales.
- document_search.py e ingest_documents.py pertenecen al recorrido lexico anterior;
  esta sesion utiliza data/indice/vector_store.json.
- Los scripts 00 a 06 no necesitan ejecutarse otra vez para seguir esta clase.
- Si falta tiempo, abrevia Multi-Query y HyDE y conserva el pipeline integrado.
