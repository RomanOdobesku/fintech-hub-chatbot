from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

device='cuda:0'

title_pipeline = pipeline('text-classification', model='./models/title-distilbert', device=device)
