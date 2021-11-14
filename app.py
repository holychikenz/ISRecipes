import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
from food import *

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
app = dash.Dash(__name__)

server = app.server

with open("foods.json") as jj:
    ingredients = json.load(jj)

with open("recipes.json") as jj:
    recipes = json.load(jj)

chef = Food(ingredients, recipes)

descipt = \
'''
Food, see wiki
'''

app.layout = html.Div(children=[
    html.H1(children='Cooking Emulator'),
    html.Div(children=[
        html.H3(children="Cooking Level"),
        dcc.Input(
            id='CookingLevel',
            type='number',
            min=1,
            value=1),
        html.H3(children="Ladle Level"),
        dcc.Input(
            id='LadleLevel',
            type='number',
            min=0,
            value=0),
    ]),
    html.P(children=descipt),
    dcc.Dropdown(
        id='ing1',
        options=[{'label': x, 'value': x} for x in chef.allIngredients()]
        ),
    dcc.Dropdown(
        id='ing2',
        options=[{'label': x, 'value': x} for x in chef.allIngredients()]
        ),
    dcc.Dropdown(
        id='ing3',
        options=[{'label': x, 'value': x} for x in chef.allIngredients()]
        ),
    dcc.Dropdown(
        id='ing4',
        options=[{'label': x, 'value': x} for x in chef.allIngredients()]
        ),
    dcc.Dropdown(
        id='ing5',
        options=[{'label': x, 'value': x} for x in chef.allIngredients()]
        ),
    html.P(id="effLvl"),
    html.P(id="fName"),
    html.P(id="fHP"),
    html.P(id="fStack"),
    html.P(id="fTime"),
    html.P(id="fChance")
])
@app.callback(
        Output('fName', 'children'),
        Output('fHP', 'children'),
        Output('fStack', 'children'),
        Output('fTime', 'children'),
        Output('fChance', 'children'),
        Input('ing1', 'value'),
        Input('ing2', 'value'),
        Input('ing3', 'value'),
        Input('ing4', 'value'),
        Input('ing5', 'value'),
        Input('effLvl', 'children'),
        Input('CookingLevel', 'value'),
        Input('LadleLevel', 'value')
        )
def update_food(i1, i2, i3, i4, i5, elvl, clvl, llvl):
    chef.update_levels(clvl, llvl)
    ilist = [ x for x in [i1, i2, i3, i4, i5] if x is not None ]
    if len(ilist) > 0:
        ret = chef.cook( ilist )
        return format_response(ret)
    else:
        return '', '', '', '', ''

@app.callback(
        Output('effLvl', 'children'),
        Input('CookingLevel', 'value'),
        Input('LadleLevel', 'value')
        )
def update_chef(a, b):
    chef.update_levels(a, b)
    return f'Effective Level: {chef.level}'

def format_response( x ):
    buffTxt = f'Stacks: {int(x.stacks)} of {x.buff}' if x.buff != "" else ""
    return f'{x.name} +{int(x.bonus)}', f'HP: {int(x.hp)}', f'{buffTxt}', f'Cook Time: {x.time:0.2f}', f'Chance: {x.chance:0.2f} ({x.modchance:0.2f})'

if __name__ == "__main__":
    app.run_server(debug=False)
