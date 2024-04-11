from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

device='cuda:0'

category_pipeline = pipeline('text-classification', model='./models/category-distilbert', device=device)
