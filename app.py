import streamlit as st
from PIL import Image, UnidentifiedImageError
import io
from dotenv import load_dotenv
import os
import google.generativeai as genai
print(dir(genai))
# Load environment variables
load_dotenv()

# Configure Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please ensure it is correctly set in the .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Set Streamlit page title and header
st.set_page_config(page_title="AI Nutritionist App", layout="wide")
st.title("AI Nutritionist App")
st.subheader("Upload an image of your meal, and let AI analyze the calories!")

# Define a function to process the image and generate a response
def input_image_setup(uploaded_file):
    try:
        # Check if the file is uploaded
        if uploaded_file is None:
            raise FileNotFoundError("No file uploaded. Please upload an image.")
        
        # Process the uploaded image file
        image_bytes = uploaded_file.read()
        image_parts = [{"mimeType": uploaded_file.type, "bytes": image_bytes}]
        return image_parts
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return None

# Define a function to generate Gemini Pro API response
def get_gemini_response(image_parts, input_prompt):
    try:
        # Correct method name based on inspection/documentation
        response = genai.generate_content(
            prompt=input_prompt,
            images=image_parts
        )
        return response.text
    except Exception as e:
        st.error(f"Error calling the Gemini API: {e}")
        return None

# Prompt for the Gemini Pro model
input_prompt = """
You are a nutritionist AI. Analyze the image of food items provided. Identify each food item and calculate the total calories. Provide a detailed breakdown of each item with its calorie count. Format the output as a numbered list, like this:
1. [Food Item]: [Calories]
"""

# File uploader
uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    try:
        # Display the uploaded image
        image = Image.open(io.BytesIO(uploaded_file.read()))
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Button to analyze the image
        if st.button("Tell me the total calories"):
            # Process the uploaded image
            uploaded_file.seek(0)  # Reset file pointer
            image_parts = input_image_setup(uploaded_file)

            if image_parts:
                # Get response from Gemini Pro
                response = get_gemini_response(image_parts, input_prompt)
                if response:
                    st.success("AI Analysis Complete!")
                    st.text_area("Nutrition Analysis", response, height=300)
    except UnidentifiedImageError:
        st.error("Error processing the image: Unable to identify the file. Please upload a valid image.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
else:
    st.warning("Please upload an image file.")
