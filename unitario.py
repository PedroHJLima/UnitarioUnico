from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class TestSeuBarriga(unittest.TestCase):

		def setUp(self):
				self.driver = webdriver.Chrome()
				self.driver.get("https://seubarriga.wcaquino.me/login")

		def tearDown(self):
				# Fechar o navegador após o teste
				self.driver.quit()

		# Gera um novo login aleatório para teste de cadastro
		def generate_new_user(self):
				now = datetime.now()
				data_hora_str = now.strftime("%Y%m%d_%H%M%S")
				new_login = f"teste{data_hora_str}@teste.com"
				return new_login

		# Gera uma nova fatura aleatória
		def generate_new_invoice(self):
				now = datetime.now()
				data_hora_str = now.strftime("%Y%m%d_%H%M%S")
				new_invoice_name = f"Fatura do Aluguel - Vencimento {data_hora_str}"
				return new_invoice_name

		# Teste 1: Verificar se a página de login está carregando corretamente
		def test_login_page_load(self):
				login_page_title = self.driver.title
				self.assertIn("Seu Barriga", login_page_title, "Página de login não carregou corretamente.")

		# Teste 2: Testar o cadastro de um novo usuário
		def test_register_user(self):
				login_new_user = self.generate_new_user()
				password_new_user = 'senhaestupida123'

				# Localizar página de cadastro
				cadastro = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '//*[@id="bs-example-navbar-collapse-1"]/ul/li[2]/a'))
				)
				cadastro.click()

				# Preencher campos de cadastro
				nome = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.ID, "nome"))
				)
				nome.send_keys("Alexandre")
				email = self.driver.find_element(By.ID, "email")
				email.send_keys(login_new_user)
				senha = self.driver.find_element(By.ID, "senha")
				senha.send_keys(password_new_user)
				submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/input')
				submit.click()

				# Verificar se o cadastro foi bem-sucedido
				message = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]'))
				)
				self.assertIn("Usuário inserido com sucesso", message.text, "Falha no cadastro do usuário.")

		# Teste 3: Testar login com novo usuário cadastrado
		def test_login_user(self):
				login_new_user = self.generate_new_user()
				password_new_user = 'senhaestupida123'

				# Fazer cadastro
				self.test_register_user()

				# Tentar login com o novo usuário
				email_field = self.driver.find_element(By.ID, "email")
				email_field.send_keys(login_new_user)
				password_field = self.driver.find_element(By.ID, "senha")
				password_field.send_keys(password_new_user)
				login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
				login_button.click()

				# Verificar se o login foi bem-sucedido
				message = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success']"))
				)
				self.assertIn("Bem vindo", message.text, "Falha no login.")

		# Teste 4: Testar a adição de uma nova fatura
		def test_add_invoice(self):
				self.test_login_user()  # Certifique-se de que o usuário está logado
				new_invoice = self.generate_new_invoice()

				# Navegar até a página de adição de contas
				nav_bar = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/a')
				nav_bar.click()
				add = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/ul/li[1]/a')
				add.click()

				# Preencher e salvar nova fatura
				invoice_name = self.driver.find_element(By.ID, "nome")
				invoice_name.send_keys(new_invoice)
				save = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/div[2]/button')
				save.click()

				# Verificar se a fatura foi adicionada com sucesso
				message = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success']"))
				)
				self.assertIn("Conta adicionada com sucesso", message.text, "Falha ao adicionar nova fatura.")

		# Teste 5: Testar a edição de uma fatura
		def test_edit_invoice(self):
				self.test_add_invoice()  # Adiciona uma fatura antes de tentar editar
				new_invoice = self.generate_new_invoice()

				# Navegar até a página de listagem de contas
				nav_bar = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/a')
				nav_bar.click()
				list_invoices = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/ul/li[2]/a')
				list_invoices.click()

				# Editar a primeira fatura da lista
				edit_invoice = self.driver.find_element(By.XPATH, '//*[@id="tabelaContas"]/tbody/tr/td[2]/a[1]/span')
				edit_invoice.click()

				# Alterar nome da fatura e salvar
				invoice_name = self.driver.find_element(By.ID, "nome")
				invoice_name.clear()
				invoice_name.send_keys(new_invoice)
				save = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/div[2]/button')
				save.click()

				# Verificar se a fatura foi editada com sucesso
				message = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success']"))
				)
				self.assertIn("Conta alterada com sucesso", message.text, "Falha ao editar a fatura.")


if __name__ == "__main__":
		unittest.main()
