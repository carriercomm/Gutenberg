"""Module to deal with type validation."""


def validate_etextno(etextno):
    """Raises a ValueError if the argument does not represent a valid Project
    Gutenberg text idenfifier.

    """
    if not isinstance(etextno, int) or etextno <= 0:
        msg = 'e-text identifiers should be strictly positive integers'
        raise ValueError(msg)
    return etextno


if __name__ == '__main__':
    # pylint: disable=C0111
    # pylint: disable=R0904
    import unittest

    class Test(unittest.TestCase):
        def test_is_valid_etext(self):
            self.assertIsNotNone(validate_etextno(1))
            self.assertIsNotNone(validate_etextno(12))
            self.assertIsNotNone(validate_etextno(123))
            self.assertIsNotNone(validate_etextno(1234))

        def test_is_invalid_etext(self):
            with self.assertRaises(ValueError):
                validate_etextno('not-a-positive-integer')
            with self.assertRaises(ValueError):
                validate_etextno(-123)
            with self.assertRaises(ValueError):
                validate_etextno(0)
            with self.assertRaises(ValueError):
                validate_etextno(12.3)

    unittest.main()
