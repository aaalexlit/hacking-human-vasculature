import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse

from ultralytics import YOLO
from ultralytics.engine.results import Results

from pydantic import BaseModel
from pydantic.config import ConfigDict
from PIL import Image
from io import BytesIO
import numpy as np

app = FastAPI(
    title="Blood vessel segmentation API",
)

model = YOLO('best_model.pt')

class PredictionInput(BaseModel):
    url: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"url": "https://github.com/aaalexlit/hacking-human-vasculature/raw/main/dataset/test/images/1505.tif"}}
    )


def rle_encode(mask):
    pixel = mask.flatten()
    pixel = np.concatenate([[0], pixel, [0]])
    run = np.where(pixel[1:] != pixel[:-1])[0] + 1
    run[1::2] -= run[::2]
    rle = ' '.join(str(r) for r in run)
    if rle == '':
        rle = '1 0'
    return rle


def add_masks(masks):
    result = 255*(np.sum(masks, axis=0))
    result = result.clip(0, 255).astype("uint8")
    return result


def get_rle_from_result(result: Results):
    if not result.masks:
        return '1 0'
    else:
        masks_array = result.masks.data.numpy()
        combined_mask = add_masks(masks_array)
        return rle_encode(combined_mask)
        

@app.post("/predict_rle_mask")
def predict_rle_mask(input_data: PredictionInput):
    res = model.predict(input_data.url)
    rle_mask = get_rle_from_result(res[0])
    return rle_mask


@app.post("/predict_img")
def predict_img(input_data: PredictionInput):
    res = model.predict(input_data.url)
    img = Image.fromarray(res[0].plot())
    # Save the image to a BytesIO buffer
    img_buffer = BytesIO()
    img.save(img_buffer, format="JPEG")
    img_buffer.seek(0)

    # Return the image as a StreamingResponse with content type "image/jpeg"
    return StreamingResponse(content=img_buffer, media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run("predict:app", reload=True)