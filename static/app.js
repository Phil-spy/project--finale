// ============================================================
//  app.js  —  ตรรกะหน้าเว็บ (ทำให้เสร็จแล้ว ★ นิสิตไม่ต้องแก้)
//  ปรับช่องค้นหา/ฟอร์มได้ที่ตัวแปร ENTITIES ด้านล่าง
// ============================================================
// ★ ตัวอย่าง dropdown ที่อ่านข้อมูลจากฐานข้อมูล: ฟอร์ม "ออเดอร์" ช่อง cust_id
//   แสดง name แต่ส่งค่าเป็น cust_id (อ่านรายการจาก /api/customers)
//   ช่อง FK อื่น ๆ ทำแบบเดียวกันได้ — เปลี่ยน "type": "number" เป็น select + optionsFrom
const ENTITIES = {
  "customers": {
    "label": "ลูกค้า",
    "api": "/api/customers",
    "idKey": "cust_id",
    "search": [
      {
        "key": "name",
        "label": "ชื่อ",
        "type": "text"
      },
      {
        "key": "phone",
        "label": "เบอร์โทร",
        "type": "text"
      },
      {
        "key": "member_tier",
        "label": "ระดับ",
        "type": "select",
        "options": [
          "",
          "general",
          "silver",
          "gold",
          "platinum"
        ]
      }
    ],
    "form": [
      {
        "key": "name",
        "label": "ชื่อ",
        "type": "text"
      },
      {
        "key": "phone",
        "label": "เบอร์โทร",
        "type": "text"
      },
      {
        "key": "member_tier",
        "label": "ระดับ",
        "type": "select",
        "options": [
          "general",
          "silver",
          "gold",
          "platinum"
        ]
      }
    ]
  },
  "items": {
    "label": "เมนูอาหาร",
    "api": "/api/menu-items",
    "idKey": "item_id",
    "search": [
    {
      "key": "name",
      "label": "ชื่อเมนู",
      "type": "text"
    },
    {
      "key": "category",
      "label": "หมวดหมู่",
      "type": "select",
      "options": [
        "",
        "Main Dish",
        "Beverage",
        "Dessert",
        "Combo"
      ]
    }
  ],
    "form": [
      {
        "key": "name",
        "label": "ชื่อเมนู",
        "type": "text"
      },
      {
        "key": "category",
        "label": "หมวดหมู่",
        "type": "select",
        "options": [
          "Main Dish",
          "Beverage",
          "Dessert",
          "Combo"
        ]
      },
      {
        "key": "price",
        "label": "ราคา",
        "type": "number"
      },
      {
        "key": "is_available",
        "label": "พร้อมขาย",
        "type": "select",
        "options": [
          "1",
          "0"
        ]
      }
    ]
  },
  "orders": {
    "label": "ออเดอร์",
    "api": "/api/orders",
    "idKey": "order_id",
    "search": [
      {
        "key": "cust_id",
        "label": "รหัสลูกค้า",
        "type": "number"
      },
      {
        "key": "table_id",
        "label": "รหัสโต๊ะ",
        "type": "number"
      },
      {
        "key": "status",
        "label": "สถานะ",
        "type": "select",
        "options": [
          "",
          "open",
          "paid",
          "cancelled"
        ]
      }
    ],
    "form": [
      {
        "key": "cust_id",
        "label": "ลูกค้า",
        "type": "select",
        "optionsFrom": {
          "api": "/api/customers",
          "value": "cust_id",
          "label": "name"
        }
      },
      {
        "key": "table_id",
        "label": "รหัสโต๊ะ",
        "type": "number"
      },
      {
        "key": "order_time",
        "label": "เวลาสั่ง",
        "type": "datetime-local"
      },
      {
        "key": "order_type",
        "label": "ประเภทออเดอร์",
        "type": "select",
        "options": [
          { "value": "dine_in", "label": "ทานที่ร้าน" },
          { "value": "takeaway", "label": "ซื้อกลับบ้าน" }
        ]
      },
      {
        "key": "status",
        "label": "สถานะ",
        "type": "select",
        "options": [
          "open",
          "paid",
          "cancelled"
        ]
      },
      {
        "key": "items",
        "label": "รายการอาหาร",
        "type": "order-items"
      }
    ]
  },
  "reservations": {
    "label": "จองโต๊ะ / คิว",
    "api": "/api/reservations",
    "idKey": "queue_id",
    "search": [
      {
        "key": "queue_date",
        "label": "วันที่จอง",
        "type": "date"
      },
      {
        "key": "status",
        "label": "สถานะคิว",
        "type": "select",
        "options": [
          "",
          "waiting",
          "called",
          "seated",
          "completed",
          "cancelled"
        ]
      },
      {
        "key": "customer_name",
        "label": "ชื่อลูกค้า",
        "type": "text"
      }
    ],
    "form": [
      {
        "key": "cust_id",
        "label": "ลูกค้า",
        "type": "select",
        "optionsFrom": {
          "api": "/api/customers",
          "value": "cust_id",
          "label": "name"
        }
      },
      {
        "key": "queue_date",
        "label": "วันที่จอง",
        "type": "date"
      },
      {
        "key": "reservation_time",
        "label": "เวลาจอง",
        "type": "datetime-local"
      },
      {
        "key": "party_size",
        "label": "จำนวนคน",
        "type": "number"
      },
      {
        "key": "table_id",
        "label": "รหัสโต๊ะ (เว้นว่างได้)",
        "type": "number"
      },
      {
        "key": "status",
        "label": "สถานะคิว",
        "type": "select",
        "options": [
          "waiting",
          "called",
          "seated",
          "completed",
          "cancelled"
        ]
      },
      {
        "key": "note",
        "label": "หมายเหตุ",
        "type": "text"
      }
    ]
  }
};

let current = Object.keys(ENTITIES)[0];
let editingId = null;
let orderMenuItems = [];
const $ = (s) => document.querySelector(s);
function setStatus(el, msg, cls = "") { el.className = "status " + cls; el.textContent = msg; }
async function api(url, opts) { const res = await fetch(url, opts); return res.json(); }
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}
function fieldHtml(f, prefix, value = "") {
  if (f.type === "heading") return '<div class="form-section">' + f.label + '</div>';
  if (f.type === "order-items") {
    return '<div class="field"><label>' + f.label + '</label>' +
      '<div id="orderItemRows"></div>' +
      '<button class="btn sm" type="button" onclick="addOrderItemRow()">+ เพิ่มเมนู</button>' +
      '<div id="orderSummary" class="order-summary"></div></div>';
  }
  let input;
  if (f.type === "select") {
    input = '<select id="' + prefix + f.key + '">' +
      f.options.map(o => {
        const v = typeof o === "object" ? o.value : o;
        const t = typeof o === "object" ? o.label : (o || "ทั้งหมด");
        return '<option value="' + escapeHtml(v) + '"' + (String(v) === String(value ?? "") ? " selected" : "") + '>' + escapeHtml(t) + '</option>';
      }).join("") + '</select>';
  } else {
    const inputValue = f.type === "datetime-local" && value
      ? String(value).replace(" ", "T").slice(0, 16)
      : value;
    input = '<input id="' + prefix + f.key + '" type="' + f.type + '" value="' + escapeHtml(inputValue) + '">';
  }
  return '<div class="field"><label>' + f.label + '</label>' + input + '</div>';
}
function addOrderItemRow(item = {}) {
  const container = $("#orderItemRows");
  const options = orderMenuItems.map(menu =>
    '<option value="' + escapeHtml(menu.item_id) + '"' +
    (String(menu.item_id) === String(item.item_id ?? "") ? " selected" : "") + '>' +
    escapeHtml(menu.name + " — " + menu.price + " บาท") + '</option>'
  ).join("");
  container.insertAdjacentHTML("beforeend",
    '<div class="order-item-row">' +
    '<select class="order-item-menu" onchange="updateOrderSummary()"><option value="">เลือกเมนู</option>' + options + '</select>' +
    '<input class="order-item-qty" type="number" min="1" step="1" value="' + escapeHtml(item.qty ?? 1) + '" aria-label="จำนวน" oninput="updateOrderSummary()">' +
    '<input class="order-item-note" type="text" value="' + escapeHtml(item.note ?? "") + '" placeholder="หมายเหตุ (ถ้ามี)" aria-label="หมายเหตุ">' +
    '<button class="btn sm del" type="button" onclick="removeOrderItemRow(this)">ลบ</button></div>'
  );
  updateOrderSummary();
}
function removeOrderItemRow(button) {
  button.closest(".order-item-row").remove();
  updateOrderSummary();
}
function updateOrderSummary() {
  const summary = $("#orderSummary");
  if (!summary) return;
  const subtotal = [...document.querySelectorAll(".order-item-row")].reduce((sum, row) => {
    const item = orderMenuItems.find(menu =>
      String(menu.item_id) === row.querySelector(".order-item-menu").value
    );
    const qty = Number(row.querySelector(".order-item-qty").value) || 0;
    return sum + (item ? Number(item.price) * qty : 0);
  }, 0);
  const discount = subtotal > 600 ? Math.round(subtotal * 0.05 * 100) / 100 : 0;
  summary.textContent = "ยอดก่อนลด " + subtotal.toFixed(2) + " บาท · ส่วนลด " +
    discount.toFixed(2) + " บาท · ยอดสุทธิ " + (subtotal - discount).toFixed(2) + " บาท" +
    (subtotal > 600 ? "" : " (ยอดเกิน 600 บาท รับส่วนลด 5%)");
}
function collectOrderItems() {
  return [...document.querySelectorAll(".order-item-row")].map(row => ({
    item_id: row.querySelector(".order-item-menu").value,
    qty: row.querySelector(".order-item-qty").value,
    note: row.querySelector(".order-item-note").value
  }));
}
// ช่อง select ที่มี optionsFrom → ดึงตัวเลือกจาก API
async function loadOptions(fields, forSearch) {
  for (const f of fields.filter(f => f.optionsFrom)) {
    const src = f.optionsFrom, r = await api(src.api);
    f.options = r.ok ? (r.data || []).map(row => ({ value: row[src.value], label: row[src.label] }))
                     : [{ value: "", label: (r.todo ? "🚧 " : "⚠️ ") + r.error }];
    if (forSearch && r.ok) f.options.unshift({ value: "", label: "ทั้งหมด" });
  }
}
// ช่องในฟอร์มที่ใช้อยู่ตอนนี้ (ช่อง editOnly แสดงเฉพาะตอนแก้ไข)
function formFields() { return ENTITIES[current].form.filter(f => !f.editOnly || editingId !== null); }
async function buildSearch() {
  const cfg = ENTITIES[current];
  await loadOptions(cfg.search, true);
  if (cfg !== ENTITIES[current]) return;
  $("#searchTitle").textContent = cfg.label;
  $("#searchFields").innerHTML = cfg.search.map(f => fieldHtml(f, "s_")).join("");
}
async function doSearch() {
  const cfg = ENTITIES[current];
  const params = new URLSearchParams();
  cfg.search.forEach(f => { const v = $("#s_" + f.key).value; if (v) params.append(f.key, v); });
  setStatus($("#status"), "กำลังค้นหา...");
  renderTable(await api(cfg.api + "?" + params.toString()));
}
function renderTable(r) {
  const head = $("#tableHead"), body = $("#tableBody"), st = $("#status");
  head.innerHTML = ""; body.innerHTML = "";
  if (!r.ok) { setStatus(st, (r.todo ? "🚧 " : "⚠️ ") + r.error, r.todo ? "todo" : "err"); return; }
  const rows = r.data || [];
  if (rows.length === 0) { setStatus(st, "ไม่พบข้อมูล"); return; }
  setStatus(st, "พบ " + rows.length + " รายการ");
  const cols = Object.keys(rows[0]);
  const columnLabels = {
    subtotal: "ยอดก่อนลด (บาท)",
    discount: "ส่วนลด (บาท)",
    total: "ยอดสุทธิ (บาท)"
  };
  head.innerHTML = cols.map(c => "<th>" + escapeHtml(
    c === "order_items" ? "รายการอาหาร (เมนู × จำนวน)" : columnLabels[c] || c
  ) + "</th>").join("") + "<th>จัดการ</th>";
  body.innerHTML = rows.map(row => {
    const id = row[ENTITIES[current].idKey];
    return "<tr>" + cols.map(c => "<td>" + escapeHtml(row[c] ?? "—") + "</td>").join("") +
      '<td><button class="btn sm" onclick="editRow(' + id + ')">แก้ไข</button> ' +
      '<button class="btn sm del" onclick="deleteRow('+id+')">'+
      (current === "reservations" ? "ลบ/ยกเลิก" : "ลบ")+
      '</button></td></tr>';
  }).join("");
}
async function openForm(title, data = {}) {
  await loadOptions(formFields(), false);
  if (current === "orders") {
    const menuResponse = await api("/api/menu-items");
    if (!menuResponse.ok) {
      alert((menuResponse.todo ? "🚧 " : "⚠️ ") + menuResponse.error);
      return;
    }
    orderMenuItems = menuResponse.data || [];
    if (orderMenuItems.length === 0) {
      alert("กรุณาเพิ่มเมนูอาหารก่อนสร้างออเดอร์");
      return;
    }
  }
  $("#modalTitle").textContent = title;
  $("#modal").classList.toggle("order-modal", current === "orders");
  $("#formFields").innerHTML = formFields().map(f => fieldHtml(f, "f_", data[f.key])).join("");
  if (current === "orders") {
    (data.items?.length ? data.items : [{}]).forEach(addOrderItemRow);
    updateOrderSummary();
  }
  $("#modal").classList.remove("hidden");
}
function collectForm() {
  const d = {};
  formFields().filter(f => f.key && f.type !== "order-items")
    .forEach(f => d[f.key] = $("#f_" + f.key).value);
  if (current === "orders") d.items = collectOrderItems();
  return d;
}
async function editRow(id) {
  const cfg = ENTITIES[current];
  const r = await api(cfg.api + "/" + id);
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  editingId = id; openForm("แก้ไขข้อมูล", r.data);
}
async function deleteRow(id) {
  const isReservation = current === "reservations";
  const message = isReservation
    ? "ยืนยันลบรายการจองนี้ออกจากฐานข้อมูลอย่างถาวรหรือไม่?\nข้อมูลที่ลบจะไม่สามารถกู้คืนผ่านระบบนี้ได้"
    : "ยืนยันการลบ?";

  if (!confirm(message)) return;

  const r = await api(ENTITIES[current].api + "/" + id, {
    method: "DELETE"
  });

  if (!r.ok) {
    alert(r.error || r.message || "ลบข้อมูลไม่สำเร็จ");
    return;
  }

  alert(isReservation ? "ลบรายการจองออกจากฐานข้อมูลแล้ว" : "ลบข้อมูลสำเร็จ");
  doSearch();
}

async function save() {
  const cfg = ENTITIES[current], data = collectForm();
  const opts = { method: editingId ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) };
  const r = await api(editingId ? cfg.api + "/" + editingId : cfg.api, opts);
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  $("#modal").classList.add("hidden"); doSearch();
}
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
  t.classList.add("active"); current = t.dataset.entity;
  buildSearch(); $("#tableHead").innerHTML = ""; $("#tableBody").innerHTML = "";
  setStatus($("#status"), 'กด "ค้นหา" เพื่อแสดงข้อมูล');
}));
$("#btnSearch").onclick = doSearch;
$("#btnClear").onclick = () => buildSearch();
$("#btnAdd").onclick = () => { editingId = null; openForm("เพิ่มข้อมูลใหม่"); };
$("#btnSave").onclick = save;
$("#btnCancel").onclick = () => $("#modal").classList.add("hidden");
buildSearch();
setStatus($("#status"), 'กด "ค้นหา" เพื่อแสดงข้อมูล');
