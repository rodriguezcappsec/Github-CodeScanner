import re

GGPL = r"GNU GENERAL PUBLIC LICENSE\s*Version ([^,]*)"
LGPL = r"(?:LESSER|LIBRARY) GENERAL PUBLIC LICENSE\s*Version ([^,]*)"
GAGPL = r"GNU AFFERO GENERAL PUBLIC LICENSE\s*Version ([^,]*)"
GENERAL = r"(\bgpl\b|\bagpl\b|\bAGPL\b|\bGPL\b|\bLesser GPL\b|\bLibrary GPL\b)"

print(
    re.findall(r"let\s\w\s\=.","hola mundo, let chocolate = 10")
)
# def invalid_license_scanner(data):
