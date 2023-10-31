from flask import Flask, render_template, request, redirect, url_for
import copy

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
        prazo = request.form.get('prazo')
        tarefas.append({'nome': nome, 'carga_de_trabalho': carga_de_trabalho, 'prazo': prazo})
        return redirect(url_for('index'))
    return render_template('tarefas.html')

@app.route('/relatorio')
def gerar_relatorio():
    relatorio_funcionarios = copy.deepcopy(funcionarios)
    relatorio_tarefas = copy.deepcopy(tarefas)
    return render_template('relatorio.html', funcionarios=relatorio_funcionarios, tarefas=relatorio_tarefas)

def agendar_tarefas(funcionarios, tarefas):
    tarefas_ordenadas = sorted(tarefas, key=lambda x: x['prazo'])
    funcionarios_ordenados = sorted(funcionarios, key=lambda x: x['carga_de_trabalho'])
    agendamento = []

    for tarefa in tarefas_ordenadas:
        funcionario_disponivel = None
        for funcionario in funcionarios_ordenados:
            if funcionario['carga_de_trabalho'] >= tarefa['carga_de_trabalho']:
                funcionario_disponivel = funcionario
                break

        if funcionario_disponivel:
            agendamento.append({
                'tarefa': tarefa,
                'funcionario': funcionario_disponivel['nome'],
            })
            funcionario_disponivel['carga_de_trabalho'] -= tarefa['carga_de_trabalho']

    return agendamento

if __name__ == '__main__':
    app.run()
