import re
from enum import Enum
import argparse


class AllLicenses:
    GGPL = r"GNU GENERAL PUBLIC LICENSE\s*Version*([^,]*)"
    LGPL = r"(?:LESSER|LIBRARY) GENERAL PUBLIC LICENSE\s*Version ([^,]*)"
    GAGPL = r"GNU AFFERO GENERAL PUBLIC LICENSE\s*([^,]*)"
    AGPL = r"AGPL\s*([^,]*)"
    GPL = r"GPL\s*([^,]*)"
    LGPL2 = r"LGPL\s*([^,]*)"
    FDL = r"FDL\s*([^,]*)"
    MPL = r"MPL\s*([^,]*)"
    BSD = r"BSD\s*([^,]*)"
    MIT = r"MIT\s*([^,]*)"
    Apache = r"Apache\s*([^,]*)"
    GENERAL = r"(\bgpl\b|\bagpl\b|\bAGPL\b|\bGPL\b|\bLesser GPL\b|\bLibrary GPL\b)"


class Licenses(AllLicenses):
    def __init__(self, invalid_license):
        self.scan_licenses = invalid_license

    def scan(self):
        print(
            re.match(
                self.GGPL,
                """GNU GENERAL PUBLIC LICENSE
            Version""",
            ).string
        )
