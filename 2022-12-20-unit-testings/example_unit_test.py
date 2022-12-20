import unittest


def trim(s):
    """This will trim the whitespace around the input and return it."""
    if s:
        if s.startswith(" "):
            s = s[1:]

    # TODO: is there any bugs with this code?

    return s


class TestTrim(unittest.TestCase):

    def test_with_space(self):
        s = " foo"
        s_trimmed = trim(s)
        self.assertEqual("foo", s_trimmed)

    def test_no_space(self):
        s = "foo"
        s_trimmed = trim(s)
        self.assertEqual("foo", s_trimmed)



if __name__ == '__main__':
    unittest.main()
