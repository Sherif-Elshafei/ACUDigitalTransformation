from odoo import models, fields, api, exceptions


class students_finance_accounts(models.Model):
    _name = "students_finance_accounts"
    _description = ""
    _rec_name = "student"
    active = fields.Boolean(default=True, string="هل الحساب نشط ؟")
    student = fields.Many2one("students", string="Student")
    category_ids = fields.Many2many('accounts_category', 'accounts_category_rel', 'student', 'category_id',
                                    string='Tags')
    debts = fields.One2many("students_debts", "account", string="Debts", domain=[
                            ('receipt', '=', False), ('is_mandatory', '=', True)])
    semester_debts = fields.One2many("students_debts", "account", string="Semester Debts", domain=[
                                     ('semester', '=', 'Spring2020-2021')])
    payments = fields.One2many("students_payments", "account", string="Semester Payments", domain=[
                               ('semester', '=', 'Spring2020-2021')])
    reductions = fields.One2many(
        "students_reductions", "account", string="Reductions")
    refunds = fields.One2many("students_refunds", "account", string="Refunds")
    transferes = fields.One2many(
        "students_payments_transfers", "account", string="Transfers")
    delays = fields.One2many("payments_delays", "account", string="Delays")
    total_debts = fields.Float(
        compute="_compute_total_debts", string="Total Debts")
    total_semester_debts = fields.Float(
        compute="_compute_total_semester_debts", string="Semester Debts")
    total_unpaid_debts = fields.Float(
        compute="_compute_totals", string="Total Unpaid Debts")
    total_payments = fields.Float(
        compute="_compute_total_payments", string="Semester Payments")
    total_transfers = fields.Float(
        compute="_compute_totals", string="Total Transfers")
    total_reductions = fields.Float(
        compute="_compute_total_reductions", string="Total Reductions")
    account_balance = fields.Float(
        compute="_compute_totals", string="Balance", default=0.0)
    account_status = fields.Selection([("debit", "debit"), ("credit", "credit"), ("balanced", "balanced")],
                                      default="balanced", string="Account Status")
    dont_send = fields.Boolean()
    balance = fields.Float(string="الرصيد")

    @api.model
    def unenroll_student(self):
        accounts = self.env['students_finance_accounts'].browse(
            self._context.get('active_ids'))
        for account in accounts:
            student = account.student
            if account.enrollment_status == "1":
                status = '0'
            else:
                status = '1'

            a = student.write({'enrollment_status': status})

    @api.depends('debts')
    def _compute_total_debts(self):
        total = 0.0
        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        for record in self:
            total = 0.0
            for debt in record.debts:
                total = total + (debt.to_pay_amount)
            record.total_debts = total

    @api.depends('semester_debts')
    def _compute_total_semester_debts(self):
        total = 0.0
        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        for record in self:
            total = 0.0
            for debt in record.semester_debts:
                total = total + (debt.to_pay_amount)
            record.total_semester_debts = total

    @api.depends('semester_debts')
    def _compute_total_payments(self):

        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        current_year = self.env['academic_years'].search(
            [('is_current', '=', True)])
        for record in self:
            total = 0.0
            for debt in record.payments:
                total = total + (debt.amount)
            record.total_payments = total

    @api.depends('payments')
    def _compute_total_reductions(self):

        # accounts = self.env['students_finance_accounts'].browse(self._context.get('active_ids'))
        semester = self.env['academic_semesters'].search(
            [('is_current', '=', True)])
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
            res = self.env['ir.actions.act_window']._for_xml_id(
                'acums.%s' % xml_id)
            res.update(
                context=dict(self.env.context,
                             default_account=self.id, group_by=False),
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
        semester = self.env['academic_semesters'].search(
            [('is_current', '=', True)])
        debts = self.env['bylaws_debts'].search(
            ['&', ('bylaw', '=', self.bylaw.id), '|', ('loading_date', '=', '2'), ('loading_date', '=', '3')])
        if self.student.academic_semester.code == 'Fall2020-2021':
            debts = self.env['bylaws_debts'].search(
                ['&', ('bylaw', '=', self.bylaw.id), '|', ('loading_date', '=', '2'), ('loading_date', '=', '3'),
                 ('loading_date', '=', '1')])
        semester_debts = self.env['students_debts'].search_count(
            [('account', '=', self.id), ('semester', '=', semester.id)])
        student_debts = self.env['students_debts'].search(
            [('account', '=', self.id)])
        if semester_debts > 0:
            raise exceptions.ValidationError(
                "تم تحميل مصروفات الفصل الدراسي بالفعل")
        else:
            for debt in debts:
                new_debt = student_debts.create(
                    {'account': self.id, 'debt_type': debt.debt_type.id, 'debt': debt.id, 'semester': semester.id})
                print(debt.debt_type.name_ar)
                print(debt.name_ar)
                print(debt.actual_amount)

    @api.model
    def load_bank_debts(self):
        students = self.env['students_finance_accounts'].browse(
            self._context.get('active_ids'))
        debts = self.env['bylaws_debts']
        semester1 = self.env['academic_semesters'].search(
            [('code', '=', 'Fall2020-2021')])
        semester2 = self.env['academic_semesters'].search(
            [('code', '=', 'Spring2020-2021')])
        type1 = self.env['debts_types'].search([('code', '=', 2)])
        type2 = self.env['debts_types'].search([('code', '=', 11)])
        student_debts = self.env['students_debts']
        for student in students:
            bylaw = student.bylaw
            print(bylaw)
            mandatory_debt = debts.search([('bylaw', '=', student.bylaw.id), (
                'debt_type', '=', type1.id), ('code', '=', 3), ('status', '=', '1')], limit=1)

            extra_debt = debts.search(
                [('bylaw', '=', student.bylaw.id), ('debt_type', '=', type2.id), ('code', '=', 321)], limit=1)
            new_debt1 = student_debts.create(
                {'account': student.id, 'debt_type': type2.id, 'debt': extra_debt.id, 'semester': semester1.id})
            new_debt2 = student_debts.create(
                {'account': student.id, 'debt_type': type2.id, 'debt': extra_debt.id, 'semester': semester2.id})
            new_debt3 = student_debts.create(
                {'account': student.id, 'debt_type': type1.id, 'debt': mandatory_debt.id, 'semester': semester2.id})

            # mandatory_debt = debts.search([('bylaw', '=', student.bylaw.id),('debt_type', '=', type1.id), ('code', '=', 3)], limit=1)
            # extra_debt = debts.search([('bylaw', '=', student.bylaw.id),('debt_type', '=', type2.id), ('code', '=', '321')], limit=1)
            # mandatory = student_debts.create({'account': student.id, 'debt': mandatory_debt, 'semester': semester2.id})
            # extra = student_debts.create({'account': student.id, 'debt': extra_debt, 'semester': semester1.id})

    @api.model
    def create_email_log(self):
        for record in self:
            logs = self.env['emails_log']
            log_record = logs.create({'to': self.id})


class finance_related_fields(models.Model):
    _inherit = "s_f_a"
    student_active = fields.Boolean(related="student.active")
    faculty = fields.Many2one(
        related="student.faculty", string="Faculty", store=True)
    academic_year = fields.Many2one(
        related="student.academic_year", string="Academic Year", store=True)
    nationality = fields.Many2one(
        related="student.nationality", string="Nationality")
    citizenship = fields.Selection(
        related="student.citizenship", string="Nationality", store=True)
    study_language = fields.Selection(
        related="student.study_language", string="Study Language", store=True)
    file_number = fields.Integer(
        related="student.file_number", string="File Number")
    status = fields.Selection(related="student.status",
                              string="Status", store=True)
    notes = fields.One2many(related="student.notes", string="ملاحظات")
    enrollment_status = fields.Selection(
        related="student.enrollment_status", string="Enrollment Status", store=True)
    application_number = fields.Integer(
        related="student.id", string="Application Number")
    image_1920 = fields.Image(related="student.image_1920", string="Image")
    name_en = fields.Char(related="student.name_en", string="Name En")
    name_ar = fields.Char(related="student.name_ar", string="Name Ar")
    academic_email = fields.Char(
        related="student.academic_email", string="Email")
    bylaw = fields.Many2one(
        related="student.finance_bylaw", string="Financial Bylaw")
