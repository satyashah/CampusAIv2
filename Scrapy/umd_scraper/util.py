import json

# Open the visited_links.json file
with open('Scrapy/umd_scraper/visited_links.json') as file:
    data = json.load(file)

# Print the length of the array
print(len(data))