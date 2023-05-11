from Parsers.AEA import parse_file
import pandas as pd
import os


os.chdir('Scrapers/Scrapers/spiders/data/AEA/full')

data = []
for filename in os.listdir():
    data.append(parse_file(filename))

for i in range(6):
    os.chdir('..')

os.chdir('Result')
pd.DataFrame(data).to_csv('AEA.csv', index=False)