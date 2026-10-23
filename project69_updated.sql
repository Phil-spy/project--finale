-- ============================================================
-- project69_updated.sql — ระบบร้านอาหาร
-- เพิ่ม/ปรับปรุง:
--   1) ระบบสั่งอาหาร (food_order + order_item)
--   2) ระบบสั่งอาหารแบบ Combo (combo + menu_item)
--   3) ระบบจองคิว/จองโต๊ะ (reservation_queue)
-- ความสัมพันธ์หลัก:
--   customer 1:N food_order
--   food_order M:N menu_item ผ่าน order_item
--   menu_item M:N menu_item ผ่าน combo (สำหรับ Combo)
--   customer 1:N reservation_queue
--   dining_table 1:N food_order
--   dining_table 1:N reservation_queue
-- ============================================================

-- ลบตารางตามลำดับ FK เพื่อให้สามารถรันไฟล์ซ้ำได้
DROP TABLE IF EXISTS reservation_queue;
DROP TABLE IF EXISTS combo;
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS food_order;
DROP TABLE IF EXISTS dining_table;
DROP TABLE IF EXISTS menu_item;
DROP TABLE IF EXISTS customer;

-- ============================================================
-- 1. CUSTOMER
-- ============================================================
CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    member_tier ENUM('general', 'silver', 'gold',"platinum") DEFAULT 'general'
);

-- ============================================================
-- 2. MENU ITEM
--    เมนูอาหารปกติ และเมนู Combo จะเก็บรวมในตารางนี้
-- ============================================================
CREATE TABLE menu_item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    is_available BOOLEAN DEFAULT TRUE
);

-- ============================================================
-- 3. DINING TABLE
-- ============================================================
CREATE TABLE dining_table (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    seats INT NOT NULL DEFAULT 2,
    zone VARCHAR(50) DEFAULT 'Main Dining'
);

-- ============================================================
-- 4. FOOD ORDER
--    ระบบสั่งอาหาร
--
--    order_type:
--      dine_in  = ทานที่ร้าน
--      takeaway = ซื้อกลับบ้าน
-- ============================================================
CREATE TABLE food_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT,
    table_id INT NULL,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    order_type ENUM('dine_in', 'takeaway') DEFAULT 'dine_in',

    status ENUM('open', 'paid', 'cancelled') DEFAULT 'open',

    FOREIGN KEY (cust_id)
        REFERENCES customer(cust_id)
        ON DELETE SET NULL,

    FOREIGN KEY (table_id)
        REFERENCES dining_table(table_id)
        ON DELETE SET NULL
);

-- ============================================================
-- 5. ORDER ITEM
--    1 Order มีหลายเมนู
--    1 Menu สามารถอยู่ในหลาย Order
--    จึงเป็น M:N ผ่าน order_item
-- ============================================================
CREATE TABLE order_item (
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    qty INT NOT NULL DEFAULT 1,
    note VARCHAR(255),

    PRIMARY KEY (order_id, item_id),

    FOREIGN KEY (order_id)
        REFERENCES food_order(order_id)
        ON DELETE CASCADE,

    FOREIGN KEY (item_id)
        REFERENCES menu_item(item_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 6. COMBO
--    ใช้เก็บรายละเอียดว่า Combo หนึ่งชุดประกอบด้วยเมนูอะไรบ้าง
--
--    เช่น
--      Combo 6
--        -> ข้าวผัดกุ้ง 1
--        -> ต้มยำกุ้ง 1
--        -> โค้ก 1
--
--    menu_item เป็นตัวแทนของ Combo หลัก
--    sub_item_id เป็นเมนูที่อยู่ภายใน Combo
-- ============================================================
CREATE TABLE combo (
    combo_id INT AUTO_INCREMENT PRIMARY KEY,

    item_id INT NOT NULL,
    sub_item_id INT NOT NULL,
    amount INT NOT NULL DEFAULT 1,

    FOREIGN KEY (item_id)
        REFERENCES menu_item(item_id)
        ON DELETE CASCADE,

    FOREIGN KEY (sub_item_id)
        REFERENCES menu_item(item_id)
        ON DELETE CASCADE,

    -- ป้องกันการเพิ่มเมนูซ้ำใน Combo เดียวกัน
    UNIQUE KEY unique_combo_item (item_id, sub_item_id)
);

-- ============================================================
-- 7. RESERVATION QUEUE
--    ระบบจองคิว / จองโต๊ะ
--
--    ตัวอย่างสถานะ:
--      waiting   = รอคิว
--      called    = เรียกคิวแล้ว
--      seated    = ลูกค้านั่งโต๊ะแล้ว
--      completed = ใช้งานเสร็จ
--      cancelled = ยกเลิก
--
--    queue_no จะเป็นเลขคิวของวันนั้น
-- ============================================================
CREATE TABLE reservation_queue (
    queue_id INT AUTO_INCREMENT PRIMARY KEY,

    queue_date DATE NOT NULL,
    queue_no INT NOT NULL,

    cust_id INT NOT NULL,

    party_size INT NOT NULL DEFAULT 1,

    -- โต๊ะอาจยังไม่ถูกจัดสรรตอนจองคิว
    table_id INT NULL,

    reservation_time DATETIME NULL,

    status ENUM(
        'waiting',
        'called',
        'seated',
        'completed',
        'cancelled'
    ) DEFAULT 'waiting',

    note VARCHAR(255),

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (cust_id)
        REFERENCES customer(cust_id)
        ON DELETE CASCADE,

    FOREIGN KEY (table_id)
        REFERENCES dining_table(table_id)
        ON DELETE SET NULL,

    -- เลขคิวไม่ซ้ำกันภายในวันเดียวกัน
    UNIQUE KEY unique_daily_queue (queue_date, queue_no)
);


-- ============================================================
-- SAMPLE DATA
-- ============================================================

-- ------------------------------------------------------------
-- Customer
-- ------------------------------------------------------------
INSERT INTO customer (cust_id, name, phone, member_tier) VALUES
(1, 'สมชาย สายกิน', '0812345678', 'gold'),
(2, 'สมหญิง จริงใจ', '0898765432', 'silver'),
(3, 'กิตติพงษ์ วงศ์สว่าง', '0861112223', 'general'),
(4, 'สุดา ใจดี', '0822223333', 'general');


-- ------------------------------------------------------------
-- Dining Table
-- ------------------------------------------------------------
INSERT INTO dining_table (table_id, seats, zone) VALUES
(1, 2, 'Indoor'),
(2, 4, 'Indoor'),
(3, 4, 'Outdoor'),
(4, 8, 'VIP');

-- ------------------------------------------------------------
-- Menu
-- ------------------------------------------------------------
INSERT INTO menu_item (item_id, name, category, price, is_available) VALUES
(1, 'ข้าวผัดกุ้ง', 'Main Dish', 80.00, TRUE),
(2, 'ต้มยำกุ้ง', 'Main Dish', 150.00, TRUE),
(3, 'โค้ก', 'Beverage', 20.00, TRUE),
(4, 'น้ำเปล่า', 'Beverage', 10.00, TRUE),
(5, 'ไอศกรีมวานิลลา', 'Dessert', 40.00, TRUE),

-- Combo
(6, 'ชุดอิ่มคุ้มสุดเซต (Combo)', 'Combo', 220.00, TRUE),

-- เพิ่ม Combo อีกชุดเพื่อทดสอบระบบ
(7, 'ชุดครอบครัว (Combo)', 'Combo', 350.00, TRUE);

-- ------------------------------------------------------------
-- Combo Detail
-- Combo 6 = ข้าวผัดกุ้ง + ต้มยำกุ้ง + โค้ก
-- ------------------------------------------------------------
INSERT INTO combo (item_id, sub_item_id, amount) VALUES
(6, 1, 1),
(6, 2, 1),
(6, 3, 1),

-- Combo 7 = ข้าวผัดกุ้ง 2 + โค้ก 2 + ไอศกรีม 1
(7, 1, 2),
(7, 3, 2),
(7, 5, 1);

-- ------------------------------------------------------------
-- Food Order
-- ------------------------------------------------------------
INSERT INTO food_order
(order_id, cust_id, table_id, order_time, order_type, status)
VALUES
(1, 1, 1, '2026-10-08 18:00:00', 'dine_in', 'paid'),
(2, 2, 2, '2026-10-08 19:15:00', 'dine_in', 'open'),
(3, 3, NULL, '2026-10-09 12:30:00', 'takeaway', 'open');

-- ------------------------------------------------------------
-- Order Item
-- ------------------------------------------------------------
INSERT INTO order_item (order_id, item_id, qty, note) VALUES
-- Order 1
(1, 1, 2, 'เผ็ดน้อย'),
(1, 3, 2, 'ใส่น้ำแข็ง'),

-- Order 2 : สั่ง Combo
(2, 6, 1, 'ไม่ใส่ผักชี'),
(2, 4, 1, 'เย็น'),

-- Order 3 : ซื้อกลับบ้าน
(3, 7, 1, 'แยกน้ำแข็ง');

-- ------------------------------------------------------------
-- Reservation Queue
-- ------------------------------------------------------------
INSERT INTO reservation_queue
(queue_id, queue_date, queue_no, cust_id, party_size, table_id,
 reservation_time, status, note)
VALUES
(1, '2026-10-09', 1, 1, 2, NULL,
 '2026-10-09 18:00:00', 'waiting', 'ขอโต๊ะด้านใน'),

(2, '2026-10-09', 2, 2, 4, 2,
 '2026-10-09 18:30:00', 'called', 'มากับครอบครัว'),

(3, '2026-10-09', 3, 3, 3, 3,
 '2026-10-09 19:00:00', 'seated', 'ขอโต๊ะโซน Outdoor'),

(4, '2026-10-09', 4, 4, 2, NULL,
 '2026-10-09 19:30:00', 'waiting', NULL);

-- ============================================================
-- ตัวอย่าง Query สำหรับทดสอบระบบ
-- ============================================================

-- ดูรายการอาหารทั้งหมด
-- SELECT * FROM menu_item WHERE is_available = TRUE;


-- ดูรายละเอียด Combo
-- SELECT
--     c.item_id AS combo_id,
--     combo_menu.name AS combo_name,
--     c.sub_item_id,
--     sub_menu.name AS sub_item_name,
--     c.amount
-- FROM combo c
-- JOIN menu_item combo_menu ON c.item_id = combo_menu.item_id
-- JOIN menu_item sub_menu ON c.sub_item_id = sub_menu.item_id
-- ORDER BY c.item_id;


-- ดูรายการอาหารของ Order
-- SELECT
--     fo.order_id,
--     cu.name AS customer,
--     mi.name AS menu,
--     oi.qty,
--     mi.price,
--     (oi.qty * mi.price) AS subtotal,
--     oi.note
-- FROM food_order fo
-- JOIN customer cu ON fo.cust_id = cu.cust_id
-- JOIN order_item oi ON fo.order_id = oi.order_id
-- JOIN menu_item mi ON oi.item_id = mi.item_id
-- ORDER BY fo.order_id;


-- ดูคิวที่กำลังรอ
-- SELECT
--     rq.queue_no,
--     cu.name AS customer,
--     cu.phone,
--     rq.party_size,
--     rq.reservation_time,
--     rq.status,
--     rq.note
-- FROM reservation_queue rq
-- JOIN customer cu ON rq.cust_id = cu.cust_id
-- WHERE rq.queue_date = CURDATE()
--   AND rq.status = 'waiting'
-- ORDER BY rq.queue_no;


-- ดูรายละเอียดคิวทั้งหมดของวันนี้
-- SELECT
--     rq.queue_no,
--     cu.name AS customer,
--     rq.party_size,
--     dt.table_id,
--     dt.zone,
--     rq.reservation_time,
--     rq.status
-- FROM reservation_queue rq
-- JOIN customer cu ON rq.cust_id = cu.cust_id
-- LEFT JOIN dining_table dt ON rq.table_id = dt.table_id
-- WHERE rq.queue_date = CURDATE()
-- ORDER BY rq.queue_no;