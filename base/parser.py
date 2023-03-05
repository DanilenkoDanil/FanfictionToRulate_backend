import undetected_chromedriver
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.models import Book, Chapter
from background_task import background


@background
def parse_book(url: str, genre: str, fandom: str) -> bool:
    book_name = False
    try:
        options = undetected_chromedriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        driver = undetected_chromedriver.Chrome(options=options)
        page = url.split('/')[5]
        while True:
            new_link_lst = url.split('/')
            new_link_lst[5] = str(page)
            new_url = '/'.join(str(page_num) for page_num in new_link_lst)
            driver.get(str(new_url))
            try:
                WebDriverWait(driver, timeout=1).until(EC.presence_of_element_located((By.CLASS_NAME, 'gui_normal')))
                print('Конец книги')
                driver.quit()
                return True
            except Exception as ex:
                pass
            parsed_text = WebDriverWait(driver, timeout=10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'storycontent')))
            if not book_name:
                book_name = driver.find_element(By.XPATH, '/html/body/div[4]/div/b').text
                book = Book.objects.create(name=book_name, genre=genre, link=url, fandom=fandom)
                print(book_name)
            chapter = driver.find_element(By.XPATH, '//*[@id="content"]').text.split('\n')[-1]
            chapter = chapter.replace(f"Chapter {page}: ", '')
            Chapter.objects.create(book=book, number=int(page), name=chapter, text=parsed_text.text)
            print(chapter)
            page = int(page) + 1
    finally:
        driver.quit()
        return False


url = 'https://www.fanfiction.net/s/13955771/1/A-Flight-Into-Games'