# Índice de Temas de Salud

Esta aplicación permite procesar un archivo XML con temas de salud (“health topics”) obtenidos de Medline Plus y lleva a
cabo análisis léxico y sintáctico del mismo, mostrando los datos resultantes al usuario de manera legible y agradable.

## Contenidos

- [Dependencias](#Dependencias)
- [Instalación](#Instalación)
- [Ejecución](#Ejecución)

## Dependencias

- Python 3.12+
- sentence-transformers
- matplotlib
- streamlit
- watchdog
- pandas
- ply

## Instalación

- Crear un entorno virtual

```bash
python -m venv venv
```

- Instalar el proyecto

```bash
pip install .
```

## Ejecución

```bash
health_topic_index
```
