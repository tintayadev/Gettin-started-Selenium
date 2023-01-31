import unittest
from selenium import webdriver
from pyunitreport import HTMLTestRunner


#from HtmlTestRunner import HTMLTestRunner
# submodulo  para usar el dropdown
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
# Herramienta para seleccionar elementos de la web con sus selectores
from selenium.webdriver.common.by import By

# Herramienta para hacer uso de las expected conditions y esperas explicitas
from selenium.webdriver.support.ui import WebDriverWait


# Importar esperar explicitas
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from mercado_libre_page import MercadoLibrePage


class GoogleTest(unittest.TestCase):

    # Realiza todo lo necesario antes de empezar la prueba
    @classmethod  # Decorador para que las distintas paginas corran en una sola pestaña
    def setUpClass(cls):
        s=Service('./chromedriver')
        cls.driver = webdriver.Chrome(
            service=s)
        driver = cls.driver
        # esperamos 10 seg antes de realizar la siguiente accion
        driver.implicitly_wait(5)
        driver.maximize_window()

    def test_search(self):
        ml = MercadoLibrePage(self.driver)
        ml.open_page()
        ml.select_country('CO')
        ml.accept_coockies()
        ml.ignore_location()
        ml.search('Playstation 4')
        ml.select_product_condition('Nuevo')
        ml.select_product_location('Bogotá D.C.')
        ml.order_by('Mayor precio')
        products = ml.get_products(5)
        print(products)

    @classmethod
    def tearDownClass(cls):
        # Cerramos el navegador una vez terminadas las pruebas
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(
        output='reports/MercadoLibreTest', report_name='MercadoLibreTest_report'))
