from flask import Flask, render_template
import pandas as pd
import random
import matplotlib.pyplot as plt

app = Flask(__name__)

data = pd.read_csv('100 Highest-Valued Unicorns.csv', sep=';')
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)
new = data['Total Funding'].str.replace('$', '')
new = new.str.replace('M', '')
new = new.str.replace(',', '')
data['Total Funding'] = new
data = data.astype({'Total Funding': float})

new_1 = data['Valuation'].str.replace('US$', '')
new_1 = new_1.str.replace(' ', '')
new_1 = new_1.str.replace(',', '.')
data['Valuation'] = new_1
data = data.astype({'Valuation': float})


def bar_plot():
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)

    d = data.groupby('Company').agg(total_funding=('Total Funding', 'mean')).reset_index()
    d['Total Funding'] = d['Total Funding'].apply(lambda x: round(x, 1))
    plt.xlabel('Компании')
    plt.ylabel('Средняя цена')
    barplot = plt.bar(x=d['Company'], height=d['Total Funding'])
    plt.bar_label(barplot, labels=d['Total Funding'])
    plt.show()


def new_csv():
    data.dropna(inplace=True)

    company = data['Company'].value_counts().index[0]
    country = data['Country'].value_counts().index[0]
    state = data['State'].value_counts().index[0]
    city = data['City'].value_counts().index[0]
    industries = data['Industries'].value_counts().index[0]
    name_of_founders = data['Name of Founders'].value_counts().index[0]
    number_of_employees = data['Number of Employees'].value_counts().index[0]
    new_founded_year = data['Founded Year'].value_counts().index[0]

    for i in range(data.shape[0], round(data.shape[0] * 1.1) + 1, 1):
        max_total_funding = data['Total Funding'].max()
        min_total_funding = data['Total Funding'].min()
        avg_total_funding = data['Total Funding'].mean()
        new_total_funding = round(avg_total_funding + random.uniform(min_total_funding - avg_total_funding,
                                                                     max_total_funding - avg_total_funding), 1)

        max_valuation = data['Valuation'].max()
        min_valuation = data['Valuation'].min()
        avg_valuation = data['Valuation'].mean()
        new_valuation = round(avg_valuation + random.uniform(min_valuation - avg_valuation, max_valuation -
                                                             avg_valuation), 1)

        # max_founded_year = data['Founded Year'].max()
        # min_founded_year = data['Founded Year'].min()
        # avg_founded_year = data['Founded Year'].mean()
        # new_founded_year = round(avg_founded_year + random.uniform(min_founded_year - avg_founded_year, max_founded_year
        #                                                            - avg_founded_year), 1)

        new_row = [company, new_valuation, country, state, city, industries, name_of_founders, new_founded_year,
                   new_total_funding, number_of_employees]
        data.loc[i] = new_row

    data.to_csv('updated.csv', index=False)


new_csv()


@app.route('/')
def home():
    data_new = pd.read_csv('updated.csv', sep=';')
    data_new.dropna(inplace=True)
    data_new.drop_duplicates(inplace=True)

    html = """""
    <div class="container mt-4">
          <div class="card">
                <h1 class="text-center"> {task} </h1>
                <br>
                <h3 class="text-center"> Было строк данных - {old} </h3>
                <h3 class="text-center"> Стало строк данных - {new} </h3>
                <br>
                <div class="container mt-4">
                    <div class="table align-middle table-bordered">
                        {table_head}
                    </div>
                </div>
                <div class="container mt-4">
                    <div class="table align-middle table-bordered">
                        {table_tail}
                    </div>
                </div>
          </div>
    </div>
    """""

    return render_template("base.html") \
        + html.format(task="Расширенный датасет",
                      old=pd.read_csv('100 Highest-Valued Unicorns.csv',  sep=';').shape[0],
                      new=pd.read_csv('updated.csv',  sep=';').shape[0],
                      table_head=data.head(5).to_html(
                          classes='table-sm table align-middle table-bordered',
                          justify='center'),
                      table_tail=data.tail(5).to_html(
                          classes='table-sm table align-middle table-bordered', justify='center'))


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
