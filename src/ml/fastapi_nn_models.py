from time import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import torch

from src.ml.llm import model, tokenizer, device
from src.ml.title_distilbert import title_pipeline
from src.ml.category_distilbert import category_pipeline

app = FastAPI()

class TextItem(BaseModel):
    text: str

class TextList(BaseModel):
    texts: List[str]

category_mapping = {
    'cr': 1,
    'ai': 2,
    'cbdc': 3,
    'oth': 4,
    'none': 4,
    'bid': 5,
    'tok': 6,
    'defi': 7,
    'api': 8
}

@app.get("/")
async def hello():
    try:
        return 'hello'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/llm/")
async def query_text(query: TextItem):
    try:

        with torch.no_grad():
            article = query.text

            messages = [
                {"role": "user", "content": f"Write a short summary of 1 sentence for the article: {article}"},
            ]

            encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
            model_inputs = encodeds.to(device)

            generated_ids = model.generate(model_inputs, max_new_tokens=100, do_sample=False, num_beams=1)
            decoded = tokenizer.batch_decode(generated_ids)

            text = decoded[0] 

            index = text.find('[/INST]')
            response = text[index+len('[/INST] '):-4]
            if response[-1]=='.':
                response+='..'
            else:
                response+='...'
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/title/")
async def query_text(query: TextItem):
    try:
        with torch.no_grad():
            title = query.text
            result = title_pipeline(title, truncation=True, max_length=512)
            response = 0
            if result[0]['label']=='LABEL_1':
                if result[0]['score'] > 0.5:
                    response = 1
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/category/")
async def query_text(query: TextItem):
    try:
        with torch.no_grad():
            category = query.text
            result = category_pipeline(category, truncation=True, max_length=512)
            label = result[0]['label']
            response = category_mapping[label]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    