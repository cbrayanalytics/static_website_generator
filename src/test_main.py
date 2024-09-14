import unittest
from main import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        test_text = "# Hello"
        result = extract_title(test_text)
        self.assertEqual(result, "Hello")

    def test_props_to_html_multi(self):
        test_text = """## Hello
# Correct line"""
        result = extract_title(test_text)
        self.assertEqual(result, "Correct line")

    def test_extract_title_none(self):
        test_text = ""

        def title_none():
            nonlocal test_text
            return extract_title(test_text)

        self.assertRaises(Exception, title_none)


if __name__ == "__main__":
    unittest.main()
