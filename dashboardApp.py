# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 18:05:53 2019

@author: mazzi
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from AnalyseRTTwitter import get_twitter_buffer,tweet_analysis
from TwitterWordcloudGen import generate_wordcloud
import pandas as pd
import flask
import os

# Server
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

# Clean up wordcloud file
open('1000tweets.txt','w',encoding='utf8').write('')

# Variables
txt_h1='test'
df_stored_scores = pd.DataFrame({'id':[],'tweet':[],'positive_score':[],'negative_score':[],'total_score':[],'var':[]})
df_buffer = pd.DataFrame({'id':[],'tweet':[]})
query = ['de','que','viu','foi','no','na','da','onde']
df_line_graph_data = pd.DataFrame({'x':[],'y':[]})
new_query =  query

# Layout
tweet_box_style = {'background-color':'gray','alpha':0.5,'width':'90%','margin':'0 auto','border':'10px','border-color':'black','padding':'20px'}
tweet_txt_style = {'color': 'black', 'fontSize': 20,'font-weight':'bold','opacity':1}


# DASH - Layout
app = dash.Dash(__name__,static_folder='assets')

app.layout = html.Div([
    html.Link(href='/assets/main.css', rel='stylesheet'),
    html.Div([
    html.H1(id='topperson',children='Twitter Sentiment Analysis - Made by: Raphael Mazzine',style={'text-align':'center'}),
    html.Label('Input Query - PRESS SEARCH'),
    html.Div([
            dcc.Input(id='input-1-submit', type='text', value='brasil',style={'width':'40%'}),
            html.Button('Search',id='buttonsearch')
    ]
    ),
    html.H1(id='h1-txt',children=txt_h1)],
    className='upper-settings'
    ),
    
    html.Div(
        [
        html.Div([
            html.H1(id='title_tweet_box',children='Real-Time Tweets',style={'fontSize':34,'color':'black','text-align':'center'}),
            html.Div([html.H1(id='txt0',children=txt_h1,style=tweet_txt_style)],id='txtbox0',style=tweet_box_style),
            html.Div([html.H1(id='txt1',children=txt_h1,style=tweet_txt_style)],id='txtbox1',style=tweet_box_style),
            html.Div([html.H1(id='txt2',children=txt_h1,style=tweet_txt_style)],id='txtbox2',style=tweet_box_style),
            html.Div([html.H1(id='txt3',children=txt_h1,style=tweet_txt_style)],id='txtbox3',style=tweet_box_style),
            html.Div([html.H1(id='txt4',children=txt_h1,style=tweet_txt_style)],id='txtbox4',style=tweet_box_style),
            
            ],
            className='six columns',style={'background-color':'white','width':'46%','height':520}
        ),
        html.Div([
                html.H1(id='title-graph',children='Sentiment Graph',style={'fontSize':34,'color':'black','text-align':'center'}),
                dcc.Graph(
                id='upper-left-graph',
                figure={
                        'data':[{
                                'x':[1,2,3],
                                'y':[1,2,3],
                                'type':'bar'
                                }],
                        'layout':{
                                'height':570
                                }
                        }
                )
                ],
                className='six columns',style={'width':'46%'}
                )
        ],className='row',style={'height':722}
    ),
    html.Div(
            [
            html.Div([
                html.Div(
                        html.H1(id='wordcloud_title',children='WordCloud',style={'fontSize':34,'color':'black','text-align':'center'})
                        ),
                html.Div(
                        html.Img(id='wordcloudimage',style={'margin-lef':'auto','margin-right':'auto','width':'80%'}),
                        style={'text-align':'center'}
                        )
                    ],
                className='six columns'
                ),
            html.Div([
                    html.Div(
                            html.H1(id='pie-title',children='Pie Chart',style={'fontSize':34,'color':'black','text-align':'center'})
                            ),
                    html.Div(
                            dcc.Graph(
                                    id='pie-chart',
                                    figure={
                                            'data':[{
                                                    
                                                    'values':[20,40,20,20],
                                                    'type':'pie',
                                                    'labels':['positive','negative','neutral','mixed'],
                                                    
                                                    'marker':{
                                                    'colors':['green','red','gray','yellow']
                                                            }
                                                    
                                                    }]
                                            }
                                    )
                            )
                    
                    ],
                className='six columns'
                ),
            ],
        className='row'
    ),
    html.H1(id='hidden'),
    dcc.Interval(id='interval1', interval=2 * 1000, n_intervals=0),
    dcc.Interval(id='interval_wordcloud', interval=20*1000, n_intervals=0),
    dcc.Interval(id='intervalbuffer',interval=5*1000,n_intervals=0)
    
    
    
])

# DASH - Action
@app.callback(
        Output('hidden','style'),
        [Input('intervalbuffer','n_intervals')]
        )
def buffer(n):
    # Buffer interval
    # Run to check buffer and ask for more data
    global df_buffer
    global df_stored_scores
    global query
    global new_query
    global df_line_graph_data
    
    if new_query==query and df_buffer.shape[0]==0:
        df_buffer = get_twitter_buffer(new_query)
    elif new_query!=query and df_buffer.shape[0]==0:
        df_buffer = get_twitter_buffer(new_query)
        # Reset stored scores for a new query statistics
        df_stored_scores = pd.DataFrame({'id':[],'tweet':[],'positive_score':[],'negative_score':[],'total_score':[],'var':[]})
        df_line_graph_data = pd.DataFrame({'x':[],'y':[]})
        open('1000tweets.txt','w',encoding='utf8').write('')
        query = new_query
        

@app.callback(
        Output('h1-txt','children'),
        [Input('buttonsearch','n_clicks')],
        [State('input-1-submit','value')]
        )
def update_output(n_clicks,input1):
    # Update when click
    global new_query
    new_query = [input1]
    return u'''
        Results for: "{}"
        '''.format(input1)

@app.callback([
            Output('txt0', 'children'),
            Output('txtbox0', 'style'),
            Output('txt1', 'children'),
            Output('txtbox1', 'style'),
            Output('txt2', 'children'),
            Output('txtbox2', 'style'),
            Output('txt3', 'children'),
            Output('txtbox3', 'style'),
            Output('txt4', 'children'),
            Output('txtbox4', 'style')
               ],
          [Input('interval1', 'n_intervals')])
def update_interval(n):
    # Here the raw tweet data (from df_buffer) is analysed in real-time
    # it is stored on the df_stored_scores and showed on tweet box
    global df_stored_scores
    global df_buffer
    global df_line_graph_data
    
    def get_style(score,var):
        style = tweet_box_style.copy()
        if score>=0.1:
            # Positive
            style['background-color'] = 'rgba(0,255,0,0.5)'
        elif score<=-0.2:
            # Negative
            style['background-color'] = 'rgba(255,0,0,0.5)'
        else:
            if var>=0.25:
                # Mixed
                style['background-color'] = 'rgba(255,255,0,0.5)'
            else:
                # Neutral
                style['background-color'] = 'rgba(89,89,89,0.5)'
                
        return style
    
    
    
    # if there is tweets in buffer / if not, ask for more
    if df_buffer.shape[0]>=1:
        tweet_data = tweet_analysis(df_buffer.iloc[0]['tweet'],df_buffer.iloc[0]['id'])
        df_stored_scores.loc[df_stored_scores.shape[0]] = tweet_data
        df_line_graph_data.loc[df_line_graph_data.shape[0]] = [df_line_graph_data.shape[0],df_stored_scores['total_score'].mean()]
        df_buffer = df_buffer.iloc[1:]
        
    # Shorter name for better writting
    df = df_stored_scores
    
    
    
    text0 = df.iloc[-5]['tweet'] if df.shape[0]>=5 else "Receiving..."
    text1 = df.iloc[-4]['tweet'] if df.shape[0]>=4 else "Receiving..."
    text2 = df.iloc[-3]['tweet'] if df.shape[0]>=3 else "Receiving..."
    text3 = df.iloc[-2]['tweet'] if df.shape[0]>=2 else "Receiving..."
    text4 = df.iloc[-1]['tweet'] if df.shape[0]>=1 else "Receiving..."
    
    
    style0 = get_style(df.iloc[-5]['total_score'],df.iloc[-5]['var']) if df.shape[0]>=5 else tweet_box_style
    style1 = get_style(df.iloc[-4]['total_score'],df.iloc[-4]['var']) if df.shape[0]>=4 else tweet_box_style
    style2 = get_style(df.iloc[-3]['total_score'],df.iloc[-3]['var']) if df.shape[0]>=3 else tweet_box_style
    style3 = get_style(df.iloc[-2]['total_score'],df.iloc[-2]['var']) if df.shape[0]>=2 else tweet_box_style
    style4 = get_style(df.iloc[-1]['total_score'],df.iloc[-1]['var']) if df.shape[0]>=1 else tweet_box_style

    
    return u'''
        Tweet: "{}"
        '''.format(text0),style0,u'''
        Tweet: "{}"
        '''.format(text1),style1,u'''
        Tweet: "{}"
        '''.format(text2),style2,u'''
        Tweet: "{}"
        '''.format(text3),style3,u'''
        Tweet: "{}"
        '''.format(text4),style4
        
        
@app.callback(Output('upper-left-graph', 'figure'),
          [Input('interval1', 'n_intervals')])
def display_graphs(n):
    # Line graph
    return{'data':[{
            'x':df_line_graph_data['x'].tolist(),
            'y':df_line_graph_data['y'].tolist(),
            'type':'lines+markers'
            }],
          'layout':{
                  'height':520
                  }
            }
@app.callback(Output('pie-chart','figure'),
              [Input('interval1','n_intervals')])
def display_pie_graphs(n):
    # Pie chart
    df = df_stored_scores
    n_pos = (df['total_score']>=0.1).sum()
    n_neg = (df['total_score']<=-0.2).sum()
    n_mix = ((df['total_score']<=0.1)&(df['total_score']>=-0.2)&(df['var']>=0.25)).sum()
    n_neu = df.shape[0]-n_pos-n_neg-n_mix
    return {
            'data':[{
            'values':[n_pos,n_neg,n_neu,n_mix],
            'type':'pie',
            'labels':['positive','negative','neutral','mixed'],
            
            'marker':{
                    'colors':['green','red','gray','yellow']
                    }
                  }]
              }
              
@app.callback(Output('wordcloudimage', 'src'),
          [Input('interval_wordcloud', 'n_intervals')])
def update_image_src(value):
    # Generate wordcloud
    uri = generate_wordcloud()
    return uri



if __name__ == '__main__':
    app.run_server(host='localhost',debug=False,port=8060)
