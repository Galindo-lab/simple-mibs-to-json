import json
import re

def parse_mib_to_json(mib_text):
    mib_dict = {}

    # Definición de las expresiones regulares
    patterns = {
        "name": r'(\S+)\s+OBJECT-TYPE',
        "syntax": r'SYNTAX\s+(\S+)',
        "max_access": r'MAX-ACCESS\s+(\S+)',
        "status": r'STATUS\s+(\S+)',
        "description": r'DESCRIPTION\s+"((?:.|\n)*?)"',
        "default_value": r'DEFVAL\s+\{ "((?:.|\n)*?)" \}',
        "oid": r'::=\s+\{ (\S+)\s+(\d+) \}'
    }

    # Aplicar las expresiones regulares y llenar el diccionario
    for key, pattern in patterns.items():
        match = re.search(pattern, mib_text)
        if match:
            if key == "oid":  # Para OID, extraer dos partes
                mib_dict["oid_parent"], mib_dict["oid"] = match.groups()
            else:
                mib_dict[key] = match.group(1).strip()

    return mib_dict if "name" in mib_dict else None  # Solo retornar si tiene 'name'

def extract_mibs_from_file(file_content):
    mib_blocks = re.findall(r'(\S+\s+OBJECT-TYPE(?:.|\n)*?::=\s+\{\s+\S+\s+\d+\s*\})', file_content)
    mib_list = [parse_mib_to_json(mib) for mib in mib_blocks if parse_mib_to_json(mib)]
    return json.dumps(mib_list, indent=4)

def process_mib_file(filename):
    with open(filename, 'r') as file:
        file_content = file.read()

    mib_json = extract_mibs_from_file(file_content)

    output_filename = filename.replace(".txt", "_mibs.json")
    with open(output_filename, 'w') as json_file:
        json_file.write(mib_json)
    
    print(f"Se han extraído los MIBs y guardado en: {output_filename}")

# Ejemplo de uso con un archivo
filename = "archivo_mibs.txt"
process_mib_file(filename)
