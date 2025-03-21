from F_taste_common.ma import ma
from marshmallow import fields
from F_taste_common.models.QA import QA

class QASchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = QA
        load_instance = True
        # sqla_session = db.session

    categoria = fields.String(required=True)
    domanda = fields.String(required=True)
    risposta = fields.String(required=True)
    discriminante = fields.Integer()