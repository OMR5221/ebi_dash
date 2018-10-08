from __future__ import generators    # needs to be at the top of your module
from flask import Flask, request, abort
import dataset
import datafreeze
import datetime
from json import dumps
import flask_restless
import re
import os
import inflect
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dateutil
from datetime import datetime, date
from dateutil.relativedelta import relativedelta as rd
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text
import dataset
import datafreeze
from json import dumps

def GetUpdates(start_date, end_date):
    return QueryData(GetDateInt(start_date), GetDateInt(end_date))

def GetDateInt(date):
    # Convert String format to DateTime (input format): datetime.strptime(date_str, '%Y-%m-%d')
    # Convert DateTime back to String: dateTime.strftime('%Y%m%d')
    date = datetime.strptime(date, '%Y-%m-%d').date()
    date_str = date.strftime('%Y%m%d')
    return int(date_str)

def QueryData(start_date, end_date):

    plDonsbyMonthQuery = """
    select regionID,
    locationName,
    donationType,
    yearmonthdayNum,
    yearmonthdayName,
    numDonors
    from VW_INT_Agg_DailyDonorsPerLocation
    WHERE yearmonthdayNum >= '{0}' AND yearmonthdayNum <= '{1}'
    """.format(start_date, end_date)


    # mkt_text = text(plDonsbyMonthQuery)
    # mkt_res = conn.execute(mkt_text, minDate=20180701, maxDate=20180801).fetchall()
    df = pd.read_sql(plDonsbyMonthQuery, engine)

    # Convert date from string to date times
    df['yearmonthdayName'] = df['yearmonthdayName'].apply(dateutil.parser.parse, dayfirst=False)
    
    return df

	
basedir = os.path.abspath(os.path.dirname(__file__))

# Connect to MS SQL Server via Windows Authentification:
# engine = sa.create_engine('mssql+pyodbc://ORLEBIDEVDB/INTEGRATION?driver=SQL+Server+Native+Client+11.0')
engine = sa.create_engine('sqlite:///' + os.path.join(basedir, 'ebidash.db'))
conn = engine.connect()

figureName = 'Donor Type Donors by Date Range'

#startDate = datetime.datetime(2018, 7, 1) # datetime.now - 1 year
#endDate = datetime.now()
# datetime
today_date = datetime.today()
# str:
c_date_month = today_date.strftime('%Y-%m-%d')
p_date_month = (datetime.today() - rd(months=1)).strftime('%Y-%m-%d')
#curCollectDateSK = int(c_date_month)
#prCollectDateSK = int(p_date_month)

date_prior_2year = (today_date - rd(years=2)).strftime('%Y-%m-%d')

# Read in csv data:
# plDons_df = pd.read_csv('../extractors/data/mktCollect_Jul18_platelet_dons.csv')

plDons_df = GetUpdates(p_date_month, c_date_month)

"""
aggregations = {
    'person_id': 'count'
    # 'date': lambda x: max(x) - 1
}
date_groups = plDons_df.groupby('FullDateUSA')
grouped = date_groups.agg(aggregations)
grouped.columns = ["num_persons"]
"""


#fig, ax = plt.subplots(figsize=(15,7))
#plDons_df.groupby(['FullDateUSA']).count()['person_id'].plot(ax=ax)


def generate_table(dataframe, max_rows=10):

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) 
            for col in dataframe.columns
        ]) 
        for i in range(min(len(dataframe), max_rows))]
    )


server = Flask(__name__)

# db = dataset.connect('mssql+pyodbc://ORLEBIDEVDB/INTEGRATION?driver=SQL+Server+Native+Client+11.0')
db = dataset.connect('sqlite:///' + os.path.join(basedir, 'ebidash.db'))

app = dash.Dash(__name__, server=server,url_base_pathname='/ebi_dash/', csrf_protect=False)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Begin main div for DASH:
app.layout = html.Div(
    children=[
        # Title:
        html.H3(children='Donor Marketing'),
        # Date Picker Tool:
        dcc.DatePickerRange(
            id='date-picker-range',
            #month_format='YYMD',
            min_date_allowed=date_prior_2year,
            max_date_allowed=c_date_month,
            initial_visible_month=(datetime.today() - rd(months=1)).strftime('%Y-%m-%d'),
            start_date=(datetime.today() - rd(months=1)).strftime('%Y-%m-%d'),
            end_date=(datetime.today()).strftime('%Y-%m-%d')
        ),
        html.Div(id='output-container-date-picker-range'),
        # TABLE of DAILY Values:
        generate_table(plDons_df),
        #DIV for dropdown menus:
		dcc.Dropdown(
			id='my-dropdown',
			options=[
				{'label': 'New York City', 'value': 'NYC'},
				{'label': 'Montreal', 'value': 'MTL'},
				{'label': 'San Francisco', 'value': 'SF'}
			],
			value='NYC'
		),
        # Div for Graph:
        html.Div([
            # Graph Title
            html.Div([ 
            html.H3("Donor Type Count for Date Range")
            ], className='GraphTitle'),
            # LINE GRAPH: Monthly Donor Count
            dcc.Graph(id='plDonors_MTD_Graph')
        ],className='pldonor_line_graph')
    ])

@server.route('/api/plDailyDonors')
def get_plMonthDonors():

    print('Request args: ' + str(dict(request.args)))
    query_dict = {}
    
    for key in ['regionID',
    'locationName',
    'donationType',
    'yearmonthdayNum',
    'yearmonthdayName',
    'numDonors']:
        # Request the field from database model
        arg = request.args.get(key)
        
        if arg:
            query_dict[key] = arg
            
            
    #print(query_dict) = {'CollectionDateSK' : ['20180604']}
    plDonsDate = db['VW_INT_Agg_DailyDonorsPerLocation'].find(**query_dict)
    
    #list(plDons.find(_limit=10))
    if plDonsDate:
        return dumps([pl for pl in plDonsDate])
    abort(404)


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        #start_date = datetime.strptime(start_date, '%Y%m%d')
        #start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date + ' | '
    if end_date is not None:
        #end_date = datetime.strptime(end_date, '%Y%m%d')
        #end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix
    
@app.callback(
    dash.dependencies.Output('plDonors_MTD_Graph', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date')])
def update_figure(start, end):

    filtered_df = GetUpdates(start, end)
    
    aggregations={'numDonors': 'sum'}
    date_groups = filtered_df.groupby('yearmonthdayName')
    grouped = date_groups.agg(aggregations)
    grouped.columns = ["num_persons"]

    
    return {
        'data':[{'x': grouped.index, 'y': grouped.num_persons, 'type': 'line', 'name': figureName}],
        'layout': {'title': figureName}
    }

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
    app.run_server(debug=True)