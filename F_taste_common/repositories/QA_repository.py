from F_taste_common.models.QA import QA
from F_taste_common.db import get_session
from sqlalchemy.exc import SQLAlchemyError

class QARepository:

    @staticmethod
    def get_all_QA(session=None):
        session = session or get_session('patient')
        return session.query(QA).all()

    @staticmethod
    def get_question_for_category(category, session=None):
        session = session or get_session('patient')
        return session.query(QA).filter_by(categoria=category).all()

    @staticmethod
    def get_questions_for_user(discriminant, session=None):
        session = session or get_session('patient')
        return session.query(QA).filter_by(discriminante=discriminant).all()    
    
    @staticmethod
    def add(domanda, session=None):
        session = session or get_session('patient')
        session.add(domanda)
        session.commit()
