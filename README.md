# Yerel AI Sunum Hazırlayıcı (AI Presentation Agent)

Bu proje, şirket politikalarına uygun, tamamen yerel (local) çalışan ve verilerinizi dışarı aktarmayan bir AI sunum hazırlama asistanıdır. Görsellerinizi ve metinlerinizi analiz ederek kurumsal PowerPoint şablonlarınıza uygun sunumlar hazırlar.

## Özellikler

- **Tamamen Yerel:** İnternet bağlantısı gerektirmez, verileriniz bilgisayarınızda kalır.
- **Düşük Kaynak Kullanımı:** 16GB RAM'e sahip bilgisayarlarda (8-10GB RAM kullanımı ile) CPU-only çalışacak şekilde optimize edilmiştir.
- **VLM Desteği:** Phi-3.5-vision modeli ile görsel içerik analizi yapabilir.
- **Şablon Sistemi:** Mevcut kurumsal `.pptx` dosyalarınızı şablon olarak kullanır.
- **Günlük Kaydı:** Tüm prompt'lar ve işlemler `/logs` klasöründe saklanır.

## Kurulum (Windows 10/11)

### 1. Python Kurulumu
Bilgisayarınızda Python 3.10 veya üzeri yüklü olmalıdır.

### 2. Bağımlılıkların Yüklenmesi
Terminali (PowerShell veya CMD) açın ve proje klasörüne gidin:

```bash
pip install -r requirements.txt
```

**Not:** `llama-cpp-python` kütüphanesinin Windows'ta CPU desteği ile düzgün derlenmesi için [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) yüklü olması önerilir. Alternatif olarak önceden derlenmiş tekerlekleri (wheels) kullanabilirsiniz.

### 3. Modellerin İndirilmesi
Uygulamanın çalışması için aşağıdaki modelleri indirip `models/` klasörüne yerleştirmeniz gerekmektedir:

- **LLM/VLM:** `phi-3.5-vision-instruct.Q4_K_M.gguf`
- **MMProject (Vision Encoder):** `phi-3.5-vision-instruct-mmproj.bin`

Modelleri Hugging Face (örneğin `bartowski/Phi-3.5-vision-instruct-GGUF`) üzerinden indirebilirsiniz.

## Kullanım

Uygulamayı başlatmak için:

```bash
streamlit run app.py
```

Tarayıcınızda açılan arayüz üzerinden:
1. Sol menüden model yollarını doğrulayın.
2. (Opsiyonel) Şirketinizin kurumsal `.pptx` şablonunu yükleyin.
3. Sunum içeriğini (.txt veya .md) yükleyin.
4. Sunumda kullanılacak görselleri seçin.
5. "Sunumu Oluştur" butonuna tıklayın.

## Klasör Yapısı

- `app.py`: Ana Streamlit uygulama dosyası.
- `src/`: Core mantık (AI Engine ve PPT Generator).
- `models/`: GGUF model dosyalarının bulunacağı yer.
- `templates/`: Yüklenen şablonların saklandığı yer.
- `output/`: Üretilen sunumların kaydedildiği yer.
- `logs/`: İşlem loglarının ve prompt geçmişinin tutulduğu yer.

## Güvenlik ve Gizlilik
Uygulama herhangi bir bulut API'sine (OpenAI, Gemini vb.) bağlanmaz. Tüm işlemler `llama-cpp-python` aracılığıyla yerel işlemciniz (CPU) üzerinde gerçekleştirilir.
