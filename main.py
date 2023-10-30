from jinja2 import Environment, FileSystemLoader

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

funcionarios = [
    {'nome': 'Funcionario1', 'carga_de_trabalho': 30},
    {'nome': 'Funcionario2', 'carga_de_trabalho': 20},
    {'nome': 'Funcionario3', 'carga_de_trabalho': 40},
]

tarefas = [
    {'nome': 'Tarefa1', 'carga_de_trabalho': 25},
    {'nome': 'Tarefa2', 'carga_de_trabalho': 15},
    {'nome': 'Tarefa3', 'carga_de_trabalho': 35},
]

agendamento = agendar_tarefas(funcionarios, tarefas)

# Configurar o ambiente Jinja2 para carregar templates de um diretório
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Renderizar o template com os dados
html_output = template.render(agendamento=agendamento)


with open('saida.html', 'w') as output_file:
    output_file.write(html_output)
