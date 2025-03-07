from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, Request, File, UploadFile
import tensorflow as tf

def load_iris_model():
    from joblib import load
    model = load("models/iris-model/sklearn/model.pk")
    return model


def load_flowers_model():
    import keras
    model = keras.models.load_model("models/flowers-model/model.keras")
    return model



@asynccontextmanager
async def life_cycle(app: FastAPI):
    app.state.model_garden = {}
    print("the app is starting")
    iris_model = load_iris_model()
    flowers_model = load_flowers_model()
    app.state.model_garden["iris"] = iris_model
    app.state.model_garden["flowers"] = flowers_model
    yield
    print("the app is shutting down")

app = FastAPI(lifespan=life_cycle)


@app.get("/")
def say_hi():
    return {"message": "Hi, there, welcome to the API!"}

@app.post("/iris-predict")
async def predict_iris(request: Request):
    data = await request.json()
    iris_model = request.app.state.model_garden["iris"]
    predictions = iris_model.predict([[
        data["sepal_length"],
        data["sepal_width"],
        data["petal_length"],
        data["petal_width"],
    ]])
    return {"predictions": predictions.tolist()}


@app.post("/flowers-predict")
async def predict_flowers(request: Request, image_file: UploadFile = File(...)):
    image_bytes: bytes = await image_file.read()
    image_stream = BytesIO(image_bytes)
    pil_image = Image.open(image_stream)
    pil_image = pil_image.resize((180, 180))
    image_tensor = tf.convert_to_tensor(pil_image, dtype=tf.float32)
    image_tensor = tf.expand_dims(image_tensor, axis=0)
    image_tensor = image_tensor / 255.0
    flowers_model = request.app.state.model_garden["flowers"]
    activation_scores = flowers_model.predict(image_tensor)
    predictions = tf.nn.softmax(activation_scores).numpy().tolist()
    labels = ['dandelion', 'daisy', 'tulips', 'sunflowers', 'roses']
    output_Labels = {label: round(prob,2) for label, prob in zip(labels, predictions[0])}
    output_Labels = dict(sorted(output_Labels.items(), key=lambda x: x[1], reverse=True))
    return {"predictions": output_Labels}
    