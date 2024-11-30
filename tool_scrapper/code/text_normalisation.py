
def normalise_text(word):
    return word.replace('\u0301', '+')


def normalise_word_descriptions(word_name, pos, comment, pos_comment):
    word_name = normalise_text(word_name.split()[0])
    pos = pos.replace('– ', '').replace('- ', '')
    comment = comment.strip('(').strip(')')
    pos_comment = pos_comment.strip('(').strip(')')
    return word_name, pos, comment, pos_comment