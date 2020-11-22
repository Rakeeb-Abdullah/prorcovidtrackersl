from flask import Flask, render_template, send_file, request, g, url_for
import pprint
import requests
import json
import pandas as pd
from matplotlib import pyplot as plt
from utils.news import get_news
import os.path


app = Flask(__name__)


# f = open('data.txt', 'r+')
# f.write(json.dumps(covid_data))


@app.route('/')
@app.route('/home')
@app.route('/home/sl')
def home():
    covid_data = get_covid_data()
    g.url = request.base_url
    plot_graph(global_=False)
    return render_template('index.html', data=covid_data, type='local', chart="chart.png")


@app.route('/home/gl')
def home_gl():
    covid_data = get_covid_data()
    g.url = request.base_url
    plot_graph(global_=True)
    info = covid_data['data']
    global_active_case = info['global_total_cases'] - \
        (info['global_recovered'] + info['global_deaths'])
    return render_template('index.html', data=covid_data, type='global', active_cases=global_active_case, chart="chart_gl.png")


@app.route('/download')
def download():
    covid_data = get_covid_data()

    g.url = request.base_url

    info = covid_data['data']
    data = {
        'Title': ['Local New Cases:', 'Local New Deaths:', 'Total Local Cases:', 'Total Local Recovered:', 'Total Local Deaths:', 'Total Active Cases:', 'Global New Cases', 'Global New Deaths', 'Global Total Cases', 'Global Recovered', 'Global Deaths'],
        'Number': [info['local_new_cases'] if info['local_new_cases'] > 0 else 'No Data Available Yet', info['local_new_deaths'] if info['local_new_deaths'] > 0 else 'No Data Available Yet', info['local_total_cases'], info['local_recovered'], info['local_deaths'], info['local_active_cases'], info['global_new_cases'], info['global_new_deaths'], info['global_total_cases'], info['global_recovered'], info['global_deaths']]
    }
    df = pd.DataFrame(data, columns=['Title', 'Number'])
    df.to_csv(r'./download/covid_report.csv')
    download = r'./download/covid_report.csv'
    return send_file(download, as_attachment=True)


@app.route('/news')
def news():
    g.url = request.base_url
    url = "https://www.newsfirst.lk/?s=covid"
    news_list = get_news(url=url)
    return render_template('news.html', news_list=news_list)


@app.route('/about')
def about():
    g.url = request.base_url
    return render_template('about.html')


def plot_graph(global_):
    covid_data = get_covid_data()

    info = covid_data['data']
    titles = ['Recovered', 'Deaths', 'Active Cases']
    colors = ['blue', 'red', 'green']
    explode = (0.05, 0.05, 0.05)
    fig = plt.figure(figsize=(5, 5), facecolor='blue')

    if global_:
        global_active_case = info['global_total_cases'] - \
            (info['global_recovered'] + info['global_deaths'])
        values = [info['global_recovered'],
                  info['global_deaths'], global_active_case]
        plt.pie(values, labels=titles, explode=explode,
                autopct='%1.1f%%')
        if os.path.isfile(r'./static/charts/chart_gl.png'):
            os.remove(r'./static/charts/chart_gl.png')
            plt.savefig(r'./static/charts/chart_gl.png')
        else:
            plt.savefig(r'./static/charts/chart_gl.png')

    else:
        values = [info['local_recovered'],
                  info['local_deaths'], info['local_active_cases']]
        plt.pie(values, labels=titles, explode=explode,
                autopct='%1.1f%%')
        if os.path.isfile(r'./static/charts/chart.png'):
            os.remove(r'./static/charts/chart.png')
            plt.savefig(r'./static/charts/chart.png')
        else:
            plt.savefig(r'./static/charts/chart.png')


def get_covid_data():

    res = requests.get(
        url="https://hpb.health.gov.lk/api/get-current-statistical")

    covid_data = res.json()
    # print('success run')
    return covid_data


if __name__ == '__main__':
    app.run(debug=True)
