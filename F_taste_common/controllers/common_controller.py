import datetime
from flask import request,jsonify, current_app
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restx import Resource, fields
from F_taste_common.services.common_service import CommonService
from F_taste_common.namespaces import common_ns,admin_ns,paziente_ns,nutrizionista_ns


from F_taste_common.utils.jwt_custom_decorators import NoAuthorizationException,admin_required




inserimento_domanda = admin_ns.model("Domanda ai faq da aggiungere", {
    "categoria" : fields.String(required = True),
    "domanda" : fields.String(required = True),
    "risposta" : fields.String(required = True),
    "discriminante" : fields.Integer(required = True)
}, strict = True )

class ServerStatus(Resource):
    def get(self):
        return CommonService.server_status()
    
class AccessTokenRefresher(Resource):

    

    @jwt_required(refresh=True)
    def get(self):
        claims = get_jwt()
        identity = get_jwt_identity()
        return CommonService.refresh(claims,identity)
    


class Logout(Resource):
    

    @jwt_required(verify_type=False)
    def post(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        return CommonService.logout(token,jti,ttype)


#da fare QA o qui o servizio separato


class QA(Resource):

    possibili_categorie = (
        "Domande Generiche su Funzionalità dell App",
        "Domande su Privacy e Sicurezza",
        "Domande su Funzionalità Specifiche",
        "Domande su Supporto e Assistenza",
        "Domande Tecniche"
    )

    # Questo metodo restituisce una struttura contenente tutte le domande attualmente conservate nel database
    # Sono divise per categoria nella struttura "question" : "answer"
    @jwt_required()
    def get(self):

        # Estraiamo il ruolo di chi ha fatto la richiesta
        role = get_jwt()['role']
        return CommonService.getQA(role)
        

    # COn il metoo post possiamo agigungere nuove domande all'interno del database
    @admin_required()
    @admin_ns.expect(inserimento_domanda)
    def post(self):

        new_question = request.get_json()

        # Validazione
        validation_errors = inserimento_domanda.validate(new_question)
        if validation_errors:
            return validation_errors, 400
        
        # Se la categoria inviata non corrisponde ad una categoria valida viene gestito il caso
        # Segnalandolo all'utente
        if new_question["categoria"] not in self.possibili_categorie :
            tmp = new_question["categoria"]
            return {"message" : f"La categoria {tmp} non è una categoria valida. Categorie valide = {self.possibili_categorie}."}, 404
        
        return CommonService.addQA(new_question)






