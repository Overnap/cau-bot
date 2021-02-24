# Let us process asynchronously
import asyncio
import functools
# For some simple text processing
import re
# Import crawling libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# On this code, only the timeout exception is handled
from selenium.common.exceptions import TimeoutException
# For headless Firefox
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")


# Post data
class Post:

    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __eq__(self, other):
        return self.title == other.title and self.link == other.link


async def college_crawl():
    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "http://coe.cau.ac.kr/main/main.php", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find("div", {"class": "main-notice board fl"}).ul.find_all("a")

        for content in raw_data:
            data.append(Post(content.text.strip(), "http://coe.cau.ac.kr/main/main.php" + content.attrs["href"]))

    except requests.exceptions.Timeout:
        print("[Timeout] College crawling timeout")
    except Exception as error:
        print("[ERROR] College error")
        print("Error :", error)
    finally:
        return data


async def abeek_review_crawl():
    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "https://abeek.cau.ac.kr/", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find("div", {"class": "review fl"}).find("div", {"class": "cont"}).find_all("a")

        for content in raw_data:
            # Tricky Preprocessing
            link = content.attrs["href"].strip()
            if link[0] == 'w':
                link = "https://" + link
            elif link[0] == '/':
                link = "https://abeek.cau.ac.kr" + link
            elif link[0] == 'n':
                link = "https://abeek.cau.ac.kr/" + link
            data.append(Post(content.text.strip(), link))

    except requests.exceptions.Timeout:
        print("[Timeout] ABEEK Review crawling timeout")
    except Exception as error:
        print("[ERROR] ABEEK Review error")
        print("Error :", error)
    finally:
        return data


async def abeek_notice_crawl():
    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "https://abeek.cau.ac.kr/", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find("div", {"class": "notice fl"}).find("div", {"class": "cont"}).find_all("a")

        for content in raw_data:
            # Tricky Preprocessing
            link = content.attrs["href"].strip()
            if link[0] == 'w':
                link = "https://" + link
            elif link[0] == '/':
                link = "https://abeek.cau.ac.kr" + link
            elif link[0] == 'n':
                link = "https://abeek.cau.ac.kr/" + link
            data.append(Post(content.text.strip(), link))

    except requests.exceptions.Timeout:
        print("[Timeout] ABEEK Notice crawling timeout")
    except Exception as error:
        print("[ERROR] ABEEK Notice error")
        print("Error :", error)
    finally:
        return data


async def me_notice_crawl():
    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "http://me.cau.ac.kr/", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find("div", {"class": "widget-box cont-sub cont1-1"}).find("ul", {"class": "post-list"}).find_all("a")

        for content in raw_data:
            splitarr = content.text.split('-')
            title = splitarr[1]
            for i in range(2, len(splitarr)):
                title += '-'
                title += splitarr[i]
            data.append(Post(title.strip(), content.attrs["href"].strip()))

    except requests.exceptions.Timeout:
        print("[Timeout] ME Notice crawling timeout")
    except Exception as error:
        print("[ERROR] ME Notice error")
        print("Error :", error)
    finally:
        return data


async def me_employment_crawl():
    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "http://me.cau.ac.kr/", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find("div", {"class": "widget-box cont-sub cont1-3"}).find("ul", {"class": "post-list"}).find_all("a")

        for content in raw_data:
            splitarr = content.text.split('-')
            title = splitarr[1]
            for i in range(2, len(splitarr)):
                title += '-'
                title += splitarr[i]
            data.append(Post(title.strip(), content.attrs["href"].strip()))

    except requests.exceptions.Timeout:
        print("[Timeout] ME Employment crawling timeout")
    except Exception as error:
        print("[ERROR] ME Employment error")
        print("Error :", error)
    finally:
        return data


async def undergraduate_crawl():
    data = []

    try:
        loop = asyncio.get_event_loop()
        drv = functools.partial(webdriver.Firefox, options=options)
        driver = await loop.run_in_executor(None, drv)
    except Exception as error:
        print("[ERROR] Undergraduate selenium firefox driver error")
        print("ERROR :", error)
        return data

    try:
        # Timeout after 90 seconds of no load
        driver.set_page_load_timeout(90)
        await loop.run_in_executor(None, driver.get, "https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=100#;")

        # Waiting for web load to avoid errors
        await asyncio.sleep(1)

        button = await loop.run_in_executor(None, driver.find_element_by_class_name, "btn_search")
        await loop.run_in_executor(None, button.click)
        await asyncio.sleep(1)

        soup = BeautifulSoup(driver.page_source, "lxml")
        raw_data = soup.find("ul", {"id": "tbody"}).find_all("div", {"class": "txtL"})

        for content in raw_data:
            link = "https://www.cau.ac.kr/cms/FR_CON/BoardView.do?MENU_ID=100&BBS_SEQ="
            link += content.a.attrs["href"].split('\'')[1]
            data.append(Post(content.a.text.strip(), link))

    except TimeoutException:
        print("[Timeout] Undergraduate crawling timeout")
    except Exception as error:
        print("[ERROR] Undergraduate unknown error")
        print("ERROR :", error)
    finally:
        driver.quit()
        return data

