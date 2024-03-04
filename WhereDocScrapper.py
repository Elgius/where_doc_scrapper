from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import httpx
from time import sleep
import json
from typing import Dict, List


class WhereDocScrapper:
    """
    The main scrapper for WhereDoc used to gather data for the website. 
    
    ## Methods
    ----------
    ### With Selenium:

    `Selenium_init()`
        Used to initialise the Selenium driver. This has to be called if you are planning to call another Selenium method.
    
    `Selenium_AdkHospitalDocs(file_name = "adk_doctors")`
        Used to scrape the doctors listed on the ADK hospital website and outputs to a JSON file called `file_name`.

    `Selenium_AdkSchedule(date)`
        Used to scrape the doctors' duty schedule of the specified `date`. Input the `date` you want in the format "DDMMYYYY" as a string.
        Returns the doctors' duty schedule of that `date`.

    ### With BS4:

    `AdkSchedule(date)`
        Used to scrape the doctors' duty schedule of the specified `date`. Input the `date` you want in the format "DDMMYYYY" as a string.
        Returns the doctors' duty schedule of that `date`.
    """
    def __init__(self):
        self.driver = None
    
    def Selenium_init(self):
        """Initialise the Selenium driver."""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_experimental_option('detach', True)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = self.options
        )
    
    def Selenium_AdkHospitalDocs(self, file_name: str = "adk_doctors"):
        """
        This will scrape ADK Hospital Doctors. `file_name` will be "adk_doctors" by default unless specified by the user.
        
        P.S: Uses Selenium.
        """
        url = "https://www.adkhospital.mv/en/employee/search?query=&submit=Search"

        if not self.driver:
            print("Initialise Selenium driver first using Selenium_init function.")
            return
        
        self.driver.get(url)
        total_data: List[Dict[str, str]] = []
        for page in range(14):
            results: List[WebElement] = self.driver.find_elements(By.CLASS_NAME, "entry")

            for result in results:
                image = result.find_element(By.TAG_NAME, "img")
                img_url = image.get_property("src")
                
                data: Dict[str, str] = {}
                result_list = result.text.split("\n")
                for _id, each in enumerate(result_list):
                    if _id == 0:
                        data["name"] = each
                        continue
                    
                    if each.lower().find("license") != -1:
                        data["license"] = each.split(":")[1].strip()
                        continue

                    sub = each.split(":")
                    if len(sub) == 2:
                        data[sub[0].lower()] = sub[1].strip()
                        continue
                    else:
                        data["designation"] = each

                data['img'] = img_url
                total_data.append(data)
            
            next_btn = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div[3]/ul/li[12]/a")
            next_btn.click()
            sleep(6)

        with open(f"{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(total_data, f, indent=4)

        self.driver.close()

        return total_data
    
    def Selenium_AdkSchedule(self, date: str):
        """
        Scrape the current doctors' duty schedule of ADK.

        Input the `date` you want in the format "DDMMYYYY" as a string.
        """
        url = f"https://www.adkhospital.mv/en/duty/{date}"

        if not self.driver:
            print("Initialise Selenium driver first using Selenium_init function.")
            return
        
        self.driver.get(url)

        result: List[Dict[str, str]] = []
        table = self.driver.find_element(By.ID, "duty-list")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            data: Dict[str, str] = {}
            cells = row.find_elements(By.TAG_NAME, "td")
            data["doctor"] = cells[1].text
            data["time"] = cells[2].text

            result.append(data)

        self.driver.close()
        return result
    
    def AdkSchedule(self, date: str) -> List[Dict[str, str]]:
        """
        Scrape Adk Doctors' Schedule using BeautifulSoup.
        
        Input the `date` you want in the format "DDMMYYYY" as a string. 
        Returns the doctors' duty schedule of that `date`.
        """
        url = f"https://www.adkhospital.mv/en/duty/{date}"
        with httpx.Client(http2=True, timeout=httpx.Timeout(5, read=None, connect=None)) as client:
            page = client.get(url)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        duty_table = soup.find("table")
        table_body = duty_table.find("tbody")
        rows: List[NavigableString | Tag] = table_body.find_all("tr")

        result: List[Dict[str, str]] = []
        for row in rows:
            data: Dict[str, str] = {}
            cells: List[NavigableString | Tag] = row.find_all("td")
            data["doctor"] = cells[1].text
            data["time"] = cells[2].text

            result.append(data)

        return result


if __name__ == "__main__":
    scrapper = WhereDocScrapper()
    # duty = scrapper.AdkSchedule("04032024")
