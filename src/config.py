import os
import sys

class Config:
    """
    Environment-aware configuration for Local, Colab, and Firebase environments.
    """
    # Detect environments
    IS_COLAB = 'google.colab' in sys.modules
    IS_FIREBASE = 'FIREBASE_CONFIG' in os.environ or os.environ.get('FORCE_FIREBASE') == '1'

    # Base Directories
    BASE_DIR = os.getcwd()

    # Path Logic
    if IS_COLAB or IS_FIREBASE:
        prefix = "colab_" if IS_COLAB else "firebase_"
        # Use absolute path for Colab if not forced
        root = "/content/" if (IS_COLAB and os.environ.get('FORCE_COLAB') != '1') else ""

        MODEL_DIR = os.path.join(root, f"{prefix}models")
        UPLOAD_DIR = os.path.join(root, f"{prefix}uploads")
        OUTPUT_DIR = os.path.join(root, f"{prefix}output")
        LOG_DIR = os.path.join(root, f"{prefix}logs")
        TEMPLATE_DIR = os.path.join(root, f"{prefix}templates")
    else:
        MODEL_DIR = "models"
        UPLOAD_DIR = "uploads"
        OUTPUT_DIR = "output"
        LOG_DIR = "logs"
        TEMPLATE_DIR = "templates"

    # Model Paths (Defaults)
    MODEL_PATH = os.path.join(MODEL_DIR, "phi-3.5-vision-instruct.Q4_K_M.gguf")
    MMPROJ_PATH = os.path.join(MODEL_DIR, "phi-3.5-vision-instruct-mmproj.bin")

    @classmethod
    def get_model_path(cls, filename=None):
        if filename:
            return os.path.join(cls.MODEL_DIR, filename)
        return cls.MODEL_PATH

    @classmethod
    def get_mmproj_path(cls, filename=None):
        if filename:
            return os.path.join(cls.MODEL_DIR, filename)
        return cls.MMPROJ_PATH

    @classmethod
    def initialize_env(cls):
        """Creates necessary folders based on environment."""
        folders = [cls.UPLOAD_DIR, cls.OUTPUT_DIR, cls.LOG_DIR, cls.TEMPLATE_DIR, cls.MODEL_DIR]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
