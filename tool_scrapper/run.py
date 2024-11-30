import argparse

import nest_asyncio
nest_asyncio.apply()

import asyncio
from pyppeteer import launch

from code.parse_word import get_word_description
from code.page_navigation import iterate_through_words, search_for_word
from code.text_normalisation import normalise_word_descriptions
from code.get_json_for_word import parse_word_by_pos


URL = "https://lcorp.ulif.org.ua/dictua/"
CHECK_INTERVAL = 0.2

async def process_word(page):
    # ------ #
    word_name, pos, comment, pos_comment = await get_word_description(page)
    # ------ #

    if not word_name:
        return
    word_name, pos, comment, pos_comment = normalise_word_descriptions(word_name, pos, comment, pos_comment)

    # ------ #
    word_json, formatter = await parse_word_by_pos(page, pos)
    # ------ #

    word_name_text = word_name.replace('+', '')

    if word_json == 'else':
        return word_name, pos, pos_comment, comment, '', ''

    if not word_json:
        print(f'Error processing word: {word_name_text}')
        return [None]*5

    return word_name, pos, pos_comment, comment, formatter, word_json


async def main():
    parser = argparse.ArgumentParser(description='Search for a word in a dictionary.')
    parser.add_argument('word', type=str, help='The word to search for')

    args = parser.parse_args()
    word_to_search = args.word

    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.goto(URL)

    await search_for_word(page, word_to_search)

    word_name, pos, pos_comment, comment, formatter, word_json = await process_word(page)

    word_info = f"""Word Information:
    -----------------
    Name: {word_name}
    Part of Speech: {pos} {pos_comment}
    Comment: {comment}
    Part of Speech: {formatter}

    Word Forms:
    -----------
    {word_json}
    """

    print(word_info)

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
