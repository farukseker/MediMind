# Versiyon Log

## 0.01.00 – İlk Sürüm
**Tarih:** 12.08.2025

### Genel
- İlaç takip uygulaması için gerekli **backend altyapısı** kuruldu ve **frontend geliştirme süreçlerine** başlandı.
- Uygulama içinde barındırılan **Counter sistemi** stabil çalışmaktadır.
- **Medicine modülü**, yeniden tasarlanmak üzere bir sonraki versiyona bırakıldı.
- Çoklu font desteği eklendi.
- Çoklu tema yapısına uyumluluk sağlandı.

### Modüller
- **Kilo Takip** ve **Su Takip** modülleri amacına uygun şekilde çalışmakta.  
  - İlerleyen sürümlerde ek geliştirmeler planlanmaktadır.

### Bilinen Sorunlar ve Hedefler
- **Pasifik Saati Problemi:**  
  Kullanıcılar kendi yerel saatine göre ilaç hatırlatması kursa bile, sistem Pasifik saatine göre hesaplama yaptığı için bildirim zamanları yanlış çıkabiliyor.  
  - **Plan:** Kullanıcı kayıt olurken saat dilimi seçeneği eklenmesi.  
  - Tüm bölgeler için yeni bir **task modülü** yazılacak.

### Gelecek Planları
- **Frontend bildirim sistemi** daha stabil hale getirilecek.
- Backend ve frontend tarafında ortak bir bildirim yapısı oluşturulacak.  
  - Backend tarafında **dataclass** ile yapılandırma planlanıyor.
  - `sw.js` dosyası daha okunabilir ve kolay işlenebilir hale getirilecek.
- Ayarlar sekmesindeki eksiklikler giderilecek.  
  - Yeni özelliklerin eklenmesi ile birlikte navigasyon sistemi güncellenecek.
