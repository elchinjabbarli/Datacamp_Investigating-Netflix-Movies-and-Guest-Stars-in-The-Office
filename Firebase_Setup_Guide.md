# Firebase Studio & App Hosting Sandbox Rehberi

Bu rehber, projenin **Firebase Studio** ve **Firebase App Hosting** üzerinde sadece **test ve sandbox** amaçlı nasıl çalıştırılacağını açıklar.

### ⚠️ ÖNEMLİ GÜVENLİK UYARISI
Firebase ortamı Google Cloud altyapısında çalışır. Bu ortama **HİÇBİR ŞEKİLDE** kurumsal, gizli veya hassas veri yüklemeyiniz. Sadece sahte (dummy) test verileri kullanınız.

## 1. Mimari Yaklaşım
Firebase ortamında (App Hosting/Cloud Run) yerel GGUF modellerini çalıştırmak yüksek kaynak (RAM/CPU) tüketimi ve timeout kısıtları nedeniyle zordur. Bu nedenle Firebase Sandbox modunda **Google Gemini (API)** motoru kullanılmaktadır.

## 2. Kurulum Adımları

### Firebase Projesi Oluşturma
1. [Firebase Console](https://console.firebase.google.com/) üzerinden yeni bir proje oluşturun.
2. Projenizi "Blaze" (Paid) planına geçirin (App Hosting için gereklidir, ancak ücretsiz kota dahilinde kalabilirsiniz).

### Firebase Studio / App Hosting'e Dağıtım
1. Proje dosyalarını GitHub deponuza yükleyin.
2. [Firebase Console > App Hosting](https://console.firebase.google.com/project/_/apphosting) bölümüne gidin.
3. "Get Started" diyerek GitHub deponuzu bağlayın.
4. Dağıtım ayarlarında `apphosting.yaml` dosyasının otomatik algılandığından emin olun.

### Gemini API Anahtarı Tanımlama
1. [Google AI Studio](https://aistudio.google.com/) üzerinden ücretsiz bir API anahtarı alın.
2. Firebase Console > App Hosting > Uygulamanız > Settings > Environment Variables kısmına gidin.
3. `GEMINI_API_KEY` adında bir değişken ekleyin ve anahtarınızı yapıştırın.

## 3. Kullanım
Dağıtım tamamlandığında size bir `xxxx.web.app` adresi verilecektir.
*   Uygulama açıldığında sol üstte **"⚠️ SANDBOX MODU (Bulut)"** uyarısını göreceksiniz.
*   Bu modda LLM işlemleri Gemini üzerinden yürütülecek, ancak sunum üretme (PPTX) mantığı aynı kalacaktır.

## 4. Neden Firebase Studio?
*   Web tabanlı bir IDE deneyimi sunar.
*   Uygulamayı ekibinizle hızlıca paylaşmanıza olanak tanır.
*   Sadece kodun mantıksal akışını (Metin -> Slayt -> PPTX) doğrulamak için idealdir.
