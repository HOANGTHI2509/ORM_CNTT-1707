import psycopg2

conn = psycopg2.connect(
    dbname="business_db",
    user="odoo",
    password="odoo",
    host="127.0.0.1",
    port=5431
)
cr = conn.cursor()

cr.execute("SELECT id, name FROM ir_ui_view WHERE arch_db LIKE '%tai_san_ids%';")
rows = cr.fetchall()
print("Views co tai_san_ids:", rows)

if rows:
    ids = [str(r[0]) for r in rows]
    cr.execute("DELETE FROM ir_ui_view WHERE id IN (%s);" % ','.join(ids))
    conn.commit()
    print("Da xoa", len(rows), "view(s). Restart Odoo de nap lai view moi.")
else:
    print("Khong tim thay view cu.")

cr.close()
conn.close()
