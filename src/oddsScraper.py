import requests

id_dict = {"NHL": "42133", "NFL": "88808",
           "NBA": "42648", "England - Premier League": "40253"}
goalScorerCat = 1190

def myScrape( league="NHL"):

    dk_api = requests.get(f"https://sportsbook.draftkings.com//sites/CA-ON/api/v5/eventgroups/{id_dict[league]}/categories/{goalScorerCat}?format=json").json()
    if 'eventGroup' in dk_api:
        for i in dk_api['eventGroup']['offerCategories']:
            if 'offerSubcategoryDescriptors' in i:
                dk_markets = i['offerSubcategoryDescriptors']

    subcategoryIds = []# Need subcategoryIds first
    for i in dk_markets:
        subcategoryIds.append(i['subcategoryId'])

    for ids in subcategoryIds:
        response = requests.get(f"https://sportsbook.draftkings.com//sites/CA-ON/api/v5/eventgroups/{id_dict[league]}/categories/{goalScorerCat}/subcategories/{ids}?format=json").json()
        
        for offerCat in response["eventGroup"]["offerCategories"]:
            if ((offerCat['offerCategoryId'] == 1190)):

                gameNum = 0
                while True:
                    try:
                        subCat = offerCat["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"][gameNum]
                    except (IndexError):
                        break
                    print("\n\nGame:")
                    for outcome in subCat[0]['outcomes']:
                        name = outcome['label']
                        bet = outcome['oddsAmerican']
                        print(f"Player: {name}, Bet: {bet}")
                    gameNum+=1

        exit(1)

    return None




if __name__ == "__main__":
    print(myScrape())