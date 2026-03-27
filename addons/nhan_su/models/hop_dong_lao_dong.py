from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class HopDongLaoDong(models.Model):
    _name = 'hop_dong_lao_dong'
    _description = 'Hợp đồng Lao động'
    _rec_name = 'so_hop_dong'

    so_hop_dong = fields.Char(string="Số hợp đồng", required=True)
    nhan_vien_id = fields.Many2one('hr.employee', string="Nhân viên", required=True)
    
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('1_nam', 'Có thời hạn 1 năm'),
        ('3_nam', 'Có thời hạn 3 năm'),
        ('khong_thoi_han', 'Không xác định thời hạn')
    ], string="Loại hợp đồng", default='1_nam', required=True)
    
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")
    file_hop_dong = fields.Binary(string="Bản scan hợp đồng")
    
    trang_thai = fields.Selection([
        ('nhap', 'Mới tạo'),
        ('hieu_luc', 'Đang hiệu lực'),
        ('het_han', 'Đã hết hạn'),
        ('cham_dut', 'Đã thanh lý/Chấm dứt')
    ], string="Trạng thái", default='nhap')

    @api.onchange('loai_hop_dong', 'ngay_bat_dau')
    def _onchange_tinh_ngay_ket_thuc(self):
        for record in self:
            if record.ngay_bat_dau:
                if record.loai_hop_dong == 'thu_viec':
                    # Mặc định thử việc 2 tháng
                    record.ngay_ket_thuc = record.ngay_bat_dau + relativedelta(months=2)
                elif record.loai_hop_dong == '1_nam':
                    record.ngay_ket_thuc = record.ngay_bat_dau + relativedelta(years=1)
                elif record.loai_hop_dong == '3_nam':
                    record.ngay_ket_thuc = record.ngay_bat_dau + relativedelta(years=3)
                elif record.loai_hop_dong == 'khong_thoi_han':
                    record.ngay_ket_thuc = False

    _sql_constraints = [
        ('so_hop_dong_unique', 'unique(so_hop_dong)', 'Số hợp đồng này đã tồn tại trong hệ thống!')
    ]

    @api.constrains('nhan_vien_id', 'trang_thai')
    def _check_1_hop_dong_active(self):
        for record in self:
            if record.trang_thai in ['nhap', 'hieu_luc']:
                count = self.search_count([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('trang_thai', 'in', ['nhap', 'hieu_luc']),
                    ('id', '!=', record.id)
                ])
                if count > 0:
                    raise ValidationError(f"Nhân viên {record.nhan_vien_id.name} đang có Hợp đồng khác ở trạng thái Mới tạo/Đang hiệu lực. Vui lòng thanh lý Hợp đồng cũ trước khi tạo mới!")
