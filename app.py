import streamlit as st
import os
import time
try:
    from src.ai_engine import AIEngine
except ImportError:
    AIEngine = None
from src.mock_ai_engine import MockAIEngine
from src.ppt_generator import PPTGenerator
from src.utils import setup_logger

# Page Config
st.set_page_config(page_title="AI Sunum Hazırlayıcı", layout="wide")

# Setup Logger
logger = setup_logger()

# Session State Initialization
if "generated_file" not in st.session_state:
    st.session_state.generated_file = None

def main():
    st.title("🚀 Yerel AI Sunum Hazırlayıcı")
    st.markdown("""
    Bu uygulama, yerel LLM/VLM modellerini kullanarak metin ve görsellerinizden otomatik sunum hazırlar.
    Tamamen çevrimdışı çalışır ve verileriniz bilgisayarınızda kalır.
    """)

    # Sidebar - Settings
    st.sidebar.header("⚙️ Ayarlar")
    mock_mode = st.sidebar.checkbox("Mock Mode (Model olmadan test et)", value=False)

    model_path = st.sidebar.text_input("GGUF Model Yolu", value="models/phi-3.5-vision-instruct.Q4_K_M.gguf")
    mmproj_path = st.sidebar.text_input("MMProject (CLIP) Yolu", value="models/phi-3.5-vision-instruct-mmproj.bin")

    st.sidebar.divider()

    # Template Upload
    st.subheader("1. Şablon ve İçerik")
    col1, col2 = st.columns(2)

    with col1:
        template_file = st.file_uploader("Kurumsal PPTX Şablonu Yükle (Opsiyonel)", type=["pptx"])
        if template_file:
            with open(os.path.join("templates", "master_template.pptx"), "wb") as f:
                f.write(template_file.getbuffer())
            st.success("Şablon yüklendi.")

    with col2:
        content_file = st.file_uploader("Metin veya Markdown Dosyası Yükle", type=["txt", "md"])
        content_text = ""
        if content_file:
            content_text = content_file.read().decode("utf-8")
            st.text_area("İçerik Önizleme", content_text[:500] + "...", height=150)

    # Image Upload
    st.subheader("2. Görseller")
    image_files = st.file_uploader("Sunuma eklenecek görselleri seçin", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    uploaded_image_paths = []
    if image_files:
        cols = st.columns(len(image_files) if len(image_files) < 5 else 5)
        for i, img_file in enumerate(image_files):
            img_path = os.path.join("uploads", img_file.name)
            with open(img_path, "wb") as f:
                f.write(img_file.getbuffer())
            uploaded_image_paths.append(img_path)

            # Preview
            with cols[i % 5]:
                st.image(img_path, caption=img_file.name, use_container_width=True)

    # Generation
    st.divider()
    if st.button("✨ Sunumu Oluştur", type="primary", use_container_width=True):
        if not content_text:
            st.error("Lütfen bir metin içeriği yükleyin.")
            return

        try:
            with st.status("Sunum hazırlanıyor...", expanded=True) as status:
                # 1. Initialize Engine
                st.write("🤖 AI Modeli yükleniyor...")
                if mock_mode:
                    engine = MockAIEngine()
                else:
                    if AIEngine is None:
                        st.error("llama-cpp-python kütüphanesi yüklü değil! Lütfen 'pip install llama-cpp-python' komutu ile yükleyin veya Mock Mode kullanın.")
                        return
                    if not os.path.exists(model_path) or not os.path.exists(mmproj_path):
                        st.error(f"Model dosyaları bulunamadı! Lütfen {model_path} ve {mmproj_path} yollarını kontrol edin.")
                        return
                    engine = AIEngine(model_path, mmproj_path)

                # 2. Analyze Images
                image_descriptions = []
                if uploaded_image_paths:
                    st.write("🖼️ Görseller analiz ediliyor...")
                    for img_path in uploaded_image_paths:
                        desc = engine.analyze_image(img_path, "Bu görselde ne var? Sunumda nasıl kullanılabilir? Kısa özetle.")
                        image_descriptions.append(desc)
                        st.write(f"✅ {os.path.basename(img_path)} analiz edildi.")

                # 3. Generate Structure
                st.write("📝 Sunum yapısı oluşturuluyor...")
                structure = engine.generate_presentation_structure(content_text, image_descriptions)

                if "error" in structure:
                    st.error(f"Hata: {structure['error']}")
                    return

                # 4. Generate PPTX
                st.write("📊 PowerPoint dosyası oluşturuluyor...")
                template_path = os.path.join("templates", "master_template.pptx") if template_file else None
                generator = PPTGenerator(template_path)

                output_filename = f"sunum_{int(time.time())}.pptx"
                output_path = os.path.join("output", output_filename)

                final_path = generator.create_presentation(structure, uploaded_image_paths, output_path)

                st.session_state.generated_file = final_path
                status.update(label="✅ Sunum başarıyla oluşturuldu!", state="complete", expanded=False)

            st.balloons()

            # Download Link
            with open(st.session_state.generated_file, "rb") as f:
                st.download_button(
                    label="📥 Sunumu İndir (.pptx)",
                    data=f,
                    file_name=os.path.basename(st.session_state.generated_file),
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )

        except Exception as e:
            st.error(f"Beklenmedik bir hata oluştu: {str(e)}")
            logger.error(f"General error: {e}", exc_info=True)

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    main()
