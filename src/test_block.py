import unittest
from unittest.case import _AssertRaisesContext

from block import markdown_to_blocks


class TestBlock(unittest.TestCase):
    ## Test simple text document with proper whitespaces
    def test_props_to_html(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block 
* This is a list item
* This is another list item"""

        result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block \n* This is a list item\n* This is another list item",
        ]

        self.assertEqual(markdown_to_blocks(text), result)

    ## Test multiple blank lines and whitespaces.
    def test_multiple_props_to_html(self):
        text = """# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is the first list item in a list block 
* This is a list item
* This is another list item"""

        result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block \n* This is a list item\n* This is another list item",
        ]

        self.assertEqual(markdown_to_blocks(text), result)

    ## Test exception in markdown_to_blocks
    def test_markdown_fail(self):
        text = ""

        def test_err():
            nonlocal text
            return markdown_to_blocks(text)

        self.assertRaises(Exception, test_err)


if __name__ == "__main__":
    unittest.main()
