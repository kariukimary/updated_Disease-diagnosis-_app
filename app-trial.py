import dash
from dash import dcc,html 
from dash.dependencies import Output, Input, State
from pages import m_dash2
from pages import login_page


app = dash.Dash(__name__,suppress_callback_exceptions=True)


app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  html.Div(id='page-content')
                     ])


@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname =='/pages/m_dash2.py':
        return m_dash2.layout
    else:
        return login_page.layout
   
   
if __name__=='__main__':
    app.run_server(debug=True) 