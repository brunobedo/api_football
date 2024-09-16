import os
import pandas as pd
import logging
import requests_apifootball
import argparse
from tqdm import tqdm


def create_df_stats(API_TOKEN, league, season):
    # Configurar o logger
    logging.basicConfig(filename='error_log.log', level=logging.ERROR, format='%(asctime)s %(message)s')

    # Lista para armazenar DataFrames de cada jogo
    data_frames = []
    
    # Lista de erros
    erros = []
    
    # Obtenção de todos os jogos da temporada
    df_jogos = requests_apifootball.get_fixtures_season(API_TOKEN, league, season)

    # Iterando sobre os jogos com barra de progresso
    for fixture_id in tqdm(df_jogos['jogo_id'], desc="Processing Fixtures", unit="fixture"):
        try:
            # Pegando estatísticas de cada jogo
            df_fixture = requests_apifootball.get_fixture_stats(API_TOKEN, fixture_id)
            data_frames.append(df_fixture)
            
            # Atualizando a barra de progresso com o ID da fixture
            tqdm.write(f"Processed fixture ID: {fixture_id}")
            
        except Exception as e:
            logging.error(f"Erro ao acessar estatísticas do jogo {fixture_id}: {e}")
            erros.append(fixture_id)
            tqdm.write(f"Erro ao acessar estatísticas do jogo {fixture_id}. Verifique o log.")
    
    # Concatenando todos os DataFrames de estatísticas
    if data_frames:
        df_stats = pd.concat(data_frames, axis=0).reset_index(drop=True)
    else:
        print("Nenhum dado de estatísticas foi obtido.")
        return
    
    # Salvando os resultados
    folder_result = f'results/{league}_{season}'
    os.makedirs(folder_result, exist_ok=True)
    df_stats.to_csv(f'{folder_result}/data_{league}-{season}.csv', index=False)
    
    print(f'Dados salvos em {folder_result}/data_{league}-{season}.csv')

    # Exibindo se houve erros
    if erros:
        print(f"Os seguintes jogos tiveram erros e não foram processados: {erros}")
    else:
        print("Todos os jogos foram processados com sucesso.")



if __name__ == "__main__":
    # Configurando argparse para aceitar argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Processar estatísticas de jogos de uma liga e temporada específicas.")
    
    # Adicionando argumentos
    parser.add_argument("--api_token", type=str, required=True, help="API token para acessar os dados.")
    parser.add_argument("--league", type=int, required=True, help="Identificação da liga (Ex: 71 Série a Campeonato Brasileiro).")
    parser.add_argument("--season", type=int, required=True, help="Ano da temporada a ser processada (Ex: 2020; 2022, etc.).")
    
    # Parseando os argumentos
    args = parser.parse_args()
    
    # Chamando a função com os argumentos da linha de comando
    create_df_stats(args.api_token, args.league, args.season)
