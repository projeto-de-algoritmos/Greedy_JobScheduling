from flask import Flask, request ,render_template

app = Flask(__name__)

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
                    'funcionario': funcionario_disponivel['Nome']
                })
                funcionario_disponivel['carga_de_trabalho'] -= tarefa['carga_de_trabalho']

        return agendamento

@app.route('/')
def index():

    # Renderize o template e retorne a saída HTML
    return render_template('template.html')

@app.route('/next-step', methods=['POST'])
def renderNextStep():
        qtdTarefas = int(request.form.get('qtd-tarefas'))
        qtdFuncionarios = int(request.form.get('qtd-funcionarios'))
        funcionarios = []

        for i in range(0, qtdFuncionarios):
           funcionarios.append(i)  

        tarefas = []

        for i in range(0, qtdTarefas):
           tarefas.append(i)  

       
        return render_template('nextStep.html',  funcionarios=funcionarios, tarefas=tarefas)


@app.route('/render-result', methods=['POST'])
def renderResult():
    funcionarios = []
    tarefas = []
    for chave, valor in request.form.to_dict().items():
        if ('funcionario' in chave):    
            funcionarios.append({'Nome': chave,'carga_de_trabalho': int(valor) })
        if ('tarefa' in chave):    
            tarefas.append({'Nome': chave,'carga_de_trabalho': int(valor) })
            
    result=agendar_tarefas(funcionarios, tarefas)
   
    
    return render_template('result.html',  result=result)

if __name__ == '__main__':
    app.run()
