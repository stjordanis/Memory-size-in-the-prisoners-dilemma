"""
A script from identifying best responses of reactive strategies
"""

import numpy as np
import sympy as sym
import opt_mo

from sympy.polys import subresultants_qq_zz
from scipy.optimize import fsolve
import itertools

def round_matrix_expressions(matrix, num_digits, variable):
    """
    Rounds matrix elements. The elements are polynomials of a given variable.
    """
    for i, element in enumerate(matrix):
        matrix[i] = element.subs({n : round(n, num_digits) 
                             for n in sym.Poly(element, variable).all_coeffs()})
    return matrix

def get_roots_eliminator_method(system, variable, other):
    """
    Uses eliminator to solve 2-variable system for a given variable.
    """
    matrix = subresultants_qq_zz.sylvester(system[0], system[1], other)
    matrix = round_matrix_expressions(matrix, 8, variable)

    resultant = matrix.det()
    num, den = sym.fraction(resultant.factor())
    
    # candidate roots
    coeffs = sym.Poly(num, variable).all_coeffs()
    roots = list(np.roots(coeffs))
    
    feasible_roots = []
    for root in roots:
        if not np.iscomplex(root):
            if root >= 0 and root <= 1:
                feasible_roots.append(root)
    
    if den != 1:
        for root in feasible_roots:
            if den.subs({variable: root}) == 0:
                feasible_roots.remove(root)

    return feasible_roots

def get_roots_of_second_unknown(system, variable, roots, other_variable):
    
    p_two_roots = []
    for root in roots:
        a = sym.lambdify(variable, system[0].subs({other_variable: root}))
        b = sym.lambdify(variable, system[1].subs({other_variable: root}))
        p_two_roots.append(fsolve(equations, x0=[0, 0], args=[a, b])[0])
    return p_two_roots

def equations(p, args):
    a, b = args
    v, _ = p
    return (a(v), b(v))

def reactive_set(opponents):
    p_1, p_2 = sym.symbols('p_1, p_2')
    utility = -opt_mo.tournament_utility((p_1, p_2, p_1, p_2), opponents)
    
    # derivatives
    derivatives = [sym.diff(utility, i) for i in [p_1, p_2]]
    derivatives = [expr.factor() for expr in derivatives]
    
    # numerator
    fractions = [sym.fraction(expr) for expr in derivatives]
    num = [expr[0] for expr in fractions]
    den = [expr[1] for expr in fractions]
    

    # roots for p_1
    p_one_roots = get_roots_eliminator_method(num, p_1, p_2)
    
    # roots for p_2
    p_two_roots = get_roots_of_second_unknown(num, p_2, p_one_roots, p_1)
    
    solution_set = set(p_one_roots) | set(p_two_roots) | set((0, 1))
    return solution_set

def argmax(opponents, solution_set):
           
    solutions = [(p_1, p_2, -opt_mo.tournament_utility((p_1, p_2, p_1, p_2), opponents))
                 for p_1, p_2 in itertools.combinations(solution_set, 2)]
    return max(solutions, key=lambda item:item[-1])