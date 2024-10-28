from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from model.alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno


alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def getIndex():
    return "Meu index"

## ROTA PARA TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("alunos.html", alunos=alunos)

## ROTA PARA UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA ACESSAR O FORMULARIO DE CRIAÇÃO DE UM NOVO ALUNOS   
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('criarAlunos.html')

## ROTA QUE CRIA UM NOVO ALUNO
@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    aluno_data = {
        'nome': request.form['nome'],
        'idade': request.form.get('idade', type=float),  # Use get para converter para float
        'turma_id': request.form['turma_id'],
        'dt_nasc': request.form['dt_nasc'],  # Certifique-se de que a data esteja no formato correto
        'nt_primeiro_semestre': request.form.get('nt_primeiro_semestre', type=float),
        'nt_segundo_semestre': request.form.get('nt_segundo_semestre', type=float)
    }
    adicionar_aluno(aluno_data)
    return redirect(url_for('alunos.get_alunos'))

## ROTA PARA O FORMULARIO PARA EDITAR UM NOVO ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA QUE EDITA UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT',"POST"])
def update_aluno(id_aluno):
        print("Dados recebidos no formulário:", request.form)
        try:
            aluno = aluno_por_id(id_aluno)
            aluno_data = {
                'nome': request.form['nome'],
                'idade': request.form.get('idade', type=float),
                'turma_id': request.form['turma_id'],
                'dt_nasc': request.form['dt_nasc'],
                'nt_primeiro_semestre': request.form.get('nt_primeiro_semestre', type=float),
                'nt_segundo_semestre': request.form.get('nt_segundo_semestre', type=float)
            }
            atualizar_aluno(id_aluno, aluno_data)  # Passar os novos dados do aluno
            return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
   
## ROTA QUE DELETA UM ALUNO
@alunos_blueprint.route('/alunos/delete/<int:id_aluno>', methods=['DELETE','POST'])
def delete_aluno(id_aluno):
        try:
            excluir_aluno(id_aluno)
            return redirect(url_for('alunos.get_alunos'))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
        
  