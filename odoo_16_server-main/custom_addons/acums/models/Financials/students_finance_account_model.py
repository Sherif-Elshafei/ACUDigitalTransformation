from odoo import models, fields, api, exceptions
class students_finance_account(models.Model):
    _name = "students_finance_account"
    _description = ""
    _rec_name = ""
    active = fields.Boolean(default=True, string="Is Active")
    #student = fields.Many2one("students", string="student_id")
    national_id = fields.Char( string="National Id")
    current_balance = fields.Float(string="Current Balance")
    account_total_debts = fields.Integer(string="Student Debts")
    dont_send = fields.Boolean()
