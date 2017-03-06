import sympy
import sympy.parsing.sympy_parser

TRANSFORMATIONS = (sympy.parsing.sympy_parser.standard_transformations +
                  (sympy.parsing.sympy_parser.implicit_multiplication_application,))

def simple_solve(expr1, expr2, variables):
    return sympy.solveset(sympy.Eq(expr1, expr2),
                          sympy.Symbol(variables[0]),
                          domain=sympy.S.Reals)

def solve_all(expr1, expr2, variables):
    for var in variables:
        yield var, sympy.solveset(sympy.Eq(expr1, expr2),
                              sympy.Symbol(var),
                              domain=sympy.S.Reals)


def simple_expr_parse(text):
    return sympy.parsing.sympy_parser.parse_expr(text,
                                                 transformations=TRANSFORMATIONS,
                                                 evaluate=0)
