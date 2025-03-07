import streamlit as st
import requests

def call_iris_api(data):
    api_endpoint = "http://127.0.0.1:8085/iris-predict"
    response = requests.post(api_endpoint, json=data)
    response.raise_for_status()
    if response.status_code == 200:
        return response
    
def call_flowers_api(image_file):
    api_endpoint = "http://127.0.0.1:8085/flowers-predict"
    response = requests.post(api_endpoint, files={"image_file": image_file})
    response.raise_for_status()
    if response.status_code == 200:
        return response
    
def render_iris_form():
    st.header("Iris Model")

    sepal_length = st.number_input("Sepal Length", min_value=0.0, max_value=10.0, value=5.0)
    sepal_width = st.number_input("Sepal Width", min_value=0.0, max_value=10.0, value=3.0)
    petal_length = st.number_input("Petal Length", min_value=0.0, max_value=10.0, value=1.0)
    petal_width = st.number_input("Petal Width", min_value=0.0, max_value=10.0, value=0.1)

    is_clicked = st.button("Make Prediction")
    if is_clicked:
        response = call_iris_api({
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
        })
        st.write(response.json())
        st.balloons()


def render_flowers_form():
    st.header("Flowers Model")
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        st.image(
            image_file, 
            width=300,
            caption="Uploaded Image", 
            use_container_width=False
        )
        is_clicked = st.button("Make Prediction")
        if is_clicked:
            response = call_flowers_api(image_file)
            st.write(response.json())
            st.balloons()

def app():
    st.set_page_config(
        page_title="My Streamlit App",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.title("Welcome to My Model Garden App")
    st.write("This is a simple app to play around with the Iris and the flowers models.")

    option_selected = st.selectbox("Select a model", ["Iris", "Flowers"])
    st.write(f"You selected the {option_selected} model.")

    if option_selected == "Iris":
        render_iris_form()
    else:
        render_flowers_form()

if __name__ == "__main__":
    app()