from multiprocessing import Process
from multiprocessing import Process

import os
os.chdir(os.path.join(os.path.dirname(__file__)))
import subprocess
from dotenv import load_dotenv
import os
import requests
import GPUtil
import shutil
import whisper
import psutil
import glob
import math
import torch
import traceback
import hashlib
import stripe
from user_agents import parse  
import sys
import json
import time
import random
import re
import subprocess
import platform
import tempfile
from firebase_admin import db
import secrets
import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yt_dlp
import uuid
from termcolor import cprint
from queue import Queue, Empty
import builtins
import requests
import pytz
from celery import Celery
import os
from celery.result import AsyncResult
import signal




import configparser
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################

from huggingface_hub import InferenceClient
from huggingface_hub import login


import os
import pickle
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter
import cv2
import torch
import json

from PIL import Image, ImageSequence
import os
import torch
import numpy as np
import json
import time
from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info

from Build.Studio.AnimateGif import create_animated_fire_with_gif

cache_dir = r"D:\LLMModels"

# detect_fire_region(image_path)
import numpy as np
import torch
import torchvision.transforms as T
from decord import VideoReader, cpu
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def blend_images(background, overlay, position):
    """Combina duas imagens com melhor controle de transparência"""
    if overlay.mode != 'RGBA':
        overlay = overlay.convert('RGBA')
    
    result = background.copy()
    result.paste(overlay, position, overlay)
    return result

def load_gif_frames(gif_path, size):
    """Carrega e redimensiona os frames do GIF para o tamanho desejado."""
    gif = Image.open(gif_path)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA").resize(size, Image.Resampling.LANCZOS)

        frames.append(frame)
    return frames

def detect_fire_region(image_path):
    """Detecta a região onde o fogo da fogueira começa com base na análise da imagem."""
    start_time = time.time()

    # Carrega o modelo na GPU
    model_path = 'OpenGVLab/InternVL2-1B'
    model = AutoModel.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        use_flash_attn=True,
        trust_remote_code=True, 
        cache_dir=cache_dir
    ).eval().cuda()

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, use_fast=False, 
        cache_dir=cache_dir)

    pixel_values = load_image(image_path, max_num=12).to(torch.bfloat16).cuda()
    generation_config = dict(max_new_tokens=1024, do_sample=True)

    question = '''<image>\nAnalyze the image to detect the presence of a campfire and identify the center where the campfire is. Then, return a JSON object like the following example:
    [
        {"bbox_2d": [x_min, y_min, x_max, y_max], "label": "ignition_point"}
    ]
    '''

    output_text = model.chat(tokenizer, pixel_values, question, generation_config)
    print("Resposta do modelo:", output_text)

    # Liberação de memória do modelo após a inferência
    del model
    torch.cuda.empty_cache()

    # Extrai o bloco JSON do texto de saída
    match = re.search(r'(\{.*\})', output_text, re.DOTALL)
    if match:
        json_text = match.group(1)

        # Tentativa de converter para JSON
        try:
            data = json.loads(json_text)

            # Suporte para quando data é um dicionário ou uma lista
            if isinstance(data, dict) and "bbox_2d" in data:
                bbox = data["bbox_2d"]
            elif isinstance(data, list) and len(data) > 0 and "bbox_2d" in data[0]:
                bbox = data[0]["bbox_2d"]
            else:
                print("Erro: Nenhuma bounding box válida foi encontrada.")
                print("Texto recebido:", json_text)
                return 547, 689

            x_min, y_min, x_max, y_max = bbox

            # Calcula o ponto de ignição como o centro da bounding box
            x_center = (x_min + x_max) // 2
            y_center = (y_min + y_max) // 2

            print(f"Coordenadas do ponto de ignição: ({x_center}, {y_center})")
            print(f"Tempo de execução: {time.time() - start_time:.2f} segundos")
            return x_center, y_center

        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e)
            print("Texto recebido:", json_text)

    print("Nenhuma fogueira detectada. Retornando coordenadas padrão.")
    return 547, 689  # Coordenadas padrão caso o modelo falhe


def create_animated_fire_with_gif(input_path, output_path, gif_path):
    """Cria um GIF animado adicionando o GIF pré-existente nas coordenadas da fogueira."""
    # Carrega a imagem de fundo
    background = Image.open(input_path).convert('RGBA')
    width, height = background.size

    # Detecta a região ideal para a fogueira
    fire_position = detect_fire_region(input_path) ## #
    if fire_position is None:
        print("Fogueira não detectada.")
        return

    fire_x_replace, fire_y_replace = fire_position

    print(fire_position)

    
    fire_x = fire_x_replace

    fire_y = fire_y_replace 
    # if gif_path == "Studio\CampFire\fire2.gif":
    # else:
       #fire_y = fire_y_replace + 40


    print(fire_x)

    print(fire_y)

    #(474.0, 490.5)


    # Define o tamanho desejado para o GIF (por exemplo, 1/4 da largura e altura da imagem)
    fire_width = width // 4
    fire_height = height // 4

    # Carrega os frames do GIF pré-existente
    fire_frames = load_gif_frames(gif_path, (fire_width, fire_height))

    # Cria uma lista para armazenar os frames combinados
    combined_frames = []
    for frame in fire_frames:
        # Sobrepõe o frame do GIF na imagem de fundo na posição detectada
        combined = blend_images(background, frame, (int(fire_x), int(fire_y)))
        combined_frames.append(combined)

    # Salva os frames combinados como um GIF animado
    combined_frames[0].save(
        output_path,
        save_all=True,
        append_images=combined_frames[1:],
        duration=50,  # Ajuste a duração conforme necessário
        loop=0,
        optimize=False
    )

def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

def load_image(image_file, input_size=448, max_num=12):
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values

image_path = r"D:\CompanyApps\Saas\MediaCutsVersions\MediaCutsStudioV3.0.0.0\Servers\Home_Server\Build\Studio\WorkEnvironment\Process\PixelBackground\tester4.jpg"
fire_gif = r"D:\CompanyApps\Saas\MediaCutsVersions\MediaCutsStudioV3.0.0.0\Servers\Home_Server\Build\Studio\CampFire\fire2replace.gif"
output_gif = "teste.png"
create_animated_fire_with_gif(image_path, output_gif, fire_gif)