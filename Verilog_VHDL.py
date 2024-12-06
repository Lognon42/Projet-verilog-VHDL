"""
Code définissant les fonctions pour convertir des fichiers Verilog en VHDL
Loïc PAGNON
22/11/2024
A faire :
"""

import re
from tkinter import Tk, filedialog

def conversion():
    """
    Fonction pour convertir verilog en vhdl.
    - Entrée : fichier texte avec le code verilog
    - Sortie : fichier texte avec le code vhdl ; coût = nombre d'opérateurs booléens
    """
    # Ouvrir une fenêtre pour sélectionner un fichier Verilog
    Tk().withdraw()  # Masquer la fenêtre principale Tkinter
    verilog_file = filedialog.askopenfilename(
        title="Sélectionner un fichier Verilog",
        filetypes=[("Fichiers Verilog", "*.txt"), ("Tous les fichiers", "*.*")]
    )

    if not verilog_file:
        print("Aucun fichier sélectionné.")
        return

    # Lire le contenu du fichier Verilog
    with open(verilog_file, 'r') as file:
        verilog_code = file.read()

    # Nettoyer le code Verilog pour supprimer les espaces inutiles
    verilog_code = verilog_code.strip()

    # Remplacer les opérateurs Verilog par leurs équivalents VHDL
    verilog_code = verilog_code.replace('^', 'xor')
    verilog_code = verilog_code.replace('&', 'and')
    verilog_code = verilog_code.replace('|', 'or')

    # Analyse des sections importantes
    module_name = re.search(r'module\s+(\w+)', verilog_code).group(1)
    ports = re.search(r'\((.*?)\);', verilog_code, re.DOTALL).group(1).replace('\n', '').split(',')
    ports = [p.strip() for p in ports]
    
    inputs = re.findall(r'input\s+(.*?);', verilog_code)
    outputs = re.findall(r'output\s+(.*?);', verilog_code)
    wires = re.findall(r'wire\s+(.*?);', verilog_code)
    assigns = re.findall(r'assign\s+(.*?)\s*=\s*(.*?);', verilog_code)

    # Calculer le coût (nombre d'opérateurs logiques dans le circuit)
    operators = re.findall(r'[\^\&\|]', verilog_code)  # ^, &, et |
    cost = len(operators)

    # Préparer les ports VHDL
    vhdl_ports = []
    for port in ports:
        if any(port in inp for inp in inputs):
            vhdl_ports.append(f"{port} : in std_logic")
        elif any(port in outp for outp in outputs):
            vhdl_ports.append(f"{port} : out std_logic")

    # Préparer les signaux internes (wires)
    vhdl_signals = [f"signal {wire.strip()} : std_logic;" for wire in wires]

    # Préparer les assignations
    vhdl_assignments = [f"{left.strip()} <= {right.strip()};" for left, right in assigns]

    # Générer le code VHDL (en utilisant uniquement des chaînes concaténées)
    vhdl_code = "library IEEE;\n" + "use IEEE.STD_LOGIC_1164.ALL;\n" + "use IEEE.NUMERIC_STD.ALL;\n\n"
    vhdl_code += "entity " + module_name + " is\n"
    vhdl_code += "port (\n    " + ";\n    ".join(vhdl_ports) + ");\n"
    vhdl_code += "end " + module_name + ";\n\n"
    vhdl_code += "architecture " + module_name + "_struct of " + module_name + " is\n"
    vhdl_code += "    " + "\n    ".join(vhdl_signals) + "\n"
    vhdl_code += "begin\n"
    vhdl_code += "    " + "\n    ".join(vhdl_assignments) + "\n"
    vhdl_code += "end " + module_name + "_struct;"

    # Sauvegarder le fichier VHDL
    vhdl_file = verilog_file.rsplit('.', 1)[0] + ".vhdl"
    with open(vhdl_file, 'w') as file:
        file.write(vhdl_code)

    # Afficher le résultat
    print(f"Fichier VHDL généré : {vhdl_file}")
    print(f"Coût : {cost} opérateurs logiques.")
    return cost
