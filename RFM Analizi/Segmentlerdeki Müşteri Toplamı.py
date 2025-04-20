# RFM Analizinde ihtiyacımızın olduğu kütüphaneleri dahil ederek başlıyoruz.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Verilerimin olduğu dosyayı çalışmama dahil edip okutuyoruz.(xlsx, txt vb. formatlarda da okuma işlemi sağlayabiliriz)
df = pd.read_csv("/content/online.csv")

# Veri dosyamızın içerisinde tarih formatı (12/1/2009 9:06) bu ancak bunu dönüştürüyoruz.
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Verilerinizin içerisinde ister istemez boş alanlar muhakkak olacaktır. Bu yüzden boş müşteri ID'lerini çıkartarak doğru bir analiz gerçekleştirmeliyiz.(Ya da boş alanlara değer atamalıyız.)
df = df.dropna(subset=["Customer ID"])

# Toplam harcamayı hesapla
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Analiz için referans tarih (verideki en son tarihin 1 gün sonrası)
analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# RFM metriklerini hesaplıyoruz
rfm = df.groupby("Customer ID").agg({
    "InvoiceDate": lambda x: (analysis_date - x.max()).days,  # Recency
    "Invoice": "nunique",                                     # Frequency
    "TotalPrice": "sum"                                       # Monetary
}).reset_index()

# Metriklerden sonra kolon adlarını güncelliyoruz
rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]

# RFM skorlarını 1-5 arası belirliyoruz
rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

# RFM skorunu birleştir
rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

# Segment fonksiyonu
def segment_customer(row):
    if row["RFM_Score"] == '555':
        return "VIP"
    elif int(row["R_Score"]) >= 4 and int(row["F_Score"]) >= 4:
        return "Sadık Müşteri"
    elif int(row["R_Score"]) >= 4:
        return "Yeni Müşteri"
    elif int(row["F_Score"]) >= 4:
        return "Sık Alışveriş Yapan"
    elif int(row["M_Score"]) >= 4:
        return "Yüksek Harcayan"
    else:
        return "Riskli Müşteri"

# Segmentleri ata
rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# Sonuçları yazdır
print(rfm[["CustomerID", "RFM_Score", "Segment"]].head())

# Gerekli kütüphaneleri yükle
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns



# Veri dosyasını oku (CSV formatında)
df = pd.read_csv("/content/online.csv")

# Tarih formatını düzenle
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Boş müşteri ID'lerini çıkar
df = df.dropna(subset=["Customer ID"])

# Toplam harcamayı hesapla
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Analiz için referans tarih (verideki en son tarihin 1 gün sonrası)
analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# RFM metriklerini hesapla
rfm = df.groupby("Customer ID").agg({
    "InvoiceDate": lambda x: (analysis_date - x.max()).days,  # Recency
    "Invoice": "nunique",                                     # Frequency
    "TotalPrice": "sum"                                       # Monetary
}).reset_index()

# Kolon adlarını güncelle
rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]

# RFM skorlarını 1-5 arası belirle
rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

# RFM skorunu birleştir
rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

# Segment fonksiyonu
def segment_customer(row):
    if row["RFM_Score"] == '555':
        return "VIP"
    elif int(row["R_Score"]) >= 4 and int(row["F_Score"]) >= 4:
        return "Sadık Müşteri"
    elif int(row["R_Score"]) >= 4:
        return "Yeni Müşteri"
    elif int(row["F_Score"]) >= 4:
        return "Sık Alışveriş Yapan"
    elif int(row["M_Score"]) >= 4:
        return "Yüksek Harcayan"
    else:
        return "Riskli Müşteri"

# Segmentleri ata
rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# Sonuçları yazdır
print(rfm[["CustomerID", "RFM_Score", "Segment"]].head())

# Segment bazında müşteri sayısını göster
print("\nSegmentlere Göre Müşteri Dağılımı:")
print(rfm["Segment"].value_counts())

# Segmentlerde tüm müşteri toplamı 
print("\nSegmentlerdeki toplam Müşteri Sayısı:")
print(rfm["Segment"].count())