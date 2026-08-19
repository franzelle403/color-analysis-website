from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO

from ai_analysis import analyze_image_with_ai


app = FastAPI()


# Allow our React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Color Analysis API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    image_data = await file.read()

    try:

        # Check that the uploaded file is an image
        image = Image.open(BytesIO(image_data))

        width, height = image.size

        # Send the image to the AI
        ai_result = analyze_image_with_ai(
            image_data,
            file.content_type
        )

        return {
            "success": True,
            "filename": file.filename,
            "content_type": file.content_type,
            "width": width,
            "height": height,
            "analysis": ai_result
        }

    except Exception as e:

        print("AI ERROR:", e)

        return {
            "success": False,
            "message": str(e)
        }