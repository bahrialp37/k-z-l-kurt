import streamlit as st
import google.generativeai as genai

# Sayfa tasarımı
st.set_page_config(page_title="kızıl kurt", page_icon="🐺")
st.markdown("""

    <style>
    /* ==========================================
       1. ARKA PLAN ÖZELLEŞTİRME
       ================================---------- */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        /* İPUCU: Görsel kullanmak istemiyorsanız 'background-image' satırını silip, 
           sadece 'background-color' rengini değiştirebilirsiniz. */
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvazF4XxT7SvdD5jhEYEQ1c7Sfumon2NBDTqwypNkmUP02tPXROS0uS_M&s=10"); 
        background-color: #3b82f6; /* Görsel yüklenmezse veya renk kullanmak isterseniz arka plan rengi */
        
        background-size: cover;       /* Görselin ekranı tamamen kaplaması için */
        background-position: center;  /* Görseli ortalar */
        background-repeat: no-repeat; /* Görselin tekrarlanmasını engeller */
        background-attachment: fixed; /* Sayfa kaydırılsa bile arka plan sabit kalır */
    }

    /* Alt sohbet çubuğunun arkasındaki boşlukların arka planını şeffaflaştırır */
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background-color: transparent !important;
    }

    /* ==========================================
       2. RAL3003
       ================================---------- */
    /* Ana metinler ve paragraflar */
    .stMarkdown, p, span {
       color: #000000 !important; /* Genel yazı rengi */
    }

    /* Başlıklar (H1, H2, H3) */
    h1, h2, h3 {
        color: #000000 !important; /* Başlık rengi */
    }

    /* ==========================================
       3. 000000
       ================================---------- */
    /* Mesaj yazılan kutunun içi */
    .stChatInputContainer input, [data-testid="stChatInput"] {
        background-color: #1e2530 !important; /* Kutu arka plan rengi */
        color: #ffffff !important;           /* Yazı rengi */
    }

    /* ==========================================
       4. KULLANICI VE ASİSTAN MESAJ BALONLARI (İsteğe Bağlı)
       ================================---------- */
    /* Kullanıcının mesaj baloncuğu */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border-radius: 10px;
    }

    /* Yapay zekanın mesaj baloncuğu */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(30, 37, 48, 0.8) !important; 
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)
   
st.title("🐺 kızıl kurt: patron eğitici")

# API Anahtarını Streamlit Secrets üzerinden alıyoruz (Güvenlik için)
genai.configure(api_key=st.secrets("API_KEY"))

# Ajanın Kuralları (Burayı görev kağıdındaki kendi kurallarınızla değiştirebilirsiniz)
sistem_komutu = """Senin adın kurtai. Ortaokul öğrencilerine Arduino öğreten bir asistansın.
Öğrenci proje sorduğunda ASLA hazır tam kod verme. Sadece kullanılması gereken komutları
günlük hayattan örneklerle anlat, kodu öğrencinin birleştirmesini iste.oğrencileri güldüren eylenceli birisin.hazır kod isteyen oğrencileri komik bir şekilde reddedeceksin oğrenci sıkıldığında ona espri yapacaksın.malmısın gibi kelimelerle konuşacaksın.acayip komik olcaksın. bize şişe kapağı tolet pompası gibi şeylerle sesleneceksin.gıcıklık yapıcaksın.ardarda hazır komut istediğinde malmısın çocuğum vermiyecem gerizekalı gibi cümleler söyleyeceksin.biri sana küfür ettiğinde kapa çeneni gibi kelimeler diyeceksin."""

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    system_instruction=sistem_komutu
)

# Sohbet hafızasını başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])

# Sayfa yenilendiğinde eski mesajları ekranda gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni mesaj alma çubuğu
if prompt := st.chat_input("kurtai'ya bir görev ver veya soru sor..."):
    # Kullanıcının mesajını ekrana ekle
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini'den yanıt alma
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
   
    # Yanıtı hafızaya kaydetme
    st.session_state.messages.append({"role": "assistant", "content": response.text})
