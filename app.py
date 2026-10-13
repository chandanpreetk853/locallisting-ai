import streamlit as st
import requests

st.set_page_config(page_title="LocalListing AI", page_icon="🛍️")

st.title("🛍️ LocalListing AI")
st.subheader("AI Product Description Generator")

st.write("Generate product listings for your small business using local AI.")

product = st.text_input("Product Name")
details = st.text_area("Product Details")

platform = st.selectbox(
    "Selling Platform",
    ["Instagram", "WhatsApp", "Etsy", "Amazon"]
)

language = st.selectbox(
    "Language",
    ["English", "Hindi", "Punjabi"]
)

if st.button("Generate Product Listing"):
    if not product.strip():
        st.warning("Please enter a product name.")
    else:
        prompt = f"""
Write a product listing in {language} for {platform}.

Product: {product}
Details: {details}

Include an attractive title, product description,
five hashtags, and a call to action.
Do not invent product features.
"""

        try:
            with st.spinner("Generating listing..."):
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3.2:3b",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=180
                )
                response.raise_for_status()
                result = response.json()["response"]

            st.success("Listing generated!")
            st.markdown(result)

            st.download_button(
                "Download Listing",
                data=result,
                file_name="product_listing.txt"
            )

        except requests.exceptions.RequestException as error:
            st.error(f"AI connection failed: {error}")
st.caption("Built with Python, Streamlit, and Ollama.")
