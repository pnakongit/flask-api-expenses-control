from marshmallow import Schema, fields, validate


class ExpenseSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))


expense_schema = ExpenseSchema()
