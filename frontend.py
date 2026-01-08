import streamlit as st
import requests
import sys

# -----------------------------
# CONFIG
# -----------------------------
API_URL = "http://127.0.0.1:8000/predict"
TIMEOUT_SECONDS = 5

# -----------------------------
# BASIC UI (ALWAYS RENDERS)
# -----------------------------
st.title("Insurance Premium Category Predictor")
st.caption("Streamlit frontend → FastAPI backend")

# Debug info (helps confirm venv & execution)
with st.expander("Debug Info"):
    st.write("Python executable:", sys.executable)
    st.write("API URL:", API_URL)

st.markdown("### Enter your details below")

# -----------------------------
# INPUT FIELDS
# -----------------------------
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job",
    ],
)

# -----------------------------
# PREDICTION ACTION
# -----------------------------
if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation,
    }

    st.info("Sending request to backend...")

    try:
        with st.spinner("Predicting..."):
            response = requests.post(
                API_URL,
                json=input_data,
                timeout=TIMEOUT_SECONDS,
            )

        # Raise HTTP errors (4xx / 5xx)
        response.raise_for_status()

        # Parse JSON safely
        result = response.json()

        if "response" not in result:
            st.error("Unexpected API response format")
            st.json(result)
        else:
            prediction = result["response"]

            st.success(
                f"Predicted Insurance Premium Category: "
                f"**{prediction.get('predicted_category')}**"
            )

            st.metric(
                label="Confidence",
                value=f"{prediction.get('confidence', 0):.2f}",
            )

            st.subheader("Class Probabilities")
            st.json(prediction.get("class_probabilities", {}))

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to FastAPI server (is it running on port 8000?)")

    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Backend may be busy.")

    except requests.exceptions.HTTPError as e:
        st.error("❌ Backend returned an error")
        st.write("Status code:", response.status_code)
        st.write("Response:", response.text)

    except ValueError:
        st.error("❌ Backend did not return valid JSON")

    except Exception as e:
        st.error("❌ Unexpected error occurred")
        st.exception(e)
