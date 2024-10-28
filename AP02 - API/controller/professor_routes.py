from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from model.professor_model import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor


professores_blueprint = Blueprint('professores', __name__)

@professores_blueprint.route('/', methods=['GET'])
def getIndex():
    return "Meu index"

## ROTA PARA TODOS OS ALUNOS
@professores_blueprint.route('/professores', methods=['GET'])
def get_professores():
    professores = listar_professores()
    return render_template("professores.html", professores=professores)

## ROTA PARA UM ALUNO
@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professores_id.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
    


 ## ROTA ACESSAR O FORMULARIO DE CRIAÇÃO DE UM NOVO ALUNOS   
@professores_blueprint.route('/professores/adicionar', methods=['GET'])
def adicionar_professor_page():
    return render_template('criarProfessor.html')

## ROTA QUE CRIA UM NOVO ALUNO
@professores_blueprint.route('/professores', methods=['POST'])
def create_professores():
    professor_data = {
        'nome': request.form['nome'],
        'idade': request.form.get('idade', type=int),  # Use get para converter para float
        'materia': request.form['materia'],
        'observacoes': request.form['observacoes'],
   
    
    }
    adicionar_professor(professor_data)
    return redirect(url_for('professores.get_professores'))


## ROTA PARA O FORMULARIO PARA EDITAR UM NOVO ALUNO
@professores_blueprint.route('/professores/<int:id_professor>/editar', methods=['GET'])
def editar_professor_page(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professor_update.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrada'}), 404


## ROTA QUE EDITA UM ALUNO
@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT',"POST"])
def update_professor(id_professor):
        print("Dados recebidos no formulário:", request.form)
        try:
            professor = professor_por_id(id_professor)
            professor_data = {
               'nome': request.form['nome'],
               'idade': request.form.get('idade', type=int),  # Use get para converter para float
               'materia': request.form['materia'],
               'observacoes': request.form['observacoes']
   
            }
            atualizar_professor(id_professor, professor_data)  # Passar os novos dados do aluno
            return redirect(url_for('professores.get_professor', id_professor=id_professor))
        except ProfessorNaoEncontrado:
            return jsonify({'message': 'Professor não encontrado'}), 404
 

@professores_blueprint.route('/professores/delete/<int:id_professor>', methods=['DELETE','POST'])
def delete_professor(id_professor):
        try:
            excluir_professor(id_professor)
            return redirect(url_for('professores.get_professores'))
        except ProfessorNaoEncontrado:
            return jsonify({'message': 'Professor não encontrado'}), 404 
        
