# ChallengeDrive

ACLARACIONES SOBRE EL APLICATIVO:

- Realizado con Python 3.7
- En caso de no disponer de todas las librearías empleadas en el proyecto, se pueden instalar las mismas ejecutando: "pip install -r requirements.py" en la carpeta del proyecto.
- El archivo principal que contiene la función "main" es: challenge.py
- Para realizar un correcto envío de e-mail en el módulo "gmail.py", la cuenta de gmail que se utilizará debe estar configurada para aceptar "Aplicaciones menos seguras".
- El aplicativo solo cambia la visibilidad de "público" a "privado" de los archivos en la hora de cargar los mismos por primera vez en la Base de Datos. En futuras modificaciones de visibilidad de los archivos ya cargados, el aplicativo no los modifica automáticamente (solo almacena la modificación en la BD).
- El historial de todos los archivos que fueron públicos almacena los que justamente fueron públicos en algún momento (con anterioridad o actualmente).
- Se considera extensión "drive" a aquellos archivos "docs" de la unidad Drive.

BIBLIOGRAFÍA CONSULTADA:

- https://developers.google.com/drive/api/v3/about-sdk
- https://www.codecademy.com/learn/learn-python
