import os

import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

LINK = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")


def importar_tabela(arquivo):
    """Importa um arquivo CSV e devolve a tabela

    Args:
        arquivo (str): caminho do arquivo CSV

    Returns:
        df (DataFrame): tabela com os produtos
    """

    df = pd.read_csv(arquivo)
    return df


def ent_navegador():
    """Abre o Chrome controlado pelo Selenium

    Returns:
        driver (WebDriver): navegador pronto para ser usado nas outras funções
    """
    opcoes = Options()

    preferencias = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    opcoes.add_experimental_option("prefs", preferencias)

    driver = webdriver.Chrome(options=opcoes)
    driver.maximize_window()
    return driver


def esperar_visivel(driver, tipo, valor, tempo=10):
    """Espera um elemento ficar visível na página e o devolve

    Args:
        driver (WebDriver): navegador criado em ent_navegador
        tipo (str): tipo de busca do localizador (ex.: By.ID, By.NAME)
        valor (str): valor do localizador (ex.: 'email')
        tempo (int): tempo máximo de espera em segundos (padrão: 10)

    Returns:
        elemento (WebElement): elemento visível, pronto para o send_keys

    Raises:
        TimeoutException: se o elemento não ficar visivel dentro do tempo
    """

    elemento = WebDriverWait(driver, tempo).until(
        EC.visibility_of_element_located((tipo, valor))
    )
    return elemento


def esperar_clicavel(driver, tipo, valor, tempo=10):
    """Espera um elemento ficar clicável na página e o devolve

    Args:
        driver (WebDriver): navegador criado na etapa 1
        tipo (str): tipo de busca do localizador (ex.: By.ID, By.NAME)
        valor (str): valor do localizador (ex.: 'pgtpy-botao')
        tempo (int): tempo máximo de espera em segundos (padrão: 10)

    Returns:
        elemento (WebElement): elemento clicável, pronto para o click()

    Raises:
        TimeoutException: se o elemento não ficar clicável dentro do tempo
    """

    elemento = WebDriverWait(driver, tempo).until(
        EC.element_to_be_clickable((tipo, valor))
    )
    return elemento


def ent_sys_empresa(driver, link, email, senha):
    """Entra no sistema da empresa e faz o login

    Args:
        driver (WebDriver): navegador criado em ent_navegador
        link (str): URL do sistema
        email (str): E-mail para login
        senha (str): Senha para login
    """
    driver.get(link)

    campo_email = esperar_visivel(driver, By.ID, "email")
    campo_email.send_keys(email)

    campo_senha = esperar_visivel(driver, By.ID, "password")
    campo_senha.send_keys(senha)

    botao_login = esperar_clicavel(driver, By.ID, "pgtpy-botao")
    botao_login.click()


def cadastrar_produtos(driver, tabela):
    """Cadastra os produtos da tabela no sistema da empresa

    Se um produto falhar, anota o código dele, recarrega a pagina
    e segue para o próximo.

    Args:
        driver (WebDriver): navegador já logado no sistema
        tabela (DataFrame): tabela com os produtos do CSV
    """
    falhas = []

    for linha in tabela.index:
        codigo = str(tabela.loc[linha, "codigo"])
        try:
            campo_codigo = esperar_visivel(driver, By.ID, "codigo")
            campo_codigo.send_keys(codigo)

            campo_marca = esperar_visivel(driver, By.ID, "marca")
            campo_marca.send_keys(str(tabela.loc[linha, "marca"]))

            campo_tipo = esperar_visivel(driver, By.ID, "tipo")
            campo_tipo.send_keys(str(tabela.loc[linha, "tipo"]))

            campo_categoria = esperar_visivel(driver, By.ID, "categoria")
            campo_categoria.send_keys(str(tabela.loc[linha, "categoria"]))

            campo_preco_uni = esperar_visivel(driver, By.ID, "preco_unitario")
            campo_preco_uni.send_keys(str(tabela.loc[linha, "preco_unitario"]))

            campo_custo = esperar_visivel(driver, By.ID, "custo")
            campo_custo.send_keys(str(tabela.loc[linha, "custo"]))

            campo_obs = esperar_visivel(driver, By.ID, "obs")
            obs = tabela.loc[linha, "obs"]
            if not pd.isna(obs):
                campo_obs.send_keys(str(obs))

            botao_cadastrar = esperar_clicavel(driver, By.ID, "pgtpy-botao")
            botao_cadastrar.click()

            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.ID, "codigo").get_attribute("value") == ""
            )
        except (TimeoutException, ElementClickInterceptedException):
            falhas.append(codigo)
            print(f"Falha no produto {codigo}. Recarregando a pagina...")
            driver.refresh()
    return falhas


def main():
    tabela = importar_tabela("produtos.csv")
    print(tabela.head())
    driver = ent_navegador()
    try:
        ent_sys_empresa(driver, LINK, EMAIL, SENHA)
        falhas = cadastrar_produtos(driver, tabela)
        if falhas:
            tabela_falhas = tabela[tabela["codigo"].isin(falhas)]
            tabela_falhas.to_csv("produtos_falhos.csv", index=False)
            print(
                f"{len(falhas)} produto(s) não cadastrados. "
                "Veja o arquivo produtos_falhos.csv para mais detalhes."
            )
        else:
            print("Todos os produtos foram cadastrados.")
    except TimeoutException as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
