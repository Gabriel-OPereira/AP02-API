from config import db

class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100)) # adicionar foreign key
    observacoes = db.Column(db.String(300)) 
     
    turmas = db.relationship('Turma', back_populates='professor')
    
    

    def __init__(self, nome, idade, materia, observacoes ):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes,
    
        }

class ProfessorNaoEncontrado(Exception):
    pass

def professor_por_id(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor.to_dict()

def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def adicionar_professor(professor_data):
    novo_professores = Professor(
        nome=professor_data['nome'],
        idade=professor_data['idade'],
        materia=professor_data.get('materia'),
        observacoes=professor_data.get('observacoes')
        
        
    )
    db.session.add(novo_professores)
    db.session.commit()

def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado

    professor.nome= novos_dados.get('nome', professor.nome)  # Atualizar se houver novo nome
    professor.idade = novos_dados.get('idade', professor.idade)  # Atualizar se houver nova turma
    professor.materia = novos_dados.get('materia', professor.materia)
    professor.observacoes= novos_dados.get('observacoes', professor.observacoes) # Atualizar se houver nova idade
   
    db.session.commit()

def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()