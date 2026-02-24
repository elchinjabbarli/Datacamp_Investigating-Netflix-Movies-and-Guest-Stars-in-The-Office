# Teknik Analiz: Yerel Mimari vs. Bulut (Google Colab/GCP) Entegrasyonu

Bu rapor, geliştirilen AI Sunum Hazırlayıcı'nın bulut ortamlarına taşınmasının teknik ve idari etkilerini incelemektedir.

## 1. Güvenlik ve Uyumluluk Analizi
**Risk Skoru: Kritik**

*   **Veri Gizliliği İhlali:** Mevcut "tamamen local" politikası, verinin (metinler, kurumsal görseller, sunum içerikleri) fiziksel olarak şirketin kontrolündeki bir donanımın dışına çıkmamasını garanti eder. Buluta taşındığında, bu veriler Google altyapısına yüklenir.
*   **İşleme Şartları:** Google Colab ve GCP kullanım şartları, verilerin belirli koşullarda (anonimleştirilmiş olsa bile) model iyileştirme veya sistem denetimi için kullanılabileceği maddeler içerebilir. Bu, kurumsal gizli bilgilerin (KPI'lar, stratejik planlar) sızma riskini doğurur.
*   **Ağ Erişimi:** Bulut tabanlı bir sistem, doğası gereği internete bağlıdır. Bu durum, yerel sistemdeki "tam izole" yapıyı bozar ve siber saldırı yüzeyini genişletir.

## 2. Kaynak Yeterliliği (Colab/GCP)
*   **RAM:** Google Colab (Ücretsiz) ~12.7 GB RAM sunar. Phi-3.5-vision (4-bit) yaklaşık 3-4 GB RAM (model + context + overhead) kullanır. Bu açıdan Colab yeterlidir. Ancak GCP'de maliyet odaklı düşük segment makineler (n1-standard-1 gibi) 3.75 GB RAM ile yetersiz kalacaktır.
*   **CPU Performansı:** Colab CPU'ları paylaşımlıdır. `llama-cpp-python` CPU üzerinde çalışırken yerel bir i7/i9 veya M1/M2 işlemciye göre 2-3 kat daha yavaş kalabilir.

## 3. Kalıcılık (Persistence)
*   **Efemeral Yapı:** Colab oturumu kapandığında `uploads/`, `logs/` ve `output/` klasörlerindeki her şey silinir.
*   **Çözüm:** Verileri saklamak için Google Drive'ı mount etmek veya bir GCS (Google Cloud Storage) bucket'ı kullanmak gerekir. Bu da veri sızıntısı riskini artıran ek bir "dış bağlantı" katmanıdır.

## 4. Kod Değişikliği Gereksinimleri
*   **Streamlit Erişimi:** Colab doğrudan bir web sunucusu gibi davranmaz. Streamlit arayüzünü görebilmek için `localtunnel` veya `ngrok` gibi tünelleme servisleri kullanılmalıdır.
*   **Dosya Yolları:** Kod içindeki dosya yolları `/content/` dizinine göre güncellenmelidir.
*   **Model Yönetimi:** Modellerin her oturumda tekrar indirilmesi (veya Drive'dan kopyalanması) gerekir, bu da başlangıç süresini 5-10 dakika uzatır.

---

## Neden Yerel (Local) Kalmalı? (Şirket Yönetimi İçin Teknik Argümanlar)

1.  **Sıfır Veri Sızıntısı (Zero Data Leakage):** Şirket verileri hiçbir zaman internete çıkmaz. "Air-gapped" (internet bağlantısı olmayan) bilgisayarlarda bile çalışabilir.
2.  **Maliyet Kontrolü:** Bulut servisleri (GCP, Colab Pro) aylık abonelik veya kullanım bazlı ücret üretir. Yerel sistemde bir kez alınan donanım, sınırsız ve ücretsiz işlem gücü sağlar.
3.  **Hukuki Uyumluluk (GDPR/KVKK):** Hassas verilerin ülke sınırları veya şirket dışına çıkması durumunda oluşabilecek hukuki sorumluluklar yerel mimari ile tamamen ortadan kalkar.
4.  **Bağımsızlık:** İnternet kesintilerinden veya bulut sağlayıcısının servis kesintilerinden etkilenmez.
5.  **Performans Tahmin Edilebilirliği:** Paylaşımlı bulut kaynakları yerine, kullanıcının kendi CPU gücüyle her zaman aynı hızda yanıt alınır.
