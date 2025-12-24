import time
import cv2
from pyzbar.pyzbar import decode
import streamlit as st
import requests

APIURL = "http://localhost:5000"

st.set_page_config(page_title="Product Barcode Scanner Inventory", layout="wide")

# --- helpers ---
def fetch_and_fill_barcode(barcode: str):
    if not barcode:
        return
    r = requests.get(f"{APIURL}/get_product/{barcode}")
    if r.status_code == 200 and r.json():
        p = r.json()
        st.session_state.barcode = p["barcode"]
        st.session_state.name = p.get("name", "")
        st.session_state.price = float(p.get("price", 0.0))
        st.session_state.quantity = int(p.get("quantity", 0))
        st.session_state.description = p.get("description", "")
        st.session_state.status_msg = f"Found: {p['name']}"
    else:
        st.session_state.barcode = barcode
        st.session_state.name = ""
        st.session_state.price = 0.0
        st.session_state.quantity = 0
        st.session_state.description = ""
        st.session_state.status_msg = "Not found. Enter details and click Create."

def init_state():
    for k, v in {
        "camera_on": False,
        "barcode": "",
        "name": "",
        "price": 0.0,
        "quantity": 0,
        "description": "",
        "status_msg": ""
    }.items():
        st.session_state.setdefault(k, v)

init_state()

st.title("Product Barcode Scanner Inventory Updater")

# TITLE --- Scanner ---
st.subheader("Scanner")
col1, col2 = st.columns((1, 1))
if col1.button("Start Camera"):
    st.session_state.camera_on = True
if col2.button("Stop Camera"):
    st.session_state.camera_on = False

frame_holder = st.empty()
status = st.empty()
if st.session_state.status_msg:
    status.info(st.session_state.status_msg)

# TITLE --- Scanner ---
if st.session_state.camera_on:
    cap = cv2.VideoCapture(0)
    while st.session_state.camera_on:
        ok, frame = cap.read()
        if not ok:
            st.error("Unable to access camera.")
            break
        decoded = decode(frame)
        if decoded:
            barcode = decoded[0].data.decode("utf-8")
            fetch_and_fill_barcode(barcode)
            status.success(f"Detected barcode: {barcode}")
            # TITLE --- ONE SCAN THEN FREEZE ---
            st.session_state.camera_on = False
        frame_holder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        time.sleep(0.05)
    cap.release()
else:
    frame_holder.empty()

st.markdown("---")

# TITLE --- Manual Barcode Fetch ---
st.subheader("Manual Barcode Search")
fetch_cols = st.columns((3, 1))
with fetch_cols[0]:
    manual_barcode = st.text_input("Enter Barcode", key="manual_barcode")
with fetch_cols[1]:
    if st.button("Fetch"):
        fetch_and_fill_barcode(manual_barcode)

st.markdown("---")

# TITLE --- Manual Barcode Fetch ---
st.subheader("Product")
colL, colR = st.columns(2)
with colL:
    st.text_input("Barcode", key="barcode")
    st.text_input("Name", key="name")
    st.number_input("Price", min_value=0.0, step=0.01, key="price")
with colR:
    st.number_input("Quantity", step=1, key="quantity")
    st.text_area("Description", key="description")

c1, c2 = st.columns(2)
with c1:
    if st.button("Create Product"):
        payload = {
            "barcode": st.session_state.barcode,
            "name": st.session_state.name,
            "description": st.session_state.description,
            "quantity": int(st.session_state.quantity),
            "price": float(st.session_state.price),
        }
        r = requests.post(f"{APIURL}/add_product", json=payload)
        if r.ok:
            st.success("Product created")
        else:
            st.error(r.text)

with c2:
    if st.button("Update Details"):
        payload = {
            "barcode": st.session_state.barcode,
            "name": st.session_state.name,
            "description": st.session_state.description,
            "quantity": int(st.session_state.quantity),
            "price": float(st.session_state.price),
        }
        r = requests.post(f"{APIURL}/update_product", json=payload)
        if r.ok:
            st.success("Product updated")
        else:
            st.error(r.text)

st.markdown("---")

# TITLE --- Inventory Adjustment ---
st.subheader("Inventory Adjustment")
adj_cols = st.columns((1, 1, 3, 3))
with adj_cols[0]:
    change_val = st.number_input("Change -", value=1, step=1, key="adj_change")
with adj_cols[1]:
    st.markdown("&nbsp;")
    dec = st.button("Decrease")
with adj_cols[2]:
    st.markdown("&nbsp;")
    inc = st.button("Increase")

if dec:
    r = requests.post(
        f"{APIURL}/adjust_inventory",
        json={"barcode": st.session_state.barcode, "change": -abs(change_val)}
    )
    if r.ok:
        st.success("Stock decreased")
    else:
        st.error(r.text)

if inc:
    r = requests.post(
        f"{APIURL}/adjust_inventory",
        json={"barcode": st.session_state.barcode, "change": abs(change_val)}
    )
    if r.ok:
        st.success("Stock increased")
    else:
        st.error(r.text)

st.markdown("---")

# TITLE --- Search ---
st.subheader("Search Products")
search_cols = st.columns((3, 1))
with search_cols[0]:
    q = st.text_input("Search by name or barcode", key="search_q")
with search_cols[1]:
    do_search = st.button("Search")

if do_search:
    r = requests.get(f"{APIURL}/search", params={"q": q})
    if r.ok:
        res = r.json()
        if res:
            st.dataframe(res, use_container_width=True)
        else:
            st.info("No results.")
    else:
        st.error(r.text)
