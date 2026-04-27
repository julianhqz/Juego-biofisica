# Rehab Quest: Biofísica en acción

Aplicación educativa en Streamlit para enseñar ocho conceptos físicos esenciales en fisiología humana aplicada a rehabilitación:

1. Gradiente  
2. Flujo  
3. Presión  
4. Resistencia  
5. Energía  
6. Temperatura  
7. Membrana  
8. Retroalimentación  

La app funciona como un juego serio. El estudiante calibra variables fisiológicas y recibe un **puntaje de éxito de 0 a 5**, junto con retroalimentación formativa.

## Enfoque pedagógico

El objetivo no es memorizar definiciones, sino comprender cómo los principios físicos sostienen fenómenos relevantes para fisioterapia, fonoaudiología, terapia ocupacional y ciencias de la rehabilitación.

Cada estación incluye:

- Misión jugable.
- Variables manipulables.
- Imagen SVG original.
- Métricas de desempeño fisiológico.
- Puntaje de éxito de 0 a 5.
- Retroalimentación.
- Preguntas de discusión.
- Historial de intentos.
- Descarga de resultados en CSV.
- Descarga de reporte en Markdown.

## Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

1. Subir estos archivos a GitHub.
2. Entrar a Streamlit Community Cloud.
3. Crear una nueva app.
4. Seleccionar este repositorio.
5. Archivo principal: `app.py`.
6. Desplegar.

## Archivos

```text
.
├── app.py
├── requirements.txt
├── README.md
└── .streamlit
    └── config.toml
```

## Nota sobre imágenes

Las imágenes anatómicas/fisiológicas son esquemas conceptuales originales construidos con SVG dentro de la aplicación. No utilizan imágenes externas ni material con derechos de autor.
