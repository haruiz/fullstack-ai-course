import chainlit as cl
from ollama_client import OllamaClient
from PIL import Image
from PIL.Image import Image as PILImage
import typing
from dotenv import load_dotenv, find_dotenv
from tools import get_temperature
from image_utils import image_to_base64


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
        a: The first integer number
        b: The second integer number

    Returns:
        int: The sum of the two numbers
    """
    print(f"Calling add_two_numbers with a={a} and b={b}")
    return a + b

def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers

    Args:
        a: The first integer number
        b: The second integer number

    Returns:
        int: The difference between the two numbers
    """
    print(f"Calling subtract_two_numbers with a={a} and b={b}")
    return a - b

def get_weather(city_name: str) -> str:
    """
    Get the current temperature in a city

    Args:
        city_name: The name of the city

    Returns:
        str: The current temperature in the city
    """
    return get_temperature(city_name)

def make_appointment(date: str, time: str, location: str) -> str:
    """
    Make an appointment

    Args:
        date: The date of the appointment
        time: The time of the appointment
        location: The location of the appointment

    Returns:
        str: A confirmation message for the appointment
    """
    return f"Appointment confirmed for {date} at {time} in {location}."

def generate_image(prompt: str) -> Image:
    """
    Generate an image based on the input prompt

    Args:
        prompt: The input prompt for generating the image

    Returns:
        Image: The generated image
    """
    # Placeholder function for generating an image
    return Image.new("RGB", (100, 100), "white")

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Welcome to ollama client!"
    ).send()

    availabel_models = OllamaClient.list_models()
    response = await cl.AskActionMessage(
        content="Which model would you like to use?",
        actions=[cl.Action(
            name=model, 
            payload={"value": model}, 
            label=model) for model in availabel_models]
            
    ).send()
    
    if response is None:
        return
    payload = response.get("payload")
    model_selected = payload.get("value")
    system_instruction = (
        "You are a helpful assistant capable of providing insightful, relevant, and accurate responses based on the input you receive. You will use your reasoning and knowledge to assist the user, offering guidance, explanations, and solutions as needed, without requiring additional prompts or instructions. Your goal is to support the user in a natural, conversational manner."
    )
    ollama_client = OllamaClient(
        model_name=model_selected, 
        tools={
            "add_two_numbers": add_two_numbers,
            "subtract_two_numbers": subtract_two_numbers,
            "get_weather": get_weather,
            "make_appointment": make_appointment,
            "generate_image": generate_image
        },
        system_instruction=system_instruction
    )
    cl.user_session.set("ollama_client", ollama_client)

@cl.step(type="tool", name="Model")
async def generate_response(prompt: typing.Union[str, typing.List]):
    ollama_client = cl.user_session.get("ollama_client")
    response = await cl.make_async(ollama_client.generate_response)(prompt=prompt)
    return response

@cl.on_message
async def on_message(new_message: cl.Message):
    text_prompt = new_message.content
    message_elements = new_message.elements
    image_elements = [element for element in message_elements if element.type == "image"]
    image_parts = [Image.open(image.path) for image in image_elements]
    multimodal_prompt = [text_prompt] + image_parts
    
    response = await generate_response(prompt=multimodal_prompt)
    if isinstance(response, PILImage):
        response.save("generated_image.png")
        ollama_client = cl.user_session.get("ollama_client")
        ollama_client.message_queue.append({
            "role": "user",
            "content": "",
            "images": [image_to_base64(response)]
        })
        await cl.Message(
            content="Here is the generated image",
            elements=[cl.Image(path="generated_image.png", name="generated_image.png", display="inline")]
        ).send()
        return
    await cl.Message(
        content=response
    ).send()