# Firebase Studio Teknik Fizibilite Analizi

Bu rapor, Firebase Studio (GenAI in Firebase) ortamının mevcut VLM/LLM projemiz (llama-cpp-python + Phi-3.5-vision) için uygunluğunu değerlendirir.

## 1. Firebase Studio Genel Bakış
Firebase Studio, özellikle Google'ın **Gemini** modellerini Firebase uygulamalarına entegre etmek için tasarlanmış bir geliştirme ortamıdır. Genellikle Vertex AI üzerinden API tabanlı çalışır.

## 2. Teknik Kısıtlar ve Çakışmalar

| Kriter | Mevcut Gereksinim (Local Engine) | Firebase Studio / App Hosting Durumu | Uygunluk |
| :--- | :--- | :--- | :--- |
| **Inference Tipi** | Local GGUF (CPU-only) | API-based (Gemini) veya Cloud Functions | **Düşük** |
| **RAM** | 8-10 GB (Sürekli) | Fonksiyon başına sınırlı (Max 32GB ama maliyetli) | **Orta** |
| **Timeout** | Sınırsız (Lokal işlem süresi) | Max 540-3600 saniye (Cloud Functions) | **Düşük** |
| **Dosya Sistemi** | Yazılabilir/Kalıcı yerel dizinler | Read-only veya Ephemeral (Geçici) | **Kritik Sorun** |

## 3. Neden Uygun Değil?

1.  **Yerel Model Desteği Eksikliği:** Firebase Studio, özel GGUF dosyalarını yükleyip bir C++ binding (llama-cpp) üzerinden çalıştırmak için değil, Google'ın hazır modellerine (Gemini) API ile bağlanmak için optimize edilmiştir. Bizim motorumuz (llama-cpp) düşük seviyeli kütüphane bağımlılıkları gerektirir; bu da Firebase Functions ortamında kurulum ve çalışma hatalarına neden olur.
2.  **Maliyet ve Verimlilik:** Cloud Functions üzerinde 8GB RAM ve yoğun CPU kullanımı, her sunum oluşturma işlemi için yüksek maliyet üretir. Google Colab bu iş için ücretsiz/daha esnek bir sandbox sunarken, Firebase bir "production serverless" ortamıdır ve ağır inference işlemleri için tasarlanmamıştır.
3.  **Kalıcı Depolama:** Sunum şablonları ve üretilen dosyalar için Firebase Storage entegrasyonu gerekir. Mevcut kodumuzdaki doğrudan dosya sistemi erişimi, Firebase'in sunucusuz (serverless) yapısıyla uyumsuzdur.

## 4. Sonuç
**Firebase Studio bu proje için "Sandbox" olarak uygun değildir.**
Kodumuzun mimarisi "Serverless" değil, "Server-based/Desktop" şeklindedir. Google Colab, işletim sistemi seviyesinde erişim ve RAM esnekliği sunduğu için sandbox testi için tek mantıklı bulut alternatifidir.
