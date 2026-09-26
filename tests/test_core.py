import unittest
from core import Debate

class DebateFlowTests(unittest.TestCase):
    def test_turn_order_and_completion(self):
        for side in ("Affirmative", "Negative"):
            debate = Debate("School should start later", "Junior Open (Y9–10)", side, True)
            self.assertEqual([t.side for t in debate.turns],
                             ["Affirmative", "Negative"] * 3 + ["Negative", "Affirmative"])
            self.assertEqual(sum(t.side == side for t in debate.turns[:6]), 3)
            for turn in debate.turns:
                self.assertEqual(debate.current, turn)
                debate.add(f"Speech for {turn.side}")
            self.assertIsNone(debate.current)
            with self.assertRaises(ValueError):
                debate.add("extra")

    def test_six_turn_short_mode(self):
        self.assertEqual(len(Debate("moot", "Senior Open (Y11–12)", "Negative").turns), 6)

if __name__ == "__main__":
    unittest.main()
