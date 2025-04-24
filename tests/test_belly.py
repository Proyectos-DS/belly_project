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
    

