import requests



url = "https://markhint.in/topical/igcse/0606/results?papers=&topics=CH+1+-+SETS&years=&sessions=&variants=&levels=&units=&difficulty=&page=0"
print(requests.get(url).text)