from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

data = pd.read_csv('100 Highest-Valued Unicorns.csv', sep=';')
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)
new = data['Total Funding'].str.replace('$', '')
new = new.str.replace('M', '')
new = new.str.replace(',', '')
data['Total Funding'] = new
data = data.astype({'Total Funding': float})


task1 = "Задание 1. Минимальное, максимальное, среднее общее финансирование по странам."
task2 = "Задание 2. Минимальное, максимальное, среднее общее финансирование по году основания."
task3 = "Задание 3. Минимальное, максимальное, среднее общее финансирование по количеству служащих."
task4 = "Задание 4. Минимальное, максимальное, среднее общее финансирование по городам."


@app.route('/')
def home():
    html = """"" 
            <div class="container mt-4">
                  <div class="card">
                        <h5 class="text-center"> Min = {min}, Max = {max}</h5>
                  </div>
            </div>
        """""
    html_task1 = """"" 
            <div class="container mt-4">
                  <div class="card">
                        <h1 class="text-center"> {task} </h1>
                        <br>
                        <h5 class="text-center">
                        По проанализированным данным можно сделать вывод, что 
                        Минимальное финансирование по странам - {min} = {min_res},
                        Максимальное финансирование по странам - {max} = {max_res}
                        </h5>
                        <div class='container mt-4'>
                            <div class='table align-middle table-bordered'>
                                {category}
                            </div>
                        </div>
                  </div>
            </div>
            """""

    html_task2 = """""
            <div class="container mt-4">
                  <div class="card">
                        <h1 class="text-center"> {task} </h1>
                        <br>
                        <h5 class="text-center">
                        По проанализированным данным можно сделать вывод, что 
                        Минимальное финансирование по году основания - {min} = {min_res},
                        Максимальное финансирование по году основания - {max} = {max_res}
                        </h5>
                        <div class="container mt-4">
                            <div class="table align-middle table-bordered">
                                {sub_category}
                            </div>
                        </div>
                  </div>
                </div>
            """""

    html_task3 = """""
            <div class="container mt-4">
                  <div class="card">
                        <h1 class="text-center"> {task} </h1>
                        <br>
                        <h5 class="text-center">
                        По проанализированным данным можно сделать вывод, что 
                        Минимальное финансирование по количеству служащих - {min} = {min_res},
                        Максимальное финансирование по количеству служащих - {max} = {max_res}
                        </h5>
                        <div class="container mt-4">
                            <div class="table align-middle table-bordered">
                                {sub_category}
                            </div>
                        </div>
                  </div>
                </div>
            """""

    html_task4 = """""
                <div class="container mt-4">
                  <div class="card">
                        <h1 class="text-center"> {task} </h1>
                        <br>
                        <h5 class="text-center">
                        По проанализированным данным можно сделать вывод, что 
                        Минимальное финансирование по городам - {min} = {min_res},
                        Максимальное финансирование по городам - {max} = {max_res}
                        </h5>
                        <div class="container mt-4">
                            <div class="table align-middle table-bordered">
                                {sub_category}
                            </div>
                        </div>
                  </div>
                </div>
            """""

    country = data.groupby(['Country']).agg({'Total Funding': ['min', 'max', 'mean']}).reset_index()
    country.columns = ['Страна', 'Минимальное финансирование', 'Максимальное финансирование', 'Среднее финансирование']
    country['Среднее финансирование'] = country['Среднее финансирование'].apply(lambda x: round(x, 2))
    country_max = country.loc[country['Среднее финансирование'].idxmax()]
    country_min = country.loc[country['Среднее финансирование'].idxmin()]

    founded_year = data.groupby(['Founded Year']).agg({'Total Funding': ['min', 'max', 'mean']}).reset_index()
    founded_year.columns = ['Год основания', 'Минимальное финансирование', 'Максимальное финансирование', 'Среднее финансирование']
    founded_year['Среднее финансирование'] = founded_year['Среднее финансирование'].apply(lambda x: round(x, 2))
    founded_year_max = founded_year.loc[founded_year['Среднее финансирование'].idxmax()]
    founded_year_min = founded_year.loc[founded_year['Среднее финансирование'].idxmin()]

    number_of_employees = data.groupby(['Number of Employees']).agg({'Total Funding': ['min', 'max', 'mean']}).reset_index()
    number_of_employees.columns = ['Количество служащих', 'Минимальное финансирование', 'Максимальное финансирование', 'Среднее финансирование']
    number_of_employees['Среднее финансирование'] = number_of_employees['Среднее финансирование'].apply(lambda x: round(x, 2))
    number_of_employees_max = number_of_employees.loc[number_of_employees['Среднее финансирование'].idxmax()]
    number_of_employees_min = number_of_employees.loc[number_of_employees['Среднее финансирование'].idxmin()]

    city = data.groupby(['City']).agg({'Total Funding': ['min', 'max', 'mean']}).reset_index()
    city.columns = ['Город', 'Минимальное финансирование', 'Максимальное финансирование', 'Среднее финансирование']
    city['Среднее финансирование'] = city['Среднее финансирование'].apply(lambda x: round(x, 2))
    city_max = city.loc[city['Среднее финансирование'].idxmax()]
    city_min = city.loc[city['Среднее финансирование'].idxmin()]

    return render_template("base.html") \
        + html.format(min=data['Total Funding'].min(), max=data['Total Funding'].max()) \
        + html_task1.format(task=task1,
                            min=country_min['Страна'],
                            max=country_max['Страна'],
                            max_res=country_max['Среднее финансирование'],
                            min_res=country_min['Среднее финансирование'],
                            category=country.to_html(
                                classes='table-sm table align-middle table-bordered', justify='center')) \
        + html_task2.format(task=task2,
                            min=founded_year_min['Год основания'],
                            max=founded_year_max['Год основания'],
                            max_res=founded_year_max['Среднее финансирование'],
                            min_res=founded_year_min['Среднее финансирование'],
                            sub_category=founded_year.to_html(
                                classes='table-sm table autofit align-middle table-bordered', justify='center')) \
        + html_task3.format(task=task3,
                            min=number_of_employees_min['Количество служащих'],
                            max=number_of_employees_max['Количество служащих'],
                            max_res=number_of_employees_max['Среднее финансирование'],
                            min_res=number_of_employees_min['Среднее финансирование'],
                            sub_category=number_of_employees.to_html(
                                classes='table-sm table autofit align-middle table-bordered', justify='center')) \
        + html_task4.format(task=task4,
                            min=city_min['Город'],
                            max=city_max['Город'],
                            max_res=city_max['Среднее финансирование'],
                            min_res=city_min['Среднее финансирование'],
                            sub_category=city.to_html(
                                classes='table-sm table autofit align-middle table-bordered', justify='center'))


if __name__ == '__main__':
     app.run(debug=True, threaded=True)

