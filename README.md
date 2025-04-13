# Streamlit Translator App

Una aplicación de traducción de idiomas basada en Streamlit con funcionalidad de texto a voz.

## Características

- Traducción en tiempo real entre múltiples idiomas
- Funcionalidad de texto a voz para escuchar las traducciones
- Interfaz de usuario moderna y receptiva
- Traducción automática mientras escribes
- Botón para copiar el texto traducido al portapapeles

## Tecnologías utilizadas

- Streamlit para la interfaz de usuario
- Googletrans para las traducciones
- gTTS (Google Text-to-Speech) para la conversión de texto a voz

## Cómo ejecutar localmente

1. Clona este repositorio:
```
git clone <url-de-tu-repositorio>
cd streamlit-translator
```

2. Instala las dependencias:
```
pip install -r render_requirements.txt
```

3. Ejecuta la aplicación:
```
streamlit run app.py
```

## Despliegue en Render.com

Esta aplicación está configurada para ser desplegada fácilmente en Render.com:

1. Sube este repositorio a GitHub
2. En Render.com, selecciona "New Web Service"
3. Conecta tu repositorio de GitHub
4. Selecciona la rama principal
5. Usar la configuración automática de render.yaml

## Estructura del proyecto

- `app.py`: Punto de entrada principal de la aplicación
- `translator.py`: Módulo para manejar las traducciones
- `audio.py`: Módulo para la conversión de texto a voz
- `languages.py`: Lista de idiomas soportados
- `.streamlit/config.toml`: Configuración de Streamlit
- `render_requirements.txt`: Dependencias para despliegue
- `render.yaml`: Configuración para despliegue en Render.com