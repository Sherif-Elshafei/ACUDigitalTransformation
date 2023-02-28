from odoo import models, fields, api, exceptions
class academic_semesters(models.Model):
    _name = "academic_semesters"
    _rec_name = "code"
    _description = ""
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    year = fields.Many2one("academic_years")
    type = fields.Selection([("fall", "Fall"), ("spring", "Spring"), ("summer", "Summer")])
    graduation_month = fields.Selection([("february", "February"), ("july", "July"), ("september", "September")])
    is_current = fields.Boolean("Is Current")
