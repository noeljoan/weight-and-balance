"""
Fixe Parameter der Cessna-172 (Standard-Modell, 2022-Version)
"""

# Referenz-Datum (inches)
DATUM_INCH = 36.0

# Länge des Mean Aerodynamic Chord (MAC) - für %MAC Berechnung
MAC_INCH = 57.0

# Maximal zulässiges Gesamtgewicht (lb) - aus dem POH
MAX_WEIGHT_LB = 2550.0

# CG-Grenzwerte (inches vom Datum)
CG_FORWARD_LIMIT_INCH = 35.0   # 0 % MAC (ungefähr)
CG_AFT_LIMIT_INCH = 47.3      # 20 % MAC (ungefähr)