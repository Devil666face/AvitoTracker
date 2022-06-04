import lxml, requests, json, asyncio
from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

async def pars(id, db, bot, url, query):
    while True:
        if db.get_state(id):
            await asyncio.sleep(60)
            new_cards = parsing(id, url, query)
            for card in new_cards:
                await bot.send_message(id,card)
            if len(new_cards) == 0:
                print("Новых объявлений не найдено")
                #await bot.send_message(id, "Новых объявлений не найдено")
        else:
            return 0

def get_user_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()

def parsing (id, url, query):
        headers = {
            "Accept": "*/*",
            "User-Agent": get_user_agent()
        }

        request = requests.get(url,headers)
        soup = BeautifulSoup(request.text, "lxml")
        # print(request.text)
        all_item_cards = soup.find_all(class_="iva-item-titleStep-pdebR")

        old_cards = get_card_list(f"{id}.txt")
        cards = get_new_card_list(all_item_cards, query)

        write_cards(id, cards)

        return get_differen(cards,old_cards)

def get_new_card_list(cards, query):
    new_cards = []
    for item in cards:
        card_name = item.get_text()
        if have_key_word(card_name, query):
            href = f'https://avito.ru{(item.find_next().get("href"))}'
            new_cards.append(href)
    return new_cards


def write_cards(id, cards):
    with open(f"{id}.txt", "w", encoding="utf-8") as file:
        for card in cards:
            file.write(card + "\n")

def get_differen(new_cards, old_cards):
    dif_cards = []
    for new_card in new_cards:
        unique = True
        for old_card in old_cards:
            if (new_card == old_card):
                unique = False
        if (unique):
            dif_cards.append(new_card)
    return dif_cards

def get_card_list(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        card_list = []
        for line in file:
            card_list.append(line.replace("\n",""))
        return card_list


def have_key_word(name, query):
    check = False
    for key_word in str(query).split():
        if str(name).find(key_word)!=-1:
            check = True
    return check