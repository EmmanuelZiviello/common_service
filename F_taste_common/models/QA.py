from F_taste_common.db import Base
from sqlalchemy import Column, Integer, String, Boolean

# Questa classe rappresenta la tabella contenente tutti i log riguardo all'accettazione dei consensi da parte degli utenti

class QA(Base):
    
    __tablename__ = "qa"

    id_qa = Column(Integer, primary_key=True)
    categoria = Column(String(500), nullable=False)
    domanda = Column(String(1000), nullable=False)
    risposta = Column(String(1000), nullable=False)
    # Il discriminante serve a definire se sono domande per i dietologi o se lo sono per i pazienti
    discriminante = Column(Integer, nullable = False)

    def __repr__(self):
        return " categoria: {0}, domanda :{1}, risposta :{2}".format(self.categoria, self.domanda, self.risposta)

    def __init__(self, categoria, domanda, risposta, discriminante):
        self.categoria = categoria
        self.domanda = domanda
        self.risposta = risposta
        self.discriminante = discriminante

    def __repr__(self):
        return 'QA(id_qa=%s, categoria=%s, domanda=%s, risposta=%s)' % (self.id_qa, self.categoria, self.domanda, self.risposta)

    def __json__(self):
        return { 'id_qa': self.id_qa, 'categoria': self.categoria, 'domanda': self.domanda, 'risposta': self.risposta, 'discriminante' : self.discriminante }
    
    