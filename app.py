import streamlit as st
import requests
import io
from PIL import Image

# Hugging Face API token
hf_token = st.secrets["HUGGINGFACE_API_TOKEN"]
headers = {"Authorization": f"Bearer {hf_token}"}

# Set the title of the web page
st.set_page_config(page_title="Flux Image Generator")

# Map model names to URLs
model_urls = {
    "FLUX.1-dev": "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
    "FLUX.1-schnell": "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
}

# Function to query the API
def query(payload, model_url):
    response = requests.post(model_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"API request failed with status code {response.status_code}: {response.content.decode('utf-8')}")
        return None

# Streamlit interface
st.title("Reimagine your imagination 🚀")
st.write("Generate an image from text using Flux.1 models.")

# Model selection
model_choice = st.selectbox(
    "Choose a model:",
    ["FLUX.1-dev", "FLUX.1-schnell"]
)

# Text input from the user
user_input = st.text_input("Enter a description for the image:", "Astronaut riding a horse")

# Full-width "Generate Image" button
generate_button = st.button("Generate Image", use_container_width=True)

# If the button is clicked, generate the image
if generate_button:
    with st.spinner("Generating image..."):
        # Query the selected model
        model_url = model_urls[model_choice]
        image_bytes = query({"inputs": user_input}, model_url)
        
        if image_bytes:
            # Display the image
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=user_input)
            
            # Convert image to a downloadable format (e.g., PNG)
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            # Full-width download button
            st.download_button(
                label="Download Image",
                data=byte_im,
                file_name="generated_image.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.error("Failed to generate image. Please try again.")
