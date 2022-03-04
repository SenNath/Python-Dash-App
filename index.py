#------------------------------------------------------------------------------
# Script to run the dash app

from dash import Dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Input,Output
from app import app
import task1
import task2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='task-content')
])


colors = {
'background': '#111111',
'title': '#FFFFFF',
'text': '#E7EA39'
}


home_page = html.Div([
	html.H1(
	children='Elucidata Assignment',
	style={'textAlign':'center','color': colors['title'],'backgroundColor':colors['background']}
		),
    dcc.Link('Go to Task 1', href='/task-1'),
    html.Br(),
    dcc.Link('Go to Task 2', href='/task-2'),
])

task_1_layout = html.Div([
    html.H1('Task 1'),
    html.Div(task1.data_ovw()),
    html.Br(),
    dcc.Link('Go to Task 2', href='/task-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


task_2_layout = html.Div([
    html.H1('Task 2'),
    html.Div(task2.data_vis()),
    html.Br(),
    dcc.Link('Go to Task 1', href='/task-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


# Update page layout
@app.callback(
	Output('task-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/task-1':
        return task_1_layout
    elif pathname == '/task-2':
        return task_2_layout
    else:
        return home_page



if __name__ == '__main__':
    app.run_server(debug=True,port=8000)

