from odoo import models, fields, api
from datetime import date

from odoo.exceptions import ValidationError

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    ma_dinh_danh = fields.Char("Mã định danh")

    ho_ten_dem = fields.Char("Họ tên đệm")
    ten = fields.Char("Tên")
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True)
    
    ngay_sinh = fields.Date("Ngày sinh", related="birthday", readonly=False)
    que_quan = fields.Char("Quê quán")
    so_dien_thoai = fields.Char("Số điện thoại", related="work_phone", readonly=False)
    
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac", 
        inverse_name="nhan_vien_id", 
        string = "Danh sách lịch sử công tác")
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    danh_sach_chung_chi_bang_cap_ids = fields.One2many(
        "danh_sach_chung_chi_bang_cap", 
        inverse_name="nhan_vien_id", 
        string = "Danh sách chứng chỉ bằng cấp")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban", help="Phòng ban nhân viên trực thuộc")
    hop_dong_lao_dong_ids = fields.One2many(
        "hop_dong_lao_dong",
        inverse_name="nhan_vien_id",
        string="Hợp đồng lao động"
    )
    so_nguoi_bang_tuoi = fields.Integer("Số người bằng tuổi", 
                                        compute="_compute_so_nguoi_bang_tuoi",
                                        store=True
                                        )

    @api.depends("tuoi")
    def _compute_so_nguoi_bang_tuoi(self):
        for record in self:
            if record.tuoi:
                records = self.env['hr.employee'].search(
                    [
                        ('tuoi', '=', record.tuoi),
                        ('id', '!=', record.id)
                    ]
                )
                record.so_nguoi_bang_tuoi = len(records)
            else:
                 record.so_nguoi_bang_tuoi = 0

    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất')
    ]

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = record.ho_ten_dem + ' ' + record.ten
                record.name = record.ho_va_ten
            else:
                record.ho_va_ten = record.name if record.name else ''
                
    @api.onchange("ten", "ho_ten_dem")
    def _default_ma_dinh_danh(self):
        for record in self:
            if record.ho_ten_dem and record.ten and not record.ma_dinh_danh:
                chu_cai_dau = ''.join([tu[0][0] for tu in record.ho_ten_dem.lower().split()])
                record.ma_dinh_danh = record.ten.lower() + chu_cai_dau
    
    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                year_now = date.today().year
                record.tuoi = year_now - record.ngay_sinh.year
            else:
                record.tuoi = 0

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi > 0 and record.tuoi < 18:
                raise ValidationError("Tuổi không được bé hơn 18")
