from odoo import models, fields, api

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
    luong_co_ban = fields.Float(string="Mức lương cơ bản (VNĐ)")
    file_hop_dong = fields.Binary(string="Bản scan hợp đồng")
    
    trang_thai = fields.Selection([
        ('nhap', 'Mới tạo'),
        ('hieu_luc', 'Đang hiệu lực'),
        ('het_han', 'Đã hết hạn'),
        ('cham_dut', 'Đã thanh lý/Chấm dứt')
    ], string="Trạng thái", default='nhap')

    _sql_constraints = [
        ('so_hop_dong_unique', 'unique(so_hop_dong)', 'Số hợp đồng này đã tồn tại trong hệ thống!')
    ]
