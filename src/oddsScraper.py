import requests

id_dict = {"NHL": "42133", "NFL": "88808",
           "NBA": "42648", "England - Premier League": "40253"}
goalScorerCat = 1190

def main():
    playerInfo = scraper()

def scraper( league="NHL"):

    playerInfo = []

    dk_api = requests.get(f"https://sportsbook.draftkings.com//sites/CA-ON/api/v5/eventgroups/{id_dict[league]}/categories/{goalScorerCat}?format=json").json()
    if 'eventGroup' in dk_api:
        for i in dk_api['eventGroup']['offerCategories']:
            if 'offerSubcategoryDescriptors' in i:
                dk_markets = i['offerSubcategoryDescriptors']

    subcategoryIds = []# Need subcategoryIds first

    try:
        for i in dk_markets:
            subcategoryIds.append(i['subcategoryId'])
    except UnboundLocalError:
        print("No Goalscorer bets on Draftkings")
        return

    for ids in subcategoryIds:
        print("\nGathering odds...\n")
        response = requests.get(f"https://sportsbook.draftkings.com//sites/CA-ON/api/v5/eventgroups/{id_dict[league]}/categories/{goalScorerCat}/subcategories/{ids}?format=json").json()
        
        for offerCat in response["eventGroup"]["offerCategories"]:
            if ((offerCat['offerCategoryId'] == 1190)):

                gameNum = 0
                while True:
                    try:
                        subCat = offerCat["offerSubcategoryDescriptors"][0]["offerSubcategory"]["offers"][gameNum]
                    except (IndexError):
                        break
                    for outcome in subCat[0]['outcomes']:
                        try:
                            name = outcome['playerNameIdentifier']
                        except KeyError:
                            name = outcome['participant']
                            
                        bet = outcome['oddsAmerican']
                        playerInfo.append({
                            "name": name,
                            "bet": bet
                        })
                        # print(f"Player: {playerInfo[-1]['name']}, bet: {playerInfo[-1]['bet']}")
                    gameNum+=1
        
        return playerInfo

if __name__ == "__main__":
    print(scraper())
    