# Football Data Collector

Este repositório contém um conjunto de scripts em Python desenvolvidos para coletar dados de futebol a partir da API Football (https://rapidapi.com/api-sports/api/api-football). O objetivo é criar uma base de dados contendo informações detalhadas sobre ligas, times, temporadas e estatísticas de jogos.

## Documentação da API 
Toda a documentação da API pode ser encontrada em [https://www.api-football.com/documentation-v3](https://www.api-football.com/documentation-v3).


## Estrutura dos Arquivos
- **`requests_apifootball.py`**: Contém as funções responsáveis por realizar as requisições à API Football e processar os dados retornados.
- **`get_stats.py`**: Arquivo principal que coordena a coleta e processamento das estatísticas dos jogos, utilizando as funções definidas no `requests_apifootball.py`. Ele processa os dados de uma liga e temporada específicas e os armazena em arquivos CSV.

## Funcionalidades

### 1. Requisições à API (`requests_apifootball.py`)
Este arquivo contém as seguintes funções:

- **api_request(url, API_TOKEN, method='GET', headers=None, params=None, payload=None)**: Função genérica para realizar requisições HTTP à API. Retorna os dados da API em formato JSON ou texto.
- **get_teams_season(API_TOKEN, league, season)**: Coleta informações sobre os times de uma determinada liga e temporada.
- **get_fixtures_season(API_TOKEN, league, season)**: Coleta as partidas (fixtures) de uma determinada liga e temporada.
- **get_fixture_stats(API_TOKEN, fixture)**: Coleta as estatísticas detalhadas de uma partida específica.

### 2. Processamento de Dados de Jogos (`get_stats.py`)
Este arquivo contém a função principal:

- **create_df_stats(API_TOKEN, league, season)**: Realiza o processo de coleta de todas as estatísticas de uma liga e temporada. Os dados são salvos em um arquivo CSV no diretório `results/{league}_{season}/`.

### Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/brunobedo/api_football.git
   cd api_football
   ```

2. Instale as dependências necessárias:
   ```bash
   pip install requests pandas tqdm argparse
   ```

3. Execute o script principal `get_stats.py` passando os parâmetros da linha de comando:
   ```bash
   python get_stats.py --api_token SEU_API_TOKEN --league ID_LIGA --season ANO_TEMPORADA
   ```

   - **`--api_token`**: O seu token de acesso da API Football.
   - **`--league`**: O ID da liga. Por exemplo, para o Campeonato Brasileiro, o ID é 71.
   - **`--season`**: O ano da temporada. Por exemplo, 2020 ou 2022.

Exemplo:
   ```bash
   python get_stats.py --api_token "SUA_CHAVE_API" --league 71 --season 2022
   ```

### Estrutura do CSV

Os dados coletados serão salvos no diretório `results/{league}_{season}/` e conterão as seguintes colunas:

- **team_id**: ID do time.
- **team_name**: Nome do time.
- **team_rank**: Colocação do time na liga.
- **win**: Número de vitórias.
- **draw**: Número de empates.
- **loss**: Número de derrotas.
- **mandante**: Indica se o time é mandante na partida.
- **duracao**: Duração da partida.
- **Scouts**: Alguns Scouts da partida
### Registro de Erros

Os erros encontrados durante o processo de coleta serão registrados no arquivo `error_log.log`. Além disso, uma lista de partidas com erro será exibida ao final da execução, caso existam.

## Exemplo de Uso

- Coletar dados de uma temporada do Campeonato Brasileiro (Série A - ID 71):
   ```bash
   python get_stats.py --api_token "SUA_CHAVE_API" --league 71 --season 2022
   ```

- Os dados serão salvos em `results/71_2022/data_71-2022.csv`.

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Para isso:

1. Faça um fork do repositório.
2. Crie uma nova branch: `git checkout -b minha-feature`.
3. Faça as suas alterações.
4. Envie um pull request.
