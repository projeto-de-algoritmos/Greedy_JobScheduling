from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

funcionarios = []
tarefas = []

@app.route('/')
def index():
    return render_template('index.html', agendamento=agendar_tarefas(funcionarios, tarefas))

@app.route('/adicionar_funcionario', methods=['GET', 'POST'])
def adicionar_funcionario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        carga_de_trabalho = int(request.form.get('carga_de_trabalho'))
        funcionarios.append({'nome': nome, 'carga_de_trabalho': carga_de_trabalho})
        return redirect(url_for('index'))
    return render_template('funcionarios.html')

@app.route('/adicionar_tarefa', methods=['GET', 'POST'])
def adicionar_tarefa():
    if request.method == 'POST':
        nome = request.form.get('nome')
        carga_de_trabalho = int(request.form.get('carga_de_trabalho'))
        tarefas.append({'nome': nome, 'carga_de_trabalho': carga_de_trabalho})
        return redirect(url_for('index'))
    return render_template('tarefas.html')

def agendar_tarefas(funcionarios, tarefas):
    funcionarios_ordenados = sorted(funcionarios, key=lambda x: x['carga_de_trabalho'])
    agendamento = []

    for tarefa in tarefas:
        funcionario_disponivel = None
        for funcionario in funcionarios_ordenados:
            if funcionario['carga_de_trabalho'] >= tarefa['carga_de_trabalho']:
                funcionario_disponivel = funcionario
                break

        if funcionario_disponivel:
            agendamento.append({
                'tarefa': tarefa,
                'funcionario': funcionario_disponivel['nome']
            })
            funcionario_disponivel['carga_de_trabalho'] -= tarefa['carga_de_trabalho']

    return agendamento

if __name__ == '__main__':
    app.run()
