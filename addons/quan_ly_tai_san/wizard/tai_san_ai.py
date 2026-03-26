from odoo import models, fields, api, exceptions
import logging
import requests
import json
import re

_logger = logging.getLogger(__name__)

class TaiSanAIWizard(models.TransientModel):
    _name = 'tai_san.ai.wizard'
    _description = 'Trợ lý ảo AI Quản trị Tài sản'

    ai_request = fields.Text(string="Nhập yêu cầu/câu hỏi", help="VD: Cấp phát cái Laptop cho Dũng hoặc Máy in có ai đang mượn không?")
    ai_response = fields.Html(string="AI Trả Lời", readonly=True)

    def action_generate(self):
        self.ensure_one()
        if not self.ai_request or not self.ai_request.strip():
            raise exceptions.UserError("Sếp chưa nhập lệnh kìa! Hãy gõ nội dung vào ô hỏi nhé.")
        api_key = self.env['ir.config_parameter'].sudo().get_param('gemini_api_key')
        if not api_key:
            raise exceptions.UserError("Chưa cấu hình Google Gemini API Key. Vui lòng vào Cài đặt -> Tham số hệ thống nhập 'gemini_api_key'.")

        # Context
        nhan_viens = self.env['hr.employee'].search([])
        nv_info = ", ".join([f"ID {nv.id}: {nv.name}" for nv in nhan_viens])

        tai_sans = self.env['tai_san'].search([])
        ts_info = ", ".join([f"ID {ts.id}: {ts.ten_tai_san} (Trạng thái: {ts.trang_thai})" for ts in tai_sans])

        prompt = f"""
Bạn là Trợ lý Ảo AI cao cấp về Quản lý Tài sản.
Người dùng yêu cầu (Có thể là Lập phiếu hoặc Chỉ Hỏi thông tin): "{self.ai_request}"

DANH SÁCH NHÂN SỰ: {nv_info}
DANH SÁCH TÀI SẢN: {ts_info}

Nhiệm vụ: 
1. Nếu người dùng HIỂN NHIÊN MỐN LẬP PHIẾU BÀN GIAO/THU HỒI, trả về JSON theo mẫu "create". (Dò tìm ID nhân sự/tài sản và chọn loai_phieu "giao_moi" hoặc "thu_hoi").
2. Nếu người dùng CHỈ HỎI VỀ THÔNG TIN (Ví dụ: Có bao nhiêu cái máy? Tình trạng ra sao? Có ai mượn?), dùng thông tin trong Danh sách Tài sản ở trên để trả lời tự nhiên. Trả về mẫu "answer".

Cấu trúc trả về BẮT BUỘC (TUYỆT ĐỐI KHÔNG CÓ MARKDOWN, CHỈ TRẢ CHUỖI JSON MẶC ĐỊNH):
Trường hợp Lập Phiếu:
{{
    "action": "create",
    "loai_phieu": "<giao_moi hoặc thu_hoi>",
    "nguoi_giao_id": <ID người giao>,
    "nguoi_nhan_id": <ID người nhận>,
    "tai_san_ids": [<mảng các ID tài sản (kiểu số nguyên)>]
}}

Trường hợp Trả Lời:
{{
    "action": "answer",
    "message": "<Câu trả lời bằng tiếng Việt của bạn, có thể dùng thẻ HTML <b> để bôi đậm nếu cần>"
}}
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1}
        }

        try:
            response = requests.post(url, json=payload, timeout=20)
            response.raise_for_status()
            res_data = response.json()
            
            raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
            clean_json = re.sub(r'```json\n|\n```|```', '', raw_text).strip()
            
            ai_data = json.loads(clean_json)
            
            if ai_data.get('action') == 'answer':
                answer_text = ai_data.get('message', 'Tôi không có thông tin về câu hỏi này.')
                self.ai_response = f"<div style='margin-bottom: 10px; border-bottom: 1px dashed #ccc; padding-bottom: 5px;'><i><b style='color:#555;'>Bạn hỏi:</b> {self.ai_request}</i></div>{answer_text}"
                self.ai_request = False
                return {
                    'type': 'ir.actions.act_window',
                    'name': '✨ Trợ lý Tài Sản (AI)',
                    'res_model': 'tai_san.ai.wizard',
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'new',
                }

            create_vals = {
                'loai_phieu': ai_data.get('loai_phieu', 'giao_moi'),
            }
            if 'nguoi_giao_id' in ai_data and ai_data['nguoi_giao_id']: create_vals['nguoi_giao_id'] = ai_data['nguoi_giao_id']
            if 'nguoi_nhan_id' in ai_data and ai_data['nguoi_nhan_id']: create_vals['nguoi_nhan_id'] = ai_data['nguoi_nhan_id']

            tai_san_ids = ai_data.get('tai_san_ids', [])
            if tai_san_ids:
                create_vals['chi_tiet_ids'] = [(0, 0, {'tai_san_id': ts_id}) for ts_id in tai_san_ids]
            
            new_record = self.env['phieu_ban_giao'].create(create_vals)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Phiếu Bàn Giao (Sinh bởi AI)',
                'res_model': 'phieu_ban_giao',
                'res_id': new_record.id,
                'view_mode': 'form',
                'target': 'current',
            }

        except Exception as e:
            _logger.error("Lỗi gọi Gemini AI Asset: %s", str(e))
            raise exceptions.UserError("AI Gemini không thể phân tích nội dung. Gọi lại hoặc chi tiết hơn nhé:\n" + str(e))
