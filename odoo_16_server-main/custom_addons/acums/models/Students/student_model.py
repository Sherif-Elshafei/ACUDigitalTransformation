from datetime import date

from odoo import models, fields, api, exceptions
from odoo.tools.populate import randint


class students(models.Model):
    _name = "students"
    _description = ""
    _rec_name = "student_id"

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
    # high_school_certificate_name = fields.Many2one('high_schools_names', string='High School Name')
    # high_school_type = fields.Selection(related='high_school_certificate_name.type',store=True, string='High School Type')
    # high_school_certificate_major = fields.Selection([("3", "Literary"), ("1", "Science"), ("2", "Math")],
    #                                                 string="High School Major")
    high_school_certificate_country = fields.Many2one("countries", string="High School Country")
    high_school_certificate_year = fields.Integer(string="High School year")
    total_mark = fields.Float(string="High School Mark")
    total_percentage = fields.Float(string="High School Percentage")
    seat_number = fields.Integer(string="High School Seat Number")
    # finance_bylaw = fields.Many2one("finance_bylaws", string="Finance Bylaw")
    # academic_bylaw = fields.Many2one("academic_bylaws", string="Academic ByLaw")
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
    study_language = fields.Selection([('ar', 'Arabic'), ('en', 'English')], string="Study Language", default="en")
    # faculty_major = fields.Many2one("faculty_majors", string="Faculty Major")
    status = fields.Selection(
        [('0', "Willing"), ('1', "Applicant"), ('2', "Accepted"), ('3', "Student"), ('4', "Expected"),
         ('5', "not fulfilled"), ('6', 'Alumni'), ('7', 'Withdrawn')], string="Student Status", default="0")
    enrollment_status = fields.Selection([('1', "مقيد"), ('0', "غير مقيد")], default="1",string="Enrollment Status")
    image_1920 = fields.Image(string="Student Image")
    certificate_image = fields.Image(string="High School Certificate Image")
    birth_image = fields.Image(string="Birth Certificate Image")
    national_id_image = fields.Image(string="National ID Image")
    #administrative_requirements = fields.Many2many("administrative_requirements", string="Administrative Requirements")
    # military_service = fields.One2many("military_service", "student", string="Military Service")
    # military_courses = fields.One2many("students_military_courses", "student", string="Military Courses")
    # graduation_information = fields.One2many("alumnus", "student", string="Graduation Information")
    # transference_information = fields.One2many("transferred_students", "student", string="Transference Information")
    # punishments = fields.One2many("students_punishments", "student", string="Punishments")
    # finance_account = fields.One2many("students_finance_accounts" , string="Finance Account")
    # total_payments = fields.Float(related="finance_account.total_payments")
    # total_debts = fields.Float(related="finance_account.total_debts")
    admission_date = fields.Date(string="Admission Date", default=date.today())
    second_language_exemption = fields.Boolean(string="second language exemption")
    # non_egyptians_certificates_docs = fields.Binary(string="non Egyptians Certificates")
    admission_revision_status = fields.Selection([('0', "Not Revised"), ('1', "Revised-OK"), ('2', "Revised-Error")],
                                                 default="0", string="Revision Status")
    # notes=fields.One2many("students_notes", "student", string ="Notes")
    # withdrawal_info=fields.One2many("withdrawals", "student", string ="withdrawal info")
    # revised_by = fields.Many2one('res.users')
    # revised_by_name=fields.Char(related=revised_by.name)
    revision_notes = fields.Text(string="Revision Notes")
    is_latest = fields.Boolean(string="is Latest", default=True)
    is_latest = fields.Boolean(string="is Latest", default=True)
    # accepted_by = fields.Many2one('res.users')
    accepted_on = fields.Date()
    imported_date = fields.Date()
    is_current=fields.Boolean("is Current")
    # category_ids = fields.Many2many('students_category', 'students_category_rel', 'student_id', 'category_id', string='Tags')
    active = fields.Boolean('Active', default=True, store=True, readonly=False)
    departure_reason = fields.Selection([('fired', 'إداري'),('resigned', 'أكاديمي'),('retired', 'محاسبي')], string="نوع الغلق", copy=False)
    departure_description = fields.Text(string="سبب الغلق" ,copy=False)
    departure_date = fields.Date(string="تاريخ الغلق", copy=False)
    age_class = fields.Selection([('under18', 'under 18'),('18-25', 'between 18 and 25'),('over25', 'Over 25')])
    # age = fields.Integer(compute="_compute_age_class")
    # current_date = fields.Date(compute='_compute_current_date')
    withdrawal_date = fields.Date(string ="تاريخ الانسحاب")
