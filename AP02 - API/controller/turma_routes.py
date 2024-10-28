from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from model.turma_model import TurmaNaoEncontrado, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma


turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/', methods=['GET'])
def getIndex():
    return "Meu index"

## ROTA PARA TODOS OS ALUNOS
@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template("turmas.html", turmas=turmas)

## ROTA PARA UM ALUNO
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turmas_id.html', turma=turma)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrado'}), 404
    


 ## ROTA ACESSAR O FORMULARIO DE CRIAÇÃO DE UM NOVO ALUNOS   
@turmas_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('criarTurmas.html')

## ROTA QUE CRIA UM NOVO ALUNO
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turmas():
    turma_data = {
        'descricao': request.form['descricao'],
        'professor': request.form.get('professor', type=float),  # Use get para converter para float
        'ativo': request.form['ativo'],
    
    }
    adicionar_turma(turma_data)
    return redirect(url_for('turmas.get_turmas'))

## ROTA PARA O FORMULARIO PARA EDITAR UM NOVO ALUNO
@turmas_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma_update.html', turma=turma)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404


## ROTA QUE EDITA UM ALUNO
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT',"POST"])
def update_turma(id_turma):
        print("Dados recebidos no formulário:", request.form)
        try:
            turma = turma_por_id(id_turma)
            turma_data = {
                'descricao': request.form['descricao'],
                'professor': request.form.get('professor', type=float),
                'ativo': request.form['ativo'],
            }
            atualizar_turma(id_turma, turma_data)  # Passar os novos dados do aluno
            return redirect(url_for('turmas.get_turma', id_turma=id_turma))
        except TurmaNaoEncontrado:
            return jsonify({'message': 'Turma não encontrada'}), 404
 

## ROTA QUE DELETA UM ALUNO

@turmas_blueprint.route('/turmas/delete/<int:id_turma>', methods=['DELETE','POST'])
def delete_turma(id_turma):
        try:
            excluir_turma(id_turma)
            return redirect(url_for('turmas.get_turmas'))
        except TurmaNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
        
