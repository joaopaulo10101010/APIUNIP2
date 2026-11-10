class Aluno:

    def __init__(self, id=None, nome="", email="", curso=""):
        self.id = id
        self.nome = nome
        self.email = email
        self.curso = curso

    def resumo(self):
        return f"{self.nome} - {self.curso}"
    
    def __str__(self):
            return self.resumo()