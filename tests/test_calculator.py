import unittest
from src.item import WeightItem
from src.calculator import WeightAndBalance


class TestWeightAndBalance(unittest.TestCase):
    def test_basic_calculation(self):
        """Test basic weight and balance calculation."""
        items = [
            WeightItem("Pilot", 170, 36.0),
            WeightItem("Fuel", 84, 48.0),  # 14 gal * 6 lb/gal
            WeightItem("Baggage", 30, 95.0),
        ]
        wb = WeightAndBalance(items)

        self.assertAlmostEqual(wb.total_weight, 284.0, places=1)
        self.assertAlmostEqual(wb.total_moment, 12264.0, places=1)
        self.assertAlmostEqual(wb.cg_position_in, 43.18, places=2)

    def test_within_limits(self):
        """Test that valid configuration is within limits."""
        items = [
            WeightItem("Pilot", 170, 36.0),
            WeightItem("Fuel", 84, 48.0),
        ]
        wb = WeightAndBalance(items)
        ok, _ = wb.is_within_limits()
        self.assertTrue(ok)

    def test_exceeds_weight_limit(self):
        """Test that exceeding max weight is detected."""
        items = [WeightItem("Cargo", 3000, 95.0)]
        wb = WeightAndBalance(items)
        ok, msg = wb.is_within_limits()
        self.assertFalse(ok)
        self.assertIn("Gesamtgewicht", msg)

    def test_zero_weight(self):
        """Test handling of zero total weight."""
        wb = WeightAndBalance([])
        with self.assertRaises(ZeroDivisionError):
            _ = wb.cg_position_in


if __name__ == "__main__":
    unittest.main()