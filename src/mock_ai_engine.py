import json
import time
from typing import List, Dict, Any

class MockAIEngine:
    """
    Mock AI Engine that mimics the real AIEngine interface.
    Used for testing UI and logic without a real model.
    """
    def __init__(self, model_path=None, mmproj_path=None):
        pass

    def load_model(self):
        print("Mock model loading...")
        time.sleep(1)

    def unload_model(self):
        print("Mock model unloading...")

    def analyze_image(self, image_path: str, prompt: str) -> str:
        return f"Bu bir mock görsel analizidir. Görsel yolu: {image_path}"

    def generate_presentation_structure(self, text_content: str, image_descriptions: List[str]) -> Dict[str, Any]:
        return {
            "presentation_title": "Mock Sunum",
            "slides": [
                {
                    "title": "Giriş Slaytı",
                    "content": ["Yerel AI Sunum Hazırlayıcıya Hoş Geldiniz", "Bu bir mock örneğidir."],
                    "image_index": None,
                    "layout_hint": "Title Slide"
                },
                {
                    "title": "Analiz Sonuçları",
                    "content": ["Görsel başarıyla analiz edildi.", "Metin işleme tamamlandı."],
                    "image_index": 0,
                    "layout_hint": "Title and Content"
                }
            ]
        }
