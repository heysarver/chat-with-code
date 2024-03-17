import dash_core_components as dcc
import dash_html_components as html

def Sidebar():
    return html.Div([
        html.H3('Settings', className='mt-3 text-lg font-bold'),
        html.Div([
            html.Label('Source URL', className='block text-sm font-medium text-gray-700'),
            dcc.Input(id='source-url', type='url', placeholder='Enter URL', className='mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'),
        ], className='mb-3'),
        html.Div([
            html.Label('Temperature', className='block text-sm font-medium text-gray-700'),
            dcc.Input(id='temperature', type='number', placeholder='Temperature', step=0.01, min=0, max=1, className='mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'),
        ], className='mb-3'),
    ], className='col-span-3 p-4 shadow-lg rounded-lg bg-white')
