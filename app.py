import os
import base64
import requests
from io import BytesIO

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

st.set_page_config(page_title="Generator Imagine", layout="centered")
st.markdown("<h1 style='text-align:center;margin-bottom:0.4rem'>Generator Imagine</h1>", unsafe_allow_html=True)
st.caption("Interfață Streamlit care folosește **OpenAI – DALL-E-3**.")

with st.sidebar:
    st.header("Setări")
    mock_mode = st.toggle(
        "Mock mode (fără API)", value=False,
        help="Dacă e activ, se generează o imagine placeholder (fără apel la API)."
    )
    size = st.radio("Dimensiune (DALL·E 3)", ["1024x1024", "1024x1792", "1792x1024"], index=0)
    quality = st.radio("Calitate", ["standard", "hd"], index=0)
    st.markdown("---")

prompt = st.text_area("Prompt", value="O pisică albă care doarme pe o pernă albastră", height=120)

def resize_to_size(img: Image.Image, size_str: str) -> Image.Image:
    W, H = map(int, size_str.split("x"))
    return img.resize((W, H), Image.LANCZOS)

def pil_to_png_bytes(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def placeholder_image(size_str: str, text: str = "PLACEHOLDER") -> Image.Image:

    W, H = map(int, size_str.split("x"))
    img = Image.new("RGBA", (W, H), (34, 34, 34, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    try:

        left, top, right, bottom = d.textbbox((0, 0), text, font=font)
        tw, th = right - left, bottom - top
    except Exception:

        tw, th = d.textlength(text, font=font), 12
    d.text(((W - tw) / 2, (H - th) / 2), text, fill=(220, 220, 220, 255), font=font)
    return img

def extract_image_bytes(result) -> bytes:

    img_obj = result.data[0] if getattr(result, "data", None) else result["data"][0]

    b64 = getattr(img_obj, "b64_json", None) or (img_obj.get("b64_json") if isinstance(img_obj, dict) else None)
    if b64:
        return base64.b64decode(b64)

    url = getattr(img_obj, "url", None) or (img_obj.get("url") if isinstance(img_obj, dict) else None)
    if url:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.content

    raise ValueError(f"Răspuns fără imagine utilă: {img_obj}")

def show_placeholder_with_message(message: str, size_str: str, text: str = "PLACEHOLDER"):

    st.info(message)
    img = placeholder_image(size_str, text=text)
    st.session_state.image_bytes = pil_to_png_bytes(img)

if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "last_params" not in st.session_state:
    st.session_state.last_params = {}

go = st.button("Generează")

if go:
    st.session_state.image_bytes = None
    st.session_state.last_params = {"prompt": prompt, "size": size, "quality": quality, "mock": mock_mode}

    api_key = st.secrets.get("OPENAI_API_KEY", "")

    if mock_mode:
        show_placeholder_with_message(
            "Mock mode activ – am generat o imagine placeholder.",
            size, text="MOCK PLACEHOLDER"
        )

    elif not api_key:
        show_placeholder_with_message(
            "Cheia API lipsește – am generat o imagine placeholder. "
            "Adaugă cheia în Streamlit Cloud → Settings → Secrets (OPENAI_API_KEY).",
            size, text="NO API KEY"
        )

    else:
        if OpenAI is None:
            show_placeholder_with_message(
                "Pachetul `openai` nu este instalat. Am generat o imagine placeholder. "
                "Adaugă `openai` în requirements.txt.",
                size, text="SDK MISSING"
            )
        else:
            client = OpenAI(api_key=api_key)
            with st.spinner("Generez cu OpenAI (dall-e-3)..."):
                try:
                    res = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size=size,
                        quality=quality,
                        n=1,
                    )
                    st.session_state.image_bytes = extract_image_bytes(res)
                except Exception as e:

                    show_placeholder_with_message(
                        f"Cheia API este invalidă sau a apărut o eroare la generare. "
                        f"Am creat un placeholder. Detalii: {e}",
                        size, text="API ERROR"
                    )

if st.session_state.image_bytes:
    st.markdown("### Rezultat")
    st.image(st.session_state.image_bytes, caption="Imagine generată", use_container_width=True)
    st.download_button(
        "Descarcă PNG",
        data=st.session_state.image_bytes,
        file_name="imagine.png",
        mime="image/png",
        key="dl_1",
    )
else:
    st.info("Completează promptul și apasă **Generează** pentru a produce o imagine.")
