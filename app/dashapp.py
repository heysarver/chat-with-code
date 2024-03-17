import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
# Import the new components
from .components.sidebar import Sidebar
from .components.chat_interface import ChatInterface

def create_dash_application(flask_app):
    dash_app = dash.Dash(
        server=flask_app,
        routes_pathname_prefix='/dashboard/',
        external_stylesheets=[
            'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'  # Tailwind CSS CDN
        ]
    )

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        Sidebar(),  # Use the Sidebar component
        ChatInterface(),  # Use the Chat Interface component
    ], className='container mx-auto h-full flex flex-row')

    @dash_app.callback(Output('chat-interface', 'children'),
                       [Input('source-url', 'value'), Input('temperature', 'value')])
    def update_chat_interface(source_url, temperature):
        # Implementation of chat interface update logic
        return f'Source URL: {source_url}, Temperature: {temperature}'

    return dash_app
