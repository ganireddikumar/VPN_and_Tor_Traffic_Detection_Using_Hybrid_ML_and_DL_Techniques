import streamlit as st
import joblib
import tensorflow as tf
import numpy as np

# Load the deep learning model and label encoder
model = tf.keras.models.load_model('dlmodel.h5')
le = joblib.load('labelencoderfordl.joblib')

# Set the background image URL
background_image_url = "http://bit.ly/projectvpnandtor"

# Streamlit web app with enhanced styling
st.markdown(
    f"""
    <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('{background_image_url}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .title {{
            font-family: Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            font-size: 3em;
            text-align: center;
            padding: 20px;
            background: linear-gradient(90deg, #4285f4, #0F9D58, #F4B400, #DB4437, #4285f4);
            -webkit-background-clip: text;
            color: transparent;
            animation: changeColor 10s infinite alternate-reverse, moveUpDown 5s infinite alternate;
        }}
        @keyframes moveUpDown {{
            0%, 100% {{
                transform: translateY(0);
            }}
            50% {{
                transform: translateY(-20px);
            }}
        }}
        .card {{
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        .input-label {{
            font-size: 1.5em;
            font-family: 'Montserrat', sans-serif;
            font-weight: bold;
            color: #ffffff;
        }}
        .predict-button {{
            background-color: #8F9779; /* Earth tone green color */
            color: #000000; /* black text color */
            font-family: 'Adelle', sans-serif;  /* Adelle font */
            font-size: 1.2em;
            padding: 10px 20px;
            border-radius: 10px;
            margin-top: 20px;
            cursor: pointer;
        }}
        .result {{
            font-size: 2em;
            margin-top: 20px;
            padding: 10px;
            border-radius: 10px;
            background-color: #8F9779; /* Earth tone green color */
            color: #000000; /* Black text color */
            font-family: 'Adelle', sans-serif;  /* Adelle font */
        }}
        @keyframes changeColor {{
            0% {{color: #4285f4;}}
            25% {{color: #0F9D58;}}
            50% {{color: #F4B400;}}
            75% {{color: #DB4437;}}
            100% {{color: #4285f4;}}
        }}
        .footer {{
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.9);
            color: #ffffff;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 class='title'>IDENTIFY YOUR NETWORK: Is it Tor, VPN, or Plain Internet?</h1>", unsafe_allow_html=True)

# Input card
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<label class='input-label'>Flow Duration:</label>", unsafe_allow_html=True)
flow_dur = st.number_input('', min_value=0.0, key='flow_duration', format="%.2f")
st.markdown("<label class='input-label'>Bwd Packet Length Min:</label>", unsafe_allow_html=True)
bwd_len_pkt = st.number_input('', min_value=0.0, key='bwd_packet_length_min', format="%.2f")
st.markdown("<label class='input-label'>Fwd Header Length:</label>", unsafe_allow_html=True)
fwd_header_len = st.number_input('', min_value=0.0, key='fwd_header_length', format="%.2f")
st.markdown("<label class='input-label'>Fwd Packet/S:</label>", unsafe_allow_html=True)
fwd_pkt = st.number_input('', min_value=0.0, key='fwd_packets_per_second', format="%.2f")
st.markdown("</div>", unsafe_allow_html=True)

# Button for prediction
sub = st.button('Predict', key='predict_button')

# Make prediction when the button is clicked
if sub:
    # Ensure all input fields are filled
    if not all([flow_dur, bwd_len_pkt, fwd_header_len, fwd_pkt]):
        st.warning("Please fill in all input fields.")
    else:
        ins = [[flow_dur, bwd_len_pkt, fwd_header_len, fwd_pkt]]
        pred = model.predict(ins)
        pred = np.argmax(pred)
        pred = le.inverse_transform([pred])
        st.markdown("<div class='result'>", unsafe_allow_html=True)
        st.write(f"Prediction: {pred[0]}")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class='footer'>
        <p>Powered by Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
