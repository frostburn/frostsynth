import unittest


from frostsynth.polysequence import PolySequence, LinearSequence, CubicSequence


class PolySequenceTests(unittest.TestCase):
    def test_linear(self):
        linear_sequence = LinearSequence([(0, 1), (9, 10), (13, 2)])
        self.assertEqual([linear_sequence(i) for i in range(13)], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 8, 6, 4])
        linear_sequence.srate = 1
        self.assertEqual(list(linear_sequence), [linear_sequence(i) for i in range(13)])
        linear_sequence.srate = 0.5
        self.assertEqual(list(linear_sequence), [linear_sequence(i) for i in range(0, 13, 2)])

    def test_quadratic(self):
        quadratic_sequence = PolySequence([0, 5, 11], [(1, 2, 3), (4, 5, 6)])
        quadratic_sequence.srate = 0.5
        for generated_value, calculated_value in zip(quadratic_sequence, [quadratic_sequence(i) for i in range(0, 11, 2)]):
            self.assertAlmostEqual(generated_value, calculated_value)

    def test_cubic(self):
        cubic_sequence = CubicSequence([(0, 1, None, 1), (7, 3, 4, 5), (17, 1, -1, None)])
        cubic_sequence.srate = 0.5
        for generated_value, calculated_value in zip(cubic_sequence, [cubic_sequence(i) for i in range(0, 17, 2)]):
            self.assertAlmostEqual(generated_value, calculated_value)

if __name__ == '__main__':
    unittest.main()
