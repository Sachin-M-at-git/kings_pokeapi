import json
from bs4 import BeautifulSoup
import requests


def get_poke_details(name):
    try:
        # Fetch the HTML content
        html_text = requests.get(f"https://pokemondb.net/pokedex/{name.replace(' ', '-')}").text
        soup = BeautifulSoup(html_text, 'lxml')

        # Find all relevant sections in the HTML
        all_info = soup.findAll('div', class_='grid-row')
        base_info = all_info[0].findAll('table', class_='vitals-table')
        pokedex_data = base_info[0].findAll('tr')

        # Initialize an empty dictionary to store the parsed data
        base_data = {}
        train_data = {}
        pokemon_data = {}
        base_data["name"] = soup.find('h1').text
        # print(all_info[0].findAll('picture'))
        img = all_info[0].find('picture').find('img')
        s_img = img['src'] if img else None

        img = all_info[0].find('a')
        l_img = img['href'] if img else None
        base_data["image"] = {"small_img": s_img, "large_img": l_img}
        # Parse the data
        for poke_d in pokedex_data[:-1]:
            if poke_d.td.strong:
                base_data[f"{poke_d.th.text[:-2]} No"] = int(poke_d.td.strong.text)
                # print(f"\"{poke_d.th.text[:-2]} No\" : {poke_d.td.strong.text}")
            elif poke_d.th.text == 'Abilities':
                base_data[f"{poke_d.th.text}"] = []
                for ability in poke_d.td.findAll('a'):
                    base_data[f"{poke_d.th.text}"].append(
                        {
                            "name": ability.text,
                            "effect": ability['title'],
                            "hidden": (True if "(hidden ability)" in poke_d.td.find(
                                'small').text else False) if ability.find_parent('small') else False
                        })
                    # True if a_tag.find_parent('small') else False
            elif types := poke_d.td.findAll('a'):
                types_text = [typee.text for typee in types]
                base_data[f"{poke_d.th.text}"] = types_text
                # print(f"\"{poke_d.th.text}\" : {types_text}")
            elif poke_d.th.text in ['Height', 'Weight']:
                base_data[f"{poke_d.th.text}"] = poke_d.td.text.replace('\xa0', ' ')
            else:
                base_data[f"{poke_d.th.text}"] = poke_d.td.text
                # print(f"\"{poke_d.th.text}\" : {value}")

        pokemon_data[all_info[0].find('h2').text] = base_data

        training_info = all_info[1].findAll('table', class_='vitals-table')
        pokedex_data = training_info[0].findAll('tr')
        for poke_d in pokedex_data:
            train_data[f"{poke_d.th.text}"] = poke_d.td.text.replace('\n', '')

        pokemon_data[all_info[1].find('h2').text] = train_data

        pokemon_json = json.dumps(pokemon_data, ensure_ascii=False)
        return pokemon_json
    except:
        return json.dumps({"error": "pokemon not found!"}, ensure_ascii=False)
