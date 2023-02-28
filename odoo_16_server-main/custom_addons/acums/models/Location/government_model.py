from odoo import models, fields, api, exceptions

class governorates(models.Model):
    _name = "governorates"
    _description = ""
    _rec_name = "name_ar"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
