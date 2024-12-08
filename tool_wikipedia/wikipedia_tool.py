import wikipediaapi

CUSTOM_USER_AGENT = "ZNO/1.0 (sofiyafolv@gmail.com)"
wiki = wikipediaapi.Wikipedia(user_agent="ZNO/1.0 (sofiyafolv@gmail.com)", language="uk")

def get_wikipedia_context(query: str) -> str:
    keywords = query.split()
    context = ""
    for keyword in keywords:
        page = wiki.page(keyword)
        if page.exists():
            context += f"{keyword}:\n{page.summary}\n\n"
        else:
            context += f"{keyword}: Не можливо знайти інформацію.\n\n"
    
    return context.strip()

if __name__ == "__main__":
    print(get_wikipedia_context("Конституцію України було ухвалено"))
