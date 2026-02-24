import os
import sys

class Config:
    """
    Environment-aware configuration for Local and Colab/Sandbox environments.
    """
    # Detect if running in Google Colab
    IS_COLAB = 'google.colab' in sys.modules

    # Base Directories
    BASE_DIR = os.getcwd()

    # Model Paths (Defaults)
    MODEL_PATH = "models/phi-3.5-vision-instruct.Q4_K_M.gguf"
    MMPROJ_PATH = "models/phi-3.5-vision-instruct-mmproj.bin"

    # If in Colab, models might be in a different path (e.g., Google Drive or /content/models)
    if IS_COLAB:
        MODEL_DIR = "/content/models"
        UPLOAD_DIR = "/content/uploads"
        OUTPUT_DIR = "/content/output"
        LOG_DIR = "/content/logs"
        TEMPLATE_DIR = "/content/templates"
    else:
        MODEL_DIR = "models"
        UPLOAD_DIR = "uploads"
        OUTPUT_DIR = "output"
        LOG_DIR = "logs"
        TEMPLATE_DIR = "templates"

    @classmethod
    def get_model_path(cls, filename=None):
        if filename:
            return os.path.join(cls.MODEL_DIR, filename)
        return os.path.join(cls.MODEL_DIR, os.path.basename(cls.MODEL_PATH))

    @classmethod
    def get_mmproj_path(cls, filename=None):
        if filename:
            return os.path.join(cls.MODEL_DIR, filename)
        return os.path.join(cls.MODEL_DIR, os.path.basename(cls.MMPROJ_PATH))

    @classmethod
    def initialize_env(cls):
        """Creates necessary folders based on environment."""
        folders = [cls.UPLOAD_DIR, cls.OUTPUT_DIR, cls.LOG_DIR, cls.TEMPLATE_DIR, cls.MODEL_DIR]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
