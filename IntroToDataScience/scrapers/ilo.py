# External imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Local imports
from utils.config import config
from utils.dl import get_abs_path, file_count, wait_for_download


def scrape():

    # Query for the ilo url
    query: str = "?id=TUR_A&indicator="

    # Indicators for data
    indicators = ['POP_XWAP_SEX_AGE_NB', 'POP_XWAP_SEX_AGE_EDU_NB', 'EMP_NIFL_SEX_NB',
                  'EMP_NIFL_SEX_AGE_NB', 'EMP_NIFL_SEX_EDU_NB', 'EMP_NIFL_SEX_MTS_NB',
                  'EMP_NIFL_SEX_STE_NB', 'EMP_NIFL_SEX_ECO_NB', 'EMP_NIFL_SEX_OCU_NB',
                  'EMP_NIFL_SEX_HOW_NB', 'UNE_TUNE_SEX_AGE_NB', 'UNE_TUNE_SEX_AGE_EDU_NB',
                  'UNE_TUNE_SEX_AGE_MTS_NB', 'UNE_TUNE_SEX_EDU_NB', 'UNE_TUNE_SEX_EDU_MTS_NB',
                  'GED_PHOW_SEX_HHT_CHL_NB', 'INJ_DAYS_SEX_MIG_NB', 'INJ_FATL_SEX_MIG_NB',
                  'INJ_NFTL_SEX_MIG_NB', 'INJ_NFTL_SEX_INJ_MIG_NB', 'INJ_FATL_SEX_MIG_RT',
                  'INJ_NFTL_SEX_MIG_RT', 'MST_XWAP_SEX_AGE_CBR_NB', 'MST_XWAP_SEX_EDU_CBR_NB',
                  'MFL_FPOP_SEX_CBR_NB', 'MFL_NCIT_SEX_CCT_NB', 'MFL_NEMP_SEX_ECO_NB',
                  'MFL_NEMP_SEX_OCU_NB', 'MST_TEAP_SEX_AGE_CBR_NB', 'MST_TEAP_SEX_AGE_CBR_RT',
                  'MST_TEAP_SEX_EDU_CBR_NB', 'MST_TEAP_SEX_EDU_CBR_RT', 'MST_TEMP_SEX_AGE_CBR_NB',
                  'MST_TEMP_SEX_EDU_CBR_NB', 'MST_TEMP_SEX_ECO_CBR_NB', 'MST_TEMP_SEX_OCU_CBR_NB',
                  'MST_TEMP_SEX_STE_CBR_NB', 'MST_TEMP_SEX_AGE_CBR_RT', 'MST_TEMP_SEX_EDU_CBR_RT',
                  'MST_TUNE_SEX_AGE_CBR_NB', 'MST_TUNE_SEX_EDU_CBR_NB', 'MST_TUNE_SEX_AGE_CBR_RT',
                  'MST_TUNE_SEX_EDU_CBR_RT', 'MST_EARA_SEX_CBR_NB', 'MST_TEIP_SEX_AGE_CBR_NB',
                  'MST_TEIP_SEX_AGE_CBR_RT', 'MST_TEIP_SEX_EDU_CBR_NB', 'MST_TEIP_SEX_EDU_CBR_RT',
                  'EIP_NEET_SEX_CBR_NB', 'EIP_NEET_SEX_CBR_RT']

    url = config.ILO_URL + query + '+'.join(indicators)

    # Launch selenium
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": get_abs_path()}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options, service=Service(
        ChromeDriverManager().install()))
    driver.get(url)

    # Get the export button
    export_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export')]")))

    # Click the button
    export_button.click()

    # Download check
    dl_count = file_count()

    # Download csv
    download_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'download')))
    download_link.click()

    # Wait for download
    wait_for_download(dl_count)

    # Quit selenium
    driver.quit()
