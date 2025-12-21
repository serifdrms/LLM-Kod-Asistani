import streamlit as st
import google.generativeai as genai

API_KEY = "AIzaSyAqgqxgeJA5gOGkgcaHmkpMNZ5K5-U9CzE" 

# Model Yapılandırması
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- FONKSİYONLAR ---
def kod_uret(problem_tanimi):
    """Kullanıcının problemine göre Türkçe açıklamalı kod üretir."""
    prompt = f"""
    Sen uzman bir yazılım geliştiricisisin. Aşağıdaki problem için Python diliyle temiz, optimize edilmiş bir kod yaz.
    
    Problem: {problem_tanimi}
    
    Kurallar:
    1. Sadece Python kodu üretme, kodun içine Türkçe yorum satırları ekle.
    2. Kodun en başına ne yaptığını kısaca özetle.
    3. Kod bloklarını markdown formatında ver.
    """
    response = model.generate_content(prompt)
    return response.text

def kod_acikla(kod_blogu):
    """Verilen kod bloğunun ne işe yaradığını adım adım anlatır."""
    prompt = f"""
    Aşağıdaki kod bloğunu yazılıma yeni başlayan birine anlatır gibi, adım adım Türkçe olarak açıkla.
    Teknik terimleri basitleştir.
    
    Kod:
    {kod_blogu}
    """
    response = model.generate_content(prompt)
    return response.text

# --- ARAYÜZ (UI) TASARIMI ---
st.set_page_config(page_title="TR-Kod Asistanı", layout="wide")

st.title("Kod Üretici ve Açıklayıcı")
st.markdown("---")

# Yan Menü (Sidebar)
st.sidebar.header("Menü")
secim = st.sidebar.radio("Ne yapmak istersiniz?", ["Proje Yarat", "Kod Açıkla"])

st.sidebar.info("Bu proje LLM Olarak Gemini Kullanılarak, Müh.Bil.Uygulamaları Dersi İçin Geliştirilmiştir")

# ANA EKRAN AKIŞI
if secim == "Proje Yarat":
    st.subheader("📝 Konuşma Dilinden -> Koda")
    st.write("Yapmak istediğiniz projeyi Türkçe anlatın, sizin için kodlayalım.")
    
    user_input = st.text_area("Örnek: 'Python Dili Kullanarak, Yılan Oyunu Yap.'", height=150)
    
    if st.button("Kodu Oluştur"):
        if user_input:
            with st.spinner('Projenizin Kodları Yazılıyor...'):
                try:
                    sonuc = kod_uret(user_input)
                    st.success("İşlem Tamamlandı")
                    st.markdown(sonuc)
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen bir problem tanımı girin.")

elif secim == "Kod Açıkla":
    st.subheader("🔍 Kod Analizi ve Açıklama")
    st.write("Anlamadığınız kodları yapıştırın, sizin için ne olduğunu adım adım açıklayalım.")
    
    code_input = st.text_area("Kodunuzu buraya yapıştırın:", height=200)
    
    if st.button("Kodu Analiz Et"):
        if code_input:
            with st.spinner('Kod inceleniyor...'):
                try:
                    aciklama = kod_acikla(code_input)
                    st.success("Analiz Tamamlandı")
                    st.markdown(aciklama)
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen açıklanacak kodu girin.")

# Alt Bilgi
st.markdown("---")
st.markdown("*Geliştirici: 212523203-Ömer Şerif DURMUŞ | Mühendislikte Bilgisayar Uygulamaları Dersi İçin Geliştirilmiştir.*")