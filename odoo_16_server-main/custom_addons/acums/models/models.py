# -*- coding: utf-8 -*-


#in every field it should include an string name.

from odoo import models, fields, api, exceptions
from datetime import date
from datetime import datetime
from num2words import num2words
from random import randint
<<<<<<< HEAD
=======

class academic_years(models.Model):
    _name = "academic_years"
    _rec_name = "code"
    _description = ""
    code = fields.Char()
    start_year = fields.Integer()
    end_year = fields.Integer()
    is_current = fields.Boolean()
    # is_enrollment = fields.Boolean(default=False)




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

class faculties(models.Model):
    _name = "faculties"
    _rec_name = "name_ar"
    _description = ""
    code = fields.Integer()
    name_en = fields.Char()
    name_ar = fields.Char()
    receipts_counter = fields.Integer()
    levels = fields.Integer()



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



#for nantionalities
class countries(models.Model):
    _name = "countries"
    _description = ""
    _rec_name = "name_ar"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    nationality_name_en = fields.Char()
    nationality_name_ar = fields.Char()


class governorates(models.Model):
    _name = "governorates"
    _description = ""
    _rec_name = "name_ar"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()

#
class locations_types(models.Model):
    _name = "locations_types"
    _rec_name = "name_en"
    name_en = fields.Char()
    name_ar = fields.Char()


class locations(models.Model):
    _name = "locations"
    _rec_name = "code"
    faculty = fields.Many2one("faculties")
    code = fields.Char()
    type = fields.Many2one("locations_types")
    capacity = fields.Integer()
    biometric_device_ip = fields.Char()

class students(models.Model):
    _name = "students"
    _rec_name = "code"
    academic_id = fields.Char(string="Academic Id")
    code = fields.Char(string="Student Code")
    student_type = fields.Selection([("new", "New"), ("transfer", "Transfer")])
    admission_semester = fields.Many2one("academic_semesters")
    name_ar = fields.Char(string="name arabic")
    name_en = fields.Char(string="name english")
    date_of_birth = fields.Date(string="date of birth")
    nationality = fields.Many2one("countries", string="student nationality")
    place_of_birth = fields.Many2one("countries", string="Place Of Birth")
    national_id = fields.Char(string="National Id")
    passport_no = fields.Char(string="passport Number")
    gender = fields.Selection([("male", "Male"),("female","Female")], string="Gender")
    religion = fields.Selection([("muslim","Muslim"), ("christian","Christian"), ("nonreligious","Non-Religious")],)
    address = fields.Char(string="Address")
    country = fields.Many2one("countries",string = "Address Country")
    governorate = fields.Many2one("governorates")
    mobile_no = fields.Char(string="Mobile Number")
    phone_no = fields.Char(string="Phone Number")
    email = fields.Char(string="E-Mail")
    #mailing address
    building_no = fields.Char(string="Building Number")
    floor_number = fields.Char(string="Floor Number")
    street_name = fields.Char(string="Street Name")
    district_name = fields.Char(string="District Name")
    faculty_choices = fields.Many2many("faculties",string="Factulties of interest")

    #prior education
    highschool_certificate_country = fields.Many2one("countries",string="Country of high school certificate")
    Diploma_Type = fields.Selection([("thanaweya_aama", "Thanaweya Aama"),("IGCSE","IGCSE"),("SAT","SAT"),("non-egyptian","Non-Egyptian")])
    school_name = fields.Char(string="School Name")
    highschool_graduation_year = fields.Char(string="Year Graduated from HighSchool")
    high_school_section = fields.Selection([("science","Science"),("math","Math"),("litrture","Litrature")])
    percentage = fields.Integer(string="Percentage (without %)")
    seating_number = fields.Integer(string="Seating Number")

    #external students
    university = fields.Char(string="University")
    faculty = fields.Char(string="Faculty")
    no_of_semesters = fields.Integer(string="No Of Semesters Attended")
    gpa = fields.Integer(string="Cumulative GPA")

    #guardian_info
    father_state = fields.Selection([("alive", "Alive"), ("passed_away","Passed Away")])
    mother_state = fields.Selection([("alive", "Alive"), ("passed_away","Passed Away")])
    father_number = fields.Char(string="Father Number")
    father_position = fields.Char(string="Father Position")
    father_company = fields.Char(string="Father Company")
    father_email = fields.Char(string="Father E-Mail")
    mother_number = fields.Char(string="Mother Number")
    mother_position = fields.Char(string="Mother Position")
    mother_company = fields.Char(string="Mother Company")
    mother_email = fields.Char(string="Mother E-Mail")

    student_state = fields.Selection([("willing", "Willing"), ("applicant", "Applicant"), ("student", "Student"), ("alumini", "Alumini"), ("withdrawn", "Withdrawn")])
    finance_account = fields.Many2one(comodel_name='students_finance_account', inverse_name='student', string='finance_account')
    @api.onchange("father_state")
    def _onchange_father_state(self):
        if self.father_state == "passed_away":
            self.father_email = ""
            self.father_company = ''
            self.father_number = ''
            self.father_position = ''

    @api.onchange("mother_state")
    def _onchange_mother_state(self):
        if self.mother_state == "passed_away":
            self.mother_email = ""
            self.mother_company = ''
            self.mother_number = ''
            self.mother_position = ''

    #@api.model
    #def create(self,vals):
   #     old = self.env['students'].search([("code", "=", vals['code'])])
    #    print(old)
    #    if vals['student_state'] == 'student' and old['code'] == 'applicant':
    #        self.env["student_finance_account"].create({"nationalId": self.national_id,'student': self.code})
    #        print("HERE")

    #    return super(students, self).create(vals)

    def write(self, vals):
        if vals['student_state'] == 'student':
            print(self.code)
            test = self.env["students_finance_account"].create({"national_id": self.national_id, "student": self.id})
            vals['finance_account'] = test.id
        return super(students, self).write(vals)


class students_finance_account(models.Model):
    _name = "students_finance_account"
    _description = ""
    _rec_name = "student"
    active = fields.Boolean(default=True, string="Is Active")
    student= fields.Many2one("students", string="student_id")
    national_id = fields.Char( string="National Id")
    current_balance = fields.Float(string="Current Balance")
    account_total_debts = fields.Integer(string="Student Debts")
    dont_send = fields.Boolean()
>>>>>>> bcfde15a5d67d39eb50ec8c0fab75e188bf1e40d
