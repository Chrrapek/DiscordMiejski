import unittest

from utils import Utils


class TestModule(unittest.TestCase):
    def test_html_parsing(self):
        self.assertEqual(Utils.parse_html("This shoul* *e escaped"), "This shoul\* \*e escaped")
        self.assertEqual(Utils.parse_html("<b>This should be bold</b>"), "**This should be bold**")
        self.assertEqual(Utils.parse_html("<i>This should be italic</i>"), "_This should be italic_")


if __name__ == '__main__':
    unittest.main()
