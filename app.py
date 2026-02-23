import streamlit as st
import os
import time
import shutil
from src.mock_ai_engine import MockAIEngine
from src.ppt_generator import PPTGenerator
from src.utils import setup_logger

# Self-Correction: Handle AIEngine import failure (e.g. llama-cpp not installed)
try:
    from src.ai_engine import AIEngine
except ImportError:
    AIEngine = None

# App Configuration
st.set_page_config(page_title="AI Sunum Hazırlayıcı", layout="wide", page_icon="🚀")
logger = setup_logger()

# Constants
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"

def init_folders():
    for folder in [UPLOAD_DIR, OUTPUT_DIR, TEMPLATE_DIR, "logs"]:
        os.makedirs(folder, exist_ok=True)

def cleanup_uploads():
    """Self-Correction: Prevent disk bloat by cleaning old uploads."""
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
        os.makedirs(UPLOAD_DIR)

def main():
    init_folders()

    st.title("🚀 Yerel AI Sunum Hazırlayıcı")
    st.info("Bu uygulama tamamen çevrimdışı çalışır. Verileriniz cihazınızdan dışarı çıkmaz.")

    # Sidebar - Settings & Hardware
    with st.sidebar:
        st.header("⚙️ Sistem Ayarları")
        mock_mode = st.checkbox("Mock Mode (Model olmadan test)", value=False)

        st.subheader("Modeller")
        model_path = st.text_input("GGUF Model Yolu", "models/phi-3.5-vision-instruct.Q4_K_M.gguf")
        mmproj_path = st.text_input("Vision Projector Yolu", "models/phi-3.5-vision-instruct-mmproj.bin")

        st.divider()
        st.write(f"💻 CPU Çekirdek Sayısı: {os.cpu_count()}")
        if st.button("🗑️ Geçici Dosyaları Temizle"):
            cleanup_uploads()
            st.success("Temizlendi.")

    # Main UI Layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. İçerik ve Şablon")
        template_file = st.file_uploader("Kurumsal Şablon (.pptx)", type=["pptx"])
        content_file = st.file_uploader("Metin/Markdown İçeriği (.txt, .md)", type=["txt", "md"])

        content_text = ""
        if content_file:
            content_text = content_file.read().decode("utf-8")
            st.text_area("İçerik Önizleme", content_text[:300] + "...", height=100)

    with col2:
        st.subheader("2. Görseller")
        image_files = st.file_uploader("Görselleri Seçin", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

        image_paths = []
        if image_files:
            for img_file in image_files:
                path = os.path.join(UPLOAD_DIR, img_file.name)
                with open(path, "wb") as f:
                    f.write(img_file.getbuffer())
                image_paths.append(path)
            st.write(f"{len(image_paths)} görsel yüklendi.")

    st.divider()

    # Generation Logic
    if st.button("✨ Sunumu Oluştur", type="primary", use_container_width=True):
        if not content_text:
            st.warning("Lütfen önce bir içerik metni yükleyin.")
            return

        try:
            with st.status("İşlem başlatılıyor...", expanded=True) as status:
                # Engine Selection
                if mock_mode:
                    status.update(label="Mock Engine kullanılıyor...")
                    engine = MockAIEngine()
                else:
                    if AIEngine is None:
                        st.error("llama-cpp-python bulunamadı. Lütfen kurulumu kontrol edin.")
                        return
                    if not os.path.exists(model_path):
                        st.error(f"Model dosyası bulunamadı: {model_path}")
                        return
                    status.update(label="AI Modeli yükleniyor (Bu işlem RAM miktarına göre zaman alabilir)...")
                    engine = AIEngine(model_path, mmproj_path)

                # Step 1: Image Analysis
                img_desc = []
                if image_paths:
                    status.update(label="Görseller analiz ediliyor...")
                    for p in image_paths:
                        desc = engine.analyze_image(p, "Bu görseli sunum içeriği için kısaca açıkla.")
                        img_desc.append(desc)
                        st.write(f"✅ {os.path.basename(p)} analiz edildi.")

                # Step 2: Structure Generation
                status.update(label="Sunum planı oluşturuluyor...")
                structure = engine.generate_presentation_structure(content_text, img_desc)

                if "error" in structure:
                    st.error(f"AI Planlama Hatası: {structure['error']}")
                    return

                # Step 3: PPTX Creation
                status.update(label="PowerPoint dosyası hazırlanıyor...")

                # Handle template
                t_path = None
                if template_file:
                    t_path = os.path.join(TEMPLATE_DIR, "current_template.pptx")
                    with open(t_path, "wb") as f:
                        f.write(template_file.getbuffer())

                gen = PPTGenerator(t_path)
                out_name = f"sunum_{int(time.time())}.pptx"
                out_path = os.path.join(OUTPUT_DIR, out_name)

                final_file = gen.create_presentation(structure, image_paths, out_path)

                status.update(label="✅ Sunum hazır!", state="complete", expanded=False)

            st.balloons()
            st.success(f"Başarıyla oluşturuldu: {out_name}")

            with open(final_file, "rb") as f:
                st.download_button(
                    "📥 Sunumu İndir",
                    f,
                    file_name=out_name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )

        except Exception as e:
            st.error(f"Kritik Hata: {str(e)}")
            logger.error(f"App error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
