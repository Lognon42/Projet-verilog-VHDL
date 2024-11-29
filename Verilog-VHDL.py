import re
from tkinter import Tk, filedialog

# Initialiser la fenêtre Tkinter
root = Tk()
root.withdraw()  # Masquer la fenêtre principale

# Définir les types de fichiers acceptés
filetypes = [("Fichiers Verilog", "*.v *.sv"), ("Tous les fichiers", "*.*")]

# Demander à l'utilisateur de sélectionner un fichier Verilog
selected_file = filedialog.askopenfilename(title="Sélectionnez un fichier Verilog", filetypes=filetypes)
if not selected_file:
    print("Aucun fichier sélectionné. Opération annulée.")
    exit()

# Lire le contenu du fichier sélectionné ligne par ligne
try:
    with open(selected_file, 'r') as file:
        lines = file.readlines()
    print(f"Fichier sélectionné : {selected_file}")
except Exception as e:
    print(f"Erreur lors de la lecture du fichier : {e}")
    exit()

# Liste pour stocker les lignes modifiées
modified_lines = []

# Ajouter les bibliothèques nécessaires au début du fichier VHDL
vhdl_header = """\
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

"""
modified_lines.append(vhdl_header)

# Variables pour détecter le nom du module
module_name = None
ports_list = []

# Parcourir chaque ligne du fichier
for line in lines:
    line = line.strip()  # Supprimer les espaces inutiles autour de la ligne

    # Identifier le nom du module et les ports
    module_match = re.match(r"module\s+(\w+)\s*\((.*)\);", line)
    if module_match:
        module_name = module_match.group(1)
        ports = module_match.group(2)
        ports_list = [port.strip() for port in ports.split(",")]
        modified_lines.append(f"entity {module_name} is\n    port (\n")
        continue

    # Gérer la déclaration des ports
    for port in ports_list:
        port_match = re.match(r"(input|output)\s*(\[.*\])?\s*(\w+)", port)
        if port_match:
            direction = "in" if port_match.group(1) == "input" else "out"
            size = port_match.group(2)
            name = port_match.group(3)
            if size:
                size = size.strip("[]").split(":")
                high, low = size[0], size[1]
                modified_lines.append(f"        {name} : {direction} std_logic_vector({high} downto {low});\n")
            else:
                modified_lines.append(f"        {name} : {direction} std_logic;\n")
    ports_list = []  # Réinitialiser après traitement

    # Ajouter "end entity" une fois les ports définis
    if module_match:
        modified_lines.append("    );\nend entity;\n\narchitecture Behavioral of " + module_name + " is\nbegin\nend Behavioral;\n")
        continue

    # Supprimer les déclarations wire
    if re.match(r"\s*wire", line):
        continue

    # Conversion des assignations
    line = re.sub(r"assign\s+(\w+)\s*=\s*(.*);", r"\1 <= \2;", line)

    # Conversion des blocs conditionnels
    line = re.sub(r"if\s*\((.*)\)\s*begin", r"if (\1) then", line)
    line = re.sub(r"end\s*else\s*if", r"elsif", line)
    line = re.sub(r"end\s*else", r"else", line)
    line = re.sub(r"end\s*begin", r"end if;", line)

    # Conversion des blocs always
    line = re.sub(r"always\s*@(.*)", r"process (\1) is", line)
    line = re.sub(r"end\s*always", r"end process;", line)

    # Conversion des boucles for
    line = re.sub(r"for\s+(\w+)\s*=\s*(\d+)\s*:\s*(\d+)\s*begin", r"for \1 in \2 to \3 loop", line)
    line = re.sub(r"end\s*for", r"end loop;", line)

    # Ajouter la ligne modifiée si elle n'est pas vide
    if line:
        modified_lines.append("    " + line + "\n")  # Ajoutez une indentation pour les blocs de code VHDL

# Demander à l'utilisateur de sélectionner un dossier de destination
destination_folder = filedialog.askdirectory(title="Sélectionnez un dossier de destination")
if not destination_folder:
    print("Aucun dossier sélectionné. Sauvegarde annulée.")
    exit()

# Demander le nom du fichier à sauvegarder
file_name = filedialog.asksaveasfilename(
    title="Nom du fichier à sauvegarder",
    initialdir=destination_folder,
    defaultextension=".vhdl",
    filetypes=[("Fichiers VHDL", "*.vhdl"), ("Tous les fichiers", "*.*")]
)
if not file_name:
    print("Nom de fichier non spécifié. Sauvegarde annulée.")
    exit()

# Sauvegarder le contenu converti dans le fichier spécifié
try:
    with open(file_name, 'w') as file:
        file.writelines(modified_lines)
    print(f"Fichier VHDL sauvegardé sous : {file_name}")
except Exception as e:
    print(f"Erreur lors de la sauvegarde du fichier : {e}")
