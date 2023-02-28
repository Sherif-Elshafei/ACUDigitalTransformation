from odoo import models, fields, api, exceptions
class faculties_semesters(models.Model):
    _name = "faculties_semesters"
    _rec_name = "code"


    dean = fields.Char(string="Current Dean") # should be ingrated with employee entity
    code = fields.Char(default= lambda self: self.faculty.code+"-"+self.semester.code)
    faculty = fields.Many2one("faculties")
    semester = fields.Many2one("academic_semesters")
    students_academic_ids_counter = fields.Integer()
    exam_approval_date = fields.Date()
    payment_deadline = fields.Date()

