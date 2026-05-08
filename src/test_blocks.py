from logging import exception
import unittest

from textnode import BlockType
from process_blocks import identify_block

class TestBlocks(unittest.TestCase):

    def test_heading(self):
        block = "## This is a heading block"
        expected = BlockType.HEADING

        self.assertEqual(identify_block(block), expected)

    def test_wrong_heading(self):
        block = "#This is a heading block"
        expected = BlockType.PARAGRAPH

        self.assertEqual(identify_block(block), expected)

    def test_wrong_heading2(self):
        block = "######## This is a heading block"
        expected = BlockType.PARAGRAPH

        self.assertEqual(identify_block(block), expected)

    def test_ordered_list(self):
        block = """1. groceries
2. cinema
3. restaurant
4. sleep"""
        expected = BlockType.ORDERED_LIST
        self.assertEqual(identify_block(block), expected)

    def test_wrong_ordered_list(self):
        block = """1. groceries
2. cinema
3. restaurant
5. sleep"""
        expected = BlockType.PARAGRAPH
        self.assertEqual(identify_block(block), expected)

    def test_code(self):
        block = """```
                def main():
                    print('hello word!')
                main()```"""

        expected = BlockType.CODE
        self.assertEqual(identify_block(block), expected)

    def test_wrong_code(self):
        block = """```def main():
                        print("hello word!")
                    main()```"""
        expected = BlockType.PARAGRAPH
        self.assertEqual(identify_block(block), expected)

    def test_quote(self):
        block = """> Enter your username
> admin
> Enter your password
> 
> Wrong password, try again
> Enter your username
> password
> Enter your password
> ^C"""
        expected = BlockType.QUOTE
        self.assertEqual(identify_block(block), expected)

    def test_wrong_quote(self):
        block = """> Enter your username
> admin
> Enter your password
passord
> Wrong password, try again
> Enter your username
> password
> Enter your password
> ^C"""
        expected = BlockType.PARAGRAPH
        self.assertEqual(identify_block(block), expected)

    def test_unordered_list(self):
        block = """- Analyse code
- Finds bugs
- Fixes bugs
- Creates bugs"""
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(identify_block(block), expected)

    def test_wrong_unordered_list(self):
        block = """-Analyse code
- Finds bugs
- Fixes bugs
- Creates bugs"""
        expected = BlockType.PARAGRAPH
        self.assertEqual(identify_block(block), expected)

if __name__ == "__main__":
    unittest.main()
