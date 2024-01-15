# Pizzeria_Web
Repositorio parte Web del Proyecto de Metodologias Ágiles

# Pasos para clonar el repositorio

1. Crear una Carpeta de Trabajo: Inicie creando una carpeta en su computadora donde alojará el proyecto.
2. Clonar el Repositorio: Abra la consola de comandos y navegue hasta la carpeta que ha creado. Ejecute el siguiente comando para clonar el repositorio:

      git clone https://github.com/criticalRobin/trying_websockets_django.git
      
3. Preparación del Entorno Virtual: Antes de continuar, asegúrese de tener instalado Python y el gestor de paquetes pip. Puede verificar su instalación con los comandos python --version y pip --version.
4. Instalación de Virtualenv: Si no tiene virtualenv instalado, puede hacerlo mediante pip con el siguiente comando:

   pip install virtualenv

5. Creación del Entorno Virtual: Dentro de la carpeta del proyecto, cree un entorno virtual ejecutando: python3 -m venv env
6. Activación del Entorno Virtual: Antes de proceder con la instalación de dependencias y la configuración del proyecto, active el entorno virtual.

   En Windows, use: env\Scripts\activate

   En sistemas Unix o MacOS, use: source env/bin/activate

7. Instalación de Dependencias: Una vez activado el entorno virtual, instale las dependencias del proyecto ejecutando:

   pip install -r requirements.txt

8. Instalación de redis: Una vez instaladas las dependencias, abra una nueva consola y ejecute el comando:
  
   sudo apt install redis-server

9. Comprobar instalación: En la consola que instaló redis use el comando:

    redis-server

   Si la instalación se realizó con éxito vera lo mismo que en la imagen a continuación:

   ![image](https://github.com/criticalRobin/trying_websockets_django/assets/133540422/2b34d3d9-1582-4054-a14b-f6a3e89ea34a)

10. Ejecutar migraciones: En la consola en la que esta dentro del proyecto clonado ejecute las migraciones necesarias con el comando:

    python manage.py migrate

11. Crear Super Usuario: Finalmente ejecute el comando: python manage.py createsuperuser y complete el formulario de registro, con esto ya podrá acceder al admin view del proyecto de Django.
12. Ejecución del sistema: Una vez realizados todos los pasos anteriores en la consola donde instaló redis ejecute el comando:

    redis-server

    Una vez redis este corriendo, en la consola en la que se encuentra dentro del proyecto clonado con el entorno virtual activado ejecute el comando: daphne pizzeria.asgi:application

    Si ve el resultado de la imagen el sistema ha sido levantado de forma correcta:

    ![image](https://github.com/criticalRobin/trying_websockets_django/assets/133540422/d74ac631-e53f-408a-a545-748b1ee902e8)

    Por último ingrese a la siguiente dirección dentro del navegador: http://127.0.0.1:8000/

