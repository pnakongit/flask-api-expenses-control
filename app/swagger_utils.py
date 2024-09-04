from flask_swagger import swagger


def build_swagger(app) -> dict:
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    swag["definitions"] = {
        "ExpenseIn": {
            "type": "object",
            "discriminator": "ExpenseIn",
            "description": "Create an expense",
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "title": {"type": "string", "required": True},
            },
            "example": {
                "title": "My Expense",
            }
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "description": "Return information about an expense",
                    "example": {
                        "id": 2,
                    }
                }
            ]
        }
    }
    return swag
