# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .dat_phong import gui_tin_nhan_telegram

class BienBanDenBu(models.Model):
    _name = 'bien_ban_den_bu'
    _description = 'Biên bản đền bù tài sản hỏng'
    _rec_name = 'ma_bien_ban'
    _order = 'create_date desc'

    ma_bien_ban = fields.Char(string='Mã Biên Bản', required=True, copy=False, readonly=True, default='New')
    dat_phong_id = fields.Many2one('dat_phong', string='Phiếu Đặt Phòng', required=True, ondelete='cascade')
    nhan_vien_id = fields.Many2one('hr.employee', related='dat_phong_id.nguoi_muon_id', string='Người mượn (Bị phạt)', store=True)
    available_tai_san_ids = fields.Many2many('tai_san', related='dat_phong_id.tai_san_ids')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản làm hỏng', required=True, domain="[('id', 'in', available_tai_san_ids)]")
    tinh_trang_thiet_bi = fields.Text(string='Mô tả Tình trạng', required=True)
    so_tien_phat = fields.Float(string='Số tiền đền bù (VNĐ)')
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ Cấp trên / HR duyệt'),
        ('da_duyet', 'Đã duyệt (Chờ trừ lương)'),
        ('da_huy', 'Đã hủy')
    ], string='Trạng thái', default='nhap', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_bien_ban', 'New') == 'New':
            last_record = self.search([], order='ma_bien_ban desc', limit=1)
            if last_record and last_record.ma_bien_ban.startswith('BB-'):
                last_number = int(last_record.ma_bien_ban.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_bien_ban'] = f'BB-{new_number:05d}'
            vals['ma_bien_ban'] = f'BB-{new_number:05d}'
            
        record = super(BienBanDenBu, self).create(vals)
        
        # Nhắc Telegram khi lập biên bản
        if record.dat_phong_id and record.tai_san_id:
            tele_msg = f"⚠️ <b>LẬP BIÊN BẢN ({record.ma_bien_ban})</b>\nTài sản hỏng: {record.tai_san_id.display_name}\nNgười mượn: {record.nhan_vien_id.display_name}\nPhạt: {record.so_tien_phat:,.0f} VNĐ\nTrạng thái: Chờ duyệt"
            gui_tin_nhan_telegram(tele_msg)
            
        return record

    def action_gui_duyet(self):
        for record in self:
            record.trang_thai = 'cho_duyet'

    def action_duyet(self):
        for record in self:
            record.trang_thai = 'da_duyet'
            if record.tai_san_id:
                record.tai_san_id.trang_thai = 'Hong'
                
            # Gửi Email thông báo phạt
            if record.dat_phong_id and record.dat_phong_id.email:
                subject = f"🚨 THÔNG BÁO PHẠT/ĐỀN BÙ TÀI SẢN - {record.ma_bien_ban}"
                body = f"""
                    <p>Xin chào <strong>{record.nhan_vien_id.display_name}</strong>,</p>
                    <p>Hệ thống ghi nhận bạn đã làm hỏng tài sản trong quá trình mượn phòng họp.</p>
                    <ul>
                        <li><strong>Phòng họp:</strong> {record.dat_phong_id.phong_id.display_name}</li>
                        <li><strong>Tài sản hỏng:</strong> {record.tai_san_id.display_name}</li>
                        <li><strong>Mức phạt / Đền bù:</strong> {record.so_tien_phat:,.0f} VNĐ</li>
                        <li><strong>Chi tiết tình trạng:</strong> {record.tinh_trang_thiet_bi or 'Không rõ'}</li>
                    </ul>
                    <p>Biên bản này đã được Quản lý duyệt và sẽ được chuyển cho bộ phận Nhân sự / Kế toán để tiến hành truy thu.</p>
                    <p>Vui lòng liên hệ bộ phận Hành chính nếu có thắc mắc.</p>
                    <br/>
                    <p><strong>Ban Quản Lý Phòng Họp</strong></p>
                """
                mail_values = {
                    'subject': subject,
                    'body_html': body,
                    'email_to': record.dat_phong_id.email,
                    'email_from': self.env.user.email or 'admin@example.com',
                }
                self.env['mail.mail'].create(mail_values).send()
                
            # Telegram thông báo Biên bản được duyệt
            if record.tai_san_id:
                tele_msg = f"💸 <b>ĐÃ DUYỆT PHẠT ĐỀN BÙ ({record.ma_bien_ban})</b>\nTài sản: {record.tai_san_id.display_name}\nQuân xanh bị phạt: {record.nhan_vien_id.display_name}\nSố tiền: {record.so_tien_phat:,.0f} VNĐ"
                gui_tin_nhan_telegram(tele_msg)

    def action_huy(self):
        for record in self:
            record.trang_thai = 'da_huy'
