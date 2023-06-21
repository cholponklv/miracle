
# в shell 

import requests
from game.models import Hero

url = "https://api.opendota.com/api/heroes"
response = requests.get(url)
data = response.json()

hero_ls = []
for n in data:
    name = n['localized_name']
    desc = n['roles']
    power = n['legs']

    hero = Hero(name=name, desc=desc, power=power)
    hero_ls.append(hero)

Hero.objects.bulk_create(hero_ls)


