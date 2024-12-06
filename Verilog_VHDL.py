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
    Fonction pour convertir Verilog en VHDL ligne par ligne.
    - Entrée : fichier texte avec le code Verilog
    - Sortie : fichier texte avec le code VHDL ; coût = nombre de lignes contenant des opérateurs logiques
    """
    # Ouvrir une fenêtre pour sélectionner un fichier Verilog
    Tk().withdraw()  # Masquer la fenêtre principale Tkinter
    verilog_file = filedialog.askopenfilename(
        title="Sélectionner un fichier Verilog",
        filetypes=[("Fichiers Verilog", "*.txt"), ("Tous les fichiers", "*.*")]
    )

    if not verilog_file:
        print("Aucun fichier sélectionné :/")
        return

    # Lire le contenu du fichier Verilog ligne par ligne
    with open(verilog_file, 'r') as file:
        verilog_lines = file.readlines()

    # Nettoyer les lignes pour supprimer les espaces inutiles
    verilog_lines = [line.strip() for line in verilog_lines if line.strip()]

    # Variables pour stocker les informations extraites
    module_name = None
    ports = []
    inputs = []
    outputs = []
    wires = []
    assigns = []
    opérateurs = 0

    # Parcourir chaque ligne du fichier Verilog
    for line in verilog_lines:
        # Détecter le nom du module
        if line.startswith("module"):
            module_name = re.search(r'module\s+(\w+)', line).group(1)
            ports = re.search(r'\((.*?)\);', line).group(1).replace('\n', '').split(',')

        # Identifier les ports d'entrée et de sortie
        elif line.startswith("input"):
            inputs += [p.strip() for p in re.findall(r'\w+', line.replace("input", "").strip())]
        elif line.startswith("output"):
            outputs += [p.strip() for p in re.findall(r'\w+', line.replace("output", "").strip())]
        
        # Identifier les fils internes
        elif line.startswith("wire"):
            wires += [p.strip() for p in re.findall(r'\w+', line.replace("wire", "").strip())]

        # Identifier les assignations et compter les opérateurs logiques
        elif line.startswith("assign"):
            assigns.append(line)
            if any(op in line for op in ['^', '&', '|']):
                opérateurs += 1

    # Préparer les ports VHDL
    ports = [p.strip() for p in ports]
    vhdl_ports = []
    for port in ports:
        if port in inputs:
            vhdl_ports.append(f"{port} : in std_logic")
        elif port in outputs:
            vhdl_ports.append(f"{port} : out std_logic")

    # Préparer les signaux internes (wires)
    vhdl_signals = [f"signal {wire} : std_logic;" for wire in wires]

    # Préparer les assignations VHDL
    vhdl_assignments = []
    for assign in assigns:
        left, right = re.search(r'assign\s+(\w+)\s*=\s*(.*);', assign).groups()
        right = right.replace('^', 'xor').replace('&', 'and').replace('|', 'or')  # Conversion des opérateurs
        vhdl_assignments.append(f"{left.strip()} <= {right.strip()};")

    # Générer le code VHDL
    vhdl_code = "library IEEE;\n" + "use IEEE.STD_LOGIC_1164.ALL;\n" + "use IEEE.NUMERIC_STD.ALL;\n\n"
    vhdl_code += f"entity {module_name} is\n"
    vhdl_code += "port (\n    " + ";\n    ".join(vhdl_ports) + "\n);\n"
    vhdl_code += f"end {module_name};\n\n"
    vhdl_code += f"architecture {module_name}_struct of {module_name} is\n"
    vhdl_code += "    " + "\n    ".join(vhdl_signals) + "\n"
    vhdl_code += "begin\n"
    vhdl_code += "    " + "\n    ".join(vhdl_assignments) + "\n"
    vhdl_code += f"end {module_name}_struct;"

    # Sauvegarder le fichier VHDL
    vhdl_file = verilog_file.rsplit('.', 1)[0] + ".vhdl"
    with open(vhdl_file, 'w') as file:
        file.write(vhdl_code)

    # Afficher le résultat
    print(f"Fichier VHDL généré : {vhdl_file}")
    print(f"Nombre de lignes contenant des opérateurs logiques : {opérateurs}.")
    return opérateurs
