
import streamlit as st
import joblib
from pathlib import Path

MODEL_PATH = Path("models/best_model.joblib")

st.set_page_config(
    page_title="SMS Spam Classifier",
    page_icon="📩",
    layout="centered"
)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

st.title("SMS Spam Classifier")
st.write("Enter a message below to check whether it is Spam or Ham.")

try:
    model = load_model()

    message = st.text_area(
        "Enter your SMS message:",
        placeholder="Type your message here..."
    )

    if st.button("Predict"):
        if message.strip():
            prediction = model.predict([message])[0]

            if prediction == 1:
                st.error("🚨 This message is SPAM!")
            else:
                st.success("✅ This message is HAM (Not Spam).")
        else:
            st.warning("Please enter a message first.")

except FileNotFoundError:
    st.error("Model not found. Please train the model first.")
