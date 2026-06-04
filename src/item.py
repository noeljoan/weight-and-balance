from dataclasses import dataclass

@dataclass
class WeightItem:
    """
    Einzelner Posten für die Gewicht-und Schwerpunkt-Berechnung.
    """
    name: str  # z.B. "Pilot", "Beifahrer", "Gepäck"
    weight_lb: float  # Gewicht in Pfund (lb)
    arm_in: float  # Abstand vom Datum in Zoll (in)

    @property
    def moment(self) -> float:
        """
        Moment = Gewicht × Arm.
        """
        return self.weight_lb * self.arm_in