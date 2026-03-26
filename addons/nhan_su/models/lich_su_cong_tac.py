from odoo import models, fields, api


from odoo.exceptions import ValidationError

class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lịch sử công tác'
    _order = "date_start desc"

    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ")
    don_vi_id = fields.Many2one("don_vi", string="Đơn vị")
    loai_chuc_vu = fields.Selection(
        [
            ("Chính", "Chính"), 
            ("Kiêm nhiệm", "Kiêm nhiệm")
        ], 
        string="Loại chức vụ", default="Chính"
    )
    nhan_vien_id = fields.Many2one("hr.employee", string="Nhân viên")
    
    cong_ty = fields.Char(string="Tên Đơn vị/Công ty")
    date_start = fields.Date(string="Ngày bắt đầu", required=True)
    date_end = fields.Date(string="Ngày kết thúc")

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError("Ngày kết thúc không được nhỏ hơn ngày bắt đầu!")
