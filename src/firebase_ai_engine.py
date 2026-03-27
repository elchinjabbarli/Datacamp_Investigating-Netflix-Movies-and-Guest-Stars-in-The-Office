import os
import json
import logging
import base64
from typing import List, Dict, Any, Optional
from src.utils import log_interaction

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class FirebaseAIEngine:
    """
    AI Engine for Firebase Sandbox environment using Google Gemini.
    Used for testing when local GGUF inference is not practical in the cloud.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = None

        if GENAI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.logger.warning("Gemini API Key missing or google-generativeai not installed.")

    def analyze_image(self, image_path: str, prompt: str) -> str:
        if not self.model:
            return "Hata: Gemini API yapılandırılmadı. Lütfen API anahtarını kontrol edin."

        try:
            with open(image_path, "rb") as f:
                image_data = f.read()

            # Prepare parts for Gemini
            image_part = {"mime_type": "image/jpeg", "data": image_data}

            response = self.model.generate_content([prompt, image_part])
            content = response.text

            log_interaction(prompt, content, metadata={"type": "firebase_image_analysis", "platform": "Firebase/Gemini"})
            return content
        except Exception as e:
            self.logger.error(f"Firebase görsel analiz hatası: {e}")
            return f"Görsel analiz edilemedi: {str(e)}"

    def generate_presentation_structure(self, text_content: str, image_descriptions: List[str]) -> Dict[str, Any]:
        if not self.model:
            return {"error": "Gemini API yapılandırılmadı.", "slides": []}

        prompt = f"""
Aşağıdaki verilere dayanarak maksimum 10 slaytlık bir sunum planı oluştur.
Yanıtın sadece geçerli bir JSON objesi olmalı.

İçerik: {text_content[:2000]}
Görseller: {', '.join(image_descriptions)}

JSON Formatı:
{{
  "presentation_title": "...",
  "slides": [
    {{
      "title": "...",
      "content": ["madde 1", "madde 2"],
      "image_index": 0,
      "layout_hint": "Title and Content"
    }}
  ]
}}
"""
        try:
            response = self.model.generate_content(prompt)
            content = response.text

            log_interaction(prompt, content, metadata={"type": "firebase_planning", "platform": "Firebase/Gemini"})

            # Cleanup JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)
        except Exception as e:
            self.logger.error(f"Firebase sunum yapısı hatası: {e}")
            return {"error": str(e), "slides": []}
