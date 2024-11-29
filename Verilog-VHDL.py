"""
Code pour convertir des fichiers Verilog en VHDL
Loïc PAGNON
22/11/2024
A faire :
"""

import re
from tkinter import Tk, filedialog

def verilog_to_vhdl(verilog_code):
    # Nettoyer le code Verilog pour supprimer les espaces inutiles
    verilog_code = verilog_code.strip()
    
    # Analyse des sections importantes
    module_name = re.search(r'module\s+(\w+)', verilog_code).group(1)
    ports = re.search(r'\((.*?)\);', verilog_code, re.DOTALL).group(1).replace('\n', '').split(',')
    ports = [p.strip() for p in ports]
    
    inputs = re.findall(r'input\s+(.*?);', verilog_code)
    outputs = re.findall(r'output\s+(.*?);', verilog_code)
    wires = re.findall(r'wire\s+(.*?);', verilog_code)
    assigns = re.findall(r'assign\s+(.*?)\s*=\s*(.*?);', verilog_code)
    
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
    
    # Générer le code VHDL
    vhdl_code = f"""
entity {module_name} is
port (
    {',\n    '.join(vhdl_ports)}
);
end {module_name};

architecture {module_name}_struct of {module_name} is
    {'\n    '.join(vhdl_signals)}
begin
    {'\n    '.join(vhdl_assignments)}
end {module_name}_struct;
"""
    return vhdl_code.strip()

def select_and_convert_file():
    # Ouvrir une fenêtre pour sélectionner un fichier
    Tk().withdraw()  # Masquer la fenêtre principale Tkinter
    file_path = filedialog.askopenfilename(
        title="Sélectionner un fichier Verilog",
        filetypes=[("Fichiers Verilog", "*.v"), ("Tous les fichiers", "*.*")]
    )
    
    if not file_path:
        print("Aucun fichier sélectionné.")
        return
    
    # Lire le contenu du fichier Verilog
    with open(file_path, 'r') as file:
        verilog_code = file.read()
    
    # Convertir le code Verilog en VHDL
    vhdl_code = verilog_to_vhdl(verilog_code)
    
    # Sauvegarder le fichier VHDL
    output_path = file_path.rsplit('.', 1)[0] + ".vhdl"
    with open(output_path, 'w') as file:
        file.write(vhdl_code)
    
    print(f"Fichier VHDL généré : {output_path}")

# Appel de la fonction principale
if __name__ == "__main__":
    select_and_convert_file()
