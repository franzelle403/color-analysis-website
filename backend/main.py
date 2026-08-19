from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from pydantic import BaseModel

from ai_analysis import analyze_image_with_ai

from database import (
    create_database,
    get_all_products,
    get_recommendations,
    add_product,
    update_product,
    delete_product
)


# ---------------------------------------
# APP SETUP
# ---------------------------------------

app = FastAPI()

create_database()


# ---------------------------------------
# CORS
# Allows React frontend to talk to FastAPI
# ---------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------
# BASIC ROUTES
# ---------------------------------------

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


# ---------------------------------------
# MAKEUP PRODUCT MODEL
# ---------------------------------------

class MakeupProduct(BaseModel):
    brand: str
    product_name: str
    category: str
    shade: str
    season: str

    undertone: str = ""
    depth: str = ""
    chroma: str = ""

    price: float = 0

    image_url: str = ""
    buy_url: str = ""


# ---------------------------------------
# GET ALL MAKEUP PRODUCTS
# Used by admin frontend
# ---------------------------------------

@app.get("/makeup")
def get_makeup():

    products = get_all_products()

    return {
        "success": True,
        "products": products
    }


# ---------------------------------------
# ADD MAKEUP PRODUCT
# ---------------------------------------

@app.post("/makeup")
def create_makeup(product: MakeupProduct):

    product_id = add_product(
        product.brand,
        product.product_name,
        product.category,
        product.shade,
        product.season,
        product.undertone,
        product.depth,
        product.chroma,
        product.price,
        product.image_url,
        product.buy_url
    )

    return {
        "success": True,
        "message": "Product added successfully",
        "id": product_id
    }


# ---------------------------------------
# EDIT MAKEUP PRODUCT
# ---------------------------------------

@app.put("/makeup/{product_id}")
def edit_makeup(
    product_id: int,
    product: MakeupProduct
):

    updated = update_product(
        product_id,
        product.brand,
        product.product_name,
        product.category,
        product.shade,
        product.season,
        product.undertone,
        product.depth,
        product.chroma,
        product.price,
        product.image_url,
        product.buy_url
    )

    if not updated:
        return {
            "success": False,
            "message": "Product not found"
        }

    return {
        "success": True,
        "message": "Product updated successfully"
    }


# ---------------------------------------
# DELETE MAKEUP PRODUCT
# ---------------------------------------

@app.delete("/makeup/{product_id}")
def remove_makeup(product_id: int):

    deleted = delete_product(product_id)

    if not deleted:
        return {
            "success": False,
            "message": "Product not found"
        }

    return {
        "success": True,
        "message": "Product deleted successfully"
    }


# ---------------------------------------
# COLOR ANALYSIS + MAKEUP RECOMMENDATIONS
# ---------------------------------------

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    try:

        # --------------------------------
        # READ UPLOADED IMAGE
        # --------------------------------

        image_data = await file.read()

        if not image_data:
            return {
                "success": False,
                "message": "No image data was received."
            }


        # --------------------------------
        # VERIFY FILE IS AN IMAGE
        # --------------------------------

        image = Image.open(
            BytesIO(image_data)
        )

        image.verify()


        # Re-open because verify() closes/invalidates
        # the image for some operations
        image = Image.open(
            BytesIO(image_data)
        )

        width, height = image.size


        # --------------------------------
        # RUN AI ANALYSIS
        # --------------------------------

        ai_result = analyze_image_with_ai(
            image_data,
            file.content_type
        )


        print("AI RESULT:")
        print(ai_result)


        # --------------------------------
        # MAKE SURE AI RESULT IS A DICT
        # --------------------------------

        if not isinstance(ai_result, dict):

            return {
                "success": False,
                "message": (
                    "AI analysis did not return structured data."
                )
            }


        # --------------------------------
        # GET COLOR SEASON
        # --------------------------------

        season = ai_result.get("season")


        print("DETECTED SEASON:")
        print(season)


        # --------------------------------
        # GET MAKEUP RECOMMENDATIONS
        # --------------------------------

        makeup_recommendations = []

        if season:

            makeup_recommendations = (
                get_recommendations(
                    season
                )
            )


        print("MAKEUP RECOMMENDATIONS:")
        print(makeup_recommendations)


        # --------------------------------
        # RETURN EVERYTHING TO REACT
        # --------------------------------

        return {
            "success": True,

            "filename": file.filename,
            "content_type": file.content_type,

            "width": width,
            "height": height,

            "analysis": ai_result,

            "makeup_recommendations":
                makeup_recommendations
        }


    except Exception as e:

        print("ANALYSIS ERROR:")
        print(e)

        return {
            "success": False,
            "message": str(e)
        }


# ---------------------------------------
# TEST RECOMMENDATIONS MANUALLY
# Example:
# /recommendations/Soft Autumn
# ---------------------------------------

@app.get("/recommendations/{season}")
def recommendations(season: str):

    products = get_recommendations(
        season
    )

    return {
        "success": True,
        "season": season,
        "products": products
    }