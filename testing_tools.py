from tool_spelling import spelling_correction_tool
from tool_wikipedia import wikipedia_tool
from tool_vocab import vocabulary_scrapper_tool

print(spelling_correction_tool.spelling_check_and_correct("бад..лина"))
print(wikipedia_tool.get_wikipedia_context("Тарас Шевченко"))
print(vocabulary_scrapper_tool.get_vocabulary_info_tool("ім'я"))