"""Module to deal with type validation."""


def is_valid_etext(etextno):
    raise NotImplementedError


if __name__ == '__main__':
    # pylint: disable=C0111
    # pylint: disable=R0904
    import unittest

    class Test(unittest.TestCase):
        def test_is_valid_etext(self):
            self.assertTrue(is_valid_etext(1))
            self.assertTrue(is_valid_etext(12))
            self.assertTrue(is_valid_etext(123))
            self.assertTrue(is_valid_etext(1234))

        def test_is_invalid_etext(self):
            with self.assertRaises(ValueError):
                is_valid_etext('not-a-positive-integer')
            with self.assertRaises(ValueError):
                is_valid_etext(-123)
            with self.assertRaises(ValueError):
                is_valid_etext(0)
            with self.assertRaises(ValueError):
                is_valid_etext(12.3)

    unittest.main()
