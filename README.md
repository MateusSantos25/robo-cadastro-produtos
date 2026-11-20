# Robô de Cadastro de Produtos

O robô lê um arquivo CSV com os produtos e cadastra cada um no sistema da empresa, automaticamente. Um serviço que levaria horas para fazer à mão termina em questão de minutos, e você fica livre para resolver outros problemas do dia a dia.

## Como funciona

1. Lê o arquivo `produtos.csv`.
2. Abre o Chrome e faz login no sistema.
3. Cadastra cada produto, preenchendo todos os campos.
4. Se algum produto falhar, anota o código, recarrega a página e segue para o próximo.
5. No final, salva os produtos que falharam em `produtos_falhos.csv`.

## Por que Selenium

A versão original deste projeto, feita no curso, usava **PyAutoGUI**, que controla o mouse e o teclado pela posição na tela. Eu refiz o robô do zero com **Selenium**, que conversa direto com os elementos da página. Com isso:

- **Quebra menos:** os campos são encontrados pelo ID, não por coordenadas da tela. Mudar a resolução, o zoom ou a posição da janela não atrapalha.
- **É mais rápido:** em vez de pausas fixas (`sleep`), o robô espera cada elemento ficar pronto e segue na hora.
- **Trata falhas:** um produto que dá erro não derruba a execução. Ele vai para um relatório.
- **Não prende o computador:** o robô não usa o mouse nem o teclado, então você pode usar a máquina enquanto ele trabalha.

## Tecnologias

- Python
- Selenium (automação do navegador)
- pandas (leitura do CSV)
- python-dotenv (leitura das credenciais)

## Pré-requisitos

- Python 3 (testado com o Python 3.14)
- Google Chrome instalado

Não é preciso baixar o ChromeDriver. A partir da versão 4.6, o Selenium baixa o driver certo sozinho (Selenium Manager).

## Instalação

```powershell
git clone https://github.com/MateusSantos25/robo-cadastro-produtos.git
cd robo-cadastro-produtos
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:

```
EMAIL=seu_email
SENHA=sua_senha
```

O sistema de teste do curso aceita qualquer e-mail e senha, então você pode preencher o `.env` com valores inventados.

Mesmo assim, o `.env` está no `.gitignore` e nunca vai para o repositório. É uma prática de propósito: num sistema real, ali ficariam credenciais de verdade.

## Formato do CSV

O repositório inclui o arquivo `produtos.csv`, com dados de teste. Para cadastrar seus próprios produtos, use as mesmas colunas:

| Coluna | Descrição | Obrigatória |
|---|---|---|
| `codigo` | Código único do produto (ex.: `MOLO000251`) | Sim |
| `marca` | Marca do produto | Sim |
| `tipo` | Tipo do produto (ex.: Mouse, Camisa) | Sim |
| `categoria` | Número da categoria | Sim |
| `preco_unitario` | Preço de venda, com ponto decimal (ex.: `25.95`) | Sim |
| `custo` | Custo do produto, com ponto decimal (ex.: `6.50`) | Sim |
| `obs` | Observação livre | Não |

## Como usar

```powershell
python cadastro_produtos.py
```

No final, o robô mostra uma destas mensagens:

- `Todos os produtos foram cadastrados.`
- O número de produtos que falharam. Nesse caso, os produtos com falha ficam em `produtos_falhos.csv`.

## Limitações conhecidas

- Um produto pode ser cadastrado duas vezes se a página demorar a responder depois do envio.
- O robô não confere se o login deu certo antes de começar os cadastros.
- Só aceita arquivos CSV (não lê Excel nem outros formatos).

## Créditos

Projeto baseado no Intensivão de Python da Hashtag Treinamentos. O sistema de cadastro e o arquivo `produtos.csv` são materiais de teste do curso. A automação com Selenium foi reescrita por mim a partir da versão original em PyAutoGUI.

## Autor

**Mateus Santos**

- LinkedIn: [mateus-machado-dos-santos](https://www.linkedin.com/in/mateus-machado-dos-santos)
- GitHub: [MateusSantos25](https://github.com/MateusSantos25)
