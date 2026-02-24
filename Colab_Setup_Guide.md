# Google Colab Kurulum Rehberi (Test Amaçlı)

Eğer sistemi test etmek veya bir demo yapmak için Google Colab üzerinde çalıştırmak isterseniz aşağıdaki adımları izleyebilirsiniz.

> **Uyarı:** Bu yöntem verilerinizi Google sunucularına taşır. Hassas kurumsal verilerle kullanmayınız.

### 1. Yeni Bir Notebook Açın ve Drive'ı Bağlayın
Kalıcı depolama için Google Drive'ı bağlamanız önerilir:
```python
from google.colab import drive
drive.mount('/content/drive')
```

### 2. Bağımlılıkları Yükleyin
```bash
!pip install streamlit python-pptx marko python-dotenv Pillow
!CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
!pip install pyngrok # Streamlit'i dışarı açmak için
```

### 3. Modelleri Hazırlayın
Modelleri `/content/models` klasörüne indirin:
```bash
!mkdir -p models
!wget -O models/phi-3.5-vision-instruct.Q4_K_M.gguf [MODEL_LINK]
!wget -O models/phi-3.5-vision-instruct-mmproj.bin [PROJ_LINK]
```

### 4. Streamlit'i Çalıştırın
Colab'da Streamlit'i çalıştırmak için bir arka plan işlemi başlatmalı ve bir tünel oluşturmalısınız:
```python
import os
# ngrok token'ınızı girin (ngrok.com'dan ücretsiz alabilirsiniz)
!ngrok authtoken YOR_NGROK_TOKEN

get_ipython().system_raw('streamlit run app.py &')

from pyngrok import ngrok
public_url = ngrok.connect(8501)
print(f"Uygulama Adresi: {public_url}")
```

### 5. Kod Değişiklikleri
`app.py` içinde model yollarını `/content/models/...` şeklinde güncellediğinizden emin olun.
