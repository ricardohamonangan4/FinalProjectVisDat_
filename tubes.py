import pandas as pd
import streamlit as st
from bokeh.io import show
from bokeh.models import ColumnDataSource, Select, DateRangeSlider
from bokeh.plotting import figure
from bokeh.models import CustomJS, HoverTool
from bokeh.layouts import column
from bokeh.resources import CDN

st.set_page_config(page_title='Final Project')
st.header('Final Project - Visualisasi Data')
st.subheader('Ricardo Hamonangan - 1301204201')
st.subheader('Olaza Aurora Syafira   - 1301202610')

# Baca CSV
df = pd.read_csv("datasetfix.csv")

Location_list = list(df['Location'].unique())

df['Date'] = pd.to_datetime(df['Date'])

cols1 = df.loc[:, ['Location', 'Date', 'Total Active Cases', 'Total Deaths', 'Total Recovered', 'Total Cases']]
cols2 = cols1[cols1['Location'] == 'DKI Jakarta']

Overall = ColumnDataSource(data=cols1)
Curr = ColumnDataSource(data=cols2)

callback = CustomJS(
    args=dict(source=Overall, sc=Curr),
    code="""
        var f = cb_obj.value
        sc.data['Date']=[]
        sc.data['Total Cases']=[]
        sc.data['Total Deaths']=[]
        sc.data['Total Recovered']=[]
        sc.data['Total Active Cases']=[]
        for(var i = 0; i <= source.get_length(); i++){
            if (source.data['Location'][i] == f){
                sc.data['Date'].push(source.data['Date'][i])
                sc.data['Total Cases'].push(source.data['Total Recovered'][i])
                sc.data['Total Deaths'].push(source.data['Total Recovered'][i])
                sc.data['Total Recovered'].push(source.data['Total Recovered'][i])
                sc.data['Total Active Cases'].push(source.data['Total Active Cases'][i])
            }
        }

        sc.change.emit();
    """
)

menu = Select(options=Location_list, value='DKI Jakarta', title='Location')  
bokeh_p = figure(x_axis_label='Date', y_axis_label='Total Active Cases', y_axis_type="linear",
                 x_axis_type="datetime")  
bokeh_p.line(x='Date', y='Total Cases', color='green', legend_label="Total Kasus", source=Curr)
bokeh_p.line(x='Date', y='Total Deaths', color='black', legend_label="Total Kematian", source=Curr)
bokeh_p.line(x='Date', y='Total Recovered', color='blue', legend_label="Total Sembuh", source=Curr)
bokeh_p.line(x='Date', y='Total Active Cases', color='red', legend_label="Total Kasus Aktif", source=Curr)
bokeh_p.legend.location = "top_right"

bokeh_p.add_tools(HoverTool(
    tooltips=[
        ('Total Kasus', '@{Total Cases}'),
        ('Total Kematian', '@{Total Deaths}'),
        ('Total Sembuh', '@{Total Recovered}'),
        ('Total Kasus Aktif', '@{Total Active Cases}'),
    ],

    mode='mouse'
))

menu.js_on_change('value', callback)

date_range_slider = DateRangeSlider(value=(min(df['Date']), max(df['Date'])), start=min(df['Date']),
                                   end=max(df['Date']))

date_range_slider.js_link("value", bokeh_p.x_range, "start", attr_selector=0)
date_range_slider.js_link("value", bokeh_p.x_range, "end", attr_selector=1)
layout = column(menu, date_range_slider, bokeh_p)

# Render plot Bokeh menggunakan Streamlit
st.bokeh_chart(layout)
