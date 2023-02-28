class StudentsCategory(models.Model):
    _name = "students_category"

    # def _get_default_color(self):
    #     return randint(1, 11)

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)
    accounts_ids = fields.Many2many(
        'students', 'students_category_rel', 'category_id', 'student_id', string='Students')

    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "Tag name already exists !"),
    # ]
