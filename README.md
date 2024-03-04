# WhereDoc Scrapper

The main scrapper for WhereDoc used to gather data for the website.  Uses Selenium and BeautifulSoup to scrape data from various medical websites.

## Methods
### With Selenium:

- `Selenium_init()`:
    Used to initialise the Selenium driver. This has to be called if you are planning to call another Selenium method.

- `Selenium_AdkHospitalDocs(file_name = "adk_doctors")`:
    Used to scrape the doctors listed on the ADK hospital website and outputs to a JSON file called `file_name`.

- `Selenium_AdkSchedule(date)`:
    Used to scrape the doctors' duty schedule of the specified `date`. Input the `date` you want in the format "DDMMYYYY" as a string.
    Returns the doctors' duty schedule of that `date`.
    
---
### With BS4:

- `AdkSchedule(date)`:
    Used to scrape the doctors' duty schedule of the specified `date`. Input the `date` you want in the format "DDMMYYYY" as a string.
    Returns the doctors' duty schedule of that `date`.

## Quick Start
- Get the duty schedule of ADK for the date which you input.

```python
scrapper = WhereDocScrapper()
duty = scrapper.AdkSchedule("04032024")
```
    
