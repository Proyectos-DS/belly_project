from behave import given, when, then
import re
import random

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


# Se cambia el tipo de datos recibido en 'cukes' para que maneje datos de tipo flotantes
# Usar {cukes:f} me da errores
@given('que he comido {cukes:g} pepinos')
def step_given_eaten_cukes(context, cukes):
    context.belly.comer(cukes)

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
            
@then('mi estómago debería gruñir')
def step_then_belly_should_growl(context):
    assert context.belly.esta_gruñendo(), "Se esperaba que el estómago gruñera, pero no lo hizo."

@then('mi estómago no debería gruñir')
def step_then_belly_should_not_growl(context):
    assert not context.belly.esta_gruñendo(), "Se esperaba que el estómago no gruñera, pero lo hizo."

