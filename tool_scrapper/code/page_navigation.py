import asyncio
import pyppeteer
import time


async def get_to_next_page(page):
    """Find and click the "next page" button"""
    button = await page.querySelector('#ContentPlaceHolder1_nextpage')
    await button.click()


async def get_to_previous_page(page):
    """Find and click the "previous page" button"""
    button = await page.querySelector('#ContentPlaceHolder1_backpage')
    await button.click()


async def search_for_word(page, word):
    """Clear the search input field and type the search word"""
    input_element = await page.querySelector('#ContentPlaceHolder1_tsearch')
    await input_element.click({'clickCount': 3})  # Click to select all text
    await input_element.type('', {'delay': 100})  # Clear the input field
    await input_element.type(word, {'delay': 100})  # Type the word
    await asyncio.sleep(0.2)

    # Find and click the search button
    button = await page.querySelector('#ContentPlaceHolder1_search')
    await button.click()
    await asyncio.sleep(0.2)


async def iterate_through_words(page):
    """Find the table and its rows"""
    table = await page.querySelector('#ContentPlaceHolder1_dgv')
    rows = await table.querySelectorAll('tr')
    n = len(rows)

    # Iterate through rows, skipping the first row, which is header
    for i in range(1, n):

        row = rows[i]
        # Find the button (anchor tag) in the current row and click it
        button = await row.querySelector('a')
        await button.click()

        yield

        # Reload
        table = await page.querySelector('#ContentPlaceHolder1_dgv')
        rows = await table.querySelectorAll('tr')