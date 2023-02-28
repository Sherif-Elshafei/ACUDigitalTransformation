from odoo import models, fields, api, exceptions
class locations(models.Model):
    _name = "locations"
    _rec_name = "code"
    faculty = fields.Many2one("faculties")
    code = fields.Char()
    type = fields.Many2one("locations_types")
    capacity = fields.Integer()
    biometric_device_ip = fields.Char()
