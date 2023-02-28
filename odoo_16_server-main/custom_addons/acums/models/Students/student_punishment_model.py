from odoo import models, fields, api, exceptions
from odoo.tools.populate import randint

class students_punishments(models.Model):
    _name = "students_punishments"
    _description = ""
    student = fields.Many2one("students", string="Student")
    semester = fields.Many2one("academic_semesters", string="Semester")
    number = fields.Integer(string="Number")
    date = fields.Date(string="Date")
    case = fields.Text(string="Case")
    punishment = fields.Many2many("punishments", string="Punishments")

