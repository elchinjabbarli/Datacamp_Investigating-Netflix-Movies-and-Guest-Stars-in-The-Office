# Google Colab Sandbox Kullanım Kılavuzu

Bu rehber, projenin Google Colab üzerinde sadece **test ve doğrulama** amaçlı nasıl çalıştırılacağını açıklar.

### ⚠️ ÖNEMLİ GÜVENLİK UYARISI
Colab ortamı Google'ın bulut sunucularıdır. Bu ortama **HİÇBİR ŞEKİLDE** kurumsal, gizli veya hassas veri yüklemeyiniz. Sadece sahte (dummy) test verileri kullanınız.

## Adımlar

1.  **Notebook'u Yükleyin:** Proje ana dizinindeki `Colab_Sandbox.ipynb` dosyasını bilgisayarınıza indirin ve [Google Colab](https://colab.research.google.com/) üzerine yükleyin.
2.  **Hücreleri Sırayla Çalıştırın:**
    *   **1. Hücre:** Gerekli Python kütüphanelerini (`llama-cpp-python`, `streamlit` vb.) kurar.
    *   **2. Hücre:** Phi-3.5-vision modelini HuggingFace üzerinden otomatik indirir (Hızı Colab internetine bağlıdır, genellikle 1-2 dk sürer).
    *   **3. Hücre:** Uygulama kodlarını ve `src/config.py` ayarlarını Colab ortamına göre oluşturur.
    *   **4. Hücre:** `ngrok` tüneli üzerinden Streamlit arayüzünü dış dünyaya (sizin erişiminiz için) açar.
3.  **ngrok Token:** 4. hücreyi çalıştırmadan önce [ngrok.com](https://ngrok.com/) adresinden ücretsiz bir hesap açıp "Your Authtoken" kısmındaki kodu notebook içine yapıştırmalısınız.
4.  **Erişim:** Hücre çalıştıktan sonra size verilen `http://xxxx.ngrok-free.app` benzeri adrese tıklayarak uygulamayı tarayıcınızda kullanabilirsiniz.

## Neden Colab?
*   Yerel bilgisayarınızda yeterli kaynak yoksa hızlıca doğrulama yapmanızı sağlar.
*   Hata ayıklama (debug) süreçlerini izole bir ortamda yürütmenize yardımcı olur.
*   Ekibinizle dummy veriler üzerinden demo paylaşmanıza olanak tanır.
