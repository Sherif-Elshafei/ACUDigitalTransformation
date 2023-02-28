from odoo import models, fields, api, exceptions

class locations_types(models.Model):
    _name = "locations_types"
    _rec_name = "name_en"
    name_en = fields.Char()
    name_ar = fields.Char()
