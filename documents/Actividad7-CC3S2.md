### Actividad: Pruebas BDD con behave en español

Este proyecto es un ejemplo de cómo utilizar **behave**, una herramienta para pruebas de desarrollo dirigido por comportamiento (Behavior-Driven Development - BDD) en Python, para escribir y ejecutar pruebas en español. Simula el comportamiento de un estómago (`Belly`) que gruñe o no en función de la cantidad de pepinos consumidos y el tiempo de espera.

### Objetivos de aprendizaje

Esta actividad tiene como propósito:

- Implementar los pasos de los escenarios BDD en Python, conectando las especificaciones de negocio con el código.
- Desarrollar pruebas unitarias con **Pytest**, aplicando principios de **TDD**.
- Estructurar correctamente un proyecto con **carpetas separadas para código fuente, pruebas unitarias y pruebas BDD**.
- Diseñar funciones capaces de interpretar y validar entradas humanas como descripciones de tiempo (ej. "dos horas y media").
- Manejar correctamente **errores y validaciones de entrada**, incluyendo casos fraccionarios o no válidos.
- Experimentar un ciclo completo de desarrollo: **historia de usuario → criterios de aceptación → pruebas → código → validación**.

### Tabla de contenidos

- [Requisitos previos](#requisitos-previos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Ejecutar las pruebas](#ejecutar-las-pruebas)
- [Detalles del proyecto](#detalles-del-proyecto)
- [Referencias](#referencias)

### Requisitos previos

- **Python 3.6** o superior
- **pip** (gestor de paquetes de Python)

### Estructura del proyecto

El proyecto tiene la siguiente estructura de directorios:

```
.
├── features
│   ├── belly.feature
│   ├── environment.py
│   └── steps
│       └── steps.py
├── src
│   └── belly.py
└── README.md
```

- **features**: Contiene los archivos relacionados con Behave.
  - **belly.feature**: Archivo que describe las características y escenarios en lenguaje Gherkin.
  - **environment.py**: Archivo de configuración para inicializar el contexto de Behave.
  - **steps**: Carpeta que contiene las definiciones de los pasos.
    - **steps.py**: Implementación de los pasos definidos en `belly.feature`.
- **src**: Contiene el código fuente del proyecto.
  - **belly.py**: Implementación de la clase `Belly`.
- **README.md**: Este archivo de documentación.

#### Instalación

Sigue estos pasos para configurar el entorno y ejecutar el proyecto:

1. **Clona el repositorio o descarga el código fuente**:

   ```bash
   git clone https://github.com/tu_usuario/tu_proyecto.git
   cd tu_proyecto
   ```

2. **Crea y activa un entorno virtual llamado act9**:

   ```bash
   python3 -m venv act9
   source act9/bin/activate  # En Windows usa: act9\Scripts\activate

   ```

3. **Instala las dependencias necesarias**:

   Si tienes un archivo `requirements.txt`, instala las dependencias con:

   ```bash
   pip install -r requirements.txt
   ```

   Si no tienes un `requirements.txt`, instala Behave directamente:

   ```bash
   pip install behave
   ```



### Ejecutar las pruebas

Para ejecutar las pruebas, utiliza el comando:

```bash
behave
```

Este comando buscará automáticamente los archivos `.feature` dentro de la carpeta `features` y ejecutará los escenarios definidos.


### Detalles del proyecto

#### Archivo `features/belly.feature`

Este archivo define las características y escenarios a probar utilizando el lenguaje Gherkin en español. Es importante especificar el idioma al inicio del archivo.

```gherkin
# language: es

Característica: Comportamiento del Estómago

  Escenario: Comer muchos pepinos y gruñir
    Dado que he comido 42 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir

  Escenario: Comer pocos pepinos y no gruñir
    Dado que he comido 10 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

  Escenario: Comer muchos pepinos y esperar menos de una hora
    Dado que he comido 50 pepinos
    Cuando espero media hora
    Entonces mi estómago no debería gruñir

  Escenario: Comer pepinos y esperar en minutos
    Dado que he comido 30 pepinos
    Cuando espero 90 minutos
    Entonces mi estómago debería gruñir

  Escenario: Comer pepinos y esperar en diferentes formatos
    Dado que he comido 25 pepinos
    Cuando espero "dos horas y treinta minutos"
    Entonces mi estómago debería gruñir
```

#### Archivo `features/steps/steps.py`

Contiene las definiciones de los pasos correspondientes a los escenarios en `belly.feature`. Se encarga de implementar la lógica detrás de cada paso.

```python
from behave import given, when, then
import re

# Función para convertir palabras numéricas a números
def convertir_palabra_a_numero(palabra):
    try:
        return int(palabra)
    except ValueError:
        numeros = {
            "cero": 0, "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
            "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11,
            "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciséis": 16,
            "diecisiete": 17, "dieciocho": 18, "diecinueve": 19, "veinte": 20,
            "treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70,
            "ochenta": 80, "noventa": 90, "media": 0.5
        }
        return numeros.get(palabra.lower(), 0)

@given('que he comido {cukes:d} pepinos')
def step_given_eaten_cukes(context, cukes):
    context.belly.comer(cukes)

@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    time_description = time_description.strip('"').lower()
    time_description = time_description.replace('y', ' ')
    time_description = time_description.strip()

    if time_description == 'media hora':
        total_time_in_hours = 0.5
    else:
        pattern = re.compile(r'(?:(\w+)\s*horas?)?\s*(?:(\w+)\s*minutos?)?')
        match = pattern.match(time_description)

        if match:
            hours_word = match.group(1) or "0"
            minutes_word = match.group(2) or "0"

            hours = convertir_palabra_a_numero(hours_word)
            minutes = convertir_palabra_a_numero(minutes_word)

            total_time_in_hours = hours + (minutes / 60)
        else:
            raise ValueError(f"No se pudo interpretar la descripción del tiempo: {time_description}")

    context.belly.esperar(total_time_in_hours)

@then('mi estómago debería gruñir')
def step_then_belly_should_growl(context):
    assert context.belly.esta_gruñendo(), "Se esperaba que el estómago gruñera, pero no lo hizo."

@then('mi estómago no debería gruñir')
def step_then_belly_should_not_growl(context):
    assert not context.belly.esta_gruñendo(), "Se esperaba que el estómago no gruñera, pero lo hizo."
```

#### Archivo `features/environment.py`

Inicializa el contexto antes de cada escenario, creando una nueva instancia de `Belly`.

```python
from src.belly import Belly

def before_scenario(context, scenario):
    context.belly = Belly()
```

#### Archivo `src/belly.py`

Implementa la lógica de la clase `Belly`, que simula el comportamiento del estómago.

```python
class Belly:
    def __init__(self):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0

    def comer(self, pepinos):
        self.pepinos_comidos += pepinos

    def esperar(self, tiempo_en_horas):
        self.tiempo_esperado += tiempo_en_horas

    def esta_gruñendo(self):
        # El estómago gruñe si ha esperado al menos 1.5 horas y ha comido más de 10 pepinos
        return self.tiempo_esperado >= 1.5 and self.pepinos_comidos > 10
```


---
#### Ejercicios

Presenta las respuestas de estos ejercicios utilizando la siguiente estructura de directorio **unificada** que incluye:

- **src**: Código fuente principal.  
- **features**: Escenarios BDD con Behave (incluye `belly.feature`, `steps` y `environment.py`).  
- **tests**: Pruebas unitarias con Pytest.  
- **requirements.txt**: Dependencias necesarias.  
- **.github/workflows (opcional)** o archivo `.gitlab-ci.yml` / `azure-pipelines.yml` para **CI/CD**.  

```
.
├── features
│   ├── belly.feature
│   ├── environment.py
│   └── steps
│       └── steps.py
├── src
│   ├── belly.py
│   ├── clock.py
│   └── __init__.py
├── tests
│   ├── test_belly.py
│   └── __init__.py
├── requirements.txt

```
Cuando termines **todos los ejercicios** (del 1 al 15, o los que hayas incluido en tu proyecto) y ejecutes tanto las pruebas **unitarias** (Pytest) como las **pruebas BDD** (Behave) dentro de tu pipeline de CI/CD (o localmente), la **salida final** que verás será algo parecido a esto:

1. **Salida de Pytest** mostrando:
   - Una lista de pruebas unitarias, cada una con su estado (`PASSED`, `FAILED`, etc.).
   - Un **resumen** con el número total de pruebas ejecutadas y cuántas pasaron o fallaron.
   - (Opcional) Un reporte de **cobertura de código** si usas `pytest-cov`.

   Por ejemplo, algo así en tu consola:
   ```
   ========================= test session starts =========================
   platform linux -- Python 3.9.10, pytest-7.3.1, py-1.11.0, pluggy-1.0.0
   rootdir: /home/runner/work/tu_proyecto/tu_proyecto
   plugins: cov-4.0.0
   collected 8 items

   tests/test_belly.py .........                                   [100%]

   ---------- coverage: platform linux, python 3.9.10 ----------
   Name                Stmts   Miss  Cover
   ---------------------------------------
   src/belly.py          45      2    95%
   src/clock.py           4      0   100%
   ---------------------------------------
   TOTAL                 49      2    96%

   ====================== 8 passed in 0.45s =====================
   ```

2. **Salida de Behave** mostrando:
   - La ejecución de cada **feature**, cada **escenario** y cada **step**.
   - Un **resumen final** con la cantidad de escenarios y pasos que pasaron o fallaron.
   
   Por ejemplo, en tu terminal:
   ```
   Feature: Comportamiento del Estómago (Belly)  # features/belly.feature
     Comer pepinos y esperar con horas, minutos y segundos
       Given que he comido 35
       When espero "1 hora y 30 minutos y 45 segundos"
       Then mi estómago debería gruñir ... PASSED

     Comer una cantidad fraccionaria de pepinos
       Given que he comido 0.5
       When espero "2 horas"
       Then mi estómago no debería gruñir ... PASSED

     Esperar usando horas en inglés
       Given que he comido 20
       When espero "two hours and thirty minutes"
       Then mi estómago debería gruñir ... PASSED

     Comer pepinos y esperar un tiempo aleatorio
       Given que he comido 25
       When espero "un tiempo aleatorio entre 1 y 3 horas"
       Then mi estómago debería gruñir ... PASSED

     Manejar una cantidad no válida de pepinos
       Given que he comido -5
       Then debería ocurrir un error de cantidad negativa. ... PASSED

     Comer 1000 pepinos y esperar 10 horas
       Given que he comido 1000
       When espero "10 horas"
       Then mi estómago debería gruñir ... PASSED

     Comer muchos pepinos y esperar el tiempo suficiente
       Given que he comido 15
       When espero "2 horas"
       Then mi estómago debería gruñir ... PASSED

     Saber cuántos pepinos puedo comer antes de gruñir
       Given que he comido 8
       When pregunto cuántos pepinos más puedo comer
       Then debería decirme que puedo comer 2 pepinos más ... PASSED


   1 feature passed, 8 scenarios passed, 0 failed, 0 skipped
   24 steps passed, 0 failed, 0 skipped
   ```

3. **Reporte y estado final en tu pipeline**:  
   - Si estás usando GitHub Actions, GitLab CI, Jenkins o cualquier otro, verás un **job de “build/test”** con un **estado “PASSED”** o “SUCCESS”.
   - Los **reportes** (JUnit, cobertura, etc.) quedarán **adjuntos** como “artifacts” o en la sección de reportes de tu plataforma.

En conjunto, la **salida final** refleja que:

- **Todas las pruebas unitarias** (TDD) han sido satisfactorias.  
- **Todos los escenarios BDD** (Behave) han concluido como `PASSED`.  
- Tu proyecto está **“verde”** y listo para ser desplegado o para continuar con la siguiente iteración.  

Ese **resultado verde** (todas las pruebas pasando) es el **objetivo final** de integrar todos los ejercicios en un flujo DevOps:  
- Validar la lógica básica con **Pytest**.  
- Validar el comportamiento de negocio con **Behave**.  
- Automatizarlo todo en un **pipeline** para tener feedback continuo y rápido.


#### Ejercicio 1: **Añadir soporte para minutos y segundos en tiempos de espera**

**Objetivo**  
- Ampliar la funcionalidad para reconocer tiempos de espera expresados en horas, minutos y segundos.

**Instrucciones**  
1. **Modifica** la función que maneja el tiempo de espera en `steps.py` (o donde parsees el tiempo) para que acepte:
   - "1 hora y 30 minutos"
   - "90 minutos"
   - "3600 segundos"
   - **Variaciones** que incluyan segundos (por ejemplo, `"1 hora, 30 minutos y 45 segundos"`).
2. **Implementa** un escenario de prueba en Gherkin (`belly.feature`) que valide que el estómago gruñe o no según estas variaciones de tiempo.
3. **Considera** también crear pruebas unitarias con Pytest para la lógica de parsing (función que convierte el texto de tiempo en horas decimales).
4. **En un entorno DevOps**:
   - Agrega la ejecución de `behave` y `pytest` en tu *pipeline* de CI/CD, de modo que al hacer push de los cambios se ejecuten automáticamente las pruebas.

**Ejemplo Gherkin**:
```gherkin
Escenario: Comer pepinos y esperar en minutos y segundos
  Dado que he comido 35 pepinos
  Cuando espero "1 hora y 30 minutos y 45 segundos"
  Entonces mi estómago debería gruñir
```


---

1. **Modifica**:

Método `step_when_wait_time_description` para capturar los segundos: 

```python
@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    time_description = time_description.strip('"').lower()
    time_description = time_description.replace('y', ' ')
    time_description = time_description.strip()

    # Manejar casos especiales como 'media hora'
    if time_description == 'media hora':
        total_time_in_hours = 0.5
    else:
        # Expresión regular para extraer horas y minutos, ahora agregamos tambien segundos
        pattern = re.compile(r'(?:(\w+)\s*horas?)?\s*(?:(\w+)\s*minutos?)?\s*(?:(\w+)\s*segundos?)?')
        match = pattern.match(time_description)

        if match:
            hours_word = match.group(1) or "0"
            minutes_word = match.group(2) or "0" 
            seconds_word = match.group(3) or "0" # Agregamos el caso para segundos

            hours = convertir_palabra_a_numero(hours_word)
            minutes = convertir_palabra_a_numero(minutes_word)
            seconds = convertir_palabra_a_numero(seconds_word) # Obtenemos el valor numerico de los segundos

            total_time_in_hours = hours + (minutes / 60) + (seconds / 3600) # Añadimos el calculo de segundos
        else:
            raise ValueError(f"No se pudo interpretar la descripción del tiempo: {time_description}")

    context.belly.esperar(total_time_in_hours)
```


2. **Implementa** un escenario de prueba en Gherkin (`belly.feature`) que valide que el estómago gruñe o no según estas variaciones de tiempo.

Escenario añadido a `belly.feature`:

```gherkin
  Escenario: Comer pepinos y esperar en minutos y segundos
    Dado que he comido 35 pepinos
    Cuando espero "1 hora y 30 minutos y 45 segundos"
    Entonces mi estómago debería gruñir
```

Observamos que el escenario paso la prueba Behave

<img src="imgs/Pasted image 20250423222433.png" >


3. **Considera** también crear pruebas unitarias con Pytest para la lógica de parsing (función que convierte el texto de tiempo en horas decimales).

He creado la primera prueba unitaria del proyecto: `test_belly_steps.py`

```python
import pytest
import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("Base dir:", base_dir)
sys.path.insert(0, os.path.join(base_dir, 'src'))
sys.path.insert(0, os.path.join(base_dir, 'features'))
from belly import Belly
from steps.belly_steps import step_when_wait_time_description

class Context:
    """Esta clase me ayuda a simular el contexto de Behave
    """
    def __init__(self):
        self.belly = None

def test_step_when_time_description():
    """Test para la función step_when_wait_time_description
    """
    time_description1 = "2 horas y 30 minutos y 20 segundos"
    
    context = Context()
    context.belly = Belly()
    step_when_wait_time_description(context, time_description1)
    
    assert context.belly.tiempo_esperado == (2 + (30 / 60) + (20 / 3600))
```


Observamos que la prueba se ejecuto correctamente:

<img src="imgs/Pasted image 20250423222954.png" >


4. **En un entorno DevOps**:
   - Agrega la ejecución de `behave` y `pytest` en tu *pipeline* de CI/CD, de modo que al hacer push de los cambios se ejecuten automáticamente las pruebas.

Presento mi archivo `ci.yml`:

```yml
name: Ejecutar Pruebas

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-one: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
      name: Checkout repository

    - name: Set up Python 3.x
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt

    - name: Run Behave Tests
      run: |
        source venv/bin/activate
        behave features

    - name: Run Pytest Unit Tests
      run: |
        source venv/bin/activate
        pytest tests
```


El pipeline se ejecuto correctamente (en el segundo intento):

<img src="imgs/Pasted image 20250423224743.png" >


---


#### Ejercicio 2: **Manejo de cantidades fraccionarias de pepinos**

**Objetivo**  
- Permitir que el sistema acepte cantidades fraccionarias de pepinos (decimales).

**Instrucciones**  
1. **Modifica** el sistema (la clase `Belly` y los steps en Behave) para que acepte entradas como `"0.5"`, `"2.75"`.
2. **Implementa** un nuevo escenario en Gherkin donde se ingiera una cantidad fraccionaria y verifica el comportamiento.
3. **Valida** que el sistema lance una excepción o error si se ingresa una cantidad negativa de pepinos.
4. **Pruebas unitarias**:  
   - Cubre el caso de pepinos fraccionarios en `test_belly.py`.
   - Cubre también el caso de pepinos negativos (se espera un error).

**Ejemplo Gherkin**:
```gherkin
Escenario: Comer una cantidad fraccionaria de pepinos
  Dado que he comido 0.5 pepinos
  Cuando espero 2 horas
  Entonces mi estómago no debería gruñir
```

**En un entorno DevOps**:
- Asegúrate de que la falla (excepción por valor negativo) sea reportada como *falla de build* si ocurre.  
- Configura notificaciones (por correo/Slack/Teams) si alguna de las pruebas falla.


---

1. **Modifica** el sistema (la clase `Belly` y los steps en Behave) para que acepte entradas como `"0.5"`, `"2.75"`.

```python
# Se cambia el tipo de datos recibido en 'cukes' para que maneje datos de tipo flotantes
# Usar {cukes:f} me da errores
@given('que he comido {cukes:g} pepinos')
def step_given_eaten_cukes(context, cukes):
    context.belly.comer(cukes)
```


2. **Implementa** un nuevo escenario en Gherkin donde se ingiera una cantidad fraccionaria y verifica el comportamiento.

He agregado dos escenarios para validar que se puede ingerir una cantidad fraccionaria de pepinos.

```gherkin
  Escenario: Comer una cantidad fraccionaria de pepinos
    Dado que he comido 0.5 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

  Escenario: Comer una cantidad fraccionaria de pepinos

    Dado que he comido 2.75 pepinos
    Cuando espero "treinta minutos y 40 segundos"
    Entonces mi estómago no debería gruñir

```

Vemos que se ejecutaron exitosamente: 

<img src="imgs/Pasted image 20250424153010.png" >

3. **Valida** que el sistema lance una excepción o error si se ingresa una cantidad negativa de pepinos.


He modificado el método `comer()` de la clase `Belly` para que cumpla la condición pedida
```python
    def comer(self, pepinos):
        if pepinos < 0:
            raise ValueError("Cantidad de pepinos invalida. No se permiten pepinos negativos.")
        print(f"He comido {pepinos} pepinos.")
        self.pepinos_comidos += pepinos
```

Al agregar este escenario en `belly.feature`
```gherkin
    Escenario: Comer una cantidad fraccionaria de pepinos
    Dado que he comido -8 pepinos
    Cuando espero "treinta minutos y 40 segundos"
    Entonces mi estómago no debería gruñir
```

Vemos que lanza la excepción: 
<img src="imgs/Pasted image 20250424184328.png" >


4. **Pruebas unitarias**:  
   - Cubre el caso de pepinos fraccionarios en `test_belly.py`.
   - Cubre también el caso de pepinos negativos (se espera un error).


He creado el archivo ``test_belly.py`` para definir las pruebas unitarias para la clase `Belly`

```python
import pytest
import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("Base dir:", base_dir)
sys.path.insert(0, os.path.join(base_dir, 'src'))
sys.path.insert(0, os.path.join(base_dir, 'features'))
from belly import Belly


def test_comer_pepinos_fraccionarios():
    """Test que verifica que se pueden comer pepinos fraccionarios.
    """
    belly = Belly()
    belly.comer(1.5)
    assert belly.pepinos_comidos == 1.5


def test_comer_peninos_negativos():
    """Test que valida que efectivamente no se pueden comer pepinos negativos.
    Se espera una excepción de tipo ValueError
    """
    belly = Belly()
    with pytest.raises(ValueError) as excinfo:
        belly.comer(-5)
    assert str(excinfo.value) == "Cantidad de pepinos invalida. No se permiten pepinos negativos."
```


---
#### Ejercicio 3: **Soporte para idiomas múltiples (Español e Inglés)**

**Objetivo**  
- Aceptar descripciones de tiempo en distintos idiomas (español e inglés).

**Instrucciones**  
1. **Modifica** el parsing de tiempo para que reconozca palabras clave en inglés, además de español (por ejemplo, `"two hours"`, `"thirty minutes"`).
2. **Escribe** al menos dos escenarios de prueba en Gherkin que usen tiempos en inglés.
3. **Implementa** una función que convierta las palabras en inglés a valores numéricos (similar a la que se usa para el español).
4. **En un pipeline DevOps**, podrías:
   - Dividir los escenarios en distintos *tags* (`@spanish`, `@english`) y ejecutar cada conjunto en etapas diferentes, o en paralelo.

**Ejemplo Gherkin**:
```gherkin
Escenario: Esperar usando horas en inglés
  Dado que he comido 20 pepinos
  Cuando espero "two hours and thirty minutes"
  Entonces mi estómago debería gruñir
```


----

1. **Modifica** el parsing de tiempo para que reconozca palabras clave en inglés, además de español (por ejemplo, `"two hours"`, `"thirty minutes"`).

He modificado el método `convertir_palabra_a_numero` de `belly_steps.py` para soportar palabras en inglés.
```python
# Función para convertir palabras numéricas a números
def convertir_palabra_a_numero(palabra):
    try:
        return int(palabra)
    except ValueError:
        numerosa_castellano = {
            "cero": 0, "uno": 1, "una":1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
            "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11,
            "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciséis": 16,
            "diecisiete":17, "dieciocho":18, "diecinueve":19, "veinte":20,
            "treinta": 30, "cuarenta":40, "cincuenta":50, "sesenta":60, "setenta":70,
            "ochenta":80, "noventa":90, "media": 0.5
        }
        
        numeros_english = {
            "zero": 0, "one": 1, "a": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
            "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
            "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80, "ninety": 90, "half": 0.5
        }

        
        palabra = palabra.lower()
        if palabra in numerosa_castellano:
            return numerosa_castellano[palabra]
        elif palabra in numeros_english:
            return numeros_english[palabra]
        else:
            raise ValueError(f"No se puede convertir la palabra '{palabra}' a un numero")


```

Hecho esto, modifico el método `step_when_wait_time_description` para que el regex capture palabras numéricas en ingles.

```python

@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    time_description = time_description.strip('"').lower()
    # Agregamos un espacio antes de 'y' para que no capture palabas como 'thirty'
    # Y añadimos la conversión de 'and' a vacío
    time_description = time_description.replace(' y', ' ').replace('and', ' ')
    time_description = time_description.strip()

    # Manejar casos especiales como 'media hora'
    if time_description == 'media hora':
        total_time_in_hours = 0.5
    else:
        # Mejoramos la expresion regular para que contemple palabras en ingles
        pattern = re.compile(r'(?:(\w+)\s*(?:horas?|hours?))?\s*(?:(\w+)\s*(?:minutos?|minutes?)?)?\s*(?:(\w+)\s*(?:segundos?|seconds?)?)?')
        match = pattern.match(time_description)
# Las demás líneas no se modificaron ...
```

2. **Escribe** al menos dos escenarios de prueba en Gherkin que usen tiempos en inglés.

Estos son los dos escenarios que agregué:

```gherkin
  Escenario: Esperar usando horas en inglés
    Dado que he comido 20 pepinos
    Cuando espero "two hours and thirty minutes"
    Entonces mi estómago debería gruñir

  Escenario: Esperar usando horas en ingles segundo ejemplo
    Dado que he comido 12.5 pepinos
    Cuando espero "90 minutes and 50 seconds"
    Entonces mi estómago debería gruñir
```

Podemos observar que se ejecutaron con éxito:


<img src="imgs/Pasted image 20250424192943.png" >

3. **Implementa** una función que convierta las palabras en inglés a valores numéricos (similar a la que se usa para el español).

Esto ya lo implementé en el paso 1.

4. **En un pipeline DevOps**,

A continuación muestro las modificaciones que hice:

He agregado etiquetas en cada escenario:

```gherkin
  @spanish
  Escenario: Comer una cantidad fraccionaria de pepinos
    Dado que he comido 2.75 pepinos
    Cuando espero "treinta minutos y 40 segundos"
    Entonces mi estómago no debería gruñir

  @english
  Escenario: Esperar usando horas en inglés
    Dado que he comido 20 pepinos
    Cuando espero "two hours and thirty minutes"
    Entonces mi estómago debería gruñir
```

Referencia: [Tutorial 11: Use Tags — behave 1.2.6.1: Examples and Tutorials](https://behave.github.io/behave.example/tutorials/tutorial11.html)

<img src="imgs/Pasted image 20250424223149.png" >

<img src="imgs/Pasted image 20250424223211.png" >


Y se modifico el archivo `ci.yml` para ejecutar `behave` por tipo de escenario

```yml
# ---
    - name: Run Behave Tests Spanish
      run: |
        source venv/bin/activate
        behave --tags=@spanish

    - name: Run Behave Tests English
      run: |
        source venv/bin/activate
        behave --tags=@english
# --
```



----
#### Ejercicio 4: **Manejo de tiempos aleatorios**

**Objetivo**  
- Permitir ingresar rangos de tiempo (por ejemplo, "entre 1 y 3 horas") y escoger un tiempo aleatorio dentro de ese rango.

**Instrucciones**  
1. **Crea** una función que, dada una expresión como "entre 1 y 3 horas", devuelva un valor aleatorio entre 1 y 3 horas.
2. **Implementa** un escenario en Gherkin que verifique que, tras comer pepinos y esperar un tiempo aleatorio, el estómago puede gruñir.
3. **Imprime** (en consola o logs) el tiempo aleatorio elegido para que el resultado sea rastreable en tu pipeline.
4. **En un pipeline DevOps**:  
   - Considera utilizar un *seed* de aleatoriedad fijo para evitar *flakiness* (tests intermitentes).  
   - O, si manejas aleatoriedad real, acepta el riesgo de pruebas no deterministas y monitorea cuidadosamente.

**Ejemplo Gherkin**:
```gherkin
Escenario: Comer pepinos y esperar un tiempo aleatorio
  Dado que he comido 25 pepinos
  Cuando espero un tiempo aleatorio entre 1 y 3 horas
  Entonces mi estómago debería gruñir
```


---
1. **Crea** 

Se ha creado la función `obtener_tiempo_aleatorio` para que cumpla el punto 1.

```python
def obtener_tiempo_aleatorio(expresion):
    # entre 1 y 3 horas
    pattern = re.compile(r'entre\s+(\d+)\s+y\s+(\d+)\s+horas')
    match = pattern.match(expresion)
    if match and match.group(1) and match.group(2):
        min_hours = int(match.group(1))
        max_hours = int(match.group(2))
        random_hour = random.uniform(min_hours, max_hours)
        print(f"Tiempo aleatorio en horas entre {min_hours} y {max_hours}: {random_hour}")
        return random_hour
    else:
        raise ValueError(f"Hay un error al evaluar {expresion}")
```



2. **Implementa** un escenario en Gherkin.

Se ha añadido el escenario que contempla ingresar una expresión que describa un "rango" para producir un tiempo esperado aleatorio:

```gherkin
  @spanish
  Escenario: Esperar usando un tiempo aleatorio
    Dado que he comido 12.5 pepinos
    Cuando espero "entre 2 y 4 horas"
    Entonces mi estómago debería gruñir
```


<img src="imgs/Pasted image 20250426111231.png" >


3. **Imprime** (en consola o logs) el tiempo aleatorio elegido para que el resultado sea rastreable en tu pipeline.

La linea:
```python
print(f"Tiempo aleatorio en horas entre {min_hours} y {max_hours}: 
```

Ya se encuentra en el método `obtener_tiempo_aleatorio`.

**A su vez, he añadido un test unitario para validar el tiempo aleatorio**

```python
def test_step_when_time_description_aleatorio():
    """Test para la función step_when_wait_time_description
    para cuando se ingrese una expresión 'entre a y b horas'
    """
    time_description = "entre 1 y 4 horas"
    context = Context()
    context.belly = Belly()
    step_when_wait_time_description(context, time_description)
    
    assert 1 <= context.belly.tiempo_esperado <= 4
```


4. **En un pipeline DevOps**:  
   - Considera utilizar un *seed* de aleatoriedad fijo para evitar *flakiness* (tests intermitentes).  

He añadido estas líneas que fijan una semilla para el random, antes de que se ejecuten los Test de Behave:

```yml
    - name: Set random seed to avoid flakiness
      run: |
        python -c "import random; random.seed(28)"

    - name: Run Behave Tests Spanish
```

Al hacer push a mi repo, se ejecuto el pipeline exitosamente. 

<img src="imgs/Pasted image 20250426120452.png" >

Sin embargo, no pude observar que numero aleatorio arrojo, por lo que edite el archivo `ci.yml` nuevamente:

```yml
    - name: Run Pytest Unit Tests
      run: |
        source venv/bin/activate
        pytest -v --capture=no
```

<img src="imgs/Pasted image 20250426121908.png" >


----


#### Ejercicio 5: **Validación de cantidades no válidas**

**Objetivo**  
- Manejar y reportar adecuadamente errores al ingresar cantidades no válidas.

**Instrucciones**  
1. **Añade** validaciones para evitar que el usuario ingrese < 0 pepinos o > 100 pepinos.
2. **Modifica** la lógica para arrojar un error (excepción) si la cantidad no es válida.
3. **Implementa** un escenario de prueba que verifique el comportamiento de error.
4. **En tu pipeline**, verifica que la excepción se maneje y el test falle de manera controlada si el sistema no lanza la excepción esperada.

**Ejemplo Gherkin**:
```gherkin
Escenario: Manejar una cantidad no válida de pepinos
  Dado que he comido -5 pepinos
  Entonces debería ocurrir un error de cantidad negativa.
```

---

1. **Añade** validaciones para evitar que el usuario ingrese < 0 pepinos o > 100 pepinos.

Se ha agregado la validación generando una excepción si se ingresa una cantidad de pepinos fuera del rango $[0, 100]$.

```python
    def comer(self, pepinos):
        if pepinos < 0:
            raise ValueError("No se permite una cantidad negativa de pepinos")
        if pepinos > 100:
            raise ValueError("No se permite una cantidad de pepinos mayor a 100")
        print(f"He comido {pepinos} pepinos.")
        self.pepinos_comidos += pepinos
```


2. **Modifica** la lógica para arrojar un error (excepción) si la cantidad no es válida.

He modificado el archivo `test_belly.py`

```python
def test_comer_peninos_fuera_de_rango():
    """Test que valida que efectivamente no se pueden comer pepinos fuera
    del rango de [0, 100]. Se espera una excepción de tipo ValueError
    """
    belly = Belly()
    pepinos = -5
    with pytest.raises(ValueError) as excinfo:
        belly.comer(pepinos)
    assert str(excinfo.value) == f"{pepinos} es una cantidad invalida"
    
    pepinos = 101
    with pytest.raises(ValueError) as excinfo:
        belly.comer(pepinos)
    assert str(excinfo.value) == f"{pepinos} es una cantidad invalida"
    
```


Validamos el test para el método modificado (anteriormente era `test_comer_peninos_negativos`)
	
<img src="imgs/Pasted image 20250427113315.png" >

3. **Implementa** un escenario de prueba que verifique el comportamiento de error.

Si añado este escenario:

```gherkin
  @english
  Escenario: Esperar dado que ha comido una cantidad invalida de pepinos
    Dado que he comido 101 pepinos
    Cuando espero "1 hour and 40 minutes"
    Entonces mi estómago debería gruñir
```

Observo que me sale la excepción:

<img src="imgs/Pasted image 20250427114026.png" >

A continuación añadiré los escenarios necesarios (el escenario anterior se eliminará)

```gherkin
  @spanish
  Escenario: Arrojar una excepcion si se ingresa una cantidad negativa de pepinos
    Dado que he comido -1 pepinos
    Entonces debería ocurrir un error de cantidad negativa de pepinos

  @spanish
  Escenario: Arrojar una excepcion si se ingresa una cantidad de pepinos mayor a 100
    Dado que he comido 101 pepinos
    Entonces debería ocurrir un error de cantidad mayor a 100
```

Para lo cual modifico el método `step_given_eaten_cukes`

```python
# Se cambia el tipo de datos recibido en 'cukes' para que maneje datos de tipo flotantes
# Usar {cukes:f} me da errores
@given('que he comido {cukes:g} pepinos')
def step_given_eaten_cukes(context, cukes):
    try: # Si se ingresa una cantidad valida
        context.belly.comer(cukes)
        context.error_occurred = False
    except ValueError as err: # Si se ingresa una cantidad invalida
        context.error_occurred = True
        context.error_message = str(err)
```

Y el método `step_when_wait_time_description` :
```python
@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    time_description = time_description.strip('"').lower()
    if time_description.startswith('entre'):
        try:
            random_hour = obtener_tiempo_aleatorio(time_description)
            context.belly.esperar(random_hour)
        except ValueError as err:
            print(err)
    else: 
        # Agregamos un espacio antes de 'y' para que no capture palabas como 'thirty'
        # Y añadimos la conversión de 'and' a vacío
        time_description = time_description.replace(' y', ' ').replace('and', ' ')
        time_description = time_description.strip()

        # Manejar casos especiales como 'media hora'
        if time_description == 'media hora':
            total_time_in_hours = 0.5
        else:
            # Mejoramos la expresion regular para que contemple palabras en ingles
            pattern = re.compile(r'(?:(\w+)\s*(?:horas?|hours?))?\s*(?:(\w+)\s*(?:minutos?|minutes?)?)?\s*(?:(\w+)\s*(?:segundos?|seconds?)?)?')
            match = pattern.match(time_description)

            if match:
                hours_word = match.group(1) or "0"
                minutes_word = match.group(2) or "0" 
                seconds_word = match.group(3) or "0" # Agregamos el caso para segundos

                hours = convertir_palabra_a_numero(hours_word)
                minutes = convertir_palabra_a_numero(minutes_word)
                seconds = convertir_palabra_a_numero(seconds_word) # Obtenemos el valor numerico de los segundos

                total_time_in_hours = hours + (minutes / 60) + (seconds / 3600) # Añadimos el calculo de segundos
                    
            else:
                raise ValueError(f"No se pudo interpretar la descripción del tiempo: {time_description}")
        context.belly.esperar(total_time_in_hours)
```

Para poder capturar correctamente las excepciones cuando se ingresa una cantidad invalida

4. **En tu pipeline**, verifica que la excepción se maneje y el test falle de manera controlada si el sistema no lanza la excepción esperada.

Después de un pequeño error el pipeline se ejecuto sin problemas:

<img src="imgs/Pasted image 20250427120648.png" >



---

#### Ejercicio 6: **Escalabilidad con grandes cantidades de pepinos**

**Objetivo**  
- Asegurar que el sistema no falle ni se ponga lento con cantidades y tiempos muy grandes.

**Instrucciones**  
1. **Añade** soporte para manejar cantidades de pepinos como 1000 (más allá del límite de validación anterior, o ajusta ese límite para pruebas internas).
2. **Implementa** un escenario en Gherkin para comer 1000 pepinos y esperar 10 horas.
3. **Verifica** que el sistema sigue comportándose correctamente (sin timeouts ni errores de rendimiento).
4. **En un pipeline DevOps**:
   - Ejecuta pruebas de estrés o de larga duración (puedes simular) para garantizar la robustez.
   - Mide el tiempo de ejecución para asegurarte de que no aumente drásticamente.

**Ejemplo Gherkin**:
```gherkin
Escenario: Comer 1000 pepinos y esperar 10 horas
  Dado que he comido 1000 pepinos
  Cuando espero 10 horas
  Entonces mi estómago debería gruñir
```


----
1. **Añade** soporte para manejar cantidades de pepinos como 1000 (más allá del límite de validación anterior, o ajusta ese límite para pruebas internas).



2. **Implementa** un escenario en Gherkin para comer 1000 pepinos y esperar 10 horas.



3. **Verifica** que el sistema sigue comportándose correctamente (sin timeouts ni errores de rendimiento).



4. **En un pipeline DevOps**:
   - Ejecuta pruebas de estrés o de larga duración (puedes simular) para garantizar la robustez.
   - Mide el tiempo de ejecución para asegurarte de que no aumente drásticamente.



----

#### Ejercicio 7: **Descripciones de tiempo complejas**

**Objetivo**  
- Ampliar la lógica para manejar descripciones avanzadas tipo `"1 hora, 30 minutos y 45 segundos"`.

**Instrucciones**  
1. **Refuerza** la expresión regular y parsing para que soporte múltiples separadores (comas, "y", espacios, etc.).
2. **Implementa** escenarios que cubran al menos 2-3 variaciones complejas en Gherkin.
3. **Valida** que el total en horas sea exacto (suma de horas, minutos, segundos).
4. **En un pipeline**:  
   - Puedes analizar la cobertura de pruebas (coverage) para asegurarte de que la nueva lógica de parsing está completamente testeada.

**Ejemplo Gherkin**:
```gherkin
Escenario: Manejar tiempos complejos
  Dado que he comido 50 pepinos
  Cuando espero "1 hora, 30 minutos y 45 segundos"
  Entonces mi estómago debería gruñir
```

#### Ejercicio 8: **De TDD a BDD – Convertir requisitos técnicos a pruebas en Gherkin**

**Objetivo**  
- Practicar el paso de una prueba unitaria técnica a un escenario BDD comprensible por el negocio.

**Instrucciones**  
1. **Escribe** un test unitario básico con Pytest que valide que si se han comido más de 10 pepinos y se espera 2 horas, el estómago gruñe.
2. **Convierte** ese test unitario en un escenario Gherkin, con la misma lógica, pero más orientado al usuario.
3. **Implementa** los pasos en Behave (si no existen).
4. **En un pipeline DevOps**:
   - Ejecuta primero los tests unitarios (rápidos) y luego los tests de Behave (que pueden ser más lentos y de nivel de integración).

**Ejemplo de test unitario** (TDD):
```python
def test_gruñir_si_comido_muchos_pepinos():
    belly = Belly()
    belly.comer(15)
    belly.esperar(2)
    assert belly.esta_gruñendo() == True
```

**Ejemplo Gherkin** (BDD):

```gherkin
Escenario: Comer muchos pepinos y esperar el tiempo suficiente
  Dado que he comido 15 pepinos
  Cuando espero 2 horas
  Entonces mi estómago debería gruñir
```

#### Ejercicio 9: **Identificación de criterios de aceptación para historias de usuario**

**Objetivo**  
- Traducir una historia de usuario en criterios de aceptación claros y escenarios BDD.

**Instrucciones**  
1. **Toma** la historia de usuario:  
   > "Como usuario que ha comido pepinos, quiero saber si mi estómago va a gruñir después de esperar un tiempo suficiente, para poder tomar una acción."
2. **Identifica** los criterios de aceptación (por ejemplo, cuántos pepinos y cuánto tiempo se debe esperar).
3. **Escribe** escenarios Gherkin que reflejen esos criterios.
4. **Implementa** los pasos en Behave.
5. **En un pipeline**:
   - Asegúrate de vincular (por ejemplo, en GitLab Issues o GitHub Issues) los escenarios con la historia de usuario para tener *traceability* (rastreabilidad).

**Ejemplo de escenarios Gherkin**:
```gherkin
Escenario: Comer suficientes pepinos y esperar el tiempo adecuado
  Dado que he comido 20 pepinos
  Cuando espero 2 horas
  Entonces mi estómago debería gruñir

Escenario: Comer pocos pepinos y no esperar suficiente tiempo
  Dado que he comido 5 pepinos
  Cuando espero 1 hora
  Entonces mi estómago no debería gruñir
```

#### Ejercicio 10: **Escribir pruebas unitarias antes de escenarios BDD**

**Objetivo**  
- Demostrar la secuencia TDD (tests unitarios) → BDD (escenarios).

**Instrucciones**  
1. **Escribe** un test unitario para una nueva función, por ejemplo, `pepinos_comidos()`, que retorna el total de pepinos ingeridos.
2. **Crea** un escenario Gherkin que describe este comportamiento desde el punto de vista del usuario.
3. **Implementa** los pasos en Behave y verifica que pase la misma validación.
4. **En un pipeline**:  
   - Ejecución secuencial: 1) Pytest, 2) Behave.  
   - O en etapas separadas para un mejor feedback.

**Ejemplo de test unitario**:
```python
def test_pepinos_restantes():
    belly = Belly()
    belly.comer(15)
    assert belly.pepinos_comidos == 15
```

**Ejemplo Gherkin**:
```gherkin
Escenario: Saber cuántos pepinos he comido
  Dado que he comido 15 pepinos
  Entonces debería haber comido 15 pepinos
```


#### Ejercicio 11: **Refactorización guiada por TDD y BDD**

**Objetivo**  
- Refactorizar código existente sin romper funcionalidades, validado por pruebas unitarias y escenarios BDD.

**Instrucciones**  
1. **Elige** una funcionalidad ya existente (por ejemplo, `esta_gruñendo()`).
2. **Escribe** (o asegura que existen) pruebas unitarias que cubran los casos clave.  
3. **Refactoriza** el código (`Belly` o funciones auxiliares) para mejorar eficiencia, legibilidad o reducir duplicación.
4. **Valida** que todas las pruebas unitarias y escenarios BDD siguen pasando sin cambios.
5. **En un pipeline**:
   - Activa la medición de **coverage** para asegurarte de que la refactorización no rompa funcionalidades no cubiertas.

**Ejemplo de test unitario**:
```python
def test_estomago_gruñendo():
    belly = Belly()
    belly.comer(20)
    belly.esperar(2)
    assert belly.esta_gruñendo() == True
```

**Ejemplo Gherkin**:
```gherkin
Escenario: Verificar que el estómago gruñe tras comer suficientes pepinos y esperar
  Dado que he comido 20 pepinos
  Cuando espero 2 horas
  Entonces mi estómago debería gruñir
```


#### Ejercicio 12: **Ciclo completo de TDD a BDD – Añadir nueva funcionalidad**

**Objetivo**  
- Desarrollar una nueva funcionalidad *desde cero* con TDD (prueba unitaria) y BDD (escenarios Gherkin).

**Instrucciones**  
1. **Imagina** una nueva funcionalidad, por ejemplo, "Predecir si el estómago gruñirá con una cantidad dada de pepinos y un tiempo de espera".
2. **Escribe** primero la prueba unitaria.
3. **Conviértelo** en una historia de usuario y escribe el escenario BDD.
4. **Implementa** y verifica que tanto la prueba unitaria como el escenario Gherkin pasen.
5. **En tu pipeline**, revisa que no haya *regresiones* en otros tests.

**Ejemplo de test unitario**:
```python
def test_estomago_predecir_gruñido():
    belly = Belly()
    belly.comer(12)
    belly.esperar(1.5)
    assert belly.esta_gruñendo() == True
```

**Ejemplo Gherkin**:
```gherkin
Escenario: Predecir si mi estómago gruñirá tras comer y esperar
  Dado que he comido 12 pepinos
  Cuando espero 1.5 horas
  Entonces mi estómago debería gruñir
```


#### Ejercicio 13: **Añadir criterios de aceptación claros**

**Objetivo**  
- Definir con precisión los criterios de aceptación de una nueva funcionalidad y plasmarlos en Gherkin.

**Instrucciones**  
1. **Define** una nueva historia de usuario (por ejemplo, "Ver cuántos pepinos me faltan para gruñir").
2. **Identifica** al menos 2-3 criterios de aceptación.
3. **Convierte** esos criterios en escenarios BDD.
4. **Implementa** los pasos.  
5. **En un pipeline**, agrupa los escenarios bajo un mismo *tag* (`@criterio_nuevo`) para ejecutarlos juntos.

**Ejemplo**:
```gherkin
Escenario: Ver cuántos pepinos puedo comer antes de que el estómago gruña
  Dado que he comido 8 pepinos
  Cuando pregunto cuántos pepinos más puedo comer
  Entonces debería decirme que puedo comer 2 pepinos más
```


#### Ejercicio 14: **Integración con Mocking, Stubs y Fakes (para DevOps)**

**Objetivo**  
- Demostrar cómo inyectar dependencias simuladas en tu clase `Belly` y usarlas en pruebas BDD y TDD.

**Instrucciones**  
1. **Crea** un archivo `clock.py` (por ejemplo) con una función `get_current_time()`.
2. **Modifica** `Belly` para aceptar un `clock_service` opcional que se inyecta.
3. **Crea** un test unitario con Pytest que use `unittest.mock` para simular el paso del tiempo.
4. **En Behave**, usa `environment.py` para inyectar un mock o stub del reloj en el `before_scenario`.
5. **En un pipeline DevOps**:
   - Asegúrate de no depender de la hora real, así evitas inestabilidad en las pruebas.

**Ejemplo**:
```python
def before_scenario(context, scenario):
    from unittest.mock import MagicMock
    from src.belly import Belly
    
    fake_clock = MagicMock()
    fake_clock.return_value = 10000  # tiempo fijo
    context.belly = Belly(clock_service=fake_clock)
```


#### Ejercicio 15: **Despliegue y validación continua en un entorno de integración (CI/CD)**

**Objetivo**  
- Completar el ciclo DevOps: Cada push al repositorio **desencadena** pruebas automáticas BDD y TDD.

**Instrucciones**  
1. **Configura** un pipeline (por ejemplo, en GitHub Actions o GitLab CI) con estos pasos:
   - Instalar dependencias (Python, Behave, Pytest).
   - Ejecutar pruebas unitarias (Pytest).
   - Ejecutar pruebas de comportamiento (Behave).
   - Generar reportes (HTML, JUnit) y publicarlos como *artifacts*.
2. **Incluye** verificación de calidad de código (por ejemplo, flake8 o black).
3. **Al aprobarse** el pipeline, **despliega** (si corresponde) tu aplicación o *script* a un entorno de staging/producción.


---

#### Referencias

- [Documentación de Behave](https://behave.readthedocs.io/en/latest/)
- [Referencia de Gherkin](https://cucumber.io/docs/gherkin/reference/)
- [Desarrollo Dirigido por Comportamiento (BDD) en Wikipedia](https://es.wikipedia.org/wiki/Desarrollo_guiado_por_pruebas#Desarrollo_guiado_por_el_comportamiento)

#### Notas adicionales

- **Idioma**: Asegúrate de que todos los archivos `.feature` comienzan con `# language: es` para indicar que los pasos están en español.
- **Codificación**: Guarda todos los archivos en formato UTF-8 para evitar problemas con caracteres especiales.
- **Versión de Behave**: Se recomienda utilizar la última versión de Behave para garantizar el soporte completo del idioma español.