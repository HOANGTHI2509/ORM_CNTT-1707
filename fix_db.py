acts = env['ir.actions.act_window'].search([('res_model', '=', 'nhan_vien')])
print("Found bad actions:", acts)
if acts:
    acts.unlink()

# Xóa các menu tham chiếu đến các actions bị hỏng
all_menus = env['ir.ui.menu'].search([])
for m in all_menus:
    try:
        if m.action and hasattr(m.action, 'res_model') and m.action.res_model == 'nhan_vien':
            print("Found bad menu:", m.name)
            m.unlink()
    except Exception as e:
        pass

# Xóa các view tham chiếu đến 'nhan_vien'
views = env['ir.ui.view'].search([('model', '=', 'nhan_vien')])
print("Found bad views:", views)
if views:
    for v in views:
        v.unlink()

# Gỡ lỗi đặc biệt cho action 166
act_166 = env['ir.actions.act_window'].browse(166)
if act_166.exists():
    print("Force deleting action 166:", act_166.name)
    act_166.unlink()

env.cr.commit()
print("CLEANUP SUCCESSFUL")
