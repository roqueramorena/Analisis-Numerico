import numpy as np
import re

def evaluar_f(formula,x):
    formula_python = formula.replace('^','**')
    return eval(formula_python, {
        'x':x,
        'np':np,
        'sin':np.sin,
        'sen':np.sin,
        'cos':np.cos,
        'exp':np.exp,
        'log':np.log,
        'e': np.e,
        'pi': np.pi
    })

def formateador_pro(formula):
    f = formula.replace('**','^').replace('sen','sin')

    f = re.sub(r'\((.*?)\)/\(?([a-zA-Z0-9.x\s\+\-\*]+)\)?', r'\\frac{\1}{\2}', f)

    f = re.sub(r'\^\((.*?)\)', r'^{\1}', f)

    funciones = r'(sin|cos|exp|log|pi)'
    f = re.sub(funciones, r'\\\1', f)

    f = f.replace('*', r' \cdot ')

    return f'\\displaystyle f(x) = {f}'
