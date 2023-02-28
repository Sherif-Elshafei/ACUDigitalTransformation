from odoo import models, fields, api, exceptions

class countries(models.Model):
    _name = "countries"
    _description = ""
    _rec_name = "name_ar"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    nationality_name_en = fields.Char()
    nationality_name_ar = fields.Char()
#