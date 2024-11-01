from config import db
from .professor_model import Professor

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100))
    professor_id = db.Column(db.Integer,  db.ForeignKey('professores.id'))
    ativo = db.Column(db.String(1)) 
    
    alunos = db.relationship('Aluno', back_populates='turma', cascade="all, delete-orphan")
    professor = db.relationship('Professor', back_populates='turmas')
    

    def __init__(self, descricao, professor_id, ativo):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo
       
    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'professor_id': self.professor_id,
            'ativo': self.ativo,
    
        }

class TurmaNaoEncontrado(Exception):
    pass

def turma_por_id(id_aluno):
    turma = Turma.query.get(id_aluno)
    if not turma:
        raise TurmaNaoEncontrado
    return turma.to_dict()

def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def adicionar_turma(turma_data):
    nova_turma = Turma(
        descricao=turma_data['descricao'],
        professor_id=turma_data['professor_id'],
        ativo=turma_data.get('ativo', 'S'),  
        
    )
    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrado

    turma.descricao = novos_dados.get('descricao', turma.descricao)  # Atualizar se houver novo nome
    turma.professor_id = novos_dados.get('professor_id', turma.professor_id)  # Atualizar se houver nova turma
    turma.ativo = novos_dados.get('ativo', turma.ativo)  # Atualizar se houver nova idade
   
    db.session.commit()

def excluir_turma(id_aluno):
    turma = Turma.query.get(id_aluno)
    if not turma:
        raise TurmaNaoEncontrado
    db.session.delete(turma)
    db.session.commit()