
import steamlit as st
import csv
import io
from datetime import datetime

#ตั้งค่าเว็บไซต์
st.set_page_config(
    page_title="DIGITAL MUSIC FESTIVAL"
    page_icon="🎟️"
    layout="centered"
)

#กำหนดราคาตั๋ว
prices = {
    "standrad": 100,
    "VIP": 250,
    "Premium":400
}

#เตรียมพื้นที่เก็บข้อมูลคำสั่ง
if "order" not in st.session_state:
  st.session_state.orders =[]
if "last_order" not in st.session_state:
  st.session_state.orders = None

#ส่วนหัวเว็บไซต์
st.title("🎟️DIGITAL MUSIC FESTIVAL")
st.write(
    "ยินดีต้อนรับสู่ระบบจำหน่ายตั๋วออนไลน์"
    "กรุณาเลือกประเภทตั๋วและระบุจำนวนที่ต้องการ"
)
st.divider()

#แสดงประเภทตั๋ว
st.subheader("🎟️ประเภทตั๋ว")
col1, col2, col3 = st.columns(3)
with col1:
  st.metric("standrad","100 บาท")
with col2:
  st.metric("VIP","250 บาท")
with col3:
  st.metric("Premium","400 บาท")
st.divider()

#แบบฟอร์มสั่งซื้อ
st.subheader("✍️แบบฟอร์มสั่งซื้อ")
customer_name = st.text.input("ชื่อผู้ซื้อ")
ticker_type = st.selectbox(
    "เลือกประเภทตั๋ว",
    ["Standrad","VIP","premium"]
)

quantity = st.number_input(
    "จำนวนตั๋ว",
    min_value = 1,
    max_value = 10,
    value = 1,
    step = 1
)

#คำนวณราคา
price = prices[ticker_type]
total = price * quantity

st.info(f"ราคาต่อตั๋ว {price:,} บาท")
st.write(f"จำนวน {quantity} ใบ")
st.subheader(f"ยอดรวม {total:,} บาท")

#ปุ่มยืนยันคำสั่งซื้อ
if st.botton("ยืนยันการสั่งซื้อ", type="primary"):
  if customer_name.strip() == " ":
    st.error("กรุณากรอกชื่อผู้ซื้อ")

  else:
    order = {
        "order_id":f"T{len(st.session_state.orders)+ 1:04d}",
        "customer_name": customer_name.strip(),
        "ticker_type": ticker_type,
        "quantity":int(quantity),
        "price":price,
        "total":total,
        "order_time":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    st.session_state.order.append(order)
    st.session.state.last_order = order

    st.sucess("สั่งซื้อตั๋วเรียบร้อยแล้ว!")

#แสดงสรุปคำสั่งซื้อล่าสุด
if st.session_state.last_order is not None:
  order = st.session_state.last_order

  st.divider()
  st.subheader("📝สรุปคำสั่งซื้อ")

  st.write(f"หมายเลขคำสั่งซื้อ: {order['order_id']}")
  st.write(f"ชื่อผู้ซื้อ: {order['customer_name']}")
  st.write(f"ประเภทตั๋ว: {order['ticker_type']}")
  st.write(f"จำนวน: {order['quantity']} ใบ")

  st.success(f"ยอดชำระรวม: {order['total']:,} บาท")
  
#ประวัติคำสั่งซื้อ
if st.session_state.orders:

  st.divider()
  st.subheader("ประวัติการสั่งซื้อ")

  st.dataframe(
      st.session_state.orders,
      use_contrainer_width=True
  )

  #เตรียมไฟล์ csv สำหรับดาวน์โหลด
  csv_buffer = io.stringIO()
  fieldnames = list(st.session_state.orders[0].keys())

  writer = csv.Dictwriter(
      csv_buffer,
      fildnames=fildnames
  )

  writer.writeheader()
  writer.writerows(st.session_state.orders)

  st.Download_botton(
      label = "ดาวน์โหลดประวัติคำสั่งซื้อ"
      data=csv_buffer.getvalue().encode("utf-8-sig")
      file_name="ticker_orders.csv"
      mime="text/csv"
  )
st.caption("DIGITAL MUSIC FESTIVAL | ระบบคำสั่งซื้อตั๋ว")
