import asyncio
from code.text_normalisation import normalise_text


async def _get_text_from_row(cells, idx_elem):
    """
    Fetches the text of a specific column (cell) in the row.
    """
    word_element = await cells[idx_elem].getProperty('innerText')
    word = await word_element.jsonValue()  # Retrieve the actual text value
    word = normalise_text(word.strip())
    return word if word != ' ' else ''


async def get_rows_from_table(page):
    """
    Retrieves all rows from the table in the article, loading them in one call.
    """
    article = await page.querySelector("#ContentPlaceHolder1_article")
    table = await article.querySelector("tbody")
    # await page.waitForSelector("tbody > tr", timeout=120)
    rows = await table.querySelectorAll("tr")
    return rows


async def parse_imperfective_verb(page):
    """
    Parses the imperfective verb from the rows of the table.
    """
    # Get rows
    rows = await get_rows_from_table(page)

    tasks = []

    # For the infinitive verb, we know it's in the first row, second column (0-indexed)
    tasks.append(_get_text_from_row(await rows[0].querySelectorAll('td'), 1))

    # Imperative mood
    imperative_singular_first = _get_text_from_row(await rows[3].querySelectorAll('td'), 1)
    imperative_singular_second = _get_text_from_row(await rows[4].querySelectorAll('td'), 1)
    imperative_plural_first = _get_text_from_row(await rows[3].querySelectorAll('td'), 2)
    imperative_plural_second = _get_text_from_row(await rows[4].querySelectorAll('td'), 2)

    tasks.extend(
        [imperative_singular_first, imperative_singular_second, imperative_plural_first, imperative_plural_second])

    # Future tense
    future_singular_first = _get_text_from_row(await rows[6].querySelectorAll('td'), 1)
    future_singular_second = _get_text_from_row(await rows[7].querySelectorAll('td'), 1)
    future_singular_third = _get_text_from_row(await rows[8].querySelectorAll('td'), 1)
    future_plural_first = _get_text_from_row(await rows[6].querySelectorAll('td'), 2)
    future_plural_second = _get_text_from_row(await rows[7].querySelectorAll('td'), 2)
    future_plural_third = _get_text_from_row(await rows[8].querySelectorAll('td'), 2)

    tasks.extend([future_singular_first, future_singular_second, future_singular_third, future_plural_first,
                  future_plural_second, future_plural_third])

    # Present tense
    present_singular_first = _get_text_from_row(await rows[10].querySelectorAll('td'), 1)
    present_singular_second = _get_text_from_row(await rows[11].querySelectorAll('td'), 1)
    present_singular_third = _get_text_from_row(await rows[12].querySelectorAll('td'), 1)
    present_plural_first = _get_text_from_row(await rows[10].querySelectorAll('td'), 2)
    present_plural_second = _get_text_from_row(await rows[11].querySelectorAll('td'), 2)
    present_plural_third = _get_text_from_row(await rows[12].querySelectorAll('td'), 2)

    tasks.extend([present_singular_first, present_singular_second, present_singular_third, present_plural_first,
                  present_plural_second, present_plural_third])

    # Passive/active participles
    active_participle = _get_text_from_row(await rows[14].querySelectorAll('td'), 0)
    gerund = _get_text_from_row(await rows[16].querySelectorAll('td'), 0)

    tasks.extend([active_participle, gerund])

    # Past tense
    past_singular_masculine = _get_text_from_row(await rows[18].querySelectorAll('td'), 1)
    past_singular_feminine = _get_text_from_row(await rows[19].querySelectorAll('td'), 1)
    past_singular_neuter = _get_text_from_row(await rows[20].querySelectorAll('td'), 1)
    past_plural_all = _get_text_from_row(await rows[18].querySelectorAll('td'), 2)

    tasks.extend([past_singular_masculine, past_singular_feminine, past_singular_neuter, past_plural_all])

    # Participles and impersonal form
    active_participle_past = _get_text_from_row(await rows[22].querySelectorAll('td'), 0)
    passive_participle = _get_text_from_row(await rows[24].querySelectorAll('td'), 0)
    impersonal_form = _get_text_from_row(await rows[26].querySelectorAll('td'), 0)
    gerund_past = _get_text_from_row(await rows[28].querySelectorAll('td'), 0)

    tasks.extend([active_participle_past, passive_participle, impersonal_form, gerund_past])

    # Wait for all the tasks to finish and gather the results
    results = await asyncio.gather(*tasks)

    # Construct the final dictionary with all parsed data
    return {
        'infinitive': results[0],
        'imperative_mood': {
            'singular': {
                'first_person': results[1],
                'second_person': results[2]
            },
            'plural': {
                'first_person': results[3],
                'second_person': results[4]
            }
        },
        'future_tense': {
            'singular': {
                'first_person': results[5],
                'second_person': results[6],
                'third_person': results[7]
            },
            'plural': {
                'first_person': results[8],
                'second_person': results[9],
                'third_person': results[10]
            }
        },
        'present_tense': {
            'singular': {
                'first_person': results[11],
                'second_person': results[12],
                'third_person': results[13]
            },
            'plural': {
                'first_person': results[14],
                'second_person': results[15],
                'third_person': results[16]
            }
        },
        'active_participle': results[17],
        'gerund': results[18],
        'past_tense': {
            'singular': {
                'masculine': results[19],
                'feminine': results[20],
                'neuter': results[21]
            },
            'plural': {
                'all_genders': results[22]
            },
            'active_participle': results[23],
            'passive_participle': results[24],
            'impersonal_form': results[25],
            'gerund': results[26]
        }
    }


async def parse_perfective_verb(page):
    """
    Parses the perfective verb from the rows of the table.
    """
    # Get rows once and batch-process them
    rows = await get_rows_from_table(page)

    tasks = []

    # Infinitive verb
    tasks.append(_get_text_from_row(await rows[0].querySelectorAll('td'), 1))

    # Imperative mood
    imperative_singular_first = _get_text_from_row(await rows[3].querySelectorAll('td'), 1)
    imperative_singular_second = _get_text_from_row(await rows[4].querySelectorAll('td'), 1)
    imperative_plural_first = _get_text_from_row(await rows[3].querySelectorAll('td'), 2)
    imperative_plural_second = _get_text_from_row(await rows[4].querySelectorAll('td'), 2)

    tasks.extend(
        [imperative_singular_first, imperative_singular_second, imperative_plural_first, imperative_plural_second])

    # Future tense
    future_singular_first = _get_text_from_row(await rows[6].querySelectorAll('td'), 1)
    future_singular_second = _get_text_from_row(await rows[7].querySelectorAll('td'), 1)
    future_singular_third = _get_text_from_row(await rows[8].querySelectorAll('td'), 1)
    future_plural_first = _get_text_from_row(await rows[6].querySelectorAll('td'), 2)
    future_plural_second = _get_text_from_row(await rows[7].querySelectorAll('td'), 2)
    future_plural_third = _get_text_from_row(await rows[8].querySelectorAll('td'), 2)

    tasks.extend([future_singular_first, future_singular_second, future_singular_third, future_plural_first,
                  future_plural_second, future_plural_third])

    # Past tense
    past_singular_masculine = _get_text_from_row(await rows[10].querySelectorAll('td'), 1)
    past_singular_feminine = _get_text_from_row(await rows[11].querySelectorAll('td'), 1)
    past_singular_neuter = _get_text_from_row(await rows[12].querySelectorAll('td'), 1)
    past_plural_all = _get_text_from_row(await rows[10].querySelectorAll('td'), 2)

    tasks.extend([past_singular_masculine, past_singular_feminine, past_singular_neuter, past_plural_all])

    # Participles and impersonal form
    active_participle = _get_text_from_row(await rows[14].querySelectorAll('td'), 0)
    passive_participle = _get_text_from_row(await rows[16].querySelectorAll('td'), 0)
    impersonal_form = _get_text_from_row(await rows[18].querySelectorAll('td'), 0)
    gerund = _get_text_from_row(await rows[20].querySelectorAll('td'), 0)

    tasks.extend([active_participle, passive_participle, impersonal_form, gerund])

    # Wait for all the tasks to finish and gather the results
    results = await asyncio.gather(*tasks)

    # Construct the final dictionary with all parsed data
    return {
        "infinitive": results[0],
        "imperative_mood": {
            "singular": {
                "first_person": results[1],
                "second_person": results[2]
            },
            "plural": {
                "first_person": results[3],
                "second_person": results[4]
            }
        },
        "future_tense": {
            "singular": {
                "first_person": results[5],
                "second_person": results[6],
                "third_person": results[7]
            },
            "plural": {
                "first_person": results[8],
                "second_person": results[9],
                "third_person": results[10]
            }
        },
        "past_tense": {
            "singular": {
                "masculine": results[11],
                "feminine": results[12],
                "neuter": results[13]
            },
            "plural": {
                "all_genders": results[14]
            },
            "active_participle": results[15],
            "passive_participle": results[16],
            "impersonal_form": results[17],
            "gerund": results[18]
        }
    }


async def parse_adjective(page):
    """
    Parses the adjective forms from the rows of the table.
    """
    # Get rows once and batch-process them
    rows = await get_rows_from_table(page)

    tasks = []

    # Singular forms
    singular_nominative_masculine = _get_text_from_row(await rows[2].querySelectorAll('td'), 1)
    singular_nominative_feminine = _get_text_from_row(await rows[2].querySelectorAll('td'), 2)
    singular_nominative_neuter = _get_text_from_row(await rows[2].querySelectorAll('td'), 3)
    singular_genitive_masculine = _get_text_from_row(await rows[3].querySelectorAll('td'), 1)
    singular_genitive_feminine = _get_text_from_row(await rows[3].querySelectorAll('td'), 2)
    singular_genitive_neuter = _get_text_from_row(await rows[3].querySelectorAll('td'), 3)

    tasks.extend([singular_nominative_masculine, singular_nominative_feminine, singular_nominative_neuter,
                  singular_genitive_masculine, singular_genitive_feminine, singular_genitive_neuter])

    # Dative, accusative, instrumental, and locative (singular)
    singular_dative_masculine = _get_text_from_row(await rows[4].querySelectorAll('td'), 1)
    singular_dative_feminine = _get_text_from_row(await rows[4].querySelectorAll('td'), 2)
    singular_dative_neuter = _get_text_from_row(await rows[4].querySelectorAll('td'), 3)
    singular_accusative_masculine = _get_text_from_row(await rows[5].querySelectorAll('td'), 1)
    singular_accusative_feminine = _get_text_from_row(await rows[5].querySelectorAll('td'), 2)
    singular_accusative_neuter = _get_text_from_row(await rows[5].querySelectorAll('td'), 3)

    tasks.extend([singular_dative_masculine, singular_dative_feminine, singular_dative_neuter,
                  singular_accusative_masculine, singular_accusative_feminine, singular_accusative_neuter])

    # Instrumental and locative (singular)
    singular_instrumental_masculine = _get_text_from_row(await rows[6].querySelectorAll('td'), 1)
    singular_instrumental_feminine = _get_text_from_row(await rows[6].querySelectorAll('td'), 2)
    singular_instrumental_neuter = _get_text_from_row(await rows[6].querySelectorAll('td'), 3)
    singular_locative_masculine = _get_text_from_row(await rows[7].querySelectorAll('td'), 1)
    singular_locative_feminine = _get_text_from_row(await rows[7].querySelectorAll('td'), 2)
    singular_locative_neuter = _get_text_from_row(await rows[7].querySelectorAll('td'), 3)

    tasks.extend([singular_instrumental_masculine, singular_instrumental_feminine, singular_instrumental_neuter,
                  singular_locative_masculine, singular_locative_feminine, singular_locative_neuter])

    # Plural forms (all genders)
    plural_nominative = _get_text_from_row(await rows[2].querySelectorAll('td'), 4)
    plural_genitive = _get_text_from_row(await rows[3].querySelectorAll('td'), 4)
    plural_dative = _get_text_from_row(await rows[4].querySelectorAll('td'), 4)
    plural_accusative = _get_text_from_row(await rows[5].querySelectorAll('td'), 4)
    plural_instrumental = _get_text_from_row(await rows[6].querySelectorAll('td'), 4)
    plural_locative = _get_text_from_row(await rows[7].querySelectorAll('td'), 4)

    tasks.extend([plural_nominative, plural_genitive, plural_dative, plural_accusative, plural_instrumental, plural_locative])

    # Wait for all the tasks to finish and gather the results
    results = await asyncio.gather(*tasks)

    # Return the parsed adjective data
    return {
        "singular": {
            "nominative": {
                "masculine": results[0],
                "feminine": results[1],
                "neuter": results[2]
            },
            "genitive": {
                "masculine": results[3],
                "feminine": results[4],
                "neuter": results[5]
            },
            "dative": {
                "masculine": results[6],
                "feminine": results[7],
                "neuter": results[8]
            },
            "accusative": {
                "masculine": results[9],
                "feminine": results[10],
                "neuter": results[11]
            },
            "instrumental": {
                "masculine": results[12],
                "feminine": results[13],
                "neuter": results[14]
            },
            "locative": {
                "masculine": results[15],
                "feminine": results[16],
                "neuter": results[17]
            }
        },
        "plural": {
            "nominative": {
                "all_genders": results[18]
            },
            "genitive": {
                "all_genders": results[19]
            },
            "dative": {
                "all_genders": results[20]
            },
            "accusative": {
                "all_genders": results[21]
            },
            "instrumental": {
                "all_genders": results[22]
            },
            "locative": {
                "all_genders": results[23]
            }
        }
    }


async def parse_noun(page):
    """
    Parses the noun forms from the rows of the table.
    """
    # Get rows once and batch-process them
    rows = await get_rows_from_table(page)

    tasks = []

    # Singular forms (all genders)
    singular_nominative = _get_text_from_row(await rows[1].querySelectorAll('td'), 1)
    singular_genitive = _get_text_from_row(await rows[2].querySelectorAll('td'), 1)
    singular_dative = _get_text_from_row(await rows[3].querySelectorAll('td'), 1)
    singular_accusative = _get_text_from_row(await rows[4].querySelectorAll('td'), 1)
    singular_instrumental = _get_text_from_row(await rows[5].querySelectorAll('td'), 1)
    singular_locative = _get_text_from_row(await rows[6].querySelectorAll('td'), 1)
    singular_vocative = _get_text_from_row(await rows[7].querySelectorAll('td'), 1)

    tasks.extend([singular_nominative, singular_genitive, singular_dative, singular_accusative,
                  singular_instrumental, singular_locative, singular_vocative])

    # Plural forms (all genders)
    plural_nominative = _get_text_from_row(await rows[1].querySelectorAll('td'), 2)
    plural_genitive = _get_text_from_row(await rows[2].querySelectorAll('td'), 2)
    plural_dative = _get_text_from_row(await rows[3].querySelectorAll('td'), 2)
    plural_accusative = _get_text_from_row(await rows[4].querySelectorAll('td'), 2)
    plural_instrumental = _get_text_from_row(await rows[5].querySelectorAll('td'), 2)
    plural_locative = _get_text_from_row(await rows[6].querySelectorAll('td'), 2)
    plural_vocative = _get_text_from_row(await rows[7].querySelectorAll('td'), 2)

    tasks.extend([plural_nominative, plural_genitive, plural_dative, plural_accusative,
                  plural_instrumental, plural_locative, plural_vocative])

    # Wait for all the tasks to finish and gather the results
    results = await asyncio.gather(*tasks)

    # Return the parsed noun data
    return {
        "singular": {
            "nominative": {
                "all_genders": results[0]
            },
            "genitive": {
                "all_genders": results[1]
            },
            "dative": {
                "all_genders": results[2]
            },
            "accusative": {
                "all_genders": results[3]
            },
            "instrumental": {
                "all_genders": results[4]
            },
            "locative": {
                "all_genders": results[5]
            },
            "vocative": {
                "all_genders": results[6]
            }
        },
        "plural": {
            "nominative": {
                "all_genders": results[7]
            },
            "genitive": {
                "all_genders": results[8]
            },
            "dative": {
                "all_genders": results[9]
            },
            "accusative": {
                "all_genders": results[10]
            },
            "instrumental": {
                "all_genders": results[11]
            },
            "locative": {
                "all_genders": results[12]
            },
            "vocative": {
                "all_genders": results[13]
            }
        }
    }


async def parse_numeral(page):
    """
    Parses the numeral forms from the rows of the table.
    """
    # Get rows once and batch-process them
    rows = await get_rows_from_table(page)

    tasks = []

    # Singular forms (all genders)
    nominative = _get_text_from_row(await rows[1].querySelectorAll('td'), 1)
    genitive = _get_text_from_row(await rows[2].querySelectorAll('td'), 1)
    dative = _get_text_from_row(await rows[3].querySelectorAll('td'), 1)
    accusative = _get_text_from_row(await rows[4].querySelectorAll('td'), 1)
    instrumental = _get_text_from_row(await rows[5].querySelectorAll('td'), 1)
    locative = _get_text_from_row(await rows[6].querySelectorAll('td'), 1)

    tasks.extend([nominative, genitive, dative, accusative, instrumental, locative])

    # Wait for all the tasks to finish and gather the results
    results = await asyncio.gather(*tasks)

    # Return the parsed numeral data
    return {
        "nominative": {
            "all_genders": results[0]
        },
        "genitive": {
            "all_genders": results[1]
        },
        "dative": {
            "all_genders": results[2]
        },
        "accusative": {
            "all_genders": results[3]
        },
        "instrumental": {
            "all_genders": results[4]
        },
        "locative": {
            "all_genders": results[5]
        }
    }