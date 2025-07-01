import pytest
import sys
import os

# base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# print("Base dir:", base_dir)
# sys.path.insert(0, os.path.join(base_dir, 'src'))
# sys.path.insert(0, os.path.join(base_dir, 'features'))
from src.belly import Belly


def test_comer_pepinos_fraccionarios():
    """Test que verifica que se pueden comer pepinos fraccionarios.
    """
    belly = Belly()
    belly.comer(1.5)
    assert belly.pepinos_comidos == 1.5


# def test_comer_peninos_fuera_de_rango():
#     """Test que valida que efectivamente no se pueden comer pepinos fuera
#     del rango de [0, 100]. Se espera una excepción de tipo ValueError
#     """
#     belly = Belly()
#     pepinos = -5
#     with pytest.raises(ValueError) as excinfo:
#         belly.comer(pepinos)
#     assert str(excinfo.value) == "No se permite una cantidad negativa de pepinos"
    
#     pepinos = 101
#     with pytest.raises(ValueError) as excinfo:
#         belly.comer(pepinos)
#     assert str(excinfo.value) == "No se permite una cantidad de pepinos mayor a 100"

@pytest.mark.parametrize(
        "pepinos, horas, grune",
        [
            (15, 3, True),
            (12, 5, True),
            (9, 20, False),
            (20, 1, False)
        ]
)
def test_grunir_si_comido_muchos_pepinos(pepinos, horas, grune):
    """
    Valida si se ha comido más de 10 pepinos y se espera más de dos horas, 
    entonces el estómago gruñe
    """
    # Arrange
    belly = Belly()

    # Act
    belly.comer(pepinos)
    belly.esperar(horas)

    # Assert
    assert belly.esta_gruñendo() == grune

@pytest.mark.parametrize(
        "pepinos_ingeridos",
        [(2), (40), (15) ]
)
def test_pepinos_comidos(pepinos_ingeridos):
    # Arrange
    belly = Belly()

    # Act
    belly.comer(pepinos_ingeridos)

    # Assert
    assert belly.pepinos_comidos == pepinos_ingeridos, f"Pepinos ingeridos y pepinos comidos (atributo) no coinciden"


@pytest.mark.parametrize(
        "pepinos, tiempo_horas",
        [
            (5, .5),
            (20, 4.55),
            (9, .45)
        ]
)
def test_reset(pepinos, tiempo_horas):
    # Arrange
    belly = Belly()
    belly.comer(pepinos)
    belly.esperar(tiempo_horas)
    
    # Act
    belly.reset()
    pepinos_comidos = belly.pepinos_comidos
    tiempo_esperado = belly.tiempo_esperado
    
    # Assert
    assert pepinos_comidos == 0, f"Fallo al hacer reset, pepinos_comidos: {pepinos_comidos}"
    assert tiempo_esperado == 0, f"Fallo al hacer reset, tiempo_esperado: {tiempo_esperado}" 



@pytest.mark.parametrize(
        "pepinos_negativos",
        [(-1), (-5), (-40), (-49.5)]
)
def test_ingerir_cantidad_negativa_pepinos(pepinos_negativos):
    
    # Arrange
    belly = Belly()
    
    # Act
    with pytest.raises(ValueError) as e:
        belly.comer(pepinos_negativos)
    
    # Assert
    assert str(e.value) == "No se permite una cantidad negativa de pepinos"