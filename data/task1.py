#------------------------------------------------------------------------------
# Script to define task 1 layout and callbacks

from dash import Dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Input,Output
import pandas as pd
import os
from app import app


#------------------------------------------------------------------------------
# Function to read and return the data as a Pandas DataFrame
def read_alldata():

	chronos_data = pd.read_csv(os.path.join("data","chronos.csv"))
	cn_data = pd.read_csv(os.path.join("data","cn.csv"))
	expression_data = pd.read_csv(os.path.join("data","expression.csv"))
	metadata_data = pd.read_csv(os.path.join("data","metadata.csv"))

	return(chronos_data,cn_data,expression_data,metadata_data)


#------------------------------------------------------------------------------
#Function to present the Data Overview
def data_ovw():


	#Read and Map data objects to corresponding dropdown option
	option=['Chronos','CN','Expression','Metadata']
	datamap=dict(zip(option,read_alldata()))

	colors = {
	'background': '#111111',
	'title': '#FFFFFF',
	'text': '#E7EA39'
	}

	markdown_text = '''
	### 1. Data Overview

	Select a Dataset from the dropdown below,
	use the interactive table to view/sort the data and the export button to download the data.
	'''

	#---------------------------
	#Task1 Layout Start

	task1_layout = html.Div(children=[
	#Title
	html.H1(
		children='Elucidata Assignment',
		style={'textAlign':'center','color': colors['title'],'backgroundColor':colors['background']}
			),

	#Description
	html.Div(
		dcc.Markdown(children=markdown_text,
		style={'textAlign':'center','color': colors['text'],'backgroundColor':colors['background']}
		)
		),

	#Dropdown List
	html.Div(children=[
		html.Label('DATASETS'),
		dcc.Dropdown(
			id='dropdown',
			options=[{'label': i, 'value': i} for i in option],
	        placeholder = 'Select a Dataset')
		],style = {'padding': 10, 'flex': 1}
		),		

	#Data Table
	dash_table.DataTable(
		id='table',
		fixed_columns={'headers': True,'data':1},
		export_format="csv",
	    page_current=0,
		page_size=20,
		page_action='custom',
		sort_action='custom',
		sort_mode='single',
		sort_by=[],
		style_table={'height': '700px', 'overflowX': 'auto','minWidth': '100%'},
		style_header={
	    'backgroundColor': 'rgb(30, 30, 30)',
	    'color': 'white'
		},
	style_data={
	    'backgroundColor': 'rgb(50, 50, 50)',
	    'color': 'white',
	    'whitespace' : 'normal',
	    'height': 'auto'
		},
	style_cell={
		'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
		'textOverflow': 'ellipsis',
		},
	tooltip_duration=None
	),

	#Summary Statistics
	html.Div(children=[
		html.Label('SUMMARY'),
		dcc.Markdown(id='summary',
		style={'textAlign':'center','color': colors['text'],'backgroundColor':colors['background']}
		)
		])
		
	])

	#---------------------------
	#Layout End

	#------------------------------------------------------------------------------
	# Callback function

	@app.callback(
		#Outputs
	    Output('table','columns'),
	    Output('table','data'),
	    Output('table','tooltip_data'),
	    Output('table','export_format'),
	    Output('summary','children'),
	    #Inputs
	    Input('dropdown', 'value'),
		Input('table', "page_current"),
	    Input('table', "page_size"),
	    Input('table', 'sort_by'))

	def update_table(dataset,page_current, page_size, sort_by):
		columns=[]
		data=[]
		tooltip=[]
		export="none"
		summary=""
		if dataset is not None:
			#Columns of selected dataset
			columns = [{"name": i, "id": i} for i in datamap[dataset].columns]
			
			#Sort data
			if len(sort_by):
				df = datamap[dataset].sort_values(
	            	sort_by[0]['column_id'],
	            	ascending=sort_by[0]['direction'] == 'asc',
	            	inplace=False)
			else:
				df = datamap[dataset]

			#Data records for the current page
			data=df.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

			#Tooltip to show data on hover
			tooltip=[
	        {
	          column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()
	        } for row in data
	    		]

			#Download Data
			export="csv"

			#Summary Statistics
			dff = pd.DataFrame(datamap[dataset])
			nrows = dff.shape[0]
			ncols = dff.shape[1]
			recs = nrows*ncols
			summary= "Number of rows: %d  \n\n  Number of columns: %d  \n\n  Number of records: %d"%(nrows,ncols,recs)
		
		return columns,data,tooltip,export,summary

	return task1_layout






	

