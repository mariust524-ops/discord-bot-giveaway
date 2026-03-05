"""Simple calculatrice en Python — addition, soustraction, multiplication, division

Usage (ligne de commande interactive):
python calculator.py

Fonctions:
- add(a, b)
- subtract(a, b)
- multiply(a, b)
- divide(a, b)

Contient aussi une fonction `demo()` pour vérification automatique.
"""

import sys


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division par zéro impossible")
    return a / b


def _parse_number(s):
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Valeur numérique invalide: {s}")


def main():
    print("Calculatrice simple — tapez 'q' pour quitter")
    while True:
        try:
            left = input("Nombre 1: ").strip()
            if left.lower() in ("q", "quit", "exit"):
                break
            op = input("Opération (+ - * /): ").strip()
            if op.lower() in ("q", "quit", "exit"):
                break
            right = input("Nombre 2: ").strip()
            if right.lower() in ("q", "quit", "exit"):
                break

            a = _parse_number(left)
            b = _parse_number(right)

            if op == "+":
                res = add(a, b)
            elif op == "-":
                res = subtract(a, b)
            elif op == "*" or op == "x":
                res = multiply(a, b)
            elif op == "/":
                res = divide(a, b)
            else:
                print("Opération non reconnue. Utilisez +, -, * ou /.")
                continue

            print(f"Résultat: {res}\n")

        except Exception as e:
            print(f"Erreur: {e}\n")


def demo():
    print("Exécution du mode demo — tests rapides")
    tests = [
        (add, 2, 3, 5),
        (subtract, 5, 2, 3),
        (multiply, 4, 3, 12),
        (divide, 10, 2, 5),
    ]
    for fn, a, b, expected in tests:
        out = fn(a, b)
        print(f"{fn.__name__}({a}, {b}) = {out} -> attendu {expected}")
    try:
        divide(1, 0)
    except ZeroDivisionError:
        print("divide(1, 0) lève bien ZeroDivisionError (attendu)")
    print("Demo terminée.")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        main()
