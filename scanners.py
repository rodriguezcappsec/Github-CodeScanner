import re

GGPL = r"GNU GENERAL PUBLIC LICENSE\s*Version ([^,]*)"
LGPL = r"(?:LESSER|LIBRARY) GENERAL PUBLIC LICENSE\s*Version ([^,]*)"
GAGPL = r"GNU AFFERO GENERAL PUBLIC LICENSE\s*Version ([^,]*)"
GENERAL = r"(\bgpl\b|\bagpl\b|\bAGPL\b|\bGPL\b|\bLesser GPL\b|\bLibrary GPL\b)"
# testing stuff here.