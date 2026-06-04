from typing import List, Tuple
from .constants import DATUM_INCH, MAC_INCH, MAX_WEIGHT_LB, CG_FORWARD_LIMIT_INCH, CG_AFT_LIMIT_INCH
from .item import WeightItem

class WeightAndBalance:
    """
    Klasse zur Berechnung von Gesamtgewicht, CG-Position und %MAC.
    """
    def __init__(self, items: List[WeightItem]):
        self.items = items

    @property
    def total_weight(self) -> float:
        return sum(item.weight_lb for item in self.items)

    @property
    def total_moment(self) -> float:
        return sum(item.moment for item in self.items)

    @property
    def cg_position_in(self) -> float:
        """
        CG-Position in Zoll vom Datum.
        """
        if self.total_weight == 0:
            raise ZeroDivisionError("Kein Gewicht angegeben.")
        return self.total_moment / self.total_weight

    @property
    def cg_percent_mac(self) -> float:
        """
        CG-Position als Prozent des MAC.
        """
        return ((self.cg_position_in - DATUM_INCH) / MAC_INCH) * 100.0

    def is_within_limits(self) -> Tuple[bool, str]:
        """
        Prüft, ob Gewicht und CG innerhalb der zulässigen Grenzen liegen.
        """
        msgs = []

        # Gewicht prüfen
        if self.total_weight > MAX_WEIGHT_LB:
            msgs.append(f"Gesamtgewicht {self.total_weight:.1f} lb > Max {MAX_WEIGHT_LB} lb")

        # CG-Grenzen prüfen
        if not (CG_FORWARD_LIMIT_INCH <= self.cg_position_in <= CG_AFT_LIMIT_INCH):
            msgs.append(
                f"CG {self.cg_position_in:.2f} in (={self.cg_percent_mac:.1f}% MAC) liegt außerhalb des zulässigen Bereichs "
                f"{CG_FORWARD_LIMIT_INCH:.1f}-{CG_AFT_LIMIT_INCH:.1f} in"
            )

        if not msgs:
            return True, "Alle Parameter innerhalb der zulässigen Grenzen."
        else:
            return False, " | ".join(msgs)

    def report(self) -> str:
        """
        Erzeugt einen druckfertigen Bericht.
        """
        ok, note = self.is_within_limits()
        lines = [
            "=== Cessna-172 Weight & Balance Report ===",
            f"Gesamtgewicht       : {self.total_weight:7.1f} lb",
            f"Gesamt-Moment       : {self.total_moment:7.1f} lb·in",
            f"CG-Position (in)    : {self.cg_position_in:7.2f} in",
            f"CG-% MAC            : {self.cg_percent_mac:6.1f} %MAC",
            f"Status              : {'OK' if ok else 'NICHT OK'}",
            f"Hinweis             : {note}",
            "------------------------------------------",
            "Einzelposten:",
        ]
        for it in self.items:
            lines.append(f"  {it.name:12s}: {it.weight_lb:6.1f} lb @ {it.arm_in:5.1f} in  (Moment {it.moment:7.1f})")
        return "\n".join(lines)