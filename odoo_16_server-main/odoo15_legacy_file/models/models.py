
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import date
from datetime import datetime
from num2words import num2words
from random import randint
import statistics
import pyodbc

class academic_years(models.Model):
    _name = "academic_years"
    _rec_name = "code"
    _description = ""
    code = fields.Char()
    start_year = fields.Integer()
    end_year = fields.Integer()
    is_current = fields.Boolean()
    is_enrollment = fields.Boolean(default=False)

    @api.model
    def make_it_current(self):
        years=self.env['academic_years'].search([])
        for year in years:
            year.is_current = False
            self.is_current=True


class academic_semesters(models.Model):
    _name = "academic_semesters"
    _rec_name = "code"
    _description = ""
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    year = fields.Many2one("academic_years")
    type = fields.Selection([("1", "Fall"), ("2", "Spring"), ("3", "Summer")])
    graduation_month = fields.Selection([("1", "February"), ("2", "July"), ("3", "September")])
    graduation_year = fields.Integer(related="year.end_year")
    exam_approval_date = fields.Date()
    is_current = fields.Boolean()
    payment_deadline = fields.Date()
    payments = fields.One2many('students_payments','semester')

    # def load_debts(self):
    #     accounts=self.env['students_finance_accounts'].search([('status','=','3')])
    #     students_debts=self.env['students_debts'].search([])
    #     semester=self.id
    #     deadline=self.payment_deadline
    #     for account in accounts :
    #         bylaw=account.bylaw.id
    #         debts=self.env['bylaws_debts'].search([('bylaw','=',bylaw),('loading_date','=','2')])
    #         for debt in debts :
    #             student_debt=students_debts.create({'account':account.id , 'debt_type':debt.debt_type.id , 'debt':debt.id, 'semester':semester , 'dead_line': deadline})


class global_data(models.Model):
    _name = "global_data"
    _description = ""
    current_academic_year = fields.Many2one("academic_years")
    current_semester = fields.Many2one("academic_semesters")
    stamp = fields.Binary(string = "Stamp")
    logo = fields.Binary(string = "logo")


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


class faculties(models.Model):
    _name = "faculties"
    _rec_name = "name_ar"
    _description = ""
    code = fields.Integer()
    name_en = fields.Char()
    name_ar = fields.Char()
    receipts_counter = fields.Integer()
    students_academic_ids_counter = fields.Integer()
    postgraduate_students_academic_ids_counter = fields.Char()
    current_financial_bylaw = fields.Many2one("finance_bylaws", string="Financial Bylaw")
    current_financial_bylaw_non_egyptians = fields.Many2one("finance_bylaws", string="Financial Bylaw")
    current_academic_bylaw = fields.Many2one("academic_bylaws", string="Academic Bylaw")
    dean = fields.Char(string="Current Dean")
    payment_deadline = fields.Date()
    levels = fields.Integer()
    semester_payment_amount = fields.Char(string="Semester Payment")



class faculties_semesters(models.Model):
    _name = "faculties_semesters"
    _description = ""
    faculty = fields.Many2one("faculties")
    semester = fields.Many2one("academic_semesters", string="Semester")
    dean = fields.Char(string="Current Dean")
    current_financial_bylaw = fields.Many2one("finance_bylaws", string="Financial Bylaw")
    current_academic_bylaw = fields.Many2one("academic_bylaws", string="Academic Bylaw")
    # bounds = fields.One2many("faculties_acceptance_bounds", "faculty_semester", string="Daily Bounds")
    allowed_students = fields.Integer(string="Number of Allowed Students")


class academic_bylaws(models.Model):
    _name = "academic_bylaws"
    _rec_name = "name_en"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    faculty = fields.Many2one("faculties")
    year = fields.Many2one("academic_years")
    graduation_ch = fields.Integer()
    graduation_gpa = fields.Float()
    courses = fields.One2many("courses", "bylaw")


class faculty_majors(models.Model):
    _name = "faculty_majors"
    _rec_name = "code"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    can_be_major = fields.Boolean()
    can_be_minor = fields.Boolean()
    faculty = fields.Many2one("faculties")
    bylaw = fields.Many2one("academic_bylaws")


class majors_requirements(models.Model):
    __name = "majors_requirements"
    _rec_name="major"
    major = fields.Many2one("faculty_majors")
    course_group = fields.Many2one("course_groups")
    required_ch = fields.Integer()
    required_type = fields.Selection([('1', 'Major'), ('2', 'Minor')])


class course_groups(models.Model):
    _name = "course_groups"
    _rec_name = "name_en"
    code = fields.Char()
    name_ar = fields.Char()
    name_en = fields.Char()
    bylaw = fields.Many2one("academic_bylaws")
    courses = fields.Many2many("courses")


class courses(models.Model):
    _name = "courses"
    _rec_name = "code"
    # course_id=fields.Char()
    faculty = fields.Many2one("faculties")
    bylaw = fields.Many2one("academic_bylaws", domain="[('faculty','=',faculty)]")
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    ch = fields.Float()
    practical_ch = fields.Float()
    description = fields.Text()


class prerequisites(models.Model):
    _name = "prerequisites"
    _rec_name = "course"
    faculty = fields.Many2one("faculties")
    bylaw = fields.Many2one("academic_bylaws", domain="[('faculty','=',faculty)]")
    course = fields.Many2one("courses", domain="[('bylaw','=',bylaw)]")
    prerequisites = fields.Many2many("courses")


class grades_schema(models.Model):
    _name = "grades_schema"
    _rec_name = 'code'
    code = fields.Char()
    grade_assessment = fields.Selection(
        [('0', 'Fail'), ('1', 'Pass'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')])
    bylaw = fields.Many2one("academic_bylaws")
    mark_lower_bound = fields.Float()
    mark_upper_bound = fields.Float()
    gpa = fields.Float()


class offered_courses(models.Model):
    _name = 'offered_courses'
    _rec_name = "course"
    user = fields.Many2one("res.users", default= lambda self: self.env.user)
    academic_staff = fields.Many2one("academic_staff",  domain="[('user','=',user)]")
    faculty = fields.Many2one(related = 'academic_staff.faculty')
    bylaw = fields.Many2one('academic_bylaws', domain = "[('faculty','=',faculty)]")
    course = fields.Many2one('courses', domain = "[('bylaw','=',bylaw)]")
    course_name = fields.Char(related ="course.name_en")
    semester = fields.Many2one('academic_semesters')
    students = fields.One2many('registrations', 'offered_course')
    offered_courses_results = fields.One2many('offered_courses_results', 'offered_course')

    @api.model
    def create(self, values):
        record = super(offered_courses, self).create(values)
        evaluations = self.env['course_evaluations']
        new_evaluation = evaluations.create({'offered_course': record.id, 'type': 'sw'})
        new_evaluation2 = evaluations.create({'offered_course': record.id, 'type': 'final'})
        return record



class offered_courses_results(models.Model):
    _name = 'offered_courses_results'
    _rec_name = 'offered_course'
    user = fields.Many2one("res.users", default=lambda self: self.env.user)
    academic_staff = fields.Many2one("academic_staff", domain=[('user','=',user)])
    faculty = fields.Many2one(related='academic_staff.faculty')
    semester = fields.Many2one('academic_semesters')
    offered_course = fields.Many2one('offered_courses', domain = [('semester','=',semester),('faculty','=',faculty)])
    student = fields.Many2one("students")
    student_name = fields.Char(related='student.name_en')
    semester_work = fields.Float(default=0.0)
    final = fields.Float(default=0.0)
    course = fields.Many2one(related='offered_course.course', store=True)
    total = fields.Float(compute="_compute_result")
    grade = fields.Many2one("grades_schema", compute="_compute_result")
    gpa = fields.Float(related='grade.gpa')
    grade_assessment = fields.Selection(related="grade.grade_assessment")

    @api.depends('semester_work','final')
    def _compute_result(self):
        for record in self:
            record.total = record.semester_work + record.final
            grades_schema = self.env['grades_schema'].search([])
            for grades_record in grades_schema:
                if (record .total >= grades_record.mark_lower_bound) and (record.total < grades_record.mark_upper_bound):
                    record.grade = grades_record









class registrations(models.Model):
    _name = "registrations"
    _rec_name = "student"
    offered_course = fields.Many2one('offered_courses')
    student = fields.Many2one('students')
    student_name = fields.Char(related = 'student.name_en')
    semester = fields.Many2one("academic_semesters", string="Academic Semester",
                                        default=lambda self: self.env['academic_semesters'].search(
                                            [('is_current', '=', True)]))

    @api.model
    def create(self, values):
        record = super(registrations, self).create(values)
        offered_courses_result = self.env['offered_courses_results']
        new_offered_course_result = offered_courses_result.create({'student': record.student.id})

        return record


class course_evaluations(models.Model):
    _name = "course_evaluations"
    _rec_name = "offered_course"
    user = fields.Many2one("res.users", default=lambda self: self.env.user)
    academic_staff = fields.Many2one("academic_staff", domain=[('user', '=', user)])
    semester = fields.Many2one("academic_semesters")
    offered_course = fields.Many2one("offered_courses")
    course = fields.Many2one("courses")
    code = fields.Char()
    name = fields.Char()
    maximum_mark = fields.Float()
    type = fields.Selection([('sw', 'Semester Work'),('final','Final')])
    parent = fields.Selection([('sw', 'Semester Work'),('final','Final')])
    date = fields.Date()
    in_total_mark = fields.Boolean()
    scale = fields.Float()
    marks = fields.One2many('course_evaluations_results','evaluation')

class course_evaluations_result(models.Model):
    _name = "course_evaluations_results"
    _rec_name = "registered_student"
    user = fields.Many2one("res.users", default=lambda self: self.env.user)
    academic_staff = fields.Many2one("academic_staff", domain=[('user', '=', user)])
    faculty = fields.Many2one(related='academic_staff.faculty')
    type = fields.Selection([('sw', 'Semester Work'), ('final', 'Final')])
    semester = fields.Many2one('academic_semesters')
    evaluation = fields.Many2one("course_evaluations", string="Offered Course" , domain = "[('type','=',type)]")
    course = fields.Many2one(related="evaluation.offered_course")
    registered_student = fields.Many2one("registrations", string='Student')
    mark = fields.Float()
    by = fields.Many2one('res.users', default = lambda self: self.env.user)
    on = fields.Date()

    @api.model
    def create(self, values):
        record = super(course_evaluations_result, self).create(values)
        count = self.env['registrations'].search_count([('offered_course','=',record.evaluation.offered_course.id),('student','=',record.registered_student.student.id)])
        if count == 0:
            raise exceptions.ValidationError(record.registered_student.student.student_id + " is unregistered Student")
        record.on = date.today()

        return record

class academic_staff(models.Model):
    _name = "academic_staff"
    _rec_name = 'name_en'
    user = fields.Many2one("res.users")
    faculty = fields.Many2one("faculties")
    name_en = fields.Char()


class academic_staff_courses(models.Model):
    _name = "academic_staff_courses"
    semester = fields.Many2one("academic_semesters")
    offered_courses = fields.Many2one('offered_courses')
    staff = fields.Many2one("academic_staff")
    user = fields.Many2one(related="staff.user", store=True)
    status = fields.Selection([("active", "active"), ("inactive", "inactive")], default="1", string="Status")


class evaluations_types(models.Model):
    _name = 'evaluations_types'
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()


class transcripts(models.Model):
    _name = "transcripts"
    _rec_name = "student"
    student = fields.Many2one("students")
    semester = fields.Many2one("academic_semesters")
    class_work = fields.Float()
    final = fields.Float()
    total_mark = fields.Float()
    grade = fields.Char()
    gpa = fields.Float()


class semester_schedule(models.Model):
    _name = "semester_schedule"
    # _rec_name = "schedule_id"
    # schedule_id=fields.Char(compute='_compute_schedule_id',default=False)
    # semester=fields.Many2one("academic_semesters")
    # faculty=fields.Many2one("faculties")
    # offered_course=fields.One2many("schedule_offered_course","semester_schedule")
    # location=fields.Many2one("locations",domain="[('faculty','=',faculty)]")
    # location_code=fields.Char(related="location.code")
    # day=fields.Many2one("week_days")
    # time=fields.Many2one("time_schema",domain="[('faculty','=',faculty)]")
    # program=fields.Many2one("regulation_programs")
    # start_time=fields.Float(related='time.start')
    # offer_type=fields.Many2one("offer_types")
    # instructor=fields.Many2one("instructors",domain="[('faculty','=',faculty)]")
    # group=fields.Char()
    # section=fields.Char()
    # number_of_seats=fields.Integer()
    # number_of_remaining_seats=fields.Integer()
    # number_of_registrations=fields.Integer(domain="[('faculty','=',faculty)]")
    # level=fields.Integer()
    # students=fields.Many2many('registrations', 'schedule_registrations_rel', 'student', 'schedule_id')

    # _rec_name = "student"
    # student=fields.Many2one("students")
    # student_name=fields.Char(related="student.name_en")
    # image=fields.Binary(related="student.image")
    # student_regulation=fields.Many2one(related="student.academic_regulation")
    # gpa=fields.Float(related="student.student_GPA")
    # ch=fields.Integer(related="student.student_CH")
    # code=fields.Char()
    # # schedule_id=fields.Many2many("semester_schedule",domain="[('offered_course.regulation','=',student_regulation)]")
    # schedule_id=fields.Many2many('semester_schedule', 'schedule_registrations_rel', 'schedule_id', 'student', domain="[('offered_course.regulation','=',student_regulation)]")


class time_schema(models.Model):
    _name = "time_schema"
    _rec_name = "code"
    code = fields.Char()
    faculty = fields.Many2one("faculties")
    start = fields.Float()
    end = fields.Float()
    # code=fields.Char(compute='_compute_time_code')


class students_attendance(models.Model):
    _name = "students_attendance"
    student = fields.Many2one("students")
    # student_id=fields.Char()
    # session=fields.Many2one("semester_schedule")
    # session_type=fields.Char(related="session.offer_type.name_en")
    # session_time=fields.Char(related="session.time.code")
    # session_day=fields.Char(related="session.day.name_en")
    # date=fields.Date()
    # day=fields.Char()class stud
    # time=fields.Char()
    # locations=fields.Many2one("locations")
    # is_registered=fields.Boolean()
    # record_type=fields.Selection([('1','attend'),('2','absent')])


class bus_lines(models.Model):
    _name = "bus_lines"
    _rec_name = "line_name"
    line_number = fields.Integer(string="Line Number")
    line_name = fields.Char(string="Line Name")
    semester = fields.Many2one("academic_semesters", string="Semester")
    bus = fields.Many2one("fleet.vehicle", string="Bus")
    driver = fields.Many2one("hr.employee", string="Driver")
    line_students = fields.One2many("lines_students", "line", string="Bus Students")
    line_points = fields.One2many("lines_points", "line", string="Line Points")


class lines_points(models.Model):
    _name = "lines_points"
    _rec_name = "point_name"
    line = fields.Many2one("bus_lines", string="Line")
    point_name = fields.Char(string="Point Name")
    point_sequence = fields.Integer(string="Point Order")
    point_time = fields.Float(string="Point Time")


class lines_students(models.Model):
    _name = "lines_students"
    _rec_name = "student"
    line = fields.Many2one("bus_lines", string="Bus Line")
    student = fields.Many2one("students", string="Student")
    student_name = fields.Char(related="student.name_ar", string="Student Name")
    student_station = fields.Many2one("lines_points", string="Student Station")
    pickup_time = fields.Float(related="student_station.point_time", string="Pickup Time")
    student_status = fields.Selection([('0', 'Reversed'), ('1', 'Registered'), ('2', 'stopped')], default='0',
                                      string="Status")
    line_type = fields.Selection([('1', 'Inside City'), ('2', 'Outside City'), ('3', 'On the Road')],
                                 string="Line Type")
    subscription_type = fields.Selection([('1', 'Fall'), ('2', 'Spring'), ('3', 'Summer'), ('4', 'Year')],
                                         string="Subscription Type")


class finance_bylaws(models.Model):
    _name = "finance_bylaws"
    _description = ""
    _rec_name = "code"
    code = fields.Char(string="Bylaw Code")
    name_en = fields.Char(string="Bylaw Name EN")
    name_ar = fields.Char(string="Bylaw Name AR")
    faculty = fields.Many2one("faculties")
    year = fields.Many2one("academic_years", string="Year")
    type = fields.Selection([("1", "Egyptians"), ("2", "non-Egyptians")], string="Bylaw Type")
    study_language = fields.Selection([('ar', 'Arabic'), ('en', 'English')], string="Study Language", default="en")
    students = fields.One2many("students", "finance_bylaw", string="Bylaw Students")
    debts = fields.One2many("bylaws_debts", "bylaw", string="Bylaw Debts")
    is_current=fields.Boolean(default=False)
    payments=fields.One2many("bylaws_debts",'bylaw',domain=[('students_debts','=',False)])





class debts_types(models.Model):
    _name = "debts_types"
    _description = ""
    _rec_name = "code"
    code = fields.Integer(string="Code")
    name_en = fields.Char(string="Name En")
    name_ar = fields.Char(string="Name Ar")
    type=fields.Selection([('debt','debt'),('reduction','reduction')])
    debts = fields.One2many('bylaws_debts','debt_type')
    students_debts = fields.One2many('students_debts','debt_type')

class debts(models.Model):
    _name = 'debts'
    _rec_name = "name_ar"
    debt_type = fields.Many2one('debts_types')
    debt_code = fields.Char()
    name_ar = fields.Char()
    name_en = fields.Char()

class bylaws_debts(models.Model):
    _name = "bylaws_debts"
    _description = ""
    _rec_name = "code"
    code = fields.Integer(string="Debt Code")
    bylaw = fields.Many2one("finance_bylaws", string="Bylaw")
    faculty = fields.Many2one(related="bylaw.faculty", string="faculty", store=True)
    debt_type = fields.Many2one("debts_types", string="Type")
    name_en = fields.Char(string="Name En")
    name_ar = fields.Char(string="Name Ar")
    currency = fields.Selection([("1", "EGP"), ("2", "Dollar")], default="1", string="Currency")
    is_discountable = fields.Boolean(string="Discountable?")
    partial_payments = fields.Boolean(string="partial_payments")
    priority = fields.Integer(string="priority")
    semester = fields.Many2one("academic_semesters", string="Semester")
    year = fields.Many2one("academic_years", string="Year")
    actual_amount = fields.Float(string="Actual Value")
    increase_rate = fields.Float(string="Increase Rate")
    amount = fields.Float(string="Value")
    fines_by = fields.Float(string="Fine by")
    fines_every = fields.Integer(string="Fine Every")
    status = fields.Selection([("1", "active"), ("2", "inactive")], default="1", string="Status")
    loading_date = fields.Selection([("0", "never"), ("1", "once"), ("2", "every semester"),("3", "every year")], default="0",
                                    string="Automatic Loading")
    students_debts=fields.One2many("students_debts","debt")
    is_mandatory=fields.Boolean()

    @api.model
    def update_loading_date(self):
        debts=self.env['bylaws_debts'].search([])
        for debt in debts:
            if (debt.debt_type == 2 and debt.code==3) or (debt.debt_type == 1 and debt.code==1):
                d=debt.write({'loading_date': "2"})

    # @api.model
    # def activate_debt(self):

    @api.model
    def transfer_debt(self):


        bylaws_debts = self.env['bylaws_debts']
        debts = bylaws_debts.browse(self._context.get('active_ids'))
        for debt in debts:
            year=debt.bylaw.year
            debt.year=year.id
            # to_debts = bylaws_debts.search([('debt_type','=',debt.debt_type.id),('code','=',debt.code),('status','=','1'),('faculty','=',debt.faculty.id)])
            # for to_debt in to_debts:
            #     if to_debt.amount != (debt.amount):
            #
            #         print(to_debt.bylaw.code)
            #         print(to_debt.name_ar)
            #         print(to_debt.amount)
            #         print(to_debt.status)
            #
            #         to_debt.status="2"
            #         new_debt = bylaws_debts.create(
            #             {'bylaw': to_debt.bylaw.id, 'debt_type': to_debt.debt_type.id, 'code': debt.code, 'amount': debt.amount,
            #              'status': '1'})
            #

            #
            # faculty=debt.bylaw.faculty
            # # debt.receipt = debt.payment.payment
            # debt.actual_amount = debt.debt_amount


class students_finance_accounts(models.Model):
    _name = "students_finance_accounts"
    _description = ""
    _rec_name = "student"
    active = fields.Boolean(default=True, string="هل الحساب نشط ؟")
    student = fields.Many2one("students", string="Student")
    student_active = fields.Boolean(related="student.active")
    category_ids = fields.Many2many('accounts_category', 'accounts_category_rel', 'student', 'category_id',string='Tags')
    faculty = fields.Many2one(related="student.faculty", string="Faculty", store=True)
    academic_year = fields.Many2one(related="student.academic_year", string="Academic Year", store=True)
    nationality = fields.Many2one(related="student.nationality", string="Nationality")
    citizenship = fields.Selection(related="student.citizenship", string="Nationality", store=True)
    study_language = fields.Selection(related="student.study_language", string="Study Language", store=True)
    file_number = fields.Integer(related="student.file_number", string="File Number")
    status = fields.Selection(related="student.status", string="Status", store=True)
    notes = fields.One2many(related="student.notes", string="ملاحظات")
    enrollment_status = fields.Selection(related="student.enrollment_status", string="Enrollment Status", store=True)
    application_number = fields.Integer(related="student.id", string="Application Number")
    image_1920 = fields.Image(related="student.image_1920", string="Image")
    name_en = fields.Char(related="student.name_en", string="Name En")
    name_ar = fields.Char(related="student.name_ar", string="Name Ar")
    academic_email = fields.Char(related="student.academic_email", string="Email")
    bylaw = fields.Many2one(related="student.finance_bylaw", string="Financial Bylaw")
    debts = fields.One2many("students_debts", "account", string="Debts", domain=[('receipt','=',False),('is_mandatory','=',True)])
    semester_debts = fields.One2many("students_debts", "account", string="Semester Debts", domain= [('semester','=','Spring2020-2021')])
    payments = fields.One2many("students_payments", "account", string="Semester Payments", domain= [('semester','=','Spring2020-2021')])
    reductions = fields.One2many("students_reductions", "account", string="Reductions")
    refunds = fields.One2many("students_refunds", "account", string="Refunds")
    transferes = fields.One2many("students_payments_transfers", "account", string="Transfers")
    delays = fields.One2many("payments_delays", "account", string="Delays")
    total_debts = fields.Float(compute="_compute_total_debts", string="Total Debts")
    total_semester_debts = fields.Float(compute="_compute_total_semester_debts", string="Semester Debts")
    total_unpaid_debts = fields.Float(compute="_compute_totals", string="Total Unpaid Debts")
    total_payments = fields.Float(compute="_compute_total_payments", string="Semester Payments")
    total_transfers = fields.Float(compute="_compute_totals", string="Total Transfers")
    total_reductions = fields.Float(compute="_compute_total_reductions", string="Total Reductions")
    account_balance = fields.Float(compute="_compute_totals", string="Balance", default=0.0)
    account_status = fields.Selection([("debit", "debit"), ("credit", "credit"), ("balanced", "balanced")],
                                      default="balanced", string="Account Status")
    dont_send=fields.Boolean()
    balance=fields.Float(string="الرصيد")



    @api.model
    def unenroll_student(self):
        accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        for account in accounts:
            student = account.student
            if account.enrollment_status == "1":
                status = '0'
            else:
                status = '1'

            a=student.write({'enrollment_status': status})


    @api.depends('debts')
    def _compute_total_debts(self):
        total=0.0
        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        for record in self:
            total = 0.0
            for debt in record.debts:
                total = total + (debt.to_pay_amount)
            record.total_debts = total

    @api.depends('semester_debts')
    def _compute_total_semester_debts(self):
        total=0.0
        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        for record in self:
            total = 0.0
            for debt in record.semester_debts:
                total = total + (debt.to_pay_amount)
            record.total_semester_debts = total



    @api.depends('semester_debts')
    def _compute_total_payments(self):

        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        current_year = self.env['academic_years'].search([('is_current', '=', True)])
        for record in self:
            total = 0.0
            for debt in record.payments:
                total = total + (debt.amount)
            record.total_payments = total


    @api.depends('payments')
    def _compute_total_reductions(self):

        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        semester = self.env['academic_semesters'].search([('is_current', '=', True)])
        for record in self:
            total = 0.0
            for debt in record.debts:
                if debt.debt_reduction != False:
                    total = total + (debt.debt_reduction_value)
            record.total_reductions = total



    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window']._for_xml_id('acums.%s' % xml_id)
            res.update(
                context=dict(self.env.context, default_account=self.id, group_by=False),
                domain=[('account', '=', self.id)]
            )
            return res
        return False

    @api.depends('debts', 'payments')
    def _compute_totals(self):
        total_debts = 0.0
        total_unpaid_debts = 0.0
        total_payments = 0.0
        total_transfers = 0.0
        total_reductions = 0.0
        # for debt in self.debts:
            # total_debts = total_debts + debt.to_pay_amount
            # total_unpaid_debts = total_unpaid_debts + debt.remaining_amount
            # total_payments = total_payments + debt.payed_amount
            # total_reductions = total_payments + debt.payed_amount
        self.total_unpaid_debts = 0.0
        # self.total_payments = total_payments
        self.total_transfers = 0.0
        self.account_balance = 0.0

    @api.depends('account_balance', 'account_status')
    def _compute_account_status(self):

        if self.account_balance == 0:
            self.account_status = 'balanced'
        elif self.account_balance < 0:
            self.account_status = 'debit'
        else:
            self.account_status = 'credit'

    @api.model
    def load_semester_debts(self):
        semester = self.env['academic_semesters'].search([('is_current', '=', True)])
        debts = self.env['bylaws_debts'].search(
            ['&', ('bylaw', '=', self.bylaw.id), '|', ('loading_date', '=', '2'), ('loading_date', '=', '3')])
        if self.student.academic_semester.code == 'Fall2020-2021':
            debts = self.env['bylaws_debts'].search(
                ['&', ('bylaw', '=', self.bylaw.id), '|', ('loading_date', '=', '2'), ('loading_date', '=', '3'),
                 ('loading_date', '=', '1')])
        semester_debts = self.env['students_debts'].search_count(
            [('account', '=', self.id), ('semester', '=', semester.id)])
        student_debts = self.env['students_debts'].search([('account', '=', self.id)])
        if semester_debts > 0:
            raise exceptions.ValidationError("تم تحميل مصروفات الفصل الدراسي بالفعل")
        else:
            for debt in debts:
                new_debt = student_debts.create({'account': self.id,'debt_type': debt.debt_type.id,'debt': debt.id, 'semester': semester.id})
                print(debt.debt_type.name_ar)
                print(debt.name_ar)
                print(debt.actual_amount)

    @api.model
    def load_bank_debts(self):
        students = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        debts = self.env['bylaws_debts']
        semester1 = self.env['academic_semesters'].search([('code', '=', 'Fall2020-2021')])
        semester2 = self.env['academic_semesters'].search([('code', '=', 'Spring2020-2021')])
        type1 = self.env['debts_types'].search([('code', '=', 2)])
        type2 = self.env['debts_types'].search([('code', '=', 11)])
        student_debts = self.env['students_debts']
        for student in students:
            bylaw=student.bylaw
            print(bylaw)
            mandatory_debt = debts.search([('bylaw', '=', student.bylaw.id),('debt_type', '=', type1.id), ('code', '=', 3),('status','=','1')], limit=1)

            extra_debt = debts.search([('bylaw', '=', student.bylaw.id),('debt_type', '=', type2.id), ('code', '=', 321)], limit=1)
            new_debt1 = student_debts.create({'account': student.id,'debt_type': type2.id,'debt': extra_debt.id, 'semester': semester1.id})
            new_debt2 = student_debts.create({'account': student.id,'debt_type': type2.id,'debt': extra_debt.id, 'semester': semester2.id})
            new_debt3 = student_debts.create({'account': student.id,'debt_type': type1.id,'debt': mandatory_debt.id, 'semester': semester2.id})

            # mandatory_debt = debts.search([('bylaw', '=', student.bylaw.id),('debt_type', '=', type1.id), ('code', '=', 3)], limit=1)
            # extra_debt = debts.search([('bylaw', '=', student.bylaw.id),('debt_type', '=', type2.id), ('code', '=', '321')], limit=1)
            # mandatory = student_debts.create({'account': student.id, 'debt': mandatory_debt, 'semester': semester2.id})
            # extra = student_debts.create({'account': student.id, 'debt': extra_debt, 'semester': semester1.id})


    @api.model
    def create_email_log(self):
        for record in self:
            logs=self.env['emails_log']
            log_record=logs.create({'to': self.id})

    # def load_debts(self):
    #     accounts=self.env['students_finance_accounts'].search([('status','=','3')])
    #     students_debts=self.env['students_debts'].search([])
    #     semester=self.id
    #     deadline=self.payment_deadline
    #     for account in accounts :
    #         bylaw=account.bylaw.id
    #         debts=self.env['bylaws_debts'].search([('bylaw','=',bylaw),('loading_date','=','2')])
    #         for debt in debts :
    #             student_debt=students_debts.create({'account':account.id , 'debt_type':debt.debt_type.id , 'debt':debt.id, 'semester':semester , 'dead_line': deadline})


class students_debts(models.Model):
    _name = "students_debts"
    _description = ""
    _rec_name = "id"
    imported_id = fields.Integer()
    account = fields.Many2one("students_finance_accounts", string="Account")
    academic_year = fields.Many2one(related="account.academic_year", string="Academic Year", store=True)
    bylaw = fields.Many2one(related="account.bylaw", string="Financial Bylaw")
    faculty = fields.Many2one(related="account.student.faculty", store=True, string="Faculty")
    nationality = fields.Many2one(related="account.student.nationality", store=True, string="Nationality")
    student_name = fields.Char(related="account.name_ar", string="Student Name")
    debt_type = fields.Many2one("debts_types", string="Debt Type")
    debt_type_name = fields.Char(related="debt_type.name_ar", string="Debt Type Name")
    semester = fields.Many2one("academic_semesters", string="Semester", store=True)
    debt = fields.Many2one("bylaws_debts", string="Debt", store=True, domain="[('bylaw','=',bylaw),('debt_type','=',debt_type)]")
    debt_name = fields.Char(related="debt.name_ar", string="Debt Name", store=True)
    debt_currency = fields.Selection(related="debt.currency", string="Currency")
    debt_reduction = fields.Many2one("students_reductions", string="Reduction", compute="_compute_reduction")
    debt_reductions = fields.One2many("students_reductions","debt", string="Reductions", default=False)
    partial_payments=fields.Boolean(related="debt.partial_payments")
    debt_delay = fields.Many2one("payments_delays")
    is_mandatory = fields.Boolean(related='debt.is_mandatory')
    is_discountable = fields.Boolean(related='debt.is_discountable')
    is_rest = fields.Boolean()
    debt_date=fields.Date(default=date.today())

    debt_amount = fields.Float(related="debt.amount", string="Bylaw Value")
    reduced_amount = fields.Float(compute="_compute_reduced_amount", string="Reduced Amount")
    payed_amount = fields.Float(compute="_compute_payed_amount", string="Total Payed Value",store=True, default=0.0)
    receipt_value = fields.Float(default=0.0)
    to_pay_amount = fields.Float(compute="_compute_to_pay", string="To Pay Value")
    debt_reduction_value = fields.Float(related="debt_reduction.imported_value")
    total_reductions_value = fields.Float(compute="_compute_total_reductions")

    actual_amount=fields.Float()
    payed = fields.Float(string="Payed", default=0.0)
    remaining_amount = fields.Float(compute="_compute_remaining_amount", debt="Remaining Value")
    number_of_units = fields.Float(string="عدد الوحدات", default=1)
    dead_line = fields.Date(string="Deadline")
    priority = fields.Integer(related="debt.priority", string="Priority")
    receipt = fields.Many2one("students_payments")
    receipt_number = fields.Integer(related="receipt.receipt_number")
    payment_status = fields.Selection([('0', 'none'), ('1', 'partial '), ('2', 'totally')],                                   compute="_compute_payment_status", default="0", string="Payment Status")
    status = fields.Selection(related="account.student.status", store=True)
    # payment = fields.Many2one("students_payments", string="Payment")
    currency = fields.Selection(related="receipt.currency", store=True, string="Currency")
    method = fields.Many2one(related="receipt.method", store=True, string="Payment Method")
    type = fields.Selection(related="receipt.type", store=True, string="Payment Type")
    date = fields.Date(related="receipt.date", store=True, string="Date")
    user = fields.Many2one(related="receipt.user", store=True, string="Agent")
    payment = fields.One2many("payments_details", "debt", string="Payment Number", default=False)
    debt_code = fields.Integer()



    @api.depends('debt_amount','debt_reduction_value')
    def _compute_reduced_amount(self):
        for record in self:
            record.reduced_amount = (record.debt_amount) - (record.total_reductions_value)





    @api.depends('account',)
    def _compute_total_reductions(self):
        for record in self:
            total=0.0
            reductions=record.env['students_reductions'].search([('account','=',record.account.id),('semester','=',record.semester.id)])
            if record.is_discountable == True:
                for reduction in reductions:
                    total = total + reduction.imported_value
            record.total_reductions_value = total


    @api.depends('reduced_amount','payed_amount','partial_payments')
    def _compute_to_pay(self):

        for record in self:
            amount=record.reduced_amount - record.payed_amount
            # if (record.partial_payments == True) and (record.payed_amount != 0.0):
            #     amount=((record.reduced_amount)-(record.payed_amount))

            record.to_pay_amount= amount * record.number_of_units


    @api.depends('account',)
    def _compute_reduction(self):
        for debt in self:
            reduction = False
            if (debt.debt.is_discountable == True):
                reduction = debt.env['students_reductions'].search([('semester', '=', debt.semester.id),('account', '=', debt.account.id)], limit=1).id
            debt.debt_reduction = reduction

    @api.model
    def update_actual(self):
        debts = self.env['students_debts'].browse(self._context.get('active_ids'))
        for debt in debts:
            debt_2=debt.env['bylaws_debts'].search([('code','=',3),('bylaw','=',debt.bylaw.id),('is_mandatory','=',True),('status','=','1')])

            debt.debt=debt_2.id
            # debt.actual_amount = debt.debt_amount

    @api.depends('payment')
    def _compute_payed_amount(self):
        for record in self:
            total_payed = 0.0
            payments = record.env['students_debts'].search([('account', '=', record.account.id), ('debt', '=', record.debt.id),('semester', '=', record.semester.id),('receipt','!=',False)])
            for payment in payments:
                total_payed = total_payed + payment.payed
            record.payed_amount = total_payed

    @api.model
    def _update_account(self):
        debts = self.env['students_debts'].browse(self._context.get('active_ids'))
        for debt in debts:
            debt.account = debt.receipt.account
            debt.semester = debt.receipt.semester
            debt.debt_type = debt.debt.debt_type





    @api.depends('remaining_amount', 'payed_amount', 'to_pay_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = 0.0
            # record.remaining_amount = record.to_pay_amount - record.payed_amount


    @api.onchange('debt_amount')
    def onChange_debt_amount(self):
        self.actual_amount = self.debt_amount

    @api.onchange('number_of_units')
    def onChange_number_of_units(self):
        self.to_pay_amount = self.actual_amount * self.number_of_units



    api.model
    def update_rec(self):
        # debts=self.env['students_debts'].search([])
        # for debt in self:
        #     if debt.payment != False:
        #         p=debt.payment[0].payment
        #         d=debt.write({'receipt': p})
        #         print(debt.receipt.receipt_number)
        debts = self.env['students_debts'].browse(self._context.get('active_ids'))
        for debt in debts:
            # debt.receipt = debt.payment.payment
            debt.actual_amount = debt.debt_amount



    @api.model
    def update_debt(self):
        debts = self.env['students_debts'].search([("debt_type.code", "=", 4), ('debt', '=', False)])
        for debt in debts:
            d = self.env['bylaws_debts'].search(
                [("bylaw", "=", debt.bylaw.id), ('debt_type', '=', debt.debt_type.id), ('code', '=', 20)])
            x = debt.write({"debt": d})







    @api.depends('remaining_amount', 'payed_amount', 'to_pay_amount')
    def _compute_payment_status(self):
        for record in self:
            if record.remaining_amount == 0:
                record.payment_status = "2"
            elif record.remaining_amount == record.to_pay_amount:
                record.payment_status = "0"
            elif record.payed_amount < record.to_pay_amount and record.remaining_amount > 0:
                record.payment_status = "1"
            else:
                record.payment_status = "0"

    # @api.model
    # def create(self, values):
    #     record = super(students_debts, self).create(values)
    #     if record.debt.debt_type.code == 2 and record.debt.code ==3 :
    #         record.account.student.status = "3"

    #     debt = self.env['bylaws_debts'].search([('bylaw', '=', record.bylaw.id), ('debt_type', '=', record.debt_type.id), ('code', '=', record.debt_code),('status', '=', '1')],limit=1)
    #     if debt != False:
    #         record.debt = (debt).id
    #         record.actual_amount = record.debt_amount
    #     return record


    @api.model
    def create_rest(self):
        debts = self.env['students_debts'].browse(self._context.get('active_ids'))
        students_debts=self.env["students_debts"]
        for debt in debts:
            if debt.payed_amount < debt.to_pay_amount:
                new_amount = debt.to_pay_amount - debt.payed_amount
                for i in "44444444444444444":
                    print (new_amount)
                new_debt = students_debts.create(
                    {'account': debt.account.id, 'debt_type': debt.debt_type.id, 'debt': debt.debt.id, 'semester': debt.semester.id,
                     'actual_amount': new_amount, 'is_rest': True})



class reductions_types(models.Model):
    _name = "reductions_types"
    _rec_name="code"
    type=fields.Many2one('debts_types',domain=[('type','=','reduction')])
    code = fields.Integer(string="Reduction Code")
    bylaw = fields.Many2one('finance_bylaws', string="Bylaw")
    name_en = fields.Char(string="Name En")
    name_ar = fields.Char(string="Name Ar")
    debt = fields.Many2one("bylaws_debts", string="Debt")
    value = fields.Float(string="Value")
    currency = fields.Selection([("1", "EGP"), ("2", "Dollar")], default="1", string="Currency")
    percentage=fields.Float(string="Percentage")
    status = fields.Selection([("1", "active"), ("2", "inactive")], default="1", string="Status")


class students_reductions(models.Model):
    _name = "students_reductions"
    _rec_name="reduction"
    account = fields.Many2one("students_finance_accounts", string="Account")
    bylaw = fields.Many2one(related="account.bylaw", string="Financial Bylaw")
    name_ar = fields.Char(related="account.student.name_ar", string="Student Name Ar")
    name_en = fields.Char(related="account.student.name_en", string="Student Name En")
    faculty = fields.Many2one(related="account.student.faculty", store=True, string="Faculty")
    status = fields.Selection(related="account.student.status", store=True)
    nationality = fields.Many2one(related="account.student.nationality", string="Nationality")
    type = fields.Many2one('debts_types', string="Reduction Type", domain=[('type', '=', 'reduction')])
    reduction = fields.Many2one("reductions_types", string="Reduction")
    reduction_name = fields.Char(related="reduction.name_ar", string="Reduction Name")
    debt = fields.Many2one("students_debts",compute="_compute_reduced_debt", domain ="[('account','=',account),('semester','=',semester),('is_discountable', '=' , True)]")
    semester = fields.Many2one("academic_semesters", string="Semester")
    date = fields.Date(string="Date")
    user = fields.Many2one("res.users", string="User")
    amount = fields.Float(related="reduction.value", string="Bylaw Value")
    currency = fields.Selection(related="reduction.currency")
    imported_id= fields.Integer()
    imported_value= fields.Float()
    imported_percentage= fields.Float()
    imported_type = fields.Integer()
    imported_code = fields.Integer()

    @api.model
    def reduction_transfer(self):
        reductions = self.env['students_reductions'].browse(self._context.get('active_ids'))
        students_reductions = self.env['students_reductions']
        semester = self.env['academic_semesters'].search([('is_current', '=', True)])
        for reduction in reductions:
            reduction =students_reductions.create({'account': reduction.account.id, 'reduction':reduction.reduction.id, 'semester': semester.id , 'imported_value': reduction.imported_value})


    @api.depends('account')
    def _compute_reduced_debt(self):
        for record in self:
            student_debts=record.env['students_debts'].search([('account','=',record.account.id),('semester','=',record.semester.id),('is_discountable','=',True)], limit=1)
            record.debt=student_debts.id




class payments_delays(models.Model):
    _name = "payments_delays"
    number = fields.Integer(string="Delay Number")
    account = fields.Many2one("students_finance_accounts", string="Account")
    semester = fields.Many2one("academic_semesters", string="Semester")
    to_date = fields.Date(string="To Date")
    by = fields.Many2one("res.users", string="Agent")


class students_refunds(models.Model):
    _name = "students_refunds"
    _rec_name = "receipt_number"
    debt_type_code = fields.Integer(string="Debt Type Code")
    debt_code = fields.Integer(string="Debt Code")
    account = fields.Many2one("students_finance_accounts", string="Account")
    receipt_number = fields.Integer(string="Payment")
    # receipt_number = fields.Many2one("students_payments", string="Payment")
    faculty = fields.Many2one(related="account.student.faculty", string="Faculty")
    nationality = fields.Many2one(related="account.student.nationality", string="Nationality")
    name_ar = fields.Char(related="account.student.name_ar", string="Student Name Ar")
    name_en = fields.Char(related="account.student.name_en", string="Student Name En")
    file_number = fields.Integer(related="account.student.file_number", store=True, string="File Number")
    semester = fields.Many2one("academic_semesters", string="Semester")
    date = fields.Date(string="Date")
    payments = fields.Many2many("payments_details", string="Payment Details")
    by = fields.Many2one("res.users", string="Agent")
    amount = fields.Float(string="Value")
    currency = fields.Selection([("1", "جنيه مصري"), ("2", "دولار")], string="Currency")
    notes = fields.Char(string="Notes")
    check_number = fields.Char(string="Bank check")
    check_date = fields.Date(string="Bank check Date")


class students_payments_transfers(models.Model):
    _name = "students_payments_transfers"
    _rec_name = "receipt_number"

    semester = fields.Many2one("academic_semesters", string="Semester")
    account = fields.Many2one("students_finance_accounts", string="Account")
    bylaw = fields.Many2one(related="account.bylaw", string="Bylaw")
    faculty = fields.Many2one(related="account.student.faculty", string="Faculty")
    citizenship = fields.Selection(related="account.student.citizenship", string="Citizenship")
    name_ar = fields.Char(related="account.student.name_ar", string="Student Name Ar")
    name_en = fields.Char(related="account.student.name_en", string="Student Name En")
    file_number = fields.Integer(related="account.student.file_number", store=True, string="File Number")

    # From
    receipt_number = fields.Many2one("students_payments", string="Receipt Number",domain="[('semester', '=', semester), ('account', '=', account)]")
    receipt_details = fields.One2many(related="receipt_number.payment_debts")
    debt_type = fields.Many2one("debts_types", string="Debt Type")
    debt_type_name = fields.Char(related="debt_type.name_ar", string="Debt Type Name")
    debt = fields.Many2one("bylaws_debts", string="Debt",domain="[('bylaw','=',bylaw),('debt_type','=',debt_type)]")
    debt_name = fields.Char(related="debt.name_ar", string="Debt Name", store=True)

    # To
    to_semester = fields.Many2one("academic_semesters", string="to Semester")
    to_account = fields.Many2one("students_finance_accounts", string="to Account")
    to_debt_type = fields.Many2one("debts_types", string="Debt Type")
    to_debt_type_name = fields.Char(related="to_debt_type.name_ar", string="Debt Type Name")
    to_debt = fields.Many2one("bylaws_debts", string="Debt",domain="[('bylaw','=',bylaw),('debt_type','=',debt_type)]")
    to_debt_name = fields.Char(related="to_debt.name_ar", string="Debt Name", store=True)

    # Transfer Info
    transfer_value=fields.Float()
    by = fields.Many2one("res.users", string="Agent")
    date = fields.Date(string="Date")
    type = fields.Selection([("1", "student"), ("2", "debt")], string="Transfer Type")

    @api.model
    def create(self, values):
        record = super(students_payments, self).create(values)
        student_debts = self.env['students_debts']
        student_payments =  self.env['students_payments']
        student_debts =  self.env['students_debts']
        new_receipt = student_payments.create({'account': record.account, 'semester': record.semester})
        # new_debt = student_payments.create({'account': record.account, 'semester': record.semester})
        return record

class students_payments(models.Model):
    _name = "students_payments"
    _description = ""
    _rec_name = "receipt_number"
    old_id = fields.Integer()
    account = fields.Many2one("students_finance_accounts", string="Account")
    total_debts = fields.Float(related="account.total_debts", string="اجمالي اللاستحقاقات")
    bylaw = fields.Many2one(related="account.bylaw", string="Financial Bylaw")
    faculty = fields.Many2one(related="account.student.faculty", string="Faculty", store=True)
    nationality = fields.Many2one(related="account.student.nationality", string="Nationality")
    student_active = fields.Boolean(related="account.student_active")
    name_ar = fields.Char(related="account.student.name_ar", string="Student Name Ar")
    name_en = fields.Char(related="account.student.name_en", string="Student Name En")
    file_number = fields.Integer(related="account.student.file_number", store=True, string="File Number")
    application_number = fields.Integer(related="account.student.id", store=True, string="Application Number")
    status = fields.Selection(related="account.student.status", string="Student Status", store=True)
    enrollment_status = fields.Selection(related="account.student.enrollment_status", string="Student Status")
    study_language = fields.Selection(related="account.student.study_language", string="Study Language")
    image = fields.Image(related="account.student.image_1920", string="Image")
    # receipt_number = fields.Integer(string="Receipt Number 3")
    semester = fields.Many2one("academic_semesters", string="Semester",
                               default=lambda self: self.env['academic_semesters'].search([('is_current', '=', True)]))
    method = fields.Many2one("payments_methods",default=lambda self: self.env['payments_methods'].search([('code','=',2)]))
    method_code = fields.Integer(related="method.code", store=True)
    amount = fields.Float(string="Value")
    user = fields.Many2one("res.users", string="Agent", default=lambda self: self.env.user)
    date = fields.Date(string="Date", default=date.today())
    date2 = fields.Char(string="Date 2")
    receipt_number = fields.Integer(string="Receipt Number")
    currency = fields.Selection([("1", "جنيه مصري"), ("2", "دولار")], string="Currency", default="1")
    type = fields.Selection([('1', 'New'), ('2', 'Transfer'), ('3', 'Refund'), ('4', 'Delay'), ('5', 'Error')],
                            string="Transaction Type", default="1")
    debts = fields.One2many(related="account.debts", string="Debts")
    cash_payments_details = fields.One2many("cash_payments_details", "payment", string="Cash Details", )
    payment_details = fields.One2many("payments_details", "payment", string="Payment Details")
    bank_notice = fields.One2many("bank_notices", "payment", string="Bank Notice")
    is_deleted = fields.Boolean(string="is Deleted?")
    is_transfered = fields.Boolean(string="is Transferred")
    delete_flag = fields.Integer()
    delay_value = fields.Integer()
    delay_pct = fields.Integer()
    payment_debts=fields.One2many("students_debts","receipt")
    barcode = fields.Char(string="receipt barcode", help="باركود الايصال", copy=False)
    printed = fields.Boolean()
    file_number_temp = fields.Integer()
    notes = fields.Text()

    _sql_constraints = [('barcode_uniq', 'unique (barcode)', "لا يمكن تكرار الباركود")]


    def generate_random_barcode(self):
        for payment in self:
            payment.barcode = '041'+"".join(choice(digits) for i in range(9))


    @api.model
    def is_delete(self):
        payments = self.env['students_payments'].search([])
        for payment in payments:
            if payment.amount < 0:
                payment.is_deleted = True
            else:
                payment.is_deleted = False

    @api.model
    def create(self, values):

        record = super(students_payments, self).create(values)
        if record.file_number_temp !=0:
            record.account.student.file_number = record.file_number_temp
        if record.account.student.active == False:
            raise exceptions.ValidationError('صفحة الطالب مغلقة من قبل شئون الطلاب')
        last_id = last_receipt = record.account.student.faculty.receipts_counter
        last_receipt = record.account.student.faculty.receipts_counter
        debts = record.debts
        receipt_number = fields.Integer(string="Receipt Number")
        remaining_amount=record.amount
        record.receipt_number = last_receipt + 1
        record.account.student.faculty.receipts_counter = last_receipt + 1
        students_debts=self.env['students_debts']
        payed=0.0
        for debt in debts:
            if (remaining_amount >= debt.to_pay_amount):
                payed =debt.to_pay_amount
                debt.payed = payed
                remaining_amount = remaining_amount - payed

            elif(remaining_amount > 0.0 and debt.partial_payments==True):
                payed = remaining_amount
                debt.payed = payed
                debt.is_rest=True
                remaining_amount = remaining_amount - payed
                new_debt=self.env['bylaws_debts'].search([('bylaw','=',record.account.id),('debt_type','=',debt.debt_type.id),('code','=',debt.debt.code)])
                students_debts.create({'account':record.account.id,'debt':new_debt.id, 'is_rest':True })
            debt.receipt = record
        record.account.balance=remaining_amount
        return record

    debt = fields.Many2one("bylaws_debts", string="Debt", store=True,
                           domain="[('bylaw','=',bylaw),('debt_type','=',debt_type)]")



    # @api.model
    # def create(self, values):
    #     record = super(students_payments, self).create(values)
    #     # last_id = record.account.student.faculty.students_academic_ids_counter
    #     # last_receipt = record.account.student.faculty.receipts_counter
    #     # students = record.env['students'].search([('id', '=', record.account.student.id)], limit=1)
    #     # cash_payments_count = record.cash_payments_details.search_count([('payment', '=', record.id)])
    #     # faculty = record.env['faculties'].search([('id', '=', record.account.student.faculty.id)], limit=1)
    #     # payment_details = record.env['payments_details']
    #     debts=[]
    #     for debt in record.debts:
    #         debts.append(debt)
    #     debts.sort(key=lambda x: x.debt.priority)
    #     actual_amount = record.amount
    #     for debt in debts:
    #         student_debts = record.env['students_debts'].search([('id', '=', debt.id)], limit=1)
    #         if (actual_amount - debt.remaining_amount >= 0):
    #             dept_payment = debt.remaining_amount
    #             a = student_debts.write({'payed_amount': debt.to_pay_amount, 'payed': debt.to_pay_amount, 'receipt':self.id })
    #             actual_amount = actual_amount - debt.to_pay_amount
    #         elif (actual_amount > 0) and (debt.debt.partial_payments == True):
    #             a = student_debts.write({'payed_amount': actual_amount, 'payed': actual_amount, 'receipt':self.id})
    #             dept_payment = actual_amount
    #             a = student_debts.create(
    #                 {'account': debt.account, 'debt_type': debt.debt_type, 'debt': debt.debt, 'semester': debt.semester,
    #                  'actual_amount': debt.remaining_amount})
    #         # payment_detail = payment_details.sudo().create({
    #         #         'payment': record.id,
    #         #         'debt': debt.id,
    #         #         'payment_amount': dept_payment,
    #         #     })
    #     if record.account.student.status=="2":
    #         academic_id=str(last_id + 1)
    #         b = students.write({'status': '3', 'student_id': academic_id})
    #         d = faculty.write({'students_academic_ids_counter': academic_id})
    # #
    #     if (record.method == '1') and (cash_payments_count != 1):
    #         raise exceptions.ValidationError('يوجد خطأ في إدخال بيانات الدفع النقدي')
    #     if record.amount <= 0:
    #         raise exceptions.ValidationError('يرجى إدخال المبلغ المراد دفعه')
    #     if record.account.student.file_number == 0:
    #         raise exceptions.ValidationError("يرجى إدخال رقم الملف")
    #     return record
    #     if len(vals.get('cash_payments')) > 1:
    #         raise exceptions.ValidationError("يجب ادخال تفصيل واحد فقط للدفع النقدي")
    #     record.payment_date = date.today()
    #     receipt_number= last_receipt+1
    #     record.receipt_number= receipt_number
    #     f = faculty.write({'receipts_counter': receipt_number})


    def load_debts(self):
        print("Ahmed")
        semester = self.env['academic_semesters'].search([('is_current', '=', True)])
        print(semester.code)
        debts = self.env['bylaws_debts'].search(['&',('bylaw', '=', self.bylaw.id),'|', ('loading_date', '=', '2'),('loading_date', '=', '3')])
        if account.student.academic_semester.code == 'Fall2020-2021':
            debts = self.env['bylaws_debts'].search(
                ['&', ('bylaw', '=', self.bylaw.id), '|', ('loading_date', '=', '2'), ('loading_date', '=', '3'),
                 ('loading_date', '=', '1')])
        semester_debts = self.env['students_debts'].search_count(
            [('account', '=', self.id), ('semester', '=', semester.id)])
        student_debts = self.env['students_debts'].search([('account', '=', self.id)])
        if semester_debts > 0:
            raise exceptions.ValidationError("تم تحميل مصروفات الفصل الدراسي بالفعل")
        else:
            for debt in debts:
                new_debt = student_debts.create(
                    {'account': self.id, 'debt_type': debt.debt_type.id, 'debt': debt.id, 'semester': semester.id})


class bank_notices(models.Model):
    _name = "bank_notices"
    _rec_name = "payment"
    old_id = fields.Integer(string="old_id")
    payment = fields.Many2one("students_payments", string="Payment")
    number = fields.Integer(string="Number")
    bank = fields.Many2one("bank_accounts", string="Bank")
    bank_name = fields.Char(related="bank.bank_name_ar")
    account_number = fields.Char(related="bank.account_number", string="Bank Account")
    numbering = fields.Integer(string="Numbering")
    date = fields.Date(string="Date")
    type = fields.Selection([("POS", "POS"), ("Bank", "Bank"),("Transfer", "Transfer"), ("Postal", "Postal"),("Check", "Check")], default="Bank", string="Type")
    # payment_date = fields.Date(string="Date")


class bank_accounts(models.Model):
    _name = "bank_accounts"
    _rec_name = "account_old_id"
    account_old_id = fields.Integer(string="old id")
    account_number = fields.Char(string="Account Number")
    bank_name_ar = fields.Char(string="Bank Name Ar")
    bank_name_en = fields.Char(string="Bank Name En")
    currency = fields.Selection([("1", "جنيه مصري"), ("2", "دولار")], string="Account Currency")
    branch = fields.Char(string="Bank Branch")


class payments_methods(models.Model):
    _name = "payments_methods"
    _rec_name = "name_ar"
    code = fields.Integer(string="Code")
    name_en = fields.Char(string="Name En")
    name_ar = fields.Char(string="Name Ar")


class payments_details(models.Model):
    _name = "payments_details"
    _rec_name = "payment"
    account = fields.Many2one(related="payment.account", string="Account")
    name = fields.Char(related="account.student.name_ar", string="Name")
    faculty = fields.Many2one(related="account.student.faculty", store=True, string="Faculty")
    status = fields.Selection(related="account.student.status", store=True, string="Student Status")
    nationality = fields.Many2one(related="account.student.nationality", store=True, string="Nationality")
    payment = fields.Many2one("students_payments", string="Payment")
    currency = fields.Selection(related="payment.currency", store=True, string="Currency")
    currency = fields.Selection(related="payment.currency", store=True, string="Currency")
    semester = fields.Many2one(related="payment.semester", store=True, string="Semester")
    method = fields.Many2one(related="payment.method", store=True, string="Payment Method")
    type = fields.Selection(related="payment.type", store=True, string="Payment Type")
    date = fields.Date(related="payment.date", store=True, string="Date")
    agent = fields.Many2one(related="payment.user", store=True, string="Agent")
    debt = fields.Many2one("students_debts", store=True, string="Debt",)
    debt_name = fields.Char(related="debt.debt_name", store=True, string="Debt Name")
    debt_type = fields.Many2one(related="debt.debt_type", store=True, string="Debt Type")
    debt_type_name = fields.Char(related="debt_type.name_ar", store=True, string="Debt Type Name")
    number_of_units = fields.Float(related="debt.number_of_units", string="عدد الوحدات")
    debt_amount = fields.Float(related="debt.debt_amount", string="قيمة المصروف")
    debt_to_pay = fields.Float(related="debt.to_pay_amount", string="المبلغ المطلوب")
    payment_amount = fields.Float(store=True, string="Value")

    @api.model
    def update_payed(self):
        for payment in self:
            debt = self.env['students_debts'].search([('id', '=', payment.debt.id)])
            record = debt.write({'payed_amount': payment.payment_amount})


class cash_payments_details(models.Model):
    _name = "cash_payments_details"
    payment = fields.Many2one("students_payments")
    payment_amount = fields.Float(related="payment.amount")
    payment_200 = fields.Integer(string="+200")
    payment_100 = fields.Integer(string="+100")
    payment_50 = fields.Integer(string="+50")
    payment_20 = fields.Integer(string="+20")
    payment_10 = fields.Integer(string="+10")
    payment_5 = fields.Integer(string="+05")
    payment_1 = fields.Integer(string="+1")
    remaning_200 = fields.Integer(string="-200")
    remaning_100 = fields.Integer(string="-100")
    remaning_50 = fields.Integer(string="-50")
    remaning_20 = fields.Integer(string="-20")
    remaning_10 = fields.Integer(string="-10")
    remaning_5 = fields.Integer(string="-05")
    remaning_1 = fields.Integer(string="-1")
    payment_total = fields.Float(compute="_compute_payment_total")
    remaning_total = fields.Float(compute="_compute_remaning_total")

    @api.depends('payment_200', 'payment_100', 'payment_50', 'payment_20', 'payment_10', 'payment_5', 'payment_1',
                 'remaning_200')
    def _compute_payment_total(self):
        self.payment_total = (200 * self.payment_200) + (100 * self.payment_100) + (50 * self.payment_50) + (
                20 * self.payment_20) + (10 * self.payment_10) + (5 * self.payment_5) + (1 * self.payment_1)

    @api.depends('remaning_200', 'remaning_100', 'remaning_50', 'remaning_20', 'remaning_10', 'remaning_5',
                 'remaning_1', 'remaning_200')
    def _compute_remaning_total(self):
        self.remaning_total = (200 * self.remaning_200) + (100 * self.remaning_100) + (50 * self.remaning_50) + (
                20 * self.remaning_20) + (10 * self.remaning_10) + (5 * self.remaning_5) + (1 * self.remaning_1)

    # @api.model
    # def create(self, values):
    #     record = super(cash_payments_details, self).create(values)
    #     if ((record.payment_total - record.remaning_total) != (record.payment_amount)):
    #         raise exceptions.ValidationError('يوجد خطأ في حساب المبلغ المستلم والباقي')
    #     if ((record.env['cash_payments_details'].search_count([('payment', '=', record.payment.id)])) > 1):
    #         raise exceptions.ValidationError('لا يمكن إضافة أكثر من بند للدفع النقدي')
    #     return record

class emails_log(models.Model):
    _name="emails_log"
    to = fields.Many2one("students_finance_accounts")
    sender= fields.Many2one("res.users", default=lambda self: self.env.user)
    date=fields.Date(default=date.today())


class StudentsCategory(models.Model):
    _name = "students_category"
    def _get_default_color(self):
        return randint(1, 11)
    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)
    accounts_ids = fields.Many2many('students', 'students_category_rel', 'category_id', 'student_id', string='Students')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

class AccountsCategory(models.Model):
    _name = "accounts_category"
    def _get_default_color(self):
        return randint(1, 11)
    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)
    accounts_ids = fields.Many2many('students_finance_accounts', 'accounts_category_rel', 'category_id', 'student', string='Accounts')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]




class students(models.Model):
    _name = "students"
    _description = ""
    _rec_name = "student_id"
    def _get_default_color(self):
        return randint(1, 11)
    color = fields.Integer(string='Color Index', default=_get_default_color)
    student_id = fields.Char(string="Student ID")
    web_form_type = fields.Selection([('1', 'New Admission'), ('2', 'Update Applicant Information')], string="")
    candidate_by = fields.Selection([('ministry', 'ministry'), ('university', 'university')], string='نوع الترشيح', default='university')
    file_number = fields.Integer(string="File Number")
    receipt_number = fields.Integer(string="Receipt Number")
    application_number = fields.Char(string="Application Number")
    name_en = fields.Char(string="Student Name EN")
    name_ar = fields.Char(string="Student Name Ar")
    birth_date = fields.Date(string="Date of Birth")
    birth_governorate = fields.Many2one("governorates", string="Birth Governorate")
    birth_country = fields.Many2one("countries", string="Birth Country")
    nationality = fields.Many2one("countries", string="Nationality")
    citizenship = fields.Selection([("1", "مصري"), ("0", "وافد")], default="1")
    gender = fields.Selection([('1', 'Male'), ('2', 'Female')], string="Gender")
    study_type = fields.Selection([('undergraduate', 'undergraduate'), ('postgraduate', 'postgraduate')], default="undergraduate" ,string="Study Type")
    phase_type = fields.Selection([('Diploma', 'Diploma'), ('MS', 'MS')], default="MS" ,  string="Phase")
    religion = fields.Selection([('1', 'Muslim'), ('2', 'Christian')], string="Religion")
    academic_semester = fields.Many2one("academic_semesters", string="Academic Semester",
                                        default=lambda self: self.env['academic_semesters'].search(
                                            [('is_current', '=', True)]))
    academic_year = fields.Many2one(related="academic_semester.year", String="Academic year", store=True)
    application_type = fields.Selection([('1', 'newcomer'), ('2', 'transfered'), ('3', 'transefered newcomer')],
                                        string="Application Type", default="1")
    high_school_certificate_type = fields.Selection(
        [("1", "Egyptian High School"), ("2", "Azhar High School"), ("3", "Arabic"), ("4", "Western")],
        string="High School Type")
    high_school_certificate_name = fields.Many2one('high_schools_names', string='High School Name')
    high_school_type = fields.Selection(related='high_school_certificate_name.type',store=True, string='High School Type')
    high_school_certificate_major = fields.Selection([("3", "Literary"), ("1", "Science"), ("2", "Math")],
                                                     string="High School Major")
    high_school_certificate_country = fields.Many2one("countries", string="High School Country")
    high_school_certificate_year = fields.Integer(string="High School year")
    total_mark = fields.Float(string="High School Mark")
    total_percentage = fields.Float(string="High School Percentage")
    seat_number = fields.Integer(string="High School Seat Number")
    finance_bylaw = fields.Many2one("finance_bylaws", string="Finance Bylaw")
    academic_bylaw = fields.Many2one("academic_bylaws", string="Academic ByLaw")
    national_id = fields.Char(size=14, string="National ID")
    national_id_date = fields.Date()
    national_id_place = fields.Char()
    passport_id = fields.Char(string="Passport Number")
    email_address = fields.Char(string="Email")
    academic_email = fields.Char(string="Academic Email")
    phone_number = fields.Char(string="Phone Number")
    mobile_number = fields.Char(string="Mobile Number")
    address = fields.Char(string="Address")
    faculty = fields.Many2one("faculties", string="Faculty")
    faculty_code = fields.Integer(related ="faculty.code", store=True)
    semester_payment_amount = fields.Char(related = "faculty.semester_payment_amount")
    study_language = fields.Selection([('ar', 'Arabic'), ('en', 'English')], string="Study Language", default="en")
    faculty_major = fields.Many2one("faculty_majors", string="Faculty Major")
    status = fields.Selection(
        [('0', "Willing"), ('1', "Applicant"), ('2', "Accepted"), ('3', "Student"), ('4', "Expected"),
         ('5', "not fulfilled"), ('6', 'Alumni'), ('7', 'Withdrawn')], string="Student Status", default="0")
    enrollment_status = fields.Selection([('1', "مقيد"), ('0', "غير مقيد")], default="1",string="Enrollment Status")
    image_1920 = fields.Image(string="Student Image")
    certificate_image = fields.Image(string="High School Certificate Image")
    birth_image = fields.Image(string="Birth Certificate Image")
    national_id_image = fields.Image(string="National ID Image")
    administrative_requirements = fields.Many2many("administrative_requirements", string="Administrative Requirements")
    military_service = fields.One2many("military_service", "student", string="Military Service")
    military_courses = fields.One2many("students_military_courses", "student", string="Military Courses")
    graduation_information = fields.One2many("alumnus", "student", string="Graduation Information")
    transference_information = fields.One2many("transferred_students", "student", string="Transference Information")
    punishments = fields.One2many("students_punishments", "student", string="Punishments")
    finance_account = fields.One2many("students_finance_accounts",'student' ,string="Finance Account")
    total_payments = fields.Float(related="finance_account.total_payments")
    total_debts = fields.Float(related="finance_account.total_debts")
    admission_date = fields.Date(string="Admission Date", default=date.today())
    second_language_exemption = fields.Boolean(string="second language exemption")
    non_egyptians_certificates_docs = fields.Binary(string="non Egyptians Certificates")
    admission_revision_status = fields.Selection([('0', "Not Revised"), ('1', "Revised-OK"), ('2', "Revised-Error")],
                                                 default="0", string="Revision Status")
    notes=fields.One2many("students_notes", "student", string ="Notes")
    withdrawal_info=fields.One2many("withdrawals", "student", string ="withdrawal info")
    revised_by = fields.Many2one('res.users')
    # revised_by_name=fields.Char(related=revised_by.name)
    revision_notes = fields.Text(string="Revision Notes")
    is_latest = fields.Boolean(string="is Latest", default=True)
    is_latest = fields.Boolean(string="is Latest", default=True)
    accepted_by = fields.Many2one('res.users')
    accepted_on = fields.Date()
    imported_date = fields.Date()
    is_current=fields.Boolean("is Current")
    category_ids = fields.Many2many('students_category', 'students_category_rel', 'student_id', 'category_id', string='Tags')
    active = fields.Boolean('Active', default=True, store=True, readonly=False)
    departure_reason = fields.Selection([('fired', 'إداري'),('resigned', 'أكاديمي'),('retired', 'محاسبي')], string="نوع الغلق", copy=False)
    departure_description = fields.Text(string="سبب الغلق" ,copy=False)
    departure_date = fields.Date(string="تاريخ الغلق", copy=False)
    age_class = fields.Selection([('under18', 'under 18'),('18-25', 'between 18 and 25'),('over25', 'Over 25')])
    age = fields.Integer(compute="_compute_age_class")
    current_date = fields.Date(compute='_compute_current_date')
    withdrawal_date = fields.Date(string ="تاريخ الانسحاب")
    


    @api.model
    def _withdrawl(self):
        students = self.env['students'].browse(self._context.get('active_ids'))
        for student in students:
            if student.status == "7":
                raise exceptions.ValidationError("الطالب منسحب بالفعل")
            else:
                student.status = '7'
                student.withdrawal_date = date.today().strftime('%Y-%m-%d')


    @api.model
    def _birthdate(self):
        students = self.env['students'].browse(self._context.get('active_ids'))
        for student in students:
            national_id = student.national_id
            day = int(national_id[5:7])
            month = int(national_id[3:5])
            year = int(national_id[1:3])+2000
            birth_date = date(year,month,day)
            student.birth_date = birth_date
            student.total_percentage = (student.total_mark / 410.0)*100



    @api.depends()
    def _compute_current_date(self):
        self.current_date = date.today().strftime('%Y-%m-%d')

    @api.depends('current_date')
    def _compute_age_class(self):
        age=0
        for record in self:
            if record.birth_date != False:
                fmt='%Y-%m-%d'
                start_date = record.birth_date
                end_date = record.current_date
                d1 = datetime.strptime(str(start_date), fmt)
                d2 = datetime.strptime(str(end_date), fmt)
                age = int((int((d2 - d1).days))/365)
            record.age=age



    @api.model
    def compute_age_class(self):
        docs = self.env["students"].browse(self.env.context.get('active_ids'))
        for record in docs:
            age=0
            if record.birth_date != False:
                fmt='%Y-%m-%d'
                start_date = record.birth_date
                end_date = record.current_date
                d1 = datetime.strptime(str(start_date), fmt)
                d2 = datetime.strptime(str(end_date), fmt)
                age = int((int((d2 - d1).days))/365)
                record.age=age
            if age <= 18:
                record.age_class ="under18"
            elif age >= 25:
                record.age_class = "over25"
            else:
                record.age_class = "18-25"



    @api.model
    def create_accounts(self):
        students = self.env['students'].search([])
        accounts = self.env['students_finance_accounts']
        for student in students:
            account = accounts.create({'student': student.id})

    @api.model
    def server_action1(self):
        students = self.env['students'].search([('academic_semester', '=', 'Fall2020-2021')])
        accounts = self.env['students_finance_accounts']
        for student in students:
            account = accounts.search([('student', '=', student.id)])
            if account.total_payments > 1000.0:
                student.status = "3"

    @api.model
    def assign_image(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids'))
        for doc in docs:
            data = doc.env['students_data'].search([('student_id', '=', doc.student_id),('image_1920','=',True) ], limit=1)
            if data:
                doc.image_1920 = data.image_1920
            else:
                print("الصورة غير موجودة")

    @api.model
    def accept_student(self):

        for record in self:
            debts = record.env['bylaws_debts']

            semester = record.env['academic_semesters'].search([('code', '=', 'Fall2021-2022')])
            # new_account = (record.env['students_finance_accounts']).create({'student':record.id})
            account = record.finance_account
            student_debts = record.env['students_debts']
            if record.nationality.code == "1":
                record.citizenship = "1"
                record.finance_bylaw = record.faculty.current_financial_bylaw.id
            else:
                record.citizenship="0"
                record.finance_bylaw = record.faculty.current_financial_bylaw_non_egyptians.id
            faculty =record.env['faculties'].search([('code','=',record.faculty.code)],limit=1)
            mandatory_debts = debts.search([('bylaw', '=', record.finance_bylaw.id), ('priority', '=', 5)])
            for debt in mandatory_debts:
                new_debt = student_debts.sudo().create({'account': account.id, 'debt': debt.id, 'semester': semester.id})
            if record.study_type == 'postgraduate':
                record.student_id = str(int(record.faculty.postgraduate_students_academic_ids_counter[1:]) + 1)
                f = faculty.sudo().write({'postgraduate_students_academic_ids_counter': int(record.student_id)})
            else:
                record.student_id=str((record.faculty.students_academic_ids_counter)+1)
                f=faculty.sudo().write({'students_academic_ids_counter': int(record.student_id)})
                record.status="2"
            server = 'tcp:10.10.8.160\sql2019'
            database = 'ACUSDB'
            username = 'ACUSDB'
            password = 'Acu3@DB_-09'
            # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,)
            # cursor = cnxn.cursor()
            # cursor.execute("UPDATE StudentAcu set StudentStatusID = 2, StudentNo= ? where ApplicationNo =? ", self.student_id,self.id)
            # cnxn.commit()

    @api.model
    def create(self, values):
        record = super(students, self).create(values)
        if record.nationality.code != '1':
            record.citizenship = '2'
        study_language = 2
        if record.study_language == 'ar':
            study_language = 1
        # server = 'tcp:10.10.8.160\sql2019'
        # database = 'ACUSDB'
        # username = 'ACUSDB'
        # password = 'Acu3@DB_-09'
        # FacultyID = int(record.faculty.code)
        # JoinSemester = record.academic_semester.code
        # FullNameA = record.name_ar
        # FullNameE = record.name_en
        # ApplicationNo = record.id
        # NationalID = str(record.national_id)
        # StudentStatusID = int(record.status)
        # Citizenship = int(record.citizenship)
        # Gender = str(record.gender)
        # CityOfBirth = int(record.birth_country.code)
        # NationalityTypeID = int(record.nationality.code)
        # PlaceOfBirth = int(record.birth_governorate.code)
        # BirthDate = record.birth_date
        # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,)
        # cursor = cnxn.cursor()
        # cursor.execute("""INSERT INTO StudentAcu (FacultyID,FullNameA,FullNameE,Gender,ApplicationNo,NationalID,StudentStatusID,Citizenship,CityOfBirth,NationalityTypeID,PlaceOfBirth,BirthDate,SemesterStd,LanguageID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",FacultyID,FullNameA,FullNameE,Gender,ApplicationNo,NationalID,StudentStatusID,Citizenship,CityOfBirth,NationalityTypeID,PlaceOfBirth,BirthDate,JoinSemester,study_language)
        # # # cursor.execute("INSERT INTO StudentAcu (FacultyID,FullNameA,FullNameE) VALUES (?, ?, ?)",'1','2','3')
        # # cursor.execute("INSERT INTO StudentAcu(FullNameA,FullNameE) VALUES (?,?)", FullNameA, FullNameE)
        # # cursor.execute("insert into StudentAcu(FacultyID, FullNameA, FullNameE) values (1, 'Ahmed', 'Ahmed')")
        # # count = cursor.execute("""INSERT INTO AmacTest (FacultyID, FullNameA, FullNameE) VALUES (?,?,?)""",FacultyID, FullNameA, FullNameE).rowcount
        # cnxn.commit()
        # print('Rows inserted: ' + str(count))
        # cursor.commit()
        # cnxn.commit()
        # cursor.close()
        # cursor.execute("""INSERT INTO StudentBasicInfo (FullNameA) VALUES ('ahram')""")
        # cursor.execute("SELECT * FROM StudentAcu")
        # for row in cursor.fetchall():
        #     print(row)
        return record

    @api.model
    def test_query(self):
        server = 'tcp:10.10.8.160\sql2019'
        database = 'ACUSDB'
        username = 'ACUSDB'
        password = 'Acu3@DB_-09'
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password, )
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM StudentAcu")
        for row in cursor.fetchall():
            print(row)
        cnxn.close()



    def toggle_active(self):
        res = super(students, self).toggle_active()
        unarchived_employees = self.filtered(lambda employee: employee.active)
        unarchived_employees.write({
            'departure_reason': False,
            'departure_description': False,
            'departure_date': False
        })
        # archived_addresses = unarchived_employees.mapped('address_home_id').filtered(lambda addr: not addr.active)
        # archived_addresses.toggle_active()
        if len(self) == 1 and not self.active:
            return {
                'type': 'ir.actions.act_window',
                'id': 'student_departure_action',
                'res_model': 'student_departure',
                'view_mode': 'form',
                'target': 'new',
                'context': {'active_id': self.id},
                'views': [[False, 'form']]
            }
        return res

class StudentDepartureWizard(models.TransientModel):
        _name = 'student_departure.wizard'
        _description = 'Departure Wizard'
        departure_reason = fields.Selection([('fired', 'اكاديمي'),('resigned', 'إداري'),('retired', 'محاسبي')], string="سبب اغلاق الصفحة", default="fired")
        departure_description = fields.Text(string="تفاصيل الغلق")
        departure_date = fields.Date(string="تاريخ الغلق", required=True, default=fields.Date.today)
        student_id = fields.Many2one('students', string='Student', required=True,default=lambda self: self.env.context.get('active_id', None),)
        archive_private_address = fields.Boolean('غلق حساب الطالب', default=True)
        def action_register_departure(self):
            student = self.student_id
            student.departure_reason = self.departure_reason
            student.departure_description = self.departure_description
            student.departure_date = self.departure_date
            # if self.archive_private_address:
            #     # ignore contact links to internal users
            #     private_address = student.address_home_id
            #     if private_address and private_address.active and not self.env['res.users'].search(
            #         [('partner_id', '=', private_address.id)]):


class StudentCloseWizard(models.TransientModel):
        _name = 'student_departure'
        _description = 'Departure Wizard'
        departure_reason = fields.Selection([('fired', 'اكاديمي'), ('resigned', 'إداري'), ('retired', 'محاسبي')],
                                            string="سبب اغلاق الصفحة", default="fired")
        departure_description = fields.Text(string="تفاصيل الاغلاق")
        departure_date = fields.Date(string="تاريخ الاغلاق", required=True, default=fields.Date.today)
        student_id = fields.Many2one('students', string='Student', required=True,
                                     default=lambda self: self.env.context.get('active_id', None), )
        archive_private_address = fields.Boolean('اغلاق حساب الطالب', default=True)

        def action_register_departure(self):
            student = self.student_id
            student.departure_reason = self.departure_reason
            student.departure_description = self.departure_description
            student.departure_date = self.departure_date
            # if self.archive_private_address:
            #     # ignore contact links to internal users
            #     private_address = student.address_home_id
            #     if private_address and private_address.active and not self.env['res.users'].search(
            #         [('partner_id', '=', private_address.id)]):




class students_unenrollments(models.Model):
    _name="students_unenrollments"
    student=fields.Many2one("students", string='Student')
    student_name=fields.Char(related="student.name_ar")
    type = fields.Selection([('1', "Semester"), ('2', "Year")])
    user = fields.Many2one("res.users", string="User", default=lambda self: self.env.user)
    date=fields.Date(default=date.today(), string="Date")
    semester = fields.Many2one("academic_semesters", string='Semester')
    notes=fields.Text()



    @api.model
    def create(self, values):
        record = super(students_unenrollments, self).create(values)

        record.student.sudo().write({'enrollment_status' : '0'})

        # languages = {'ar': 'arabic', 'en': 'english'}
        # citizenships = {'egyptian': 'egyptians', 'non-egyptian': 'egyptians'}
        # students_account = record.env['students_financial_accounts'].search([('student','=',record.student.id)])
        # students_debts = self.env['students_debts']
        # semester = self.env['academic_semesters'].search([('is_current', '=', True)])
        # students_debts = record.env['students_debts'].search_count([('account', '=', students_account.id),('debt_type', '=', 2),('semester', '=', semester.id),('debt','=',3)])
        # print("22222222222222222")
        #
        # bylaw_debt = self.env['bylaws_debts'].search([('bylaw', '=', students_account.financial_bylaw.id),
        #                                                   ('citizenship', '=', citizenships[students_account.student.citizenship]),
        #                                                   ('code', '=', 14),
        #                                                   ('academic_year', '=', semester.year.id),
        #                                                   ('debt_type', '=', 2), (
        #                                                       'study_language', '=',
        #                                                       languages[students_account.student.study_language])], limit=1)
        # print("33333333333333333333333333333333")
        # self.env['students_debts'].create({'debt': bylaw_debt, 'account': students_account.id, 'semester': semester.id, })
        return record




class accepted_studnts(models.Model):
    _name="accepted_students"
    national_id=fields.Char()
    name_ar=fields.Char()
    certificate_type=fields.Char()

class students_notes(models.Model):
    _name="students_notes"
    student=fields.Many2one("students", string='Student')
    note=fields.Text(string="Note")
    by = fields.Many2one("res.users", string="updated by", default=lambda self: self.env.user)
    date=fields.Date(default=date.today(), string="Date")

class transferred_students(models.Model):
    _name = "transferred_students"
    _description = ""
    student = fields.Many2one("students")
    student_name=fields.Char(related="student.name_ar")
    country = fields.Many2one("countries")
    university = fields.Char()
    faculty = fields.Char()
    major = fields.Char()
    level = fields.Integer()
    faculty_approved_credit_hours = fields.Float()
    ministry_approved_credit_hours = fields.Float()
    gpa = fields.Float()


class alumnus(models.Model):
    _name = "alumnus"
    _description = ""
    _rec_name = "student"
    student = fields.Many2one("students")
    name_ar = fields.Char(related="student.name_ar")
    name_en = fields.Char(related="student.name_en")
    faculty = fields.Many2one(related="student.faculty", store=True)
    semester = fields.Many2one("academic_semesters", string="Semester")
    month = fields.Selection(related="semester.graduation_month")
    year = fields.Integer(related="semester.graduation_year")
    gpa = fields.Float(string="GPA")
    assessment = fields.Selection([('مقبول','مقبول'),('جيد','جيد'),('جيد جدا','جيد جدا'),('جيد جدا مع مرتبة الشرف','جيد جدا مع مرتبة الشرف'),('إمتياز','إمتياز'),('إمتياز مع مرتبة الشرف','إمتياز مع مرتبة الشرف')],string="Assessment")
    major = fields.Many2one("faculty_majors")
    minor = fields.Many2one("faculty_majors")
    student_status = fields.Selection(related="student.status", store=True)

    # @api.model
    # def create(self, values):
    #     # setup required data
    #     record = super(alumnus, self).create(values)
    #     student = record.env['students'].search([('id', '=', record.student.id)])
    #     a = student.write({'status': '6'})
    #     return record





class administrative_requirements(models.Model):
    _name = "administrative_requirements"
    _description = ""
    requirement_type = fields.Selection([("1", "Supplementary Subject"), ("2", "papers")])
    requirement_name = fields.Char()


class students_punishments(models.Model):
    _name = "students_punishments"
    _description = ""
    student = fields.Many2one("students", string="Student")
    semester = fields.Many2one("academic_semesters", string="Semester")
    number = fields.Integer(string="Number")
    date = fields.Date(string="Date")
    case = fields.Text(string="Case")
    punishment = fields.Many2many("punishments", string="Punishments")


class punishments(models.Model):
    _name = "punishments"
    code = fields.Char()
    name_en = fields.Char()
    name_ar = fields.Char()
    details=fields.Text()

class withdrawals(models.Model):
    _name="withdrawals"
    student=fields.Many2one("students")
    student_name=fields.Char(related="student.name_ar")
    student_faculty=fields.Char(related="student.faculty.name_ar")
    student_status=fields.Selection(related="student.status")
    withdrawal_semester=fields.Many2one("academic_semesters")
    reason=fields.Text()
    request_date=fields.Date()
    date=fields.Date(default=date.today(), string="Date")
    by = fields.Many2one("res.users", string="updated by", default=lambda self: self.env.user)

    @api.model
    def create(self, values):
        # setup required data
        record = super(withdrawals, self).create(values)
        student = record.env['students'].search([('id','=',record.student.id)])
        a=student.write({'status':'7'})
        return record


class military_service(models.Model):
    _name = "military_service"
    _rec_name="student"
    student = fields.Many2one("students")
    student_gender = fields.Selection(related="student.gender", store=True)
    student_name = fields.Char(related="student.name_ar")
    faculty = fields.Many2one(related="student.faculty", store=True)
    academic_year = fields.Many2one(related="student.academic_year", string="Year", store=True)
    student_status = fields.Selection(related="student.status", store=True)
    number = fields.Char(compute="_compute_number")
    birth_year=fields.Integer()
    region = fields.Many2one("military_service_regions")
    region_code = fields.Integer(related="region.code")
    center_name_ar = fields.Char(related="region.center_name_ar")
    military_region = fields.Char(related="region.region", store=True)
    governorate = fields.Many2one(related="region.governorate")
    serial=fields.Integer(string="الرقم المسلسل")
    decision_number = fields.Char(string="القرار")
    decision = fields.Many2one("military_decisions", string="القرار")
    decision_state = fields.Many2one(related="decision.state", store=True)
    decision_text = fields.Char(related="decision.text")
    military_paper_status = fields.Selection([('1', 'مستكمل'), ('2', 'غير مستكمل')], string="استكمال الاوراق")
    papers = fields.Selection([('1','2 جند'),('2','6 جند'),('3','2 جند و 6 جند'),('4','شهادة الإعفاء')])
    date = fields.Date()
    level = fields.Integer(compute="_compute_level", string="عدد سنوات الدراسة")


    @api.depends('birth_year','region','serial','military_paper_status')
    def _compute_number(self):
        for record in self:
            record.number=str(record.birth_year)+"/"+str(record.region_code)+"/"+str(record.serial)


    @api.depends("academic_year")
    def _compute_level(self):
        current_year = self.env['academic_years'].search([('is_current', '=', True)])
        for record in self:
            years = (current_year.end_year) - (record.academic_year.start_year)
            record.level = years
            if years > record.faculty.levels:
                record.level  = record.faculty.levels









class military_service_regions(models.Model):
    _name = "military_service_regions"
    _rec_name="code"
    code = fields.Integer()
    center_name_ar = fields.Char()
    center_name_en = fields.Char(string="Center")
    region = fields.Char()
    governorate = fields.Many2one("governorates")
    students = fields.One2many("military_service", "region")


class military_decisions(models.Model):
    _name = "military_decisions"
    _rec_name="text"
    code = fields.Char()
    state = fields.Many2one("military_states")
    text = fields.Char()

class military_states(models.Model):
    _name = "military_states"
    _rec_name="name"
    code = fields.Char()
    name = fields.Char()





class military_courses(models.Model):
    _name = "military_courses"
    _rec_name = "number"
    number=fields.Integer()
    year=fields.Many2one("academic_years")
    semester=fields.Many2one("academic_semesters")
    date_from=fields.Date()
    date_to=fields.Date()
    location=fields.Char()
    students=fields.One2many("students_military_courses","course")



class students_military_courses(models.Model):
    name = 'students_military_courses'
    _rec_name = "student"
    student=fields.Many2one(comodel_name="students", string="Student")
    student_name=fields.Char(related="student.name_ar", string="Name")
    faculty=fields.Char(related="student.faculty.name_ar", string="Faculty")
    national_id=fields.Char(related="student.national_id", string="National ID")
    course=fields.Many2one(comodel_name="military_courses", string="Military Course")
    registration_date=fields.Date(default=date.today(), string="Date")
    registration_receipt=fields.Char(string="Receipt")
    attendance = fields.Selection([('0','Did not attend'),('1',"attend")], string="Attendance")
    result = fields.Selection([('0','Fail'),('1',"Pass")], string="Result")

    evaluation_1=fields.Integer()
    evaluation_2=fields.Integer()
    evaluation_3=fields.Integer()
    evaluation_4=fields.Integer()
    evaluation_total=fields.Integer()
    evaluation_grade=fields.Char()




class graduation_party_info(models.Model):
    _name = "graduation_party_info"
    _rec_name = "student_id"
    student_id = fields.Integer(string="Student ID")
    faculty = fields.Many2one("faculties", string="Faculty")
    name_en = fields.Char(string="Student Name English")
    name_ar = fields.Char(string="Student Name Arabic")
    birth_date = fields.Date(string="Birth Date")
    image_1920 = fields.Image(string="Student Image")
    student_image = fields.Image(filename=lambda self: self.student_id)
    gpa = fields.Float(string="CGPA")
    grade = fields.Selection([('1', "Pass"), ('2', "Good"), ('3', "Very Good"), ('4', "Excellent")], string="Grade")
    gender = fields.Selection([('male', "male"), ('female', "female")], string="Gender")
    semester = fields.Selection([('1', "Fall"), ('2', "Spring"), ('3', 'Summer')], string="Graduation Semester")
    will_attend = fields.Selection([('0', "No"), ('1', "Yes")],
                                   string="are you planning to attend the graduation ceremony?")
    number_of_extra_tickets = fields.Selection([('0', "0"), ('1', "1"), ('2', "2"), ('3', "3")],
                                               string="do you need more then 2 invitations?(will be charged)")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Phone Number")

    # @api.model
    # def create(self, values):
    #     record = super(graduation_party_info, self).create(values)
    #     domain=[('dob','=',record.birth_date),('student_id','=',record.student_id)]
    #     count=record.env['auth'].search_count(domain)
    #     for i in "aaaaaaaaaaaaaaaaaaaaaaa":
    #         print(i)
    #     if (count==0):
    #         raise exceptions.ValidationError("Unregistered Student / Invalid File and receipt number Combintion")
    #     return record


class auth(models.Model):
    _name = "auth"
    student_id = fields.Integer()
    dob = fields.Date()
    name = fields.Char()


class students_data(models.Model):
    _name = "students_data"
    _rec_name = "student_id"
    student_id = fields.Char(string="Student ID")
    file_number = fields.Char(string="File Number")
    image_1920 = fields.Image(string="Student Image")
    name_ar = fields.Char(string="Name Ar")
    name_en = fields.Char(string="Name En")
    birth_date = fields.Date(string="Date of Birth")
    birth_governorate = fields.Many2one("governorates", string="Birth Governorate")
    birth_country = fields.Many2one("countries", string="Birth Country")
    gender = fields.Selection([('1', 'Male'), ('2', 'Female')], string="Gender")
    nationality = fields.Many2one("countries", string="Nationality")
    national_id = fields.Char(size=14, string="National ID")
    email_address = fields.Char(string="Email")
    phone_number = fields.Char(string="Phone Number")
    mobile_number = fields.Char(string="Mobile Number")
    address = fields.Char(string="Address")
    high_school_certificate_type = fields.Selection(
        [("1", "Egyptian High School"), ("2", "Azhar High School"), ("3", "Arabic"), ("4", "Western")],
        string="High School Type")
    high_school_certificate_major = fields.Selection([("3", "Literary"), ("1", "Science"), ("2", "Math")],
                                                     string="High School Major")
    high_school_certificate_country = fields.Many2one("countries", string="High School Country")
    notes = fields.Text(string="Notes")

    @api.model
    def create(self, values):
        record = super(students_data, self).create(values)
        domain = [('student_id', '=', record.student_id), ('file_number', '=', record.file_number)]
        count = record.env['students'].search_count(domain)
        if (count == 0):
            raise exceptions.ValidationError("رقم الطالب و رقم الملف غير مسجلين برجاء مراجعة الكلية")
        else:
            student = record.env['students'].search(domain)
            record.image_1920 = record.image_1920
            data = student.write({'name_ar': record.name_ar, 'image_1920': record.image_1920, 'name_en': record.name_en,
                                  'birth_date': record.birth_date, 'birth_governorate': record.birth_governorate,
                                  'birth_country': record.birth_country, 'gender': record.gender,
                                  'nationality': record.nationality, 'national_id': record.national_id,
                                  'email_address': record.email_address, 'phone_number': record.phone_number,
                                  'mobile_number': record.mobile_number, 'address': record.address,
                                  'high_school_certificate_type': record.high_school_certificate_type,
                                  'high_school_certificate_major': record.high_school_certificate_major,
                                  'high_school_certificate_country': record.high_school_certificate_country,
                                  'status': "3"})

        return record




class auth2(models.Model):
    _name = "auth2"
    student_id = fields.Integer()
    file_number = fields.Integer()


class payments_dates(models.Model):
    _name = "payments_dates"
    payment = fields.Integer()
    student = fields.Char()
    d = fields.Integer()
    m = fields.Integer()
    y = fields.Integer()
    date = fields.Date()
    is_valid = fields.Integer()

    @api.model
    def update_payment_date(self):
        dates = self.env['payments_dates'].search([])
        for d in dates:
            payment = d.env['students_payments'].search([('old_id', '=', 11342)])
            print(payment.old_id)
            new_date = payment.write({"date2": str(d.payment)})
            print(new_date)


class files_check(models.Model):
    _name = "files_check"
    student_id = fields.Char(string="Student ID")

    @api.model
    def create(self, values):
        record = super(files_check, self).create(values)
        domain = [('student_id', '=', record.student_id)]
        count = record.env['students'].search_count(domain)
        student = record.env['students'].search(domain, limit=1)
        if student.file_number != 0:

            raise exceptions.ValidationError("Student file number is : " + str(student.file_number))
        else:
            raise exceptions.ValidationError("رقم الطالب و رقم الملف غير مسجلين برجاء شئون الطلاب")
        return record


class file_numbers(models.Model):
    _name = "file_numbers"
    student_id = fields.Char(string="Student ID")
    file_number = fields.Integer(string="File Number")
    by = fields.Many2one("res.users", string="updated by", default=lambda self: self.env.user)

    @api.model
    def create(self, values):
        record = super(file_numbers, self).create(values)
        domain = [('student_id', '=', record.student_id)]
        count = record.env['students'].search_count(domain)
        student = record.env['students'].search(domain, limit=1)
        if count != 0:
            data = student.write({"file_number": record.file_number})
        else:
            raise exceptions.ValidationError("الطالب غير مسجل ..برجاء تسجيل الطالب اولا")
        return record


class payments_details_report(models.AbstractModel):
    _name = 'report.acums.daily_payments_details'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        faculties = []
        payments_methods = []
        payments_types = []
        payments = self.env['payments_details'].search([('id', '=', docids)])
        for payment in payments:
            faculties.append(payment.faculty.name_ar)
            payments_types.append(payment.debt_type_name)
            payments_methods.append(payment.method.name_ar)
            docs.append({
                'payment': payment,

            });
        faculties.sort()
        payments_types.sort()
        return {
            'doc_ids': docids,
            'doc_model': 'acums.payments_details',
            'faculties': list(set(faculties)),
            'debts_types': list(set(payments_types)),
            'payments_methods': list(set(payments_methods)),
            'docs': docs,
        }


class acu_hr(models.Model):
    _name = "hr.employee"
    _inherit = ['hr.employee']
    certificate = fields.Selection([
        ('bachelor', 'Bachelor'),
        ('ba', 'ba'),
        ('literacy', 'literacy'),  # محو أمية
        ('without', 'Without'),
        ('junior', 'junior'),
        ('primary', 'primary'),
        ('high school', 'high school'),
        ('middle', 'middle'),
        ('2 year institute', '2 year institute'),
        ('master', 'Master'),
        ('phd', 'phd'),
        ('other', 'Other'),
    ], 'Certificate Level', default='other', groups="hr.group_hr_user", tracking=True)

    job_class = fields.Selection([
        ('Faculty member', 'Faculty member'),
        ('teaching assistant', 'teaching assistant'),
        ('administrative', 'administrative'),
        ('other', 'Other'),
    ], 'Job Class', default='other', groups="hr.group_hr_user", tracking=True)

    religion = fields.Selection([
        ('muslim', 'muslim'),
        ('christian', 'christian'),
        ('jewish', 'jewish'),
        ('other', 'Other'),
    ], 'religion', default='other', groups="hr.group_hr_user", tracking=True)

    insurance_number = fields.Char(string="Insurance Number")
    medical_insurance_number = fields.Char(string="Medical Insurance Number")
    employee_code = fields.Integer(string="employee code")
    birth_governorate = fields.Many2one("governorates", string="Birth Governorate")
    birth_region = fields.Char(string="Birth Region")
    insurance_date = fields.Date(string="Insurance Date")
    hire_date = fields.Date(string="Hire Date")
    hire_days = fields.Integer(string="Hide Days", compute="_compute_hire_days", default=0)
    time_off_credit = fields.Selection([('30', '30'), ('21', '21'), ('3', '3'), ('10', '10')], string="ايام الاجازة")

    @api.onchange('time_off_credit')
    def onChange(self):
        if self.time_off_credit == "30":
            self.category_ids = [(4, 8)]

    @api.depends("hire_date", "hire_days")
    def _compute_hire_days(self):
        curr = date.today()
        if self.hire_date != False:
            days_diff = (curr - (self.hire_date)).days
            print(days_diff)
            self.hire_days = days_diff

        if self.hire_days >= 3600:
            print(self.hire_days)
            self.category_ids = [(4, 8,)]

# class payments_update_date(models.Model):
#     _name = "payments_update_date"
#     payment = fields.Integer()
#     student = fields.Char()
#     y = fields.Integer()
#     m = fields.Integer()
#     day = fields.Integer()
#     date=fields.Integer()



# Payment_Receipt_Report
class PaymentReceiptCustomReport(models.AbstractModel):
    _name = 'report.acums.students_payments_receipt'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        bank_notice=False
        # dic ={"1": "نقدي", "2": "إشعار بنكي", "3": "حوالة بريدية"}
        payments = self.env['students_payments'].search([('id', '=', docids)])

        for payment in payments:
            arabic_amount = "فقط "
            curr = {'1': 'جنيه مصري', '2': 'دولار'}
            # if payment.printed == True:
            #     raise exceptions.ValidationError('لقد تم طباعة الايصال من قبل')
            if payment.method.code==2:
                bank_notice = self.env["bank_notices"].search([('payment','=',payment.id)])
            arabic_amount = (arabic_amount + str(num2words(payment.amount, lang="ar")) + " " + str(curr[payment.currency]) + " لا غير").replace("‫‪،‬‬", "و")
            num2words(payment.amount, lang="ar")

            docs.append({
                'payments': payment,
                'arabic_amount': arabic_amount,
                'curr': str(curr[payment.currency]),
                'bank_notice': bank_notice,
            });
            payment.printed = True

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students_payments',
            'docs': docs,

        }

#logistics System
class  purchase_requisitions(models.Model):
    _name="purchase_requisitions"
    number=fields.Integer(string="Requisition Number")
    date=fields.Date(string="Requisition Date")
    quotations=fields.One2many("quotations","requisition", string="Requisition Quotations")
    items=fields.One2many("purchase_requisitions_items","requisition", string="Purchase Requisitions Items")
    requisition = fields.Many2one("stock_requisitions")
    status=fields.Selection([('draft','draft'),('approved','approved'),('process','in process')], defult="draft")
    by=fields.Many2one("res.users", string="by", default=lambda self: self.env.user)


class purchase_requisitions_items(models.Model):
    _name="purchase_requisitions_items"
    requisition=fields.Many2one("purchase_requisitions")
    item=fields.Many2one("items")
    quantity=fields.Float()

class quotations(models.Model):
    _name="quotations"
    number = fields.Integer(string="Quotation Number")
    requisition=fields.Many2one("purchase_requisitions")
    supplier=fields.Many2one("suppliers", string="Supplier")
    date=fields.Date(string="Date")
    technical_document=fields.Binary(string="Technical Proposal Document")
    financial_document=fields.Binary(string="Financial Proposal Document")
    status=fields.Selection([('0','Under Revision'),('1','Rejected'),('2','Accepted')], defult="0")


class purchase_orders(models.Model):
    _name="purchase_orders"


class suppliers(models.Model):
    _name="suppliers"

class purchase_invoices(models.Model):
    _name="purchase_invoices"

class purchase_payments(models.Model):
    _name="purchase_payments"

class items_tests(models.Model):
    _name="items_tests"

class supply_orders(models.Model):
    _name="supply_orders"

class stock_requisitions(models.Model):
    _name="stock_requisitions"

class warehouses(models.Model):
    _name="warehouses"
    parent=fields.Many2one("warehouses", default=False)
    number=fields.Integer()
    name=fields.Char()
    locations=fields.Many2one("locations")

class warehouses_stocks(models.Model):
    _name="warehouses_stocks"

class warehouses_transactions_types(models.Model):
    _name = "warehouses_transactions_types"
    code=fields.Char()
    name_en=fields.Char()
    name_ar=fields.Char()

class warehouses_transactions(models.Model):
    _name = "warehouses_transactions"
    type=fields.Many2one("warehouses_transactions_types")
    date=fields.Date()
    name_ar=fields.Char()

class warehouses_issues_details(models.Model):
    _name="warehouses_issues_details"
    transaction=fields.Many2one("warehouses_transactions")

class warehouses_received_details(models.Model):
    _name="warehouses_received_details"
    transaction=fields.Many2one("warehouses_transactions")

class warehouses_returns_details(models.Model):
    _name="warehouses_returns_details"
    transaction=fields.Many2one("warehouses_transactions")


class warehouses_transfers_details(models.Model):
    _name="warehouses_transfers_details"
    transaction=fields.Many2one("warehouses_transactions")


class items(models.Model):
    _name="items"
    code=fields.Char(string="Code")
    name=fields.Char(string="Code")
    category=fields.Many2one("categories",string="Category")
    attributes=fields.One2many("items_attributes_values","item", string="Attributes")
    unit_of_measure=fields.Many2one("units_of_measure", string="Unit Of Measure")



class items_categories(models.Model):
    _name="items_categories"
    code=fields.Char()
    name=fields.Char()
    attributes=fields.One2many("items_attributes","category")

class items_attributes(models.Model):
    _name="items_attributes"
    category=fields.Many2one("items_categories")
    name=fields.Many2one("items_categories")

class items_attributes_values(models.Model):
    _name="items_attributes_values"
    category=fields.Many2one("items_categories")
    item=fields.Many2one("items")
    attribute=fields.Many2one("items_attributes")
    value=fields.Char()

class unit_of_measure(models.Model):
    _name="units_of_measure"
    code=fields.Char()
    name=fields.Char()



class students_certificates(models.TransientModel):
    _name="students_certificates"
    type=fields.Selection([('1','بيان حالة'),('2','شهادة قيد'),('3','شهادة قبول مبدئي'),('4','شهادة حسن سير وسلوك'),('5','افادة سحب'),('6','شهادة تدريب'),('7','حافظة تجنيد'),('8','شهادة قيد بالانجليزية'),('9','شهادة تدريب بالانجليزية')], string="Certificate Type")
    # type=fields.Many2one("certificates_types", string="Certificate Type")
    level=fields.Selection([('الاول','الاول'),('الثاني','الثاني'),('الثالث','الثالث'),('الرابع','الرابع'),('الخامس','الخامس'),('خريج','خريج')], string="Level")
    to=fields.Char(string="To")
    notes=fields.Text(string="Notes")
    military=fields.Boolean(string="بيانات التجنيد")
    date = fields.Date(string="Date", default=date.today())
    gpa = fields.Float(string="GPA")


    def print_report(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        students = self.env['students'].search([('id', '=', docs.id)])
        data = {
            'model': 'students_certificates',
            'form': self.read()[0],
            'student': students[0].id,
        }
        report = self.env.ref('acums.report_student_certificate')
        if data['form']['type'] == '7':
            report.sudo().paperformat_id = self.env.ref('__export__.report_paperformat_6_fad872ce').id
            return report.with_context(lanscape=True).report_action(self, data=data, config=False)
        else:
            report.sudo().paperformat_id = self.env.ref('base.paperformat_euro').id
            return report.report_action(self, data=data,config=False)


# Payment_Receipt_Report
class StudentCertificatetCustomReport(models.AbstractModel):
    _name = 'report.acums.student_certificate'

    @api.model
    def _get_report_values(self, docids, data=None):
        x = data['student']
        academic_year = (self.env["academic_years"].search([('is_enrollment','=',True)])).code
        type=data['form']['type']
        to=data['form']['to']
        level=data['form']['level']
        notes=data['form']['notes']
        date=data['form']['date']
        military=data['form']['military']
        gpa=data['form']['gpa']
        notes_lines=[]
        if notes !=False:
            notes_lines=notes.splitlines()
        students=self.env['students'].search([('id','=',int(x))])
        students=self.env['students'].search([('id','=',int(x))])
        docs = []
        for student in students:
            b=str(student.birth_date)
            student_birth_date=b[0:2]+"-"+b[3:5]+"-"+b[6:10]
            docs.append({'student': student, 'type' : type, 'to' : to, 'level' : level,'notes': notes_lines, 'academic_year': academic_year ,'military': military, 'date': date, 'english_date': student_birth_date, 'gpa': gpa, })
        return {
            'doc_ids': docids,
            'doc_model': 'acums.students',
            'docs': docs,
        }

# Payment_request_Report
class DetailedPaymentRequestCustomReport(models.AbstractModel):
    _name = 'report.acums.detailed_payment_request'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        accounts = self.env['students_finance_accounts'].search([('id', '=', docids)])
        for account in accounts:
            docs.append({
                'account': account,
                'debts':account.debts,
            });

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students_finance_accounts',
            'docs': docs,
        }

class DetailedPaymentRequestCustomReportStudents(models.AbstractModel):
    _name = 'report.acums.detailed_payment_request_students'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['students'].search([('id', '=', docids)])
        for student in students:
            docs.append({
                'student': student,
            });

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students',
            'docs': docs,
        }


# Payment_request_Report
class FilePaymentRequestCustomReport(models.AbstractModel):
    _name = 'report.acums.file_payment_request'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['students'].search([('id', '=', docids)])
        semester = self.env['academic_semesters'].search([('code', '=', 'Fall2021-2022')])

        for student in students:
            count = self.env['students_finance_accounts'].search_count([('student','=',student.id)])
            if count == 0:
                new_account = (self.env['students_finance_accounts']).create({'student': student.id})
                if student.nationality.code == "1":
                    student.citizenship = "1"
                    student.finance_bylaw = student.faculty.current_financial_bylaw.id
                else:
                    student.citizenship = "0"
                    student.finance_bylaw = student.faculty.current_financial_bylaw_non_egyptians.id

            docs.append({
                'student': student,
            });

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students',
            'docs': docs,
        }




# اذن دفع ملف
class DetailedPaymentRequestCustomReport(models.AbstractModel):
    _name = 'report.acums.students_affairs_payment'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['students'].search([('id', '=', docids)])
        for student in students:
            docs.append({
                'student': student,
            });

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students',
            'docs': docs,
        }



# Temporary ID
class DetailedPaymentRequestCustomReport(models.AbstractModel):
    _name = 'report.acums.students_temp_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['students'].search([('id', '=', docids)])

        for student in students:
            exam=self.env["english_exams"].search([('student','=',student.id)], limit=1)
            docs.append({
                'student': student,
                'exam': exam
            });

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students',
            'docs': docs,
        }


# Temporary ID
class AcademicIDustomReport(models.AbstractModel):
    _name = 'report.acums.student_academic_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['students'].search([('id', '=', docids)])

        for student in students:
            exam=self.env["english_exams"].search([('student','=',student.id)], limit=1)
            docs.append({
                'student': student,
                'exam': exam
            });

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students',
            'docs': docs,
        }

class notes_lines(models.TransientModel):
    _name="notes_lines"
    _rec_name="line"
    line=fields.Char()
    certificate = fields.Many2one("students_certificates")

class expected_students(models.Model):
    _name= "expected_students"
    _rec_name="student"
    student=fields.Char()
    date = fields.Date(string="Date", default=date.today())
    user = fields.Many2one("res.users", string="Agent", default=lambda self: self.env.user)

    @api.model
    def create(self, values):
        record = super(expected_students, self).create(values)
        student=self.env['students'].search([('student_id','=',record.student)])
        student.status="3"
        return record


class english_exams(models.Model):
    name="english_exams"
    _rec_name="student"
    student=fields.Many2one("students")
    exam=fields.Char()
    date = fields.Char()
    time=fields.Char()
    building = fields.Char()
    room =fields.Char()





# Payment_Receipt_Report
class CurrentSemesterPayments(models.AbstractModel):
    _name = 'report.acums.students_accounting_reports'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        accounts = self.env["students_finance_accounts"].search([('id', '=', docids)])
        semester = self.env['academic_semesters'].search([('is_current', '=', True)])
        for account in accounts:
            print(account)
            mandatory_debts=0.0
            extra_debts=0.0
            mandatory_payments=0.0
            extra_payments=0.0
            status = ""
            debts= self.env["students_debts"].search([('account', '=', account.id),('semester','=',semester.id)])
            for debt in debts:
                if debt.debt_type.code == 2 :
                    mandatory_debts = mandatory_debts + debt.to_pay_amount
                    mandatory_payments = mandatory_payments + debt.payed
                elif debt.debt_type.code == 11:
                    extra_debts = extra_debts + debt.to_pay_amount
                    extra_payments = extra_payments + debt.payed
            balance = (-1*(mandatory_debts+extra_debts))+(mandatory_payments+extra_payments)
            if balance == 0.0:
                status ="Balanced"
            elif balance > 0.0:
                status = "credit"
            elif balance < 0.0:
                status = "debit"
            docs.append({'account': account, 'mandatory_debts' : mandatory_debts, 'mandatory_payments' : mandatory_payments, 'extra_debts' : extra_debts,'extra_payments': extra_payments, 'balance': balance, 'status': status})
        return {
            'doc_ids': docids,
            'doc_model': 'acums.students_finance_accounts',
            'docs': docs,
        }


# Application_Form_Report
class application_form_report(models.AbstractModel):
    _name = 'report.acums.students_application_form'
    @api.model
    def _get_report_values(self, docids, data=None):
        docs=[]
        students = self.env['students'].search([('id', '=', docids)], order="name_ar asc")
        global_data = self.env['global_data'].search([('id','=',1)], limit=1)


        for student in students:
            # if(student.student_id== False) :
            #     raise exceptions.ValidationError('هذاالطالب ليس مقيد')
            docs.append({
                'students': student,
                'global_data': global_data,

            });

        return {
                'doc_ids': docids,
                'doc_model': 'acums.students',
                'docs': docs,
            }

class ministry_report(models.AbstractModel):
    _name = 'report.acums.ministry_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['students'].search([('id', '=', docids)], order="name_ar asc")
        global_data = self.env['global_data'].search([('id', '=', 1)], limit=1)
        students_list=[]
        count=1
        l = len(students)
        iteration= 0
        for student in students:
            iteration=iteration+1
            faculty = student.faculty.name_ar
            application_type = student.application_type
            certificate_type = student.high_school_certificate_type
            semester = student.academic_semester.name_ar
            students_list.append(student)
            count = count +1
            if count % 15 == 0 or ((iteration == l) and len(students_list) <15):
                docs.append({
                    'student': students_list,
                });
                students_list = []

        return {
            'doc_ids': docids,
            'doc_model': 'acums.students',
            'docs': docs,
            'faculty':faculty,
            'global_data':global_data[0],
            'application_type':application_type,
            'certificate_type':certificate_type,
            'semester':semester,
        }


# #
class miliatry_report(models.AbstractModel):
    _name = 'report.acums.miliatry_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['military_service'].search([('id', '=', docids)])
        for student in students:
            faculty = student.faculty.name_ar
            level = student.level
            state = student.decision_state.name
            docs.append({
                'student': student,
            });
        # report = self.env.ref('acums.ministry_report')
        # if application_type == '2':
        #     self.sudo().paperformat_id = self.env.ref('__export__.report_paperformat_6_fad872ce').id
        #     delf.with_context(lanscape=True).report_action(self, data=data, config=False)
        # else:
        #     self.sudo().paperformat_id = self.env.ref('base.paperformat_euro').id
        #     self.report_action(self, data=data, config=False)

        return {
            'doc_ids': docids,
            'doc_model': 'acums.military_service',
            'docs': docs,
            'faculty':faculty,
            'level':level,
            'state':state,
        }
#
class visitors_locations(models.Model):
    _name= "visitors_locations"
    _rec_name = "name_ar"
    name_ar = fields.Char()
    name_en = fields.Char()
    location_type = fields.Selection([('faculty','faculty'),('department','department'),('external','external')])

class visitors(models.Model):
    _name= "visitors"
    _rec_name = "name_ar"
    name_ar = fields.Char()
    name_en = fields.Char()
    location = fields.Many2one("visitors_locations")
    location_name = fields.Char(related="location.name_ar")
    title = fields.Char()
    notes = fields.Text()

class visits_types(models.Model):
    _name= "visits_types"
    location_name = fields.Char()
    location_type = fields.Selection([('faculty','faculty'),('department','department'),('external','external')])

class visits(models.Model):
    _name= "visits"
    location_name = fields.Char()
    location_type = fields.Selection([('faculty','faculty'),('department','department'),('external','external')])

class high_schools_names(models.Model):
    _name= "high_schools_names"
    _rec_name = 'name_ar'
    code = fields.Char()
    name_ar = fields.Char()
    name_en = fields.Char()
    type = fields.Selection([('egyptian','egyptian'),('arabic','arabic'),('western','western')])





# class MinistryReportWizard(models.TransientModel):
#         _name = 'ministry_report_wizard'
#         _description = 'Ministry Report Wizard'
#         report = self.env.ref('acums.report.acums.ministry_report')
#         faculty = fields.Many2one("faculties")
#         paoer_format = fields.Selection([])
#         high_school_type = fields.Selection([('ثانوية عامة', 'ثانوية عامة'), ('عربية', 'عربية'), ('أجنبية', 'أجنبية')],
#                                             string="نوع الشهادة")
#         application_type = fields.Selection([('محول', 'محول'), ('مستجد', 'مستجد')], string="نوع التقديم")
#         nationality = fields.Selection([('مصريين', 'مصريين'), ('وافدين', 'وافدين')], string="الجنسية")
#

