# code_ex

Proyecto Python - Test de ingreso a MELI. 
Toma 3 fuentes de datos diferentes (prints, taps y pays) y genera como resultado un dataset listo para ser ingerido por el modelo de Machine Learning para predecir el orden de un conjunto de Propuestas de Valor (aka, Value Props) en el carrusel de la app llamado “Descubrí Más”.

## Instalación

1. Clona este repositorio.
2. Ejecuta el siguiente comando para instalar las dependencias:
   ```shell
   pip install -r requirements.txt
3. Para ejecutar el proyecto desde powershell realizar (dejo en local los archivos provistos, incluso en git)
   python src/main.py
4. Para ejecutar los test unitarios desde powershell realizar
   python -m unittest tests/TestDFSLoader.py
   python -m unittest tests/TestDoResult.py
5. Para ejecutarlo dentro de docker en local
   docker build -t code_ex .
   docker run -it code_ex  
