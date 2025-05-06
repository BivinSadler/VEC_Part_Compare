# -*- coding: utf-8 -*-
"""Part Comparison App
Automatically adapted from Colab notebook
"""

import streamlit as st
import openai
import os
from PIL import Image

# Set your OpenAI API key using environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_part_description(part):
    prompt = f"""
    You are an expert in electronic and networking hardware.
    Provide a technical summary of part number {part} including:
    - What it is
    - Its primary use
    - Key specifications and features
    - Compatibility considerations
    Keep the description concise but informative.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def compare_parts(part1_info, part2_info):
    prompt = f"""
    Compare the following two hardware parts for compatibility:

    Create a table with two columns, one for each part.  The rows should be important specifications relevant to the parts. 
    
    Based on the specifications, use cases, and features, determine whether these parts:
    A. {{Green}} They are a close match and can be substituted for one another
    B. {{Red}} They are significantly different and are not able to be substituted
    C. {{Yellow}} It is tough to tell and further investigation is needed

    Part 1 Description:
    {part1_info}

    Part 2 Description:
    {part2_info}

    Provide a short summary and clearly include either {{Green}}, {{Red}}, or {{Yellow}} at the beginning of your response.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def evaluate_traffic_light(text):
    text = text.lower()
    if "{green}" in text:
        return "green", "✅ They are a close match and can be substituted"
    elif "{red}" in text:
        return "red", "❌ They are significantly different and cannot be substituted"
    elif "{yellow}" in text:
        return "yellow", "⚠️ Further investigation is needed"
    else:
        return "yellow", "⚠️ No clear recommendation"

st.set_page_config(page_title="Part Number Comparator", layout="centered")

# Load and display the logo
logo = Image.open("VECLogo.jpeg")
st.image(logo, width=150)

st.title("Part Number Substitution Checker")

with st.form("compare_form"):
    part1 = st.text_input("Enter the first part number (desired part)")
    part2 = st.text_input("Enter the second part number (potential substitute)")
    submitted = st.form_submit_button("Compare")

if submitted:
    if part1 and part2:
        with st.spinner("Getting information for Part 1..."):
            part1_info = get_part_description(part1)
        with st.spinner("Getting information for Part 2..."):
            part2_info = get_part_description(part2)

        st.markdown("---")
        st.subheader("Descriptions")
        st.write(f"**{part1}**:\n{part1_info}")
        st.write(f"**{part2}**:\n{part2_info}")

        with st.spinner("Analyzing compatibility..."):
            result = compare_parts(part1_info, part2_info)

        st.markdown("---")
        st.subheader("Comparison Result")
        st.write(result)

        color, message = evaluate_traffic_light(result)
        if color == "green":
            st.markdown("<div style='background-color:#d4edda;padding:10px;border-radius:5px;color:#155724;font-weight:bold;'>🟢 " + message + "</div>", unsafe_allow_html=True)
        elif color == "yellow":
            st.markdown("<div style='background-color:#fff3cd;padding:10px;border-radius:5px;color:#856404;font-weight:bold;'>🟡 " + message + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color:#f8d7da;padding:10px;border-radius:5px;color:#721c24;font-weight:bold;'>🔴 " + message + "</div>", unsafe_allow_html=True)
    else:
        st.error("Please enter both part numbers to compare.")
