import time
import cv2
from pyzbar.pyzbar import decode
import streamlit as st
import mysql.connector
import pandas as pd

# ---------- DB CONNECTION ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # change if needed
        password="",  # change if needed
        database="inventory_db"
    )

def fetch_product(barcode: str):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
    product = cursor.fetchone()
    cursor.close()
    db.close()
    return product

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Barcode Reader", layout="wide")
st.title("Continuous Barcode Reader (Read-Only)")

# Init session state
if "camera_on" not in st.session_state:
    st.session_state.camera_on = False
if "scanned" not in st.session_state:
    st.session_state.scanned = []  # history of scanned products
if "last_barcode" not in st.session_state:
    st.session_state.last_barcode = None

col1, col2 = st.columns((1, 1))
with col1:
    if st.button("Start Camera"):
        st.session_state.camera_on = True
with col2:
    if st.button("Stop Camera"):
        st.session_state.camera_on = False

# ---------- Layout Camera left Results right ----------
left, right = st.columns((2, 2))

frame_holder = left.empty()
status = right.empty()
history_box = right.empty()
total_box = right.empty()

with right:
    if st.button("Clear History"):
        st.session_state.scanned = []
        st.session_state.last_barcode = None
        history_box.empty()
        total_box.empty()
        status.info("History cleared")

if st.session_state.camera_on:
    cap = cv2.VideoCapture(0)
    while st.session_state.camera_on:
        ok, frame = cap.read()
        if not ok:
            status.error("Unable to access camera.")
            break
        decoded = decode(frame)
        
        # ---------- Camera Scanner ----------
        if decoded:
            barcode = decoded[0].data.decode("utf-8")
            
            # Avoid duplicate spam
            if barcode != st.session_state.last_barcode:
                st.session_state.last_barcode = barcode
                product = fetch_product(barcode)
                if product:
                    status.success(f"Detected: {product['name']} | Barcode: {barcode}")
                    st.session_state.scanned.append(product)
                else:
                    status.warning(f"Not found in database: {barcode}")
        
        # --- Auto brightness/contrast ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = gray.mean()
        if mean_brightness < 80:  # too dark
            frame = cv2.convertScaleAbs(frame, alpha=1.3, beta=40)
        elif mean_brightness > 180:  # too bright
            frame = cv2.convertScaleAbs(frame, alpha=0.8, beta=-30)
        
        # Update camera feed
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_holder.image(rgb_frame, channels="RGB", use_container_width=True)
        time.sleep(0.2)  # slower refresh avoids MediaFileStorage errors
    
    # Update history live
    if st.session_state.scanned:
        df = pd.DataFrame(st.session_state.scanned)
        df = df[["barcode", "name", "price", "quantity", "description"]]
        history_box.dataframe(df, use_container_width=True)
        
        # Update total
        total = df["price"].sum()
        total_box.subheader(f"Total: ₹{total:.2f}")
    
    time.sleep(0.05)
    cap.release()
else:
    frame_holder.empty()
    history_box.empty()
    total_box.empty()
