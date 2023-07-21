from dash import Dash, html, callback, dcc,Input,Output
import mysql
from mysql.connector import connect
import base64
import dash_auth
import os

USER_PASS_MAPPING = {'admin': '1234'}
# connection details
host = 'localhost'
user = 'root'
password = 'chatme@2023'
database = 'mydb'

#app = Dash(__name__)
#app.title = "Data Annotation application"

asset_folder = "./assets/"
image_files = [files for files in os.listdir(asset_folder) if files.endswith((".jpeg"))]
video_files = [files for files in os.listdir(asset_folder) if files.endswith((".mp4"))]
index = 0
#app=Dash(__name__)
#auth = dash_auth.BasicAuth(app, USER_PASS_MAPPING)

layout = html.Div(style={'background-color': '#3F000F'},
                      children=[dcc.Link('Log out', href='/',style={'color':'#bed4c4',}),
                          html.Div(
                              id="media-display",
                              children=[
                                  # html.Button("NEXT", id="play_button", n_clicks=0,style={"margin-left":"15px","color":"black"})
                              ]
                          ),
                          html.Div(
                              id="dropdown-textarea-div",
                              children=[
                                  html.Div([
                                      html.Label('Symptoms', style={'color': '#FFE4E1'}),
                                      dcc.Dropdown(
                                          options=['skin rashes', 'jaundice(yellow eyes)', 'pale hands', 'edema',
                                                   'swollen legs', 'facial edema', 'hepatomegaly'],
                                          value='hepatomegaly',
                                          id='symptoms',
                                          style={'background-color': 'lightgray', 'margin-right': '40%'},
                                          multi=True,
                                      ),
                                      html.Label('Disease', style={'color': '#FFE4E1'}),
                                      dcc.Dropdown(
                                          options=['skin cancer', 'liver disease ', 'blood disorder', 'Sinusitis',
                                                   'anemia', 'heart failure', ' Hepatitis'],
                                          value='blood disorder',
                                          id="disease",
                                          style={'background-color': 'lightgray', 'margin-right': '40%', },
                                          multi=True),
                                      html.Label('Comment', style={'color': '#FFE4E1'}),
                                      dcc.Textarea(
                                          id='textarea',
                                          placeholder='Enter your comment',
                                          style={'height': '100px', 'margin-right': '50%', 'width': '60%'}),

                                      html.Br(),
                                      html.Button("SAVE", id="save-button", n_clicks=0, style={"color": "black"}),
                                      html.Button("NEXT", id="play_button", n_clicks=0,
                                                  style={"margin-left": "15px", "color": "black"}),

                                      html.Div(id='container', children=[], style={'color': 'blue'}),
                                  ],
                                  )
                              ]
                          )
                      ]
                      )


@callback(
    Output("media-display", "children"),
    [Input("play_button", "n_clicks")],
)
def update_media(n_clicks):
    global index
    file = image_files[index] if index < len(image_files) else video_files[index - len(image_files)]
    file_extension = file.split(".")[-1].lower()
#checks if the media fie is an image
    if file_extension in ["jpeg"]:
        #opening,reading and clossing of the file
        with open(f"{asset_folder}/{file}", "rb") as f:
            #encoding the file as base64
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
        media = html.Img(src=f"data:image/jpeg;base64,{encoded_image}",
                         style={'max-width': '400px', 'max-height': '300px'})
#checks if the media file is in video format
    elif file_extension in ["mp4"]:
        video_path = f"{asset_folder}/{file}"
        #opening and reading in binary mode
        with open(video_path, "rb") as f:
            #encode the video as base64
            encoded_video = base64.b64encode(f.read()).decode('utf-8')
        media = html.Video(src=f"data:video/mp4;base64,{encoded_video}", autoPlay=True, controls=True,
                           style={'max-width': '400px'})
    else:
        #if the media file is not a jpg or mp4 this block is executed
        media = html.P("unsupported format")
#increments,counts the total number of video and images
    index = (index + 1) % (len(image_files) + len(video_files))

    return media


@callback(
    Output('container', 'children'),
    [Input('symptoms', 'value'),
     Input('disease', 'value'),
     Input('save-button', 'n_clicks')]
)
def update_database(symptoms, disease, n_clicks):
    if n_clicks >= 1:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        add_database = """INSERT INTO diagnosis1
        (filename,symptoms,disease)
        VALUES(%s,%s,%s)"""

        filename = "diagnosis"
        filename = str(filename)
        symptoms = str(symptoms)
        disease = str(disease)
        values = (filename,) + (symptoms,) + (disease,)

        cursor.execute(add_database, values)

        print(' labels saved to database!')

        conn.commit()
        cursor.close()
        conn.close()


#if __name__ == '__main__':
    #app.run_server(debug=True)
