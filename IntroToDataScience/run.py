# Local imports
from utils.config import config
from utils.dl import data_exists
from scrapers.ilo import scrape as ilo_scrape
from analyzers.ilo import analyze as ilo_analyze

# International Labour Organization
print("--- ILO process started! ---")
if data_exists(config.ILO_DATA):
    print("[ILO] Data cached found! Skipping scrapping.")
else:
    print("[ILO] Data scrapping..")
    ilo_scrape()
    print("[ILO] Data scrapped!")

print("[ILO] Data analysis..")
ilo_analyze()
print("[ILO] Data analysis completed!")

print("--- ILO process ended ---")