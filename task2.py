#------------------------------------------------------------------------------
# Script to define task 2 layout and callbacks

from dash import Dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Input,Output,State
import plotly.express as px
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
#Function to present the Data Visualization
def data_vis():

	plots=['Scatter Plot','Violin Plot']

	#Read and Map data objects to corresponding dropdown option
	option=['Chronos','CN','Expression','Metadata']
	datamap=dict(zip(option,read_alldata()))

	colors = {
	'background': '#111111',
	'title': '#FFFFFF',
	'text': '#E7EA39'
	}


	markdown_text = '''
	### 2. Data Visualization

	Choose a type of plot to visualize the genes from the datasets on the graph.
	'''

	#---------------------------
	#Layout Start


	task2_layout = html.Div(children=[
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

	#Radio Button
	html.Div(children=[
		html.Label('PLOTS'),
		dcc.RadioItems(
			id='plots',
			options=[{'label': i, 'value': i} for i in plots],
			#value='Scatter Plot'
	        )
		],style={'display': 'inline-block'}
		),		

	#Dropdowns
	html.Div(id='dropdown',style = {'padding': 10, 'flex': 1}
		),


	#Plot
	html.Div(id='scatter'),
	html.Div(id='violin')
	    

	])

	#---------------------------
	#Layout End

	#------------------------------------------------------------------------------
	# Callback functions

	@app.callback(
		#Outputs
	    Output('dropdown','children'),
	    #Inputs
	    Input('plots', 'value')
	    )

	# Returns dropdown layout corresponding to plot choice
	def dropdownlayout(plot):
		
		#For Scatter Plot
		if plot=='Scatter Plot':
			
			child = html.Div([html.Label('Select two genes from any two datasets and a filter from Metadata',style = {'color': colors['text']}),
	        html.Div([
	            dcc.Dropdown(
	                id='xdata',
	                options=[{'label': i, 'value': i} for i in option[0:3]],
	                placeholder='Select a Dataset (x-axis)'
	            ),
	            dcc.Dropdown(
	                id='xgene',
	                placeholder='Select a Gene (x-axis)'
	            )
	        	], style = {'padding': 10, 'flex': 1}
	        	),
	        html.Div([
	            dcc.Dropdown(
	                id='ydata',
	                options=[{'label': i, 'value': i} for i in option[0:3]],
	                placeholder='Select a Dataset (y-axis)'
	            ),
	            dcc.Dropdown(
	                id='ygene',
	                placeholder='Select a Gene (y-axis)'
	            )
	            ], style = {'padding': 10, 'flex': 1}
	        	),
	        dcc.Dropdown(
	            id='filter',
	            options=[{'label': i, 'value': i} for i in datamap['Metadata'].iloc[0:0,1:]],
	            placeholder='Select a Filter',
	            style = {'padding': 10, 'flex': 1}
	        )    
	    		],style = {'backgroundColor':colors['background']}
	   		)
		
		#For Violin Plot
		elif plot=='Violin Plot':

		    child = html.Div([html.Label('Select a gene from any dataset and a category from Metadata for distribution',style = {'color': colors['text']}),
	        dcc.Dropdown(
	            id='vdata',
	            options=[{'label': i, 'value': i} for i in option[0:3]],
	            placeholder='Select a Dataset'
	        ),
	        dcc.Dropdown(
	            id='vgene',
	            placeholder='Select a Gene'
	        ),
	        dcc.Dropdown(
	            id='cgry',
	            options=[{'label': i, 'value': i} for i in datamap['Metadata'].iloc[0:0,1:]],
	            placeholder='Select a Category'
	        )   
			],style = {'padding': 10, 'flex': 1,'backgroundColor':colors['background']}
	    	)
		else:
			child=[]
		
		return child


	# Returns essential gene choices for a given dataset - scatter plot
	@app.callback(
		#Outputs
	    Output('xgene','options'),
	    Output('ygene','options'),
	    #Inputs
	    Input('xdata', 'value'),
	    Input('ydata', 'value')
	    )
	def scatter_dropdownchoice(xd,yd):
		xoptions=[]
		yoptions=[]
		if xd is not None:
			#Genes of selected dataset - X axis
			xoptions = [{"label": i, "value": i} for i in datamap[xd].iloc[0:0,1:]]
		if yd is not None:
			#Genes of selected dataset - Y axis
			yoptions = [{"label": i, "value": i} for i in datamap[yd].iloc[0:0,1:]]

		return xoptions,yoptions


	# Returns essential gene choices for a given dataset - violin plot
	@app.callback(
		#Outputs
	    Output('vgene','options'),
	    #Inputs
	    Input('vdata', 'value')
	    )
	def violin_dropdownchoice(vd):
		voptions=[]
		if vd is not None:
			#Genes of selected dataset
			voptions = [{"label": i, "value": i} for i in datamap[vd].iloc[0:0,1:]]
		return voptions


	#For Scatter Plot
	@app.callback(
		#Outputs
	    Output('scatter','children'),
	    #Inputs for scatter plot
	    Input('xdata', 'value'),
	    Input('ydata', 'value'),
	    Input('xgene', 'value'),
	    Input('ygene', 'value'),
	    Input('filter', 'value'),
	    #State
	    State('plots', 'value'),
	    )

	def scatter_graph(xd,yd,xg,yg,fil,plot):
		
		fig=[]

		if xg and yg and fil is not None:
			if plot=='Scatter Plot':
				
				#Merge the 3 Datasets using left join
				sam_id = datamap[xd].columns[0]
				cols = [sam_id,xg]
				df1 = pd.DataFrame(datamap[xd], columns=cols)

				df2 = pd.DataFrame(datamap[yd])
				key1 = df2.columns[0]
				df1 = pd.merge(df1,df2[[key1,yg]],on=sam_id, how='left')

				df3 = pd.DataFrame(datamap['Metadata'])
				key2 = df3.columns[0]
				
				df_new = pd.merge(df1,df3[[key2,fil]],on=sam_id, how='left')
				df_new = df_new.dropna()
				cname1=df_new.columns[1]
				cname2=df_new.columns[2]
				df_new= df_new.rename(columns={cname1: str("%s Gene Effect(%s)"%(cname1,xd)).replace("_x","")})
				df_new= df_new.rename(columns={cname2: str("%s (%s)"%(cname2,yd)).replace("_y","")})

				fig = html.Div([html.Label('SCATTER PLOT',style={'textAlign':'center'}),
		        	  dcc.Graph(
		              figure = px.scatter(df_new, x=df_new.columns[1], y=df_new.columns[2],
		                color=df_new[fil], hover_name=df_new[sam_id], size_max=55
		                ))
		        	  ])
		        		

		return fig

	#For Violin Plot
	@app.callback(
		#Outputs
	    Output('violin','children'),
	    #Inputs for violin plot
	    Input('vdata', 'value'),
	    Input('vgene', 'value'),
	    Input('cgry', 'value'),
	    #State
	    State('plots', 'value')
	    )

	def violin_graph(vd,vg,cgy,plot):
		
		fig=[]

		if vg and cgy is not None:
			if plot=='Violin Plot':
				
				#Merge the 2 Datasets using left join
				sam_id = datamap[vd].columns[0]
				cols = [sam_id,vg]
				df1 = pd.DataFrame(datamap[vd], columns=cols)


				df2 = pd.DataFrame(datamap['Metadata'])
				key2 = df2.columns[0]
				
				df_new = pd.merge(df1,df2[[key2,cgy]],on=sam_id, how='left')
				df_new = df_new.dropna()
				cname=df_new.columns[1]
				df_new= df_new.rename(columns={cname: "%s Gene Effect(%s)"%(cname,vd)})

				fig = html.Div([html.Label('Violin Plot',style={'textAlign':'center'}),
		        	  dcc.Graph(
		              figure = px.violin(df_new, x=df_new.columns[1],y=df_new[cgy],
		                color=df_new[cgy], hover_name=df_new[sam_id],hover_data=df_new.columns)
		        			)
		        			  ])
		return fig

	return task2_layout


