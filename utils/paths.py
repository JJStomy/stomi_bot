from enum import Enum
import os

class Paths(Enum):

    PROMPTS = os.path.join("resources", "prompts")
    MESSAGES = os.path.join("resources", "messages")
    IMAGES = os.path.join("resources", "images", "{file}.jpg")
    IMAGES_DIR = os.path.join("resources", "images")
    SERVER = os.path.join("resources", "server")