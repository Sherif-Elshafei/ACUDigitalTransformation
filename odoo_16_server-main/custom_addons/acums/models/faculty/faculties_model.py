from odoo import models, fields, api, exceptions

class faculties(models.Model):
    _name = "faculties"
    _rec_name = "name_ar"
    _description = ""
    code = fields.Integer()
    name_en = fields.Char()
    name_ar = fields.Char()
    receipts_counter = fields.Integer()
    levels = fields.Integer()

