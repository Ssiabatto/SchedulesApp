from marshmallow import Schema, fields

class VigilanteSchema(Schema):
    id = fields.Int(required=True)
    nombre = fields.Str(required=True)
    documento_identidad = fields.Str(required=True)
    habilidades = fields.List(fields.Str(), required=False)
    certificaciones = fields.List(fields.Str(), required=False)

class TurnoSchema(Schema):
    id = fields.Int(required=True)
    vigilante_id = fields.Int(required=True)
    edificio_id = fields.Int(required=True)
    fecha_inicio = fields.DateTime(required=True)
    fecha_fin = fields.DateTime(required=True)

class EdificioSchema(Schema):
    id = fields.Int(required=True)
    nombre = fields.Str(required=True)
    direccion = fields.Str(required=True)
    telefono = fields.Str(required=False)