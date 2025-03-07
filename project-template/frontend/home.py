import streamlit as st

def render_iris_form():
    st.header("Iris Model")

    sepal_length = st.number_input("Sepal Length", min_value=0.0, max_value=10.0, value=5.0)
    sepal_width = st.number_input("Sepal Width", min_value=0.0, max_value=10.0, value=3.0)
    petal_length = st.number_input("Petal Length", min_value=0.0, max_value=10.0, value=1.0)
    petal_width = st.number_input("Petal Width", min_value=0.0, max_value=10.0, value=0.1)

    is_clicked = st.button("Make Prediction")
    if is_clicked:
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