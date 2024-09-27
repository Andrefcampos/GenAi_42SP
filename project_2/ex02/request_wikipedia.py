import wikipedia
import sys

def parse_html_with_bs4(html):
    return BeautifulSoup(html, features="html.parser")

original_parse = wikipedia.wikipedia.BeautifulSoup
wikipedia.wikipedia.BeautifulSoup = parse_html_with_bs4

def get_input():
    args = sys.argv
    if len(args) == 2:
        return args[1]
    return None

def searchInput():
    input_usr = get_input()
    if input_usr:
        search_input = wikipedia.search(input_usr, results=1)
        if search_input:
            input_usr = input_usr.replace(" ", "_")
            return search_input, input_usr
    return None, None

def getPage():
    search, input_usr = searchInput()
    if not search:
        print(f"No match result.")
        return None, None
    try:
        page = wikipedia.page(search, redirect=False)
        return page, input_usr
    except:
        print(f"unexpected error [{input_usr}]")
        return None, None

def write_file():
    content, title = getPage()
    if not content or not title:
        return
    with open(f"{title}.wiki", "w") as file:
        file.write(content.summary);

wikipedia.set_lang("pt")

if __name__ == "__main__":
    write_file()
