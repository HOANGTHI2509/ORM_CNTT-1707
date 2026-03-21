from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin Phòng ban'
    _rec_name = 'ten_phong_ban'

    ma_phong_ban = fields.Char(string="Mã phòng ban", required=True)
    ten_phong_ban = fields.Char(string="Tên phòng ban", required=True)
    
    # Liên kết với Đơn vị cấp trên
    don_vi_id = fields.Many2one(
        "don_vi", 
        string="Thuộc Đơn vị", 
        help="Phòng ban này trực thuộc Đơn vị/Phân hiệu nào?"
    )
    
    # Người quản lý phòng ban
    truong_phong_id = fields.Many2one(
        "nhan_vien", 
        string="Trưởng phòng"
    )

    # Danh sách nhân viên trong phòng
    nhan_vien_ids = fields.One2many(
        "nhan_vien",
        inverse_name="phong_ban_id",
        string="Danh sách nhân viên"
    )

    _sql_constraints = [
        ('ma_phong_ban_unique', 'unique(ma_phong_ban)', 'Mã phòng ban phải là duy nhất!')
    ]
