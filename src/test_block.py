import unittest

from block import (
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlockToBlock(unittest.TestCase):
    ## Test paragraph
    def test_paragraph(self):
        text_paragraph = "This is a paragraph of text."
        result_paragraph = "paragraph"

        text_code = "```This is some code```"
        result_code = "code"

        text_unordered = "* one item\n* two item\n- three item"
        result_unordered = "unordered list"

        text_ordered = "1. one item\n2. two item\n3. three item"
        result_ordered = "ordered list"

        text_quote = "> This is a quote\n> Here is another"
        result_quote = "quote"

        self.assertEqual(block_to_block_type(text_paragraph), result_paragraph)
        self.assertEqual(block_to_block_type(text_quote), result_quote)
        self.assertEqual(block_to_block_type(text_code), result_code)
        self.assertEqual(block_to_block_type(text_unordered), result_unordered)
        self.assertEqual(block_to_block_type(text_ordered), result_ordered)


## Test single item lists and bad list entries.
class TestBlockToBlockBadList(unittest.TestCase):
    def test_multiple_and_single_lists(self):
        text_unordered = "* one item\n* two item\n three item"
        text_unordered_one = "* one item"

        text_ordered = "1. one item\n two item\n3. three item"
        text_ordered_one = "1. one item"

        result = "paragraph"

        self.assertEqual(block_to_block_type(text_unordered), result)
        self.assertEqual(block_to_block_type(text_unordered_one), result)
        self.assertEqual(block_to_block_type(text_ordered), result)
        self.assertEqual(block_to_block_type(text_ordered_one), result)


## Test block_to_block_type error handling
class TestBlockToBlockError(unittest.TestCase):
    def test_empty_text(self):
        none_string = None

        def none_test():
            nonlocal none_string
            block_to_block_type(none_string)

        #        self.assertRaises(Exception, empty_string)
        self.assertRaises(Exception, none_test)

    def test_none_text(self):
        empty_string = " "

        def none_test():
            nonlocal empty_string
            block_to_block_type(empty_string)

        #        self.assertRaises(Exception, empty_string)
        self.assertRaises(Exception, none_test)


## Test markdown_to_html_node
class TestMarkdowntoBlock(unittest.TestCase):
    def test_block_types(self):
        header = markdown_to_html_node("## This is a header")
        markdown_header = "<div><h2>This is a header</h2></div>"

        quote = markdown_to_html_node(
            "> This is a text_quote\n> Here is another\n> and another"
        )
        markdown_quote = "<div><blockquote>This is a text_quote Here is another and another</blockquote></div>"

        code = markdown_to_html_node("""```Here is some code\n and some more```""")
        markdown_code = """<div><pre><code>Here is some code
 and some more</code></pre></div>"""

        unordered_list = markdown_to_html_node(
            """- This is an item\n* here is another\n* and a third"""
        )
        markdown_unordered = "<div><ul><li>This is an item</li><li>here is another</li><li>and a third</li></ul></div>"

        ordered_list = markdown_to_html_node(
            "1. This is an item\n2. Here is another\n3. and the last"
        )
        markdown_ordered = "<div><ol><li>This is an item</li><li>Here is another</li><li>and the last</li></ol></div>"

        paragraph = markdown_to_html_node("Here is a *paragraph* of **text**")
        markdown_paragraph = (
            "<div><p>Here is a <i>paragraph</i> of <b>text</b></p></div>"
        )

        self.assertEqual(header.to_html(), markdown_header)
        self.assertEqual(quote.to_html(), markdown_quote)
        self.assertEqual(code.to_html(), markdown_code)
        self.assertEqual(unordered_list.to_html(), markdown_unordered)
        self.assertEqual(ordered_list.to_html(), markdown_ordered)
        self.assertEqual(paragraph.to_html(), markdown_paragraph)


if __name__ == "__main__":
    unittest.main()
