"""
Code pour convertir des fichiers Verilog en VHDL
Loïc PAGNON
22/11/2024
A faire :
"""

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

# Parcourir chaque ligne du fichier
for line in lines:
    line = line.strip()  # Supprimer les espaces inutiles autour de la ligne

    # Supprimer les lignes contenant 'wire'
    if re.match(r"\s*wire", line):
        continue  # Passer à la ligne suivante si c'est une déclaration wire

    # Conversion des ports Verilog groupés (suppression des répétitions du type)
    line = re.sub(r"(input|output|inout)\s+([^;]+);", 
                  lambda m: f"{', '.join(m.group(2).split())} : {m.group(1)} std_logic;", 
                  line)

    # Conversion du module Verilog en entité VHDL
    line = re.sub(r"module\s+(\w+)\s*\((.*)\);", r"entity \1 is\nport (\2);", line)
    line = re.sub(r"endmodule", r"end entity;", line)

    # Conversion des déclarations de variables
    line = re.sub(r"input\s+(\[.*\])?\s*(\w+);", r"\2 : in std_logic;", line)
    line = re.sub(r"output\s+(\[.*\])?\s*(\w+);", r"\2 : out std_logic;", line)

    # Conversion des assignations
    line = re.sub(r"assign\s+(\w+)\s*=\s*(.*);", r"\1 <= \2;", line)

    # Conversion des structures conditionnelles
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

    # Ajouter un saut de ligne après chaque instruction convertie
    if line:  # Si la ligne n'est pas vide, ajouter un saut de ligne
        modified_lines.append(line + "\n")

# Ajouter des retours à la ligne pour les déclarations de variables
final_lines = []
for line in modified_lines:
    # Éviter de répéter std_logic dans les ports
    line = re.sub(r"(\w+,\s*\w+):\s*std_logic\s*:.*std_logic;", r"\1 : std_logic;", line)
    
    # Ajouter un saut de ligne après chaque déclaration de variable
    if re.match(r".*:\s*std_logic;", line):
        final_lines.append(line + "\n")  # Ajouter des sauts de ligne après chaque déclaration
    else:
        final_lines.append(line)  # Conserver les autres lignes telles quelles

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
        file.writelines(final_lines)
    print(f"Fichier VHDL sauvegardé sous : {file_name}")
except Exception as e:
    print(f"Erreur lors de la sauvegarde du fichier : {e}")
