import streamlit as st
import gTTS
import PyPDF2
import docx
from pptx import Presentation
from PIL import Image
import pytesseract
import io

# Configuración de la página
st.set_page_config(page_title="Lector de Documentos a Audio", page_icon="🎙️")

st.title("🎙️ Convertidor de Documentos y Fotos a Audio")
st.write("Sube tu archivo (PDF, Word, PowerPoint) o una foto de un escrito a mano para escucharlo en audio.")

# Carga de archivo
uploaded_file = st.file_uploader(
    "Selecciona un archivo o foto", 
    type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"]
)

texto_extraido = ""

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    with st.spinner("Procesando archivo..."):
        # 1. Procesar PDF
        if file_type == "pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                texto_extraido += page.extract_text() or ""
                
        # 2. Procesar Word (.docx)
        elif file_type == "docx":
            doc = docx.Document(uploaded_file)
            for paragraph in doc.paragraphs:
                texto_extraido += paragraph.text + "\n"
                
        # 3. Procesar PowerPoint (.pptx)
        elif file_type == "pptx":
            prs = Presentation(uploaded_file)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        texto_extraido += shape.text + "\n"
                        
        # 4. Procesar Fotos / Manuscritos (OCR)
        elif file_type in ["png", "jpg", "jpeg"]:
            image = Image.open(uploaded_file)
            texto_extraido = pytesseract.image_to_string(image, lang="spa")

    if texto_extraido.strip():
        st.success("¡Texto extraído con éxito!")
        
        with st.expander("Ver texto extraído"):
            st.write(texto_extraido)
            
        st.subheader("🔊 Audio Generado")
        with st.spinner("Generando audio..."):
            tts = gTTS(text=texto_extraido, lang='es')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            st.audio(fp, format='audio/mp3')
            
            st.download_button(
                label="Descargar Audio (MP3)",
                data=fp,
                file_name="documento_convertido.mp3",
                mime="audio/mp3"
            )
    else:
        st.warning("No se pudo extraer texto del archivo subido.")

st.markdown("---")
st.caption("© 2026 Todos los derechos reservados. Desarrollado bajo la idea original del Titular.")
