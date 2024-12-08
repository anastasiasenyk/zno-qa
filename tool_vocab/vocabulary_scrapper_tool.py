import subprocess
from .text_prepocessing import normalize_words

def get_vocabulary_info_tool(query):
    context = []
    normalized_words = normalize_words(query)
    for word in normalized_words:
        result = subprocess.run(
                ['python3', 'tool_scrapper/run.py', word],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
        context.append(result.stdout.strip())
    return "\n".join(context)   
