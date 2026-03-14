import os
import base64
from google.genai import types
from google import genai
from dotenv import load_dotenv

load_dotenv()


def analyze_image(
    working_directory: str,
    image_path: str,
    task: str = "image-classification",
    api_key: str = None,
):
    abs_working_directory = os.path.abspath(working_directory)

    if os.path.isabs(image_path):
        abs_image_path = image_path
    else:
        abs_image_path = os.path.abspath(os.path.join(working_directory, image_path))

        if not abs_image_path.startswith(abs_working_directory):
            return f'Error: "{image_path}" is outside the working directory.'

    if not os.path.isfile(abs_image_path):
        return f'Error: "{image_path}" does not exist.'

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "Error: GEMINI_API_KEY not provided and not found in environment variables."
        )

    client = genai.Client(api_key=api_key)

    try:
        with open(abs_image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        return f"Error: Could not read image file: {str(e)}"

    supported_tasks = {
        "image-classification": "Image Classification (identifies objects, scenes, and concepts)",
        "description": "Image Description (provides a detailed description of the image)",
    }

    if task not in supported_tasks:
        return f'Error: Unsupported task "{task}". Supported tasks: {", ".join(supported_tasks.keys())}'

    try:
        if task == "image-classification":
            prompt = "Analyze this image and identify the main objects, scenes, and concepts. List them with confidence scores."
        elif task == "description":
            prompt = "Provide a detailed description of this image, including colors, objects, setting, and any notable features."

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(
                    parts=[
                        types.Part(
                            inline_data=types.Blob(
                                mime_type="image/jpeg", data=image_data
                            )
                        ),
                        types.Part(text=prompt),
                    ]
                )
            ],
        )

        if response.text:
            if task == "image-classification":
                return f"Image Analysis Results:\n{response.text}"
            else:
                return f"Image Description:\n{response.text}"
        else:
            return "Error: No response received from the model."

    except Exception as e:
        return f"Error: Failed to analyze image: {str(e)}"


schema_analyze_image = types.FunctionDeclaration(
    name="analyze_image",
    description="Analyze an image using Gemini 2.5 Flash model. Supports image classification and detailed image description. Accepts both absolute paths (e.g., 'C:\\Users\\...\\image.jpg') and relative paths (e.g., 'images/photo.jpg').",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "image_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the image file to analyze. Can be an absolute path or a path relative to the working directory.",
            ),
            "task": types.Schema(
                type=types.Type.STRING,
                description="The analysis task to perform. Options: 'image-classification' (default), 'description'.",
                enum=["image-classification", "description"],
            ),
        },
        required=["image_path"],
    ),
)
