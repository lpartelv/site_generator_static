import unittest
from block_markdown import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
    
    def test_block_newlines(self):
        self.assertEqual(block_to_block_type("This is **bolded** paragraph"), "paragraph")
        self.assertEqual(block_to_block_type("* This is a list\n* with items"), "unordered_list")
        self.assertEqual(block_to_block_type("- This is a list\n- with items"), "unordered_list")
        self.assertEqual(block_to_block_type("* This is a list\n- with items"), "paragraph")
        self.assertEqual(block_to_block_type("```This is **bolded** paragraph```"), "code")
        self.assertEqual(block_to_block_type(">This is **bolded** paragraph"), "quote")


if __name__ == "__main__":
    unittest.main()
