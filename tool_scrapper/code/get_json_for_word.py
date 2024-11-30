
from code.parse_table import parse_noun, parse_adjective, parse_numeral ,parse_imperfective_verb, parse_perfective_verb


async def parse_word_by_pos(page, pos):
    """
    Given a part of speech (pos), return the corresponding parsed JSON for the word.

    :param page: The web driver instance.
    :param pos: The part of speech string.
    :return: JSON object corresponding to the word based on the part of speech.
    """
    # Check the part of speech and parse accordingly
    if 'дієслово недоконаного' in pos:
        # Imperfective verb
        word_json = await parse_imperfective_verb(page)
        formatter = 'imperfective_verb'
    elif 'дієслово доконаного' in pos:
        # Perfective verb
        word_json = await parse_perfective_verb(page)
        formatter = 'perfective_verb'
    elif 'прикметник' in pos or 'займеник' in pos:
        # Adjective or Pronoun
        word_json = await parse_adjective(page)
        formatter = 'adjictive'
    elif 'іменник' in pos:
        # Noun
        word_json = await parse_noun(page)
        formatter = 'noun'
    elif 'числівник' in pos:
        # Numeral
        word_json = await parse_numeral(page)
        formatter = 'numeral'
    else:
        return 'else', 'else'

    # Optionally, you can add the formatter type to the response JSON
    word_json["type"] = formatter
    return word_json, formatter
