from spyre import server
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class NOAADataVisualization(server.App):
    title = 'NOAA Data Visualization'

    inputs = [
        {
            'type': 'dropdown',
            'label': 'Metric',
            'options': [
                {'label': 'VCI', 'value': 'VCI'},
                {'label': 'TCI', 'value': 'TCI'},
                {'label': 'VHI', 'value': 'VHI'}
            ],
            'key': 'metric',
            'action_id': 'update_output'
        },
        {
            'type': 'dropdown',
            'label': 'Region',
            'options': [
                {'label': 'Vinnytsia r.', 'value': '1'},
                {'label': 'Volyn r.', 'value': '2'},
                {'label': 'Dnipro r.', 'value': '3'},
                # Add other regions as needed
            ],
            'key': 'region',
            'action_id': 'update_output'
        },
        {
            'type': 'text',
            'key': 'year_range',
            'label': 'Year Range',
            'value': '1982-2024',
            'action_id': 'update_output'
        },
        {
            'type': 'text',
            'key': 'week_range',
            'label': 'Week Range',
            'value': '1-52',
            'action_id': 'update_output'
        }
    ]

    outputs = [
        {
            'type': 'table',
            'id': 'data_table',
            'control_id': 'update_button',
            'tab': 'Table',
            'on_page_load': True
        },
        {
            'type': 'plot',
            'id': 'data_plot',
            'control_id': 'update_button',
            'tab': 'Plot',
            'on_page_load': True
        }
    ]

    tabs = ['Table', 'Plot']

    controls = [
        {
            'type': 'button',
            'id': 'update_button',
            'label': 'Update Data'
        }
    ]

    def __init__(self):
        self.df = pd.read_csv('../data.csv')

    def getData(self, params):
        year_range = self.parseRange(params['year_range'])
        week_range = self.parseRange(params['week_range'])
        metric = params['metric']
        region = int(params['region'])

        filtered_df = self.df[
            (self.df['area'] == region) &
            (self.df['Year'].isin(year_range)) &
            (self.df['Week'].isin(week_range))
        ]

        return filtered_df[['Year', 'Week', metric]]

    def getPlot(self, params):
        year_range = self.parseRange(params['year_range'])
        metric = params['metric']
        region = int(params['region'])

        filtered_df = self.df[
            (self.df['area'] == region) &
            (self.df['Year'].isin(year_range))
        ]

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=filtered_df, x='Year', y=metric, marker='o')
        plt.title(f'{metric} Trends Over Time')
        plt.xlabel('Year')
        plt.ylabel(metric)
        plt.grid(True)
        return plt.gcf()

    def parseRange(self, range_str):
        start, end = map(int, range_str.split('-'))
        return range(start, end + 1)


app = NOAADataVisualization()
app.launch()
