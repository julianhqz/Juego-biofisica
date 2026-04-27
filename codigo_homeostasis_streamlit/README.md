# Código Homeostasis

Juego serio en Streamlit para aprender sistemas humanos desde principios físicos: gradiente, flujo, presión, resistencia, energía, temperatura, membrana y retroalimentación.

## Qué incluye

- 5 sistemas: musculoesquelético, neuromuscular, cardiopulmonar, endocrino y vestibulococlear.
- Misiones por sistema.
- Imágenes anatómicas esquemáticas en SVG original.
- Sliders para manipular variables biofísicas.
- Puntaje automático de estabilidad del sistema.
- Retroalimentación automática.
- Descarga de reporte de misión en Markdown.
- Modo de mapa conceptual y comparador transversal.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Subir a GitHub y desplegar en Streamlit Community Cloud

1. Crear un repositorio en GitHub.
2. Subir estos archivos:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `README.md`
3. Entrar a Streamlit Community Cloud.
4. Crear una nueva app desde el repositorio de GitHub.
5. Seleccionar `app.py` como archivo principal.
6. Desplegar.

## Nota sobre imágenes

Las imágenes anatómicas son esquemas SVG originales creados dentro del código. No dependen de bancos de imágenes ni de material protegido por derechos de autor.
