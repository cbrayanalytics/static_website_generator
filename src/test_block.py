import unittest

from block import (
    block_to_block_type,
    markdown_to_blocks,
)
import block


class TestBlockToBlock(unittest.TestCase):
    ## Test paragraph
    def test_paragraph(self):
        text_paragraph = "This is a paragraph of text."
        result_paragraph = "paragraph"

        text_quote = "> This is one quote\n> This is the second"
        result_quote = "quote"

        text_code = "```This is some code```"
        result_code = "code"

        text_unordered = "* one item\n* two item\n- three item"
        result_unordered = "unordered list"

        text_ordered = "1. one item\n2. two item\n3. three item"
        result_ordered = "ordered list"

        self.assertEqual(block_to_block_type(text_paragraph), result_paragraph)
        self.assertEqual(block_to_block_type(text_quote), result_quote)
        self.assertEqual(block_to_block_type(text_code), result_code)
        self.assertEqual(block_to_block_type(text_unordered), result_unordered)
        self.assertEqual(block_to_block_type(text_ordered), result_ordered)


## Test single item lists and bad list entries.
class TestBlockToBlockBadList(unittest.TestCase):
    def test_multiple_and_single_lists(self):
        text_quote = "> This is one quote\n> This is the second\n This is the third"
        text_quote_one = "> This is one quote"

        text_unordered = "* one item\n* two item\n three item"
        text_unordered_one = "* one item"

        text_ordered = "1. one item\n two item\n3. three item"
        text_ordered_one = "1. one item"

        result = "paragraph"

        self.assertEqual(block_to_block_type(text_quote), result)
        self.assertEqual(block_to_block_type(text_quote_one), result)
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


if __name__ == "__main__":
    unittest.main()
