# -*- coding: utf-8 -*-
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class ZaloNotification(models.AbstractModel):
    _name = 'zalo.notification'
    _description = 'Dịch vụ thông báo Zalo'

    @api.model
    def send_message(self, phone_number, message):
        """
        Hàm dùng chung để gửi tin nhắn Zalo tới một số điện thoại.
        :param phone_number: SĐT nhận tin nhắn.
        :param message: Nội dung tin nhắn cần gửi.
        """
        if not phone_number:
            _logger.warning("Không thể gửi Zalo vì số điện thoại rỗng. Nội dung: %s", message)
            return False

        # TODO: Implement HTTPS POST tới Zalo API thực sự.
        # Ở đây chỉ log ra console để phục vụ chạy thử nghiệm.
        _logger.info("============== BẮN THÔNG BÁO ZALO ==================")
        _logger.info("Tới SĐT: %s", phone_number)
        _logger.info("Nội dung:\n%s", message)
        _logger.info("====================================================")
        return True
