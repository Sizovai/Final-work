from flask import Flask, render_template, app, request, redirect, url_for
import fp_recs

app = Flask(__name__)

recommendations = []

@app.route('/', methods=['GET', 'POST'])
def base():
    global recommendations
    if request.method == 'POST':
        salary_from = request.form['salary_from']
        salary_to = request.form['salary_to']
        print('%s..%s' % (salary_from, salary_to))
        if(len(salary_from) == 0):
            return render_template('error.html', error_msg = 'Не указан начальный уровень зарплаты')
        if(len(salary_to) == 0):
            return render_template('error.html', error_msg = 'Не указан верхний уровень зарплаты')
        if(int(salary_from) < 18000):
            return render_template('error.html', error_msg = 'Начальный уровень зарплаты ниже минимальной')
        if(int(salary_to) < int(salary_from)):
            return render_template('error.html', error_msg = 'Верхний уровень зарплаты ниже начального')
        recs = fp_recs.get_recs(salary_from, salary_to)
        recommendations.clear()
        for rec in recs:
            recommendations.append(rec)
        print('res size %d' % len(recs))
        return redirect(url_for('recomendations'))
    return render_template('base.html')

@app.route('/rec')
def recomendations():
    return render_template('recomendations.html', recs=recommendations)


if __name__ == '__main__':
    app.run()
