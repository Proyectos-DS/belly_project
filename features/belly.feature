# language: es

Característica: Característica del estómago

  @spanish
  Escenario: comer muchos pepinos y gruñir
    Dado que he comido 42 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir

  @spanish
  Escenario: comer pocos pepinos y no gruñir
    Dado que he comido 10 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

  @spanish
  Escenario: comer muchos pepinos y esperar menos de una hora
    Dado que he comido 50 pepinos
    Cuando espero media hora
    Entonces mi estómago no debería gruñir

  @spanish
  Escenario: comer pepinos y esperar en minutos
    Dado que he comido 30 pepinos
    Cuando espero 90 minutos
    Entonces mi estómago debería gruñir

  @spanish
  Escenario: comer pepinos y esperar en diferentes formatos
    Dado que he comido 25 pepinos
    Cuando espero "dos horas y treinta minutos"
    Entonces mi estómago debería gruñir

  @spanish
  Escenario: Comer pepinos y esperar en minutos y segundos
    Dado que he comido 35 pepinos
    Cuando espero "1 hora y 30 minutos y 45 segundos"
    Entonces mi estómago debería gruñir

  @spanish
  Escenario: Comer una cantidad fraccionaria de pepinos
    Dado que he comido 0.5 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

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

  @english
  Escenario: Esperar usando horas en ingles segundo ejemplo
    Dado que he comido 12.5 pepinos
    Cuando espero "90 minutes and 50 seconds"
    Entonces mi estómago debería gruñir


  @spanish
  Escenario: Esperar usando un tiempo aleatorio
    Dado que he comido 12.5 pepinos
    Cuando espero "entre 2 y 4 horas"
    Entonces mi estómago debería gruñir

  @spanish
  Escenario: Arrojar una excepcion si se ingresa una cantidad negativa de pepinos
    Dado que he comido -1 pepinos
    Entonces debería ocurrir un error de cantidad negativa de pepinos

  @spanish
  Escenario: Arrojar una excepcion si se ingresa una cantidad de pepinos mayor a 100
    Dado que he comido 101 pepinos
    Entonces debería ocurrir un error de cantidad mayor a 100