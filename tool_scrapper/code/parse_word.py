
async def get_word_description(page):
    # Wait for the article element to be present
    # await page.waitForSelector('.word_style')

    # Get the article element
    article = await page.querySelector('#ContentPlaceHolder1_article')

    # Check if word name element exists and get its text
    word_name_element = await article.querySelector('.word_style')
    word_name = await word_name_element.getProperty('innerText') if word_name_element else ''
    word_name = await word_name.jsonValue() if word_name else ''

    # Check if part of speech element exists and get its text
    pos_element = await article.querySelector('.gram_style')
    pos = await pos_element.getProperty('innerText') if pos_element else ''
    pos = await pos.jsonValue() if pos else ''

    # Check if comment element exists and get its text
    comment_element = await article.querySelector('.comment_style')
    comment = await comment_element.getProperty('innerText') if comment_element else ''
    comment = await comment.jsonValue() if comment else ''

    # Check if pos_comments elements exist and concatenate their text
    pos_comments_elements = await article.querySelectorAll('p.td_inner_center_style')
    pos_comment = ''
    if pos_comments_elements:
        for pos_element in pos_comments_elements:
            pos_element = await pos_element.getProperty('innerText') if pos_element else ''
            pos_element = await pos_element.jsonValue() if pos_element else ''
            pos_comment += pos_element

    return word_name, pos, comment, pos_comment