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
    
def test_step_when_time_description_aleatorio():
    """Test para la función step_when_wait_time_description
    para cuando se ingrese una expresión 'entre a y b horas'
    """
    time_description = "entre 1 y 4 horas"
    context = Context()
    context.belly = Belly()
    step_when_wait_time_description(context, time_description)
    
    assert 1 <= context.belly.tiempo_esperado <= 4
    
    

