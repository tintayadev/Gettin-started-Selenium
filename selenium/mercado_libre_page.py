from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class MercadoLibrePage(object):
    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://mercadolibre.com/'
        self.search_locator = 'cb1-edit'
        self.cookie_acept_locator = '/html/body/div[2]/div[1]/div[2]/button[1]'
        self.ignore_location_locator = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/button[1]'
        self.filters_locator = 'ui-search-filter-name'
        self.order_menu_locator = '//*[@id="root-app"]/div/div[2]/section/div[1]/div/div/div/div[2]/div/div/button'
        self.oder_by_options_locator = 'andes-list__item-primary'
        self.product_name_locator = '//*[@id="root-app"]/div/div[2]/section/ol/li/div/div/div[2]/div/a/h2'
        self.product_price_locator = '//*[@id="root-app"]/div/div[2]/section/ol/li/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/span[1]/span[2]/span[2]'
        self.products_locator = '//*[@id="root-app"]/div/div[2]/section/ol'

    @property
    def keyword(self):
        input_field = self._driver.find_element(By.NAME, self.search_locator)
        return input_field.get_attribute('value')

    def select_country(self, country_id):
        country = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//a[@id="{country_id}"]'))
        )
        country.click()

    def open_page(self):
        self._driver.get(self._url)

    def type_search(self, keyword):
        input_field = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.search_locator))
        )
        input_field.clear()
        input_field.send_keys(keyword)

    def click_submit(self):
        input_field = self._driver.find_element(By.ID, self.search_locator)
        input_field.submit()

    def search(self, keyword):
        self.type_search(keyword)
        self.click_submit()

    def accept_coockies(self):
        cookies_accept = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.cookie_acept_locator)))
        cookies_accept.click()

    def ignore_location(self):
        location = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.ignore_location_locator)))
        location.click()

    def get_condition_filters(self):
        filters = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, self.filters_locator)))

        filters_dictionary = {}

        # Creamos un diccionario de filtros
        for element in filters:
            filters_dictionary[element.text] = element
        return filters_dictionary

    def select_product_condition(self, condition):

        filters = self.get_condition_filters()
        print(filters[condition])

        filters[condition].click()

    def select_product_location(self, location):
        try:
            filters = self.get_condition_filters()
            filters[location].click()
        except Exception as e:
            print(e)
            print("Error at tryint to select the product location")

    def get_order_by_filters(self):
        order_by_menu = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.order_menu_locator)))
        order_by_menu.click()

        orders_by_options = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, self.oder_by_options_locator)))

        filters_dictionary = {}

        # Creamos un diccionario de filtros
        for element in orders_by_options:
            filters_dictionary[element.text] = element
        return filters_dictionary

    def order_by(self, order):
        filters = self.get_order_by_filters()
        filters[order].click()

    def get_products(self, quantity):
        products = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.products_locator))
        )
        products_names = products.find_elements(
            By.XPATH, self.product_name_locator)[:quantity]
        products_prices = products.find_elements(
            By.XPATH, self.product_price_locator)[:quantity]

        print(f"- Total products: {len(products_names)}")

        products_dictionary = {
            products_names[i].text: products_prices[i].text for i in range(quantity)}
        return products_dictionary