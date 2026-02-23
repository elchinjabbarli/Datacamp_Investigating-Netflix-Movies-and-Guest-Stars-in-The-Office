import os
import json
import logging
from typing import List, Dict, Any, Optional
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
import base64

class AIEngine:
    """
    AI Engine to handle local LLM/VLM inference using llama-cpp-python.
    Optimized for Phi-3.5-vision-instruct (GGUF).
    """
    def __init__(self, model_path: str, mmproj_path: str, n_ctx: int = 4096):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(mmproj_path):
            raise FileNotFoundError(f"MMProject file not found: {mmproj_path}")

        self.chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)
        self.llm = Llama(
            model_path=model_path,
            chat_handler=self.chat_handler,
            n_ctx=n_ctx,
            n_threads=os.cpu_count(),
            verbose=False
        )
        self.logger = logging.getLogger(__name__)

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        Analyzes an image and returns a description or answers a prompt.
        """
        try:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")

            data_uri = f"data:image/jpeg;base64,{image_base64}"

            messages = [
                {"role": "system", "content": "Sen yardımcı bir asistansın. Görselleri analiz edip sunum için içerik hazırlıyorsun."},
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
                max_tokens=500
            )

            content = response["choices"][0]["message"]["content"]
            self._log_prompt(messages, content)
            return content
        except Exception as e:
            self.logger.error(f"Error analyzing image: {e}")
            return f"Görsel analiz edilemedi: {str(e)}"

    def generate_presentation_structure(self, text_content: str, image_descriptions: List[str]) -> Dict[str, Any]:
        """
        Generates a structured plan for the presentation.
        """
        prompt = f"""
Aşağıdaki metin ve görsel analizlerini kullanarak 10 slaytı geçmeyecek bir sunum yapısı oluştur.
Her slayt için şunları belirt:
- Başlık
- İçerik (Madde işaretleri)
- Varsa hangi görselin (Görsel 1, Görsel 2 vb.) kullanılacağı
- Kullanılacak layout tipi (Giriş, İçerik, Görsel ve Metin, Kapanış)

Metin:
{text_content}

Görsel Analizleri:
{chr(10).join([f"Görsel {i+1}: {desc}" for i, desc in enumerate(image_descriptions)])}

Yanıtı sadece JSON formatında ver:
{{
  "presentation_title": "...",
  "slides": [
    {{
      "slide_number": 1,
      "title": "...",
      "content": ["...", "..."],
      "image_index": null,
      "layout": "Title Slide"
    }},
    ...
  ]
}}
"""
        messages = [
            {"role": "system", "content": "Sen profesyonel bir sunum hazırlayıcısısın. Sadece JSON formatında yanıt ver."},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            content = response["choices"][0]["message"]["content"]
            self._log_prompt(messages, content)

            # Clean JSON if it's wrapped in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)
        except Exception as e:
            self.logger.error(f"Error generating presentation structure: {e}")
            return {"error": str(e)}

    def _log_prompt(self, messages: List[Dict], response: str):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "prompts.json")

        log_entry = {
            "messages": messages,
            "response": response
        }

        try:
            logs = []
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)

            logs.append(log_entry)

            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Could not log prompt: {e}")
