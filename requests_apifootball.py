import requests
import pandas as pd 
import numpy as np

def api_request(url, API_TOKEN, method='GET', headers=None, params=None, payload=None):
    headers =   {'x-rapidapi-key': API_TOKEN,
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
    try:
        # Fazer a requisição à API
        response = requests.request(method, url, headers=headers, params=params, data=payload)

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            try:
                # Tentar retornar a resposta como JSON
                return response.json()
            except ValueError:
                # Se a resposta não for JSON, retornar como texto
                return response.text
        else:
            # Retornar o código de status e o conteúdo da resposta em caso de erro
            return f"Erro {response.status_code}: {response.text}"

    except requests.RequestException as e:
        # Capturar e exibir exceções de requisições
        return f"Erro na requisição: {str(e)}"




def get_teams_season(API_TOKEN, league, season): 
    url = f'https://v3.football.api-sports.io/standings?league={league}&season={season}'
    result  = api_request(url, API_TOKEN)
    data = []
    # Iterar sobre os dados da resposta
    for league_info in result['response']:  # Corrigido para acessar a chave 'response'
        standings = league_info['league']['standings'][0]  # Acessar o primeiro grupo de standings
        
        for team_info in standings:
            team_id = team_info['team']['id']
            team_name = team_info['team']['name']
            rank = team_info['rank']
            win = team_info['all']['win']
            draw = team_info['all']['draw']
            lose = team_info['all']['lose']
            
            # Adicionar os dados à lista
            data.append({
                'team_id': team_id,
                'team_name':team_name,
                'team_rank': rank,
                'win': win,
                'draw': draw,
                'loss': lose
            })
    # Criar um DataFrame a partir da lista de dados
    df = pd.DataFrame(data)
    return df



def get_fixtures_season(API_TOKEN, league, season):
    url = f'https://v3.football.api-sports.io/fixtures?league={league}&season={season}'
    res = api_request(url, API_TOKEN)
    # Criar o DataFrame diretamente com list comprehension
    df = pd.DataFrame([{
        'jogo_id': game['fixture']['id'],
        'mandante_id': game['teams']['home']['id'],
        'visitante_id': game['teams']['away']['id'],
        'round': game['league']['round']
    } for game in res['response']])
    return df



def get_fixture_stats(API_TOKEN, fixture):
    url = f'https://v3.football.api-sports.io/fixtures?id={fixture}'
    res = api_request(url,API_TOKEN)
    
    # Preparar os dados para o DataFrame
    data = []
    
    # Tempo da partida 
    last_event = res["response"][0]["events"][-1]

    # Somando os valores da chave 'time'
    elapsed_time = last_event["time"]["elapsed"]
    extra_time = last_event["time"]["extra"] if last_event["time"]["extra"] is not None else 0
    total_time = elapsed_time + extra_time

    if total_time < 90:
        total_time = res["response"][0]["fixture"]["status"]["elapsed"]
    
    if res["response"][0]["fixture"]["status"]["elapsed"] > total_time: 
        total_time = res["response"][0]["fixture"]["status"]["elapsed"]
    
    # Mandante
    home_id = res['response'][0]['teams']['home']['id']

    away_id = res['response'][0]['teams']['away']['id']
    
    for team_data in res['response'][0]['statistics']:
        team_stats = {'team_id': team_data['team']['id'], 'team_name': team_data['team']['name']}
        for stat in team_data['statistics']:
            team_stats[stat['type']] = stat['value']
        data.append(team_stats)

    # Criar o DataFrame
    df = pd.DataFrame(data)
    df.insert(0, 'fixture', fixture)
    df.insert(3, 'home_id', home_id)
    df.insert(4, 'away_id', away_id)
    df.insert(5, 'duracao', total_time)
    df.insert(3, 'mandante', df['team_id'] == df['home_id'])
    return df