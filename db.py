#  db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#  มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# ============================================================
import mysql.connector
import config

def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)

def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


def blank_to_none(value):
    """ช่องที่ไม่ได้กรอกในฟอร์มจะส่งมาเป็น "" — แปลงเป็น None (= NULL ใน SQL)
    ใช้กับคอลัมน์ที่ว่างได้ เช่น return_date, paid_date  เพราะ MySQL ไม่รับ '' เป็น DATE"""
    return None if value in ("", None) else value


def _todo(name):
    raise NotImplementedError(f"TODO: ยังไม่ได้เขียนฟังก์ชัน {name} ใน db.py")


def search_customers(filters):
    """ค้นหา ลูกค้า ตามเงื่อนไข (name, phone, member_tier)"""
    sql = "SELECT * FROM customer WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("phone"):
        sql += " AND phone LIKE %s"
        params.append("%" + filters["phone"] + "%")

    if filters.get("member_tier"):
        sql += " AND member_tier = %s"
        params.append(filters["member_tier"])

    return run_query(sql, params)

def get_customer(cust_id):
    """ดึงข้อมูลลูกค้ารายเดียวตาม cust_id"""
    sql = "SELECT * FROM customer WHERE cust_id = %s"
    rows = run_query(sql, (cust_id,))

    if rows:
        return rows[0]

    return None

def create_customer(data):
    """เพิ่มลูกค้าใหม่"""
    name = (data.get("name") or "").strip()
    phone = blank_to_none(data.get("phone"))
    member_tier = data.get("member_tier") or "general"

    if not name:
        raise ValueError("กรุณากรอกชื่อลูกค้า")

    if member_tier not in ("general", "silver", "gold","platinum"):
        raise ValueError("ระดับสมาชิกไม่ถูกต้อง")

    sql = """
        INSERT INTO customer (name, phone, member_tier)
        VALUES (%s, %s, %s)
    """

    return run_command(sql, (name, phone, member_tier))


def update_customer(cust_id, data):
    """แก้ไขลูกค้าตาม cust_id"""
    name = (data.get("name") or "").strip()
    phone = blank_to_none(data.get("phone"))
    member_tier = data.get("member_tier") or "general"

    if not name:
        raise ValueError("กรุณากรอกชื่อลูกค้า")

    if member_tier not in ("general", "silver", "gold", "platinum"):
        raise ValueError("ระดับสมาชิกไม่ถูกต้อง")

    sql = """
        UPDATE customer
        SET name = %s,
            phone = %s,
            member_tier = %s
        WHERE cust_id = %s
    """

    return run_command(
        sql,
        (name, phone, member_tier, cust_id)
    )

def delete_customer(cust_id):
    """ลบลูกค้าตาม cust_id"""
    sql = """
        DELETE FROM customer
        WHERE cust_id = %s
    """

    return run_command(sql, (cust_id,))

def search_items(filters):
    """ค้นหาเมนูอาหารตามชื่อและหมวดหมู่"""
    sql = "SELECT * FROM menu_item WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("category"):
        sql += " AND category LIKE %s"
        params.append("%" + filters["category"] + "%")

    return run_query(sql, params)


def get_item(item_id):
    """ดึงข้อมูลเมนูอาหารรายรายการตาม item_id"""
    sql = "SELECT * FROM menu_item WHERE item_id = %s"
    rows = run_query(sql, (item_id,))

    if rows:
        return rows[0]

    return None

def create_item(data):
    """เพิ่มเมนูอาหารใหม่"""
    name = (data.get("name") or "").strip()
    category = blank_to_none(data.get("category"))

    if not name:
        raise ValueError("กรุณากรอกชื่อเมนูอาหาร")

    # ตรวจสอบราคา
    try:
        price = float(data.get("price", 0))
    except (TypeError, ValueError):
        raise ValueError("ราคาต้องเป็นตัวเลข")

    if price < 0:
        raise ValueError("ราคาต้องไม่ติดลบ")

    # แปลงสถานะที่หน้าเว็บส่งมาเป็น 1 หรือ 0
    raw_available = str(data.get("is_available", "1"))

    if raw_available in ("1", "True", "true"):
        is_available = 1
    elif raw_available in ("0", "False", "false"):
        is_available = 0
    else:
        raise ValueError("สถานะเมนูไม่ถูกต้อง")

    sql = """
        INSERT INTO menu_item (name, category, price, is_available)
        VALUES (%s, %s, %s, %s)
    """

    return run_command(
        sql,
        (name, category, price, is_available)
    )

def update_item(item_id, data):
    """แก้ไขเมนูอาหารตาม item_id"""
    name = (data.get("name") or "").strip()
    category = blank_to_none(data.get("category"))

    if not name:
        raise ValueError("กรุณากรอกชื่อเมนูอาหาร")

    # ตรวจสอบราคา
    try:
        price = float(data.get("price", 0))
    except (TypeError, ValueError):
        raise ValueError("ราคาต้องเป็นตัวเลข")

    if price < 0:
        raise ValueError("ราคาต้องไม่ติดลบ")

    # แปลงสถานะเมนูเป็น 1 หรือ 0
    raw_available = str(data.get("is_available", "1"))

    if raw_available in ("1", "True", "true"):
        is_available = 1
    elif raw_available in ("0", "False", "false"):
        is_available = 0
    else:
        raise ValueError("สถานะเมนูไม่ถูกต้อง")

    sql = """
        UPDATE menu_item
        SET name = %s,
            category = %s,
            price = %s,
            is_available = %s
        WHERE item_id = %s
    """

    return run_command(
        sql,
        (name, category, price, is_available, item_id)
    )

def delete_item(item_id):
    """ลบเมนูอาหารตาม item_id"""
    sql = """
        DELETE FROM menu_item
        WHERE item_id = %s
    """

    return run_command(sql, (item_id,))


def search_orders(filters):
    """ค้นหาออเดอร์ตาม cust_id, table_id และ status
    พร้อมชื่อลูกค้า รายการอาหาร และยอดรวมของแต่ละออเดอร์
    """
    sql = """
        SELECT
            fo.order_id,
            fo.cust_id,
            c.name AS customer_name,
            fo.table_id,
            fo.order_time,
            fo.order_type,
            fo.status,
            IFNULL(ot.subtotal, 0) AS subtotal,
            CASE
                WHEN IFNULL(ot.subtotal, 0) > 600
                THEN ROUND(IFNULL(ot.subtotal, 0) * 0.05, 2)
                ELSE 0
            END AS discount,
            ROUND(
                IFNULL(ot.subtotal, 0) -
                CASE
                    WHEN IFNULL(ot.subtotal, 0) > 600
                    THEN ROUND(IFNULL(ot.subtotal, 0) * 0.05, 2)
                    ELSE 0
                END,
                2
            ) AS total
        FROM food_order AS fo
        LEFT JOIN customer AS c
            ON fo.cust_id = c.cust_id
        LEFT JOIN (
            SELECT
                oi.order_id,
                SUM(oi.qty * mi.price) AS subtotal
            FROM order_item AS oi
            JOIN menu_item AS mi
                ON oi.item_id = mi.item_id
            GROUP BY oi.order_id
        ) AS ot
            ON fo.order_id = ot.order_id
        WHERE 1 = 1
    """

    params = []

    if filters.get("cust_id"):
        sql += " AND fo.cust_id = %s"
        params.append(filters["cust_id"])

    if filters.get("table_id"):
        sql += " AND fo.table_id = %s"
        params.append(filters["table_id"])

    if filters.get("status"):
        sql += " AND fo.status = %s"
        params.append(filters["status"])

    sql += " ORDER BY fo.order_id ASC"

    orders = run_query(sql, params)
    if not orders:
        return orders

    order_ids = [order["order_id"] for order in orders]
    placeholders = ", ".join(["%s"] * len(order_ids))
    item_rows = run_query(
        f"""
        SELECT
            oi.order_id,
            mi.name,
            oi.qty
        FROM order_item AS oi
        JOIN menu_item AS mi
            ON oi.item_id = mi.item_id
        WHERE oi.order_id IN ({placeholders})
        ORDER BY oi.order_id, mi.name
        """,
        order_ids
    )
    items_by_order = {}
    for item in item_rows:
        items_by_order.setdefault(item["order_id"], []).append(
            f'{item["name"]} × {item["qty"]}'
        )
    for order in orders:
        order["order_items"] = ", ".join(
            items_by_order.get(order["order_id"], [])
        ) or "—"
    return orders


def get_order(order_id):
    """ดึงข้อมูลออเดอร์พร้อมรายการอาหารตาม order_id"""
    sql = """
        SELECT
            fo.*,
            IFNULL(ot.subtotal, 0) AS subtotal,
            CASE
                WHEN IFNULL(ot.subtotal, 0) > 600
                THEN ROUND(IFNULL(ot.subtotal, 0) * 0.05, 2)
                ELSE 0
            END AS discount,
            ROUND(
                IFNULL(ot.subtotal, 0) -
                CASE
                    WHEN IFNULL(ot.subtotal, 0) > 600
                    THEN ROUND(IFNULL(ot.subtotal, 0) * 0.05, 2)
                    ELSE 0
                END,
                2
            ) AS total
        FROM food_order AS fo
        LEFT JOIN (
            SELECT
                oi.order_id,
                SUM(oi.qty * mi.price) AS subtotal
            FROM order_item AS oi
            JOIN menu_item AS mi
                ON oi.item_id = mi.item_id
            GROUP BY oi.order_id
        ) AS ot
            ON fo.order_id = ot.order_id
        WHERE fo.order_id = %s
    """

    rows = run_query(sql, (order_id,))

    if rows:
        order = rows[0]
        order["items"] = run_query(
            """
            SELECT oi.item_id, mi.name, oi.qty, oi.note
            FROM order_item AS oi
            JOIN menu_item AS mi
                ON oi.item_id = mi.item_id
            WHERE oi.order_id = %s
            ORDER BY mi.name
            """,
            (order_id,)
        )
        return order

    return None


def _normalize_order_items(items):
    if not isinstance(items, list) or not items:
        raise ValueError("กรุณาเพิ่มรายการอาหารอย่างน้อย 1 รายการ")

    normalized = []
    seen_item_ids = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("รูปแบบรายการอาหารไม่ถูกต้อง")

        try:
            item_id = int(item.get("item_id"))
            qty = int(item.get("qty"))
        except (TypeError, ValueError):
            raise ValueError("กรุณาเลือกเมนูและระบุจำนวนเป็นจำนวนเต็ม")

        if item_id < 1 or qty < 1:
            raise ValueError("จำนวนอาหารต้องมากกว่า 0")
        if item_id in seen_item_ids:
            raise ValueError("เมนูเดียวกันมีซ้ำ กรุณารวมจำนวนไว้ในรายการเดียว")

        seen_item_ids.add(item_id)
        normalized.append(
            (item_id, qty, blank_to_none(item.get("note")))
        )
    return normalized


def _save_order_items(cursor, order_id, items):
    for item_id, qty, note in items:
        cursor.execute(
            "SELECT item_id FROM menu_item WHERE item_id = %s",
            (item_id,)
        )
        if not cursor.fetchone():
            raise ValueError(f"ไม่พบเมนูหมายเลข {item_id}")
        cursor.execute(
            """
            INSERT INTO order_item (order_id, item_id, qty, note)
            VALUES (%s, %s, %s, %s)
            """,
            (order_id, item_id, qty, note)
        )


def check_table_free(table_id, order_id=None):
    """ตรวจสอบว่าโต๊ะมีอยู่จริงและไม่มีออเดอร์ที่ยังเปิดอยู่"""

    # 1. ตรวจสอบว่าโต๊ะมีอยู่จริง
    sql = """
        SELECT table_id
        FROM dining_table
        WHERE table_id = %s
    """
    tables = run_query(sql, (table_id,))

    if not tables:
        raise ValueError(f"ไม่พบโต๊ะหมายเลข {table_id}")

    # 2. ตรวจสอบว่ามีออเดอร์สถานะ open อยู่ที่โต๊ะหรือไม่
    sql = """
        SELECT COUNT(*) AS n
        FROM food_order
        WHERE table_id = %s
          AND status = 'open'
          AND order_id <> %s
    """
    rows = run_query(sql, (table_id, order_id or 0))

    if rows and rows[0]["n"] > 0:
        raise ValueError(
            f"โต๊ะ {table_id} ยังมีออเดอร์ที่ยังไม่ชำระเงิน"
        )


def create_order(data):
    """เพิ่มออเดอร์ใหม่"""
    cust_id = blank_to_none(data.get("cust_id"))
    table_id = blank_to_none(data.get("table_id"))
    order_time = blank_to_none(data.get("order_time"))
    order_type = data.get("order_type") or "dine_in"
    status = data.get("status") or "open"

    # ตรวจสอบประเภทออเดอร์
    if order_type not in ("dine_in", "takeaway"):
        raise ValueError("ประเภทออเดอร์ไม่ถูกต้อง")

    # ตรวจสอบสถานะออเดอร์
    if status not in ("open", "paid", "cancelled"):
        raise ValueError("สถานะออเดอร์ไม่ถูกต้อง")

    # ออเดอร์ที่ยังเปิดอยู่และรับประทานที่ร้าน ต้องตรวจสอบโต๊ะ
    if status == "open" and order_type == "dine_in":
        if not table_id:
            raise ValueError("กรุณาระบุโต๊ะสำหรับออเดอร์รับประทานที่ร้าน")
        check_table_free(table_id)

    # ออเดอร์กลับบ้านไม่จำเป็นต้องระบุโต๊ะ
    if order_type == "takeaway":
        table_id = None

    items = (
        _normalize_order_items(data["items"])
        if "items" in data else None
    )
    conn = get_connection()
    cur = conn.cursor()
    try:
        if order_time is None:
            cur.execute(
                """
                INSERT INTO food_order
                    (cust_id, table_id, order_type, status)
                VALUES (%s, %s, %s, %s)
                """,
                (cust_id, table_id, order_type, status)
            )
        else:
            cur.execute(
                """
                INSERT INTO food_order
                    (cust_id, table_id, order_time, order_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (cust_id, table_id, order_time, order_type, status)
            )
        order_id = cur.lastrowid
        if items is not None:
            _save_order_items(cur, order_id, items)
        conn.commit()
        return {"new_id": order_id, "affected": cur.rowcount}
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def update_order(order_id, data):
    """แก้ไขออเดอร์ตาม order_id"""
    cust_id = blank_to_none(data.get("cust_id"))
    table_id = blank_to_none(data.get("table_id"))
    order_time = blank_to_none(data.get("order_time"))
    order_type = data.get("order_type") or "dine_in"
    status = data.get("status") or "open"

    if order_type not in ("dine_in", "takeaway"):
        raise ValueError("ประเภทออเดอร์ไม่ถูกต้อง")

    if status not in ("open", "paid", "cancelled"):
        raise ValueError("สถานะออเดอร์ไม่ถูกต้อง")

    if status == "open" and order_type == "dine_in":
        if not table_id:
            raise ValueError("กรุณาระบุโต๊ะสำหรับออเดอร์รับประทานที่ร้าน")
        check_table_free(table_id, order_id)

    if order_type == "takeaway":
        table_id = None

    items = (
        _normalize_order_items(data["items"])
        if "items" in data else None
    )
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE food_order
            SET cust_id = %s,
                table_id = %s,
                order_time = %s,
                order_type = %s,
                status = %s
            WHERE order_id = %s
            """,
            (cust_id, table_id, order_time, order_type, status, order_id)
        )
        if items is not None:
            cur.execute(
                "DELETE FROM order_item WHERE order_id = %s",
                (order_id,)
            )
            _save_order_items(cur, order_id, items)
        conn.commit()
        return {"new_id": cur.lastrowid, "affected": cur.rowcount}
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def delete_order(order_id):
    """ลบออเดอร์ตาม order_id"""
    sql = """
        DELETE FROM food_order
        WHERE order_id = %s
    """

    return run_command(sql, (order_id,))

def report_summary():
    """สรุปข้อมูลสำหรับการ์ด Dashboard"""

    sql = """
        SELECT
            (SELECT COUNT(*)
             FROM customer) AS 'ลูกค้า',

            (SELECT COUNT(*)
             FROM menu_item) AS 'เมนู',

            (SELECT COUNT(*)
             FROM food_order) AS 'ออเดอร์',

            (SELECT IFNULL(SUM(
                 CASE
                     WHEN order_totals.subtotal > 600
                     THEN ROUND(order_totals.subtotal * 0.95, 2)
                     ELSE order_totals.subtotal
                 END
             ), 0)
             FROM (
                 SELECT
                     oi.order_id,
                     SUM(oi.qty * mi.price) AS subtotal
                 FROM order_item AS oi
                 INNER JOIN menu_item AS mi
                     ON oi.item_id = mi.item_id
                 GROUP BY oi.order_id
             ) AS order_totals
             INNER JOIN food_order AS fo
                 ON order_totals.order_id = fo.order_id
             WHERE fo.status = 'paid') AS 'ยอดขายรวม',

            (SELECT COUNT(*)
             FROM dining_table) AS 'จำนวนโต๊ะทั้งหมด',

            (SELECT COUNT(*)
             FROM food_order
             WHERE status = 'open') AS 'ออเดอร์ที่กำลังเปิดอยู่'
    """

    rows = run_query(sql)

    if rows:
        return rows[0]

    return {}


# ---------- ระบบจองโต๊ะ / จัดการคิว ----------
def search_reservations(filters):
    """ค้นหารายการจองตามวันที่ สถานะ และชื่อลูกค้า"""
    sql = """
        SELECT
            rq.queue_id,
            rq.queue_date,
            rq.queue_no,
            rq.cust_id,
            c.name AS customer_name,
            c.phone,
            rq.party_size,
            rq.table_id,
            dt.zone,
            rq.reservation_time,
            rq.status,
            rq.note,
            rq.created_at
        FROM reservation_queue AS rq
        INNER JOIN customer AS c
            ON rq.cust_id = c.cust_id
        LEFT JOIN dining_table AS dt
            ON rq.table_id = dt.table_id
        WHERE 1 = 1
    """
    params = []

    if filters.get("queue_date"):
        sql += " AND rq.queue_date = %s"
        params.append(filters["queue_date"])

    if filters.get("status"):
        sql += " AND rq.status = %s"
        params.append(filters["status"])

    if filters.get("customer_name"):
        sql += " AND c.name LIKE %s"
        params.append("%" + filters["customer_name"] + "%")

    sql += " ORDER BY rq.queue_date ASC, rq.queue_no ASC"

    return run_query(sql, params)


def get_reservation(queue_id):
    """ดึงรายละเอียดการจองหนึ่งรายการ"""
    sql = """
        SELECT
            rq.*,
            c.name AS customer_name,
            c.phone,
            dt.seats,
            dt.zone
        FROM reservation_queue AS rq
        INNER JOIN customer AS c
            ON rq.cust_id = c.cust_id
        LEFT JOIN dining_table AS dt
            ON rq.table_id = dt.table_id
        WHERE rq.queue_id = %s
    """
    rows = run_query(sql, (queue_id,))
    return rows[0] if rows else None


def create_reservation(data):
    """เพิ่มรายการจองและสร้างเลขคิวประจำวัน"""
    cust_id = blank_to_none(data.get("cust_id"))
    queue_date = blank_to_none(data.get("queue_date"))
    reservation_time = blank_to_none(data.get("reservation_time"))
    table_id = blank_to_none(data.get("table_id"))
    note = blank_to_none(data.get("note"))
    status = data.get("status") or "waiting"

    if not cust_id:
        raise ValueError("กรุณาเลือกลูกค้าที่จอง")

    if not queue_date:
        raise ValueError("กรุณาระบุวันที่จอง")

    try:
        cust_id = int(cust_id)
        party_size = int(data.get("party_size", 1))
        table_id = int(table_id) if table_id else None
    except (TypeError, ValueError):
        raise ValueError("รหัสลูกค้า จำนวนคน หรือหมายเลขโต๊ะไม่ถูกต้อง")

    if party_size < 1:
        raise ValueError("จำนวนคนต้องอย่างน้อย 1 คน")

    if status not in (
        "waiting", "called", "seated", "completed", "cancelled"
    ):
        raise ValueError("สถานะคิวไม่ถูกต้อง")

    # ตรวจสอบว่ามีลูกค้าจริง
    if not get_customer(cust_id):
        raise ValueError("ไม่พบข้อมูลลูกค้าที่เลือก")

    # ตรวจสอบโต๊ะและจำนวนที่นั่ง หากระบุโต๊ะ
    if table_id is not None:
        tables = run_query(
            "SELECT seats FROM dining_table WHERE table_id = %s",
            (table_id,)
        )
        if not tables:
            raise ValueError("ไม่พบโต๊ะที่เลือก")
        if tables[0]["seats"] < party_size:
            raise ValueError("จำนวนที่นั่งของโต๊ะไม่เพียงพอ")

    # สร้างเลขคิวถัดไปของวันที่เลือก
    rows = run_query(
        """
        SELECT COALESCE(MAX(queue_no), 0) + 1 AS next_queue
        FROM reservation_queue
        WHERE queue_date = %s
        """,
        (queue_date,)
    )
    queue_no = rows[0]["next_queue"]

    sql = """
        INSERT INTO reservation_queue
            (queue_date, queue_no, cust_id, party_size,
             table_id, reservation_time, status, note)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    return run_command(
        sql,
        (
            queue_date, queue_no, cust_id, party_size,
            table_id, reservation_time, status, note
        )
    )


def update_reservation(queue_id, data):
    """แก้ไขสถานะ โต๊ะ และหมายเหตุของรายการจอง"""
    reservation = get_reservation(queue_id)

    if not reservation:
        raise ValueError("ไม่พบรายการจองที่ต้องการแก้ไข")

    status = data.get("status") or reservation["status"]
    table_id = blank_to_none(data.get("table_id"))
    note = blank_to_none(data.get("note"))

    if status not in (
        "waiting", "called", "seated", "completed", "cancelled"
    ):
        raise ValueError("สถานะคิวไม่ถูกต้อง")

    if table_id is None:
        table_id = reservation["table_id"]
    else:
        try:
            table_id = int(table_id)
        except (TypeError, ValueError):
            raise ValueError("หมายเลขโต๊ะไม่ถูกต้อง")

    if table_id is not None:
        tables = run_query(
            "SELECT seats FROM dining_table WHERE table_id = %s",
            (table_id,)
        )
        if not tables:
            raise ValueError("ไม่พบโต๊ะที่เลือก")
        if tables[0]["seats"] < reservation["party_size"]:
            raise ValueError("จำนวนที่นั่งของโต๊ะไม่เพียงพอ")

    sql = """
        UPDATE reservation_queue
        SET table_id = %s,
            status = %s,
            note = %s
        WHERE queue_id = %s
    """

    return run_command(sql, (table_id, status, note, queue_id))


def cancel_reservation(queue_id):
    """ยกเลิกคิวโดยเก็บประวัติไว้ในฐานข้อมูล"""
    reservation = get_reservation(queue_id)

    if not reservation:
        raise ValueError("ไม่พบรายการจองที่ต้องการยกเลิก")

    if reservation["status"] in ("completed", "cancelled"):
        raise ValueError("รายการนี้เสร็จสิ้นหรือยกเลิกไปแล้ว")

    sql = """
        UPDATE reservation_queue
        SET status = 'cancelled',
            table_id = NULL
        WHERE queue_id = %s
    """

    return run_command(sql, (queue_id,))


def delete_reservation(queue_id):
    """ลบรายการจองออกจากฐานข้อมูลจริง"""
    reservation = get_reservation(queue_id)

    if not reservation:
        raise ValueError("ไม่พบรายการจองที่ต้องการลบ")

    sql = """
        DELETE FROM reservation_queue
        WHERE queue_id = %s
    """

    return run_command(sql, (queue_id,))


def report_popular_items():
    """รายงานเมนูขายดี 5 อันดับ"""

    sql = """
        SELECT
            mi.item_id,
            mi.name AS 'ชื่อเมนู',
            SUM(oi.qty) AS 'จำนวนที่ขายได้'
        FROM order_item AS oi
        INNER JOIN menu_item AS mi
            ON oi.item_id = mi.item_id
        GROUP BY mi.item_id, mi.name
        ORDER BY SUM(oi.qty) DESC
        LIMIT 5
    """
    return run_query(sql)

def report_daily_sales():
    """รายงานยอดขายรวมแยกตามวัน"""

    sql = """
        SELECT
            DATE(fo.order_time) AS 'วันที่',
            SUM(
                CASE
                    WHEN order_totals.subtotal > 600
                    THEN ROUND(order_totals.subtotal * 0.95, 2)
                    ELSE order_totals.subtotal
                END
            ) AS 'ยอดขายรวม'
        FROM food_order AS fo
        INNER JOIN (
            SELECT
                oi.order_id,
                SUM(oi.qty * mi.price) AS subtotal
            FROM order_item AS oi
            INNER JOIN menu_item AS mi
                ON oi.item_id = mi.item_id
            GROUP BY oi.order_id
        ) AS order_totals
            ON fo.order_id = order_totals.order_id
        GROUP BY DATE(fo.order_time)
        ORDER BY DATE(fo.order_time) DESC
    """
    return run_query(sql)

def report_big_orders():
    """รายงานออเดอร์ที่มียอดสุทธิหลังส่วนลดเกิน 500 บาท"""

    sql = """
        SELECT
            fo.order_id,
            fo.cust_id,
            c.name AS 'ชื่อลูกค้า',
            fo.table_id,
            fo.order_time,
            fo.order_type,
            fo.status,
            order_totals.subtotal AS 'ยอดก่อนลด',
            CASE
                WHEN order_totals.subtotal > 600
                THEN ROUND(order_totals.subtotal * 0.05, 2)
                ELSE 0
            END AS 'ส่วนลด',
            ROUND(
                order_totals.subtotal -
                CASE
                    WHEN order_totals.subtotal > 600
                    THEN ROUND(order_totals.subtotal * 0.05, 2)
                    ELSE 0
                END,
                2
            ) AS 'ยอดสุทธิ'
        FROM food_order AS fo
        INNER JOIN (
            SELECT
                oi.order_id,
                SUM(oi.qty * mi.price) AS subtotal
            FROM order_item AS oi
            INNER JOIN menu_item AS mi
                ON oi.item_id = mi.item_id
            GROUP BY oi.order_id
        ) AS order_totals
            ON fo.order_id = order_totals.order_id
        LEFT JOIN customer AS c
            ON fo.cust_id = c.cust_id
        WHERE ROUND(
            order_totals.subtotal -
            CASE
                WHEN order_totals.subtotal > 600
                THEN ROUND(order_totals.subtotal * 0.05, 2)
                ELSE 0
            END,
            2
        ) > 500
        ORDER BY
            order_totals.subtotal -
            CASE
                WHEN order_totals.subtotal > 600
                THEN ROUND(order_totals.subtotal * 0.05, 2)
                ELSE 0
            END DESC
    """
    return run_query(sql)

# ============================================================
#  รายการรายงานที่แสดงบนหน้า /report  (เรียงตามลำดับที่แสดง)
#  ★ วิธีเพิ่มรายงานใหม่ (ไม่ต้องแก้ไฟล์อื่น):
#    1) เขียนฟังก์ชัน report_xxx() ด้านบน ให้ return run_query(sql)
#    2) เพิ่ม 1 บรรทัดในรายการนี้:  ("ชื่อใน-url", "หัวข้อที่แสดง", ชื่อฟังก์ชัน)
#  ★ รายการนี้ต้องอยู่ท้ายไฟล์ (หลังฟังก์ชันทั้งหมด) ไม่งั้น Python หาชื่อฟังก์ชันไม่เจอ
#  ★ ห้ามตั้งชื่อ url ว่า "summary" (ใช้แล้วสำหรับการ์ดสรุป)
# ============================================================
REPORTS = [
    ("popular-items", "📈 เมนูขายดี (Best Sellers)",        report_popular_items),
    ("daily-sales",   "💰 ยอดขายรวมต่อวัน (Daily Sales)",   report_daily_sales),
    ("big-orders",    "🧾 ออเดอร์ยอดเกิน 500 บาท (HAVING)", report_big_orders),
    # ("my-report", "📋 รายงานของฉัน", report_my_report),   ← ตัวอย่างการเพิ่มรายงานที่ 4
]