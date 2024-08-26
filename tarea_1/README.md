# Visualizador de Temas de Salud

## Instalación

### Dependencias

* streamlit>=1.37.1: para la GUI
* watchdog>=4.0.2: para monitorear cambios en archivos
* pandas>=2.2.2: para manejar datos
* matplotlib>=3.9.2: para graficar

## Ejecución

Desde el directorio raíz del proyecto(tarea_1), siga los siguientes pasos:

0. (Opcional) Se recomienda crear un entorno virtual para instalar las dependencias del proyecto. Para ello, ejecute el siguiente comando:

```bash
python -m venv venv
```

1. Para instalar las dependencias, ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

2. Para configurar el proyecto, ejecute el siguiente comando:

```bash
pip install -e .
```

3. Para ejecutar el proyecto, ejecute el siguiente comando:

```bash
streamlit run src/app.py
```
