from odoo import models, fields, api, exceptions
from odoo.tools.populate import randint

class punishments(models.Model):
    _name = "punishments"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    details=fields.Text()
