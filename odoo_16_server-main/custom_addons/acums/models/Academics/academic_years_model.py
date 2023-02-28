from odoo import models, fields, api, exceptions
class academic_years(models.Model):
    _name = "academic_years"
    _rec_name = "code"
    _description = ""
    code = fields.Char()
    start_year = fields.Integer()
    end_year = fields.Integer()
    is_current = fields.Boolean()
    # is_enrollment = fields.Boolean(default=False)

