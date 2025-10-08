# invoice_agent.py
import streamlit as st
from io import StringIO
from mcp.server.fastmcp import FastMCP

# --- Use the same MCP instance locally ---
mcp = FastMCP("Calculator")

@mcp.tool()
def calculate_sum(items: str) -> str:
    total = 0
    for part in items.split(","):
        if "x" in part:
            q, p = part.split("x")
            total += float(q.strip()) * float(p.strip())
    return f"{total:.2f}"

# Streamlit UI
st.set_page_config(page_title="Invoice Validator", layout="centered")
st.title("🧾 AI Invoice Validator (MCP POC)")

uploaded_file = st.file_uploader("Upload a Text Invoice (.txt)", type="txt")

def validate_invoice(invoice_text):
    items = invoice_text.replace("\n", ",")
    return calculate_sum(items)

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    invoice_text = stringio.read()

    st.markdown("### Uploaded Invoice Content")
    st.code(invoice_text, language="text")

    if st.button("Run Validation Agent"):
        if invoice_text.strip():
            total = validate_invoice(invoice_text)
            st.success(f"✅ Calculated total: {total}")
        else:
            st.warning("Uploaded file is empty.")
