from bs4 import BeautifulSoup
import requests

url = "https://www.gov.uk/government/publications/nationalities/list-of-nationalities"
def get_markup_document(url:str) -> str:
    response = requests.get(url)

    return response.text

soup = BeautifulSoup(get_markup_document(url), "html.parser")

if __name__ == "__main__":
    holder = '{ "list":['
    empty_string = ''

    for td in soup.find_all('td'):
        text:str = td.text
        if text.strip() != empty_string:
            formatted_value = f'"{text}",'
            holder += formatted_value

    no_result = -1
    last_index = holder.rfind(',')
    if last_index > no_result:
        starting_index = 0
        holder = '%s]}' % holder[starting_index:last_index]

    with open("./nationalities.json", 'w') as njson:
        njson.write(holder)
        njson.close()
