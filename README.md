# **Sistema de Barrido de Llamadas**



Este proyecto implementa un sistema para:



* Registrar llamadas iniciales desde una API.



* Realizar un proceso de "barrido" para mejorar registros con categoría *bad* hasta que todos sean *medium o good.*



* Generar estadísticas y resultados del proceso.



## Tecnologías utilizadas



* Python 3.10+



* SQLAlchemy (ORM para conexión a base de datos)



* Pytest (pruebas automatizadas)



* PostgreSQL o MySQL (base de datos relacional)



* Requests (para consumo de APIs externas)



* Flask (para exponer endpoints CRUD)



## &nbsp;Estructura del proyecto



prueba-tecnica/

│

├─ app/

│  ├─ models.py            # Definición de tablas y modelos

│  ├─ repositories/        # Acceso a datos

│  ├─ services/            # Lógica de negocio

│  └─ controllers/         # Controladores principales

│

├─ scripts/                # Scripts ejecutables

├─ tests/                  # Pruebas automatizadas

├─ requirements.txt        # Dependencias

├─ run.py                  # Punto de entrada principal

└─ README.md               # Documentación



## Instalación y ejecución

##### 1\. Clonar repositorio



git clone https://github.com/usuario/prueba-tecnica.git

cd prueba-tecnica



##### 2\. Crear entorno virtual

###### Linux / Mac



python -m venv venv

source venv/bin/activate



###### Windows



python -m venv venv

venv\\Scripts\\activate

##### 

##### 3\. Instalar dependencias



pip install -r requirements.txt



##### 4\. Crear tablas y cargar datos iniciales



python scripts/create\_tables.py

python scripts/initial\_load.py



##### 5\. Ejecutar el barrido



python scripts/run\_barrido.py



##### 6\. Consultar estado actual



python scripts/check\_status.py



##### 7\. Ejecutar pruebas



pytest -v



### Ejecución en Postman

##### 

##### Levantar la API



python run.py



##### Listar registros (GET)



URL: http://127.0.0.1:5000/registros/



###### Método: GET



URL: http://127.0.0.1:5000/registros/





##### Crear registro (POST)



URL: http://127.0.0.1:5000/registros/



Método: POST



Body (JSON):



{

&nbsp; "value": 50,

&nbsp; "category": "bad"

}



##### Actualizar registro (PUT)



URL: http://127.0.0.1:5000/registros/6



Método: PUT



Body (JSON):



{

&nbsp; "value": 80,

&nbsp; "category": "good"

}





##### Eliminar registro (DELETE)



URL: http://127.0.0.1:5000/registros/6



Método: DELETE



Respuesta esperada:



{

&nbsp; "message": "True"

}





### Resultados del barrido



Número de llamadas iniciales: 100



Número de barridos realizados: 19



Total de registros finales: 300



Total de intentos (SUM attempts): 718



Distribución final por categoría:



good: 112



medium: 188



bad: 0



SQL consultas

### 

### Arquitectura y principios SOLID



**Single Responsibility**: Cada servicio, repositorio y controlador tiene su propia responsabilidad.



**Open/Closed:** Fácil de extender sin modificar código base.



**Liskov Substitution**: Interfaces claras para reemplazar implementaciones.



**Interface Segregation**: Clases separadas para cada acción concreta.



**Dependency Inversion:** Inyección de dependencias para desacoplar módulos.



### Consultas SQL útiles para el reporte final



**Total de registros**



sql



SELECT COUNT(\*) FROM registros;



**Distribución por categoría**



sql



SELECT category, COUNT(\*) AS cantidad

FROM registros

GROUP BY category;



**Total de llamadas (sumando attempts)**



sql



SELECT SUM(attempts) AS llamadas\_totales

FROM registros;



**Barridos realizados**



sql



SELECT COUNT(\*) AS num\_barridos

FROM barridos;

### 

### Esquema de tablas



sql



CREATE TABLE registros (

&nbsp;   id INT AUTO\_INCREMENT PRIMARY KEY,

&nbsp;   value INT NOT NULL,

&nbsp;   attempts INT NOT NULL DEFAULT 0,

&nbsp;   category ENUM('bad', 'medium', 'good') NOT NULL,

&nbsp;   created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP,

&nbsp;   updated\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP ON UPDATE CURRENT\_TIMESTAMP

);



CREATE TABLE barridos (

&nbsp;   id INT AUTO\_INCREMENT PRIMARY KEY,

&nbsp;   sweep\_number INT NOT NULL,

&nbsp;   records\_checked INT NOT NULL,

&nbsp;   records\_improved INT NOT NULL,

&nbsp;   created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

);



### Manejo de errores, reintentos y anti-ráfagas



##### \*\*Cliente HTTP (ApiService)\*\*

* `**timeout**`: 6s por solicitud (evita que una llamada cuelgue el proceso).
* `**max\_retries`**: 3 intentos por llamada cuando hay errores transitorios.
* `**backoff\_factor`**: 0.5 (esperas crecientes: 0.5s, 1.0s, 2.0s…).
* &nbsp;**Validación de respuesta:** conversión segura de `value` a `int` y chequeo de `category` (`bad|medium|good`).
* **\*\*Anti-ráfagas\*\***: `min\_delay=0.12s` entre llamadas → ~8.3 req/s máx.



#### \*\*Barrido (BarridoService)\*\*

* Repite ciclos mientras existan `bad` (hasta `max\_sweeps`).
* Cada intento suma en `attempts` aun si la llamada falla (trazabilidad).
* Si la nueva categoría es `medium|good`, actualiza el registro; si no, lo deja igual.
* Si el API falla en un registro, se registra el intento y el barrido continúa (no cae todo el proceso).



### \*\*Controladores (CRUD)\*\*

* Responden JSON coherente.
* Errores comunes:
* &nbsp; `400` (datos inválidos): falta `value` o `category`.
* &nbsp; `404` (no encontrado): id inexistente.
* &nbsp; `500` (error interno): error no controlado.



### \*\*Reproducibilidad\*\*

* `scripts/check\_status.py` imprime métricas (total, distribución, SUM(attempts), barridos).
* Consultas SQL equivalentes están documentadas.



### Resumen final

El sistema logró barrer todas las llamadas con categoría bad en 19 iteraciones, quedando 0 registros en esa categoría 

y un total de 718 intentos acumulados. Esto garantiza que todos los registros finales están en estado medium o good, cumpliendo 

con los objetivos planteados.















































































