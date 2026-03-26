from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PhieuDieuChuyen(models.Model):
    _name = 'phieu_dieu_chuyen'
    _description = 'Phiếu Điều Chuyển Tài Sản'
    _order = 'ten_phieu desc'

    _states = {
        'draft': 'Nháp',
        'approved': 'Đã duyệt',
        'done': 'Hoàn thành',
        'cancelled': 'Hủy',
    }


    ten_phieu = fields.Char(string='Tên phiếu', required=True, copy=False, readonly=True, default="Mới")
    tai_san = fields.Many2one('tai_san', string='Tài sản', required=True)
    vi_tri_hien_tai = fields.Many2one(
        'vi_tri',
        string='Vị trí hiện tại',
        related='tai_san.vi_tri_hien_tai_id',
        readonly=True
    )
    vi_tri_moi = fields.Many2one('vi_tri', string='Vị trí mới', required=True)
    ngay_dieu_chuyen = fields.Datetime(string='Ngày điều chuyển', required=True, default=fields.Date.context_today)
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('duyet', 'Duyệt'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string='Trạng thái', default='nhap')
    ghi_chu = fields.Text(string='Ghi chú')

    @api.model
    def create(self, vals):
        if vals.get('ten_phieu', 'Mới') == 'Mới':
            last_record = self.search([], order='ten_phieu desc', limit=1)
            if last_record and last_record.ten_phieu.startswith('PDC-'):
                last_number = int(last_record.ten_phieu.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ten_phieu'] = f'PDC-{new_number:05d}'
        return super(PhieuDieuChuyen, self).create(vals)

    def action_duyet(self):
        self.write({'trang_thai': 'duyet'})

    def _send_telegram_message(self, message):
        import requests
        import logging
        _logger = logging.getLogger(__name__)
        bot_token = self.env['ir.config_parameter'].sudo().get_param('telegram_bot_token', "8674994673:AAGry6psZQjjR1EMXcXprIEevecQ6Ur4Ei0")
        chat_id = self.env['ir.config_parameter'].sudo().get_param('telegram_chat_id', "8262831605")
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            try:
                requests.post(url, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}, timeout=5)
            except Exception as e:
                _logger.error("Lỗi gửi Telegram: %s", str(e))

    def action_hoan_thanh(self):
        if self.trang_thai != 'duyet':
            raise UserError(_('Chỉ có thể hoàn thành phiếu đã được duyệt.'))
        self.env['lich_su_di_chuyen'].create({
            'tai_san_id': self.tai_san.id,
            'vi_tri_chuyen_id': self.vi_tri_hien_tai.id,
            'vi_tri_den_id': self.vi_tri_moi.id,
            'ngay_di_chuyen': self.ngay_dieu_chuyen,
            'ghi_chu': self.ghi_chu,
        })
        self.tai_san.write({'vi_tri_hien_tai_id': self.vi_tri_moi.id})
        self.write({'trang_thai': 'hoan_thanh'})

        # Telegram
        ten_vi_tri_cu = self.vi_tri_hien_tai.ten_vi_tri if self.vi_tri_hien_tai else 'Kho'
        tele_msg = f"<b>[ĐIỀU CHUYỂN TÀI SẢN]</b>\n" \
                   f"Tài sản: {self.tai_san.ten_tai_san} ({self.tai_san.ma_tai_san})\n" \
                   f"Từ: {ten_vi_tri_cu}\n" \
                   f"Đến Vị trí: {self.vi_tri_moi.ten_vi_tri}\n" \
                   f"Ghi chú: {self.ghi_chu or 'Không có'}"
        self._send_telegram_message(tele_msg)

    def action_huy(self):
        if self.trang_thai == 'hoan_thanh':
            raise UserError(_('Không thể hủy phiếu đã hoàn thành.'))
        self.write({'trang_thai': 'huy'})

    @api.constrains('vi_tri_moi')
    def _check_vi_tri(self):
        for record in self:
            if record.vi_tri_moi == record.vi_tri_hien_tai:
                raise ValidationError(_('Vị trí mới phải khác vị trí hiện tại.'))
