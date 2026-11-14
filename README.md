## PROJETO

Projeto de monitoramento ambiental desenvolvido para a disciplina de **Projeto e Desenvolvimento - Ciências da Computação** (Grupo 13). 

A ideia do sistema é coletar dados climáticos e de qualidade do ar em tempo real usando um microcontrolador ESP32. Em áreas urbanas, a temperatura e a qualidade do ar variam bastante de um bairro para outro (por conta de ilhas de calor, falta de vegetação, etc.). Com essa estação, conseguimos registrar essas medições localmente e exibi-las em um painel web para facilitar a análise desses dados.

## Como funciona

O fluxo do projeto é dividido em três partes principais:

1. **Coleta (Hardware):** O ESP32 roda um script em MicroPython (`boot.py`) que lê os sensores conectados na protoboard, monta um JSON com o valor coletado e o nome do sensor, e dispara via requisição HTTP POST para a rede local.
2. **Processamento e Banco de Dados (Backend):** Uma API feita em Python com Flask (`app.py`) recebe esses JSONs na rota `/sensor/insert`. Os dados são tratados e salvos em um banco de dados SQLite (`banco.db`), junto com logs de execução e erros.
3. **Visualização (Frontend):** Um dashboard web construído com HTML, CSS e Bootstrap consome os dados do banco e mostra gráficos com a média dos últimos dias e uma tabela com as leituras mais recentes de cada sensor.

## Hardware Utilizado

* **Microcontrolador:** ESP32 (alimentado via USB e conectado via Wi-Fi na rede local)
* **BMP280:** Pressão atmosférica e temperatura
* **DHT22:** Temperatura e umidade do ar
* **MQ135:** Qualidade do ar / gases
* **LDR:** Intensidade de luminosidade

## Estrutura do Projeto

```text
├── static/                 # Arquivos estáticos (CSS, imagens, etc.)
├── templates/              # Páginas HTML do dashboard (Bootstrap)
├── app.py                  # Servidor Flask, rotas do dashboard e endpoint /sensor/insert
├── Conexao.py              # Gerenciamento do SQLite e criação automática das tabelas
├── funcoes.py              # Funções auxiliares e gravação de logs no banco
├── SensorRepository.py     # Regras de negócio para processar e salvar os dados dos sensores
├── banco.db                # Banco de dados SQLite (gerado automaticamente)
└── esp32/
    └── boot.py             # Código em MicroPython que roda no ESP32