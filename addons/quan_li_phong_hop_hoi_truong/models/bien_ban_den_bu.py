# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .dat_phong import gui_tin_nhan_telegram

class BienBanDenBuInherit(models.Model):
    _inherit = 'bien_ban_den_bu'

    dat_phong_id = fields.Many2one('dat_phong', string='Phiếu Đặt Phòng', ondelete='cascade')
    available_tai_san_ids = fields.Many2many('tai_san', related='dat_phong_id.tai_san_ids')

    @api.onchange('dat_phong_id')
    def _onchange_dat_phong_id(self):
        if self.dat_phong_id and self.dat_phong_id.nguoi_muon_id:
            self.nhan_vien_id = self.dat_phong_id.nguoi_muon_id.id

    @api.model
    def create(self, vals):
        record = super(BienBanDenBuInherit, self).create(vals)
        # Bắn Telegram nếu biên bản xuất phát từ Phòng họp
        if record.dat_phong_id and record.tai_san_id:
            tele_msg = f"⚠️ <b>LẬP BIÊN BẢN ({record.ma_bien_ban})</b>\nTài sản hỏng: {record.tai_san_id.display_name}\nNgười mượn: {record.nhan_vien_id.display_name}\nPhạt: {record.so_tien_phat:,.0f} VNĐ\nTrạng thái: Chờ duyệt"
            gui_tin_nhan_telegram(tele_msg)
        return record

    def action_duyet(self):
        # Gọi base action_duyet để xử lý tài sản thành Hỏng và đổi Trạng thái
        super(BienBanDenBuInherit, self).action_duyet()
        for record in self:
            # Gửi Email và Telegram bổ sung nếu xuất phát từ Phòng họp
            if record.dat_phong_id:
                if record.dat_phong_id.email:
                    subject = f"🚨 THÔNG BÁO PHẠT TÀI SẢN - {record.ma_bien_ban}"
                    body = f"""
                        <p>Xin chào <strong>{record.nhan_vien_id.display_name}</strong>,</p>
                        <p>Hệ thống ghi nhận bạn làm hỏng tài sản trong phiên mượn phòng họp.</p>
                        <ul>
                            <li><strong>Phòng họp:</strong> {record.dat_phong_id.phong_id.display_name}</li>
                            <li><strong>Thiết bị hỏng:</strong> {record.tai_san_id.display_name}</li>
                            <li><strong>Mức phạt:</strong> {record.so_tien_phat:,.0f} VNĐ</li>
                        </ul>
                    """
                    mail_values = {
                        'subject': subject,
                        'body_html': body,
                        'email_to': record.dat_phong_id.email,
                    }
                    self.env['mail.mail'].create(mail_values).send()
                    
                tele_msg = f"💸 <b>ĐÃ DUYỆT PHẠT ĐỀN BÙ ({record.ma_bien_ban})</b>\nTài sản: {record.tai_san_id.display_name}\nQuân xanh: {record.nhan_vien_id.display_name}\nSố tiền: {record.so_tien_phat:,.0f} VNĐ"
                gui_tin_nhan_telegram(tele_msg)
    def action_huy(self):
        for record in self:
            record.trang_thai = 'da_huy'
