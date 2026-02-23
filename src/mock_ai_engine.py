import json
from typing import List, Dict, Any

class MockAIEngine:
    """
    Mock AI Engine for testing without a real model.
    """
    def __init__(self, model_path=None, mmproj_path=None):
        pass

    def analyze_image(self, image_path: str, prompt: str) -> str:
        return f"Bu bir mock görsel analizidir. Görsel: {image_path}"

    def generate_presentation_structure(self, text_content: str, image_descriptions: List[str]) -> Dict[str, Any]:
        return {
            "presentation_title": "Örnek Sunum",
            "slides": [
                {
                    "slide_number": 1,
                    "title": "Giriş",
                    "content": ["Sunumun amacına hoş geldiniz.", "Bu bir test içeriğidir."],
                    "image_index": None,
                    "layout": "Title Slide"
                },
                {
                    "slide_number": 2,
                    "title": "Görsel Analizi",
                    "content": ["Görsel başarıyla analiz edildi.", "Detaylar burada yer alacak."],
                    "image_index": 0,
                    "layout": "Title and Content"
                }
            ]
        }
