import datetime
from flask import  jsonify
from F_taste_common.db import get_session
from F_taste_common.repositories.QA_repository import QARepository
from F_taste_common.schemas.QA import QASchema
from F_taste_common.models.QA import QA
from F_taste_common.utils.jwt_token_factory import JWTTokenFactory
from F_taste_common.utils.redis import get_redis_connection

qa_schema = QASchema(only=[
    'categoria',
    'domanda',
    'risposta',
    'discriminante'
])

jwt_factory = JWTTokenFactory()

ACCESS_EXPIRES = datetime.timedelta(hours=1)

class CommonService:

    @staticmethod
    def server_status():
        return 200
    
    @staticmethod
    def refresh(claims,identity):
        return {"access_token": jwt_factory.create_access_token(identity, claims['role'])}, 200
    
    @staticmethod
    def logout(token,jti,ttype):
        get_redis_connection().set(jti, "", ex= ACCESS_EXPIRES)

        # Returns "Access token revoked" or "Refresh token revoked"
        return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


    @staticmethod
    def addQA(new_question):
        session=get_session("admin")
        # Eseguiamo un load
        domanda = qa_schema.load(new_question)
        QARepository.add(domanda,session)
        session.close()
        # Ritorniamo un messaggio di conferma
        return {"message" : "Domanda aggiunta con successo"}, 201


    @staticmethod
    def getQA(role):
        session=get_session(role)
         # In base al tupo di utente facciamo un rirorno specifico delle QA
        if role == "patient":
            questions=QARepository.get_questions_for_user(discriminant=1,session=session)
            session.close()
            return CommonService.createStructure(questions)
        
        elif role == "dietitian":
            questions=QARepository.get_questions_for_user(discriminant=0,session=session)
            return CommonService.createStructure(questions)
        
    
    @staticmethod
    def createStructure(questions):
    
        # Liste per le singole categorie
        generiche = []
        specifiche = []
        privacy = []
        supporto = []
        tecniche = []

        for question in questions:
            # Si crea il blocco della domanda
            block = {
                "question" : question.domanda,
                "risposta" : question.risposta
            }

            # Sulla base della categoria viene aggiunto il blocco alla lista giusta
            if question.categoria == "Domande Generiche su Funzionalità dell App":
                generiche.append(block)
            elif question.categoria == "Domande su Privacy e Sicurezza":
                privacy.append(block)
            elif question.categoria == "Domande su Funzionalità Specifiche":
                specifiche.append(block)
            elif question.categoria == "Domande su Supporto e Assistenza":
                supporto.append(block)
            elif question.categoria == "Domande Tecniche":
                tecniche.append(block)

        # Lista di tutte le domande
        faqs = []

        faqs.append({"category" : "Domande Generiche su Funzionalità dell App", "questions" : generiche})
        faqs.append({"category" : "Domande su Privacy e Sicurezza", "questions" : privacy})
        faqs.append({"category" : "Domande su Funzionalità Specifiche", "questions" : specifiche})
        faqs.append({"category" : "Domande su Supporto e Assistenza", "questions" : supporto})
        faqs.append({"category" : "Domande Tecniche", "questions" : tecniche})

        # Ritorniamo la strutruttura così creata con lo status code 200
        return faqs, 200