import os
import json
import logging
import base64
import gc
from typing import List, Dict, Any, Optional

# Self-Correction Note:
# 1. llama-cpp-python loading can be heavy. We must ensure model paths are verified before instantiation.
# 2. We use 'try-except' around model loading to catch potential memory allocation failures (OOM).
# 3. 'n_ctx' is limited to 2048 to keep RAM usage within the ~8-10GB budget for a 4B model + context.

try:
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Llava15ChatHandler
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False
    logging.error("llama-cpp-python not found. Ensure it is installed with appropriate CPU flags.")

class AIEngine:
    """
    AI Engine for local LLM/VLM inference (Phi-3.5-vision).
    Optimized for CPU-only environments with 8-10GB RAM limit.
    """
    def __init__(self, model_path: str, mmproj_path: str, n_ctx: int = 2048):
        self.logger = logging.getLogger(__name__)
        self.model_path = model_path
        self.mmproj_path = mmproj_path
        self.n_ctx = n_ctx
        self.llm = None
        self.chat_handler = None

        # Initial Self-Correction: Verify files before starting heavy operations
        self._validate_files()

    def _validate_files(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model dosyası bulunamadı: {self.model_path}")
        if not os.path.exists(self.mmproj_path):
            raise FileNotFoundError(f"Vision (CLIP) dosyası bulunamadı: {self.mmproj_path}")

    def load_model(self):
        """
        Loads the model into RAM. Includes error handling for memory failures.
        """
        if not LLAMA_AVAILABLE:
            raise ImportError("llama-cpp-python kütüphanesi eksik.")

        try:
            # Memory Management: Clear previous instances if any
            self.unload_model()

            self.logger.info(f"Model yükleniyor: {self.model_path}")
            self.chat_handler = Llava15ChatHandler(clip_model_path=self.mmproj_path)

            # RAM Optimization:
            # - n_threads: CPU core sayısına göre otomatik (veya kısıtlanabilir)
            # - n_batch: RAM tasarrufu için düşük tutuldu (512)
            # - n_ctx: 2048 (Phi-3.5'in yeteneklerini korurken RAM tasarrufu sağlar)
            self.llm = Llama(
                model_path=self.model_path,
                chat_handler=self.chat_handler,
                n_ctx=self.n_ctx,
                n_batch=512,
                n_threads=max(1, os.cpu_count() - 1),
                verbose=False,
                logits_all=False # RAM tasarrufu
            )
            self.logger.info("Model başarıyla yüklendi.")
        except MemoryError:
            self.logger.critical("Model yüklenirken RAM yetersiz kaldı (OOM)!")
            raise Exception("RAM yetersiz. Lütfen diğer uygulamaları kapatıp tekrar deneyin.")
        except Exception as e:
            self.logger.error(f"Model yükleme hatası: {str(e)}")
            raise

    def unload_model(self):
        """
        Unloads model and triggers garbage collection to free RAM.
        """
        if self.llm:
            del self.llm
            self.llm = None
        if self.chat_handler:
            del self.chat_handler
            self.chat_handler = None
        gc.collect()

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        Self-Correction: Checks if image exists and if model is loaded.
        """
        if not os.path.exists(image_path):
            return f"Hata: Görsel bulunamadı ({image_path})"

        if not self.llm:
            self.load_model()

        try:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")

            data_uri = f"data:image/jpeg;base64,{image_base64}"

            messages = [
                {"role": "system", "content": "Sen yardımcı bir asistansın. Görselleri Türkçe analiz et."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_uri}}
                    ]
                }
            ]

            response = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=300, # Yanıtı kısa tutup RAM/Zaman tasarrufu yapıyoruz
                temperature=0.2 # Daha tutarlı yanıtlar için düşük ısı
            )

            return response["choices"][0]["message"]["content"]
        except Exception as e:
            self.logger.error(f"Görsel analiz hatası: {e}")
            return f"Görsel analiz edilemedi: {str(e)}"

    def generate_presentation_structure(self, text_content: str, image_descriptions: List[str]) -> Dict[str, Any]:
        """
        Generates presentation layout structure as JSON.
        """
        if not self.llm:
            self.load_model()

        # Input truncation for self-correction (context management)
        # Çok uzun metinler n_ctx'i aşabilir, bu yüzden metni kısıtlıyoruz
        safe_content = text_content[:1500]

        prompt = f"""
Aşağıdaki verilere dayanarak maksimum 10 slaytlık bir sunum planı oluştur.
Yanıtın sadece geçerli bir JSON objesi olmalı.

İçerik: {safe_content}
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
            response = self.llm.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                response_format={"type": "json_object"}
            )
            content = response["choices"][0]["message"]["content"]

            # Simple cleanup for JSON strings
            if "```" in content:
                content = content.split("```")[1].replace("json", "").strip()

            return json.loads(content)
        except Exception as e:
            self.logger.error(f"Sunum yapısı oluşturma hatası: {e}")
            return {"error": str(e), "slides": []}
