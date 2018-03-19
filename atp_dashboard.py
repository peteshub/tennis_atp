import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output

def read_players():
    players = pd.read_csv('./data/atp_players.csv',
                          encoding='ISO-8859-1',
                          names=['id','firstname','sirname','hand','birthday','country'],
                          index_col=0,
                          dtype=str,
                          keep_default_na=False)
    players['year'] = players['birthday'].str[:4]
    players.sort_values(by=['firstname','sirname'])
    return players


def read_rankings():
    rankings = pd.read_csv( './data/atp_rankings_all_clean.csv',
                           names=['date','ranking','player_id','points'],
                           dtype={'date':'str','player_id':'str','ranking':'int','points':'int'})

    rankings.sort_values(by='date',inplace=True)

    return rankings

players = read_players()
rankings = read_rankings()
app = dash.Dash()

app.layout = html.Div([
    html.Label('Player:'),
    dcc.Dropdown(
        id='player-dropdown',
        options=players.apply(lambda x: {'label':x['firstname']+" "+x['sirname'], 'value':str(x.name)},axis=1).values.tolist(),
        value=None,
        searchable=True,
        multi=True
    ),
    dcc.Graph(id='rankings-graph')
], className='row', style={'columnCount': 1})


@app.callback(Output('rankings-graph', 'figure'), [Input('player-dropdown', 'value')])
def update_graph(selected_dropdown_values):
    #print(list(selected_dropdown_values))
    #print(rankings.head())

    return {
        'data': [
            {
                'x': rankings[rankings['player_id']==player_id]['date'],
                'y': rankings[rankings['player_id']==player_id]['ranking'],
                'name': player_id, 'mode': 'line',
            } for player_id in selected_dropdown_values #list(selected_dropdown_values)
        ],
        'layout': {
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': "Ranking",'type':'log'}
                }
        }


if __name__ == '__main__':
    app.run_server(debug=True)
