import language_tool_python
from .text_preprocessing import divide_into_sentences

def spelling_check_and_correct(text: str):
    tool = language_tool_python.LanguageTool('uk-UA')
    sentences = divide_into_sentences(text)
    result = []

    for sentence in sentences:
        matches = tool.check(sentence)
        
        if matches:
            errors = [match.message for match in matches]
            corrected_sentence = tool.correct(sentence)
            result.append({
                'sentence': sentence,
                'corrected_sentence': corrected_sentence
            })
            
    tool.close()
    return str(result)
