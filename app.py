import io, time, base64, os
import requests
import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison

# ===== إعدادات من Secrets أو Env =====
PROVIDER = (st.secrets.get("ENHANCER_PROVIDER", os.getenv("ENHANCER_PROVIDER", "hf")) or "hf").lower()
HF_API_KEY = st.secrets.get("HF_API_KEY", os.getenv("HF_API_KEY"))
HF_MODEL_ID = st.secrets.get("HF_MODEL_ID", os.getenv("HF_MODEL_ID", "nateraw/real-esrgan"))
DEEPAI_API_KEY = st.secrets.get("DEEPAI_API_KEY", os.getenv("DEEPAI_API_KEY"))

MAX_BYTES = 20 * 1024 * 1024  # 20MB
TIMEOUT = 180  # seconds

st.set_page_config(page_title="4K AI Image Enhancer", page_icon="✨", layout="centered")

st.title("4K AI Image Enhancer (Streamlit)")
st.caption("Upload → One-click enhance → Compare → Download PNG")

uploaded = st.file_uploader("Upload an image (JPG/PNG/WebP)", type=["jpg", "jpeg", "png", "webp"])
enhance_btn = st.button("Enhance Quality Now", disabled=uploaded is None)

def to_png_bytes(pil_img: Image.Image) -> bytes:
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()

def ensure_4k(pil_img: Image.Image) -> Image.Image:
    # اختياري: ضمان الوصول لأبعاد 4K كحدّ أقصى مع الحفاظ على النسبة (Upscale فقط إن كانت أقل)
    W4K, H4K = 3840, 2160
    w, h = pil_img.size
    if w >= W4K or h >= H4K:
        return pil_img
    ratio = w / h
    if ratio >= 16/9:
        new_w = W4K
        new_h = round(new_w / ratio)
    else:
        new_h = H4K
        new_w = round(new_h * ratio)
    return pil_img.resize((new_w, new_h), Image.LANCZOS)

def hf_enhance(img_bytes: bytes) -> bytes:
    if not HF_API_KEY:
        raise RuntimeError("HF_API_KEY missing")
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/octet-stream"}
    # بعض نماذج HF تحتاج تسخين: نكرّر الاستدعاء حتى يرجع بايتات صورة
    start = time.time()
    delay = 2.0
    while True:
        r = requests.post(url, data=img_bytes, headers=headers, timeout=TIMEOUT)
        ct = r.headers.get("content-type", "")
        if r.status_code == 200 and ct.startswith("image/"):
            return r.content
        # حاول قراءة رسالة الخطأ/التحميل
        try:
            msg = r.json()
        except Exception:
            msg = {"error": r.text[:200]}
        if time.time() - start > TIMEOUT:
            raise RuntimeError(f"HF timeout: {msg}")
        time.sleep(delay)
        delay = min(delay * 1.5, 6.0)

def deepai_enhance(img_bytes: bytes) -> bytes:
    if not DEEPAI_API_KEY:
        raise RuntimeError("DEEPAI_API_KEY missing")
    files = {"image": ("input.png", img_bytes)}
    headers = {"Api-Key": DEEPAI_API_KEY}
    r = requests.post("https://api.deepai.org/api/torch-srgan", files=files, headers=headers, timeout=TIMEOUT)
    data = r.json()
    if "output_url" not in data:
        raise RuntimeError(f"DeepAI error: {data}")
    img_r = requests.get(data["output_url"], timeout=TIMEOUT)
    return img_r.content

def enhance(img_bytes: bytes) -> bytes:
    # 1) HF أولاً (إن مُفعّل) مع سقوط تلقائي على DeepAI
    if PROVIDER == "hf" and HF_API_KEY:
        try:
            return hf_enhance(img_bytes)
        except Exception as e:
            if DEEPAI_API_KEY:
                return deepai_enhance(img_bytes)
            raise e
    # 2) DeepAI مباشرة
    if DEEPAI_API_KEY:
        return deepai_enhance(img_bytes)
    # لا مزوّد مفعّل
    raise RuntimeError("No enhancer provider configured. Set HF_API_KEY or DEEPAI_API_KEY.")

if uploaded:
    # عرض الأصل
    try:
        original = Image.open(uploaded).convert("RGB")
    except Exception:
        st.error("Invalid image.")
        st.stop()
    if uploaded.size and uploaded.size > MAX_BYTES:
        st.warning("Image is large; consider ≤ 20MB.")
    st.image(original, caption=f"Original ({original.width}×{original.height})", use_column_width=True)

if enhance_btn and uploaded:
    with st.status("Processing…", expanded=True) as status:
        st.write("Analyzing / Upscaling / Denoising…")
        # اقرأ bytes
        uploaded.seek(0)
        img_bytes = uploaded.read()
        # نفّذ التحسين
        try:
            enhanced_bytes = enhance(img_bytes)
            # افتح كصورة ثم حوّل إلى PNG وضَمِن 4K (اختياري)
            enhanced_img = Image.open(io.BytesIO(enhanced_bytes)).convert("RGB")
            enhanced_img = ensure_4k(enhanced_img)
            png_bytes = to_png_bytes(enhanced_img)
            status.update(label="Done", state="complete")

            # مقارنة قبل/بعد
            st.subheader("Before / After")
            try:
                image_comparison(
                    img1=original,
                    img2=enhanced_img,
                    label1=f"Original {original.width}×{original.height}",
                    label2=f"Enhanced {enhanced_img.width}×{enhanced_img.height}",
                    width=700
                )
            except Exception:
                # احتياط: أعرض عمودين بدل السلايدر إذا الباكيج غير متاح
                c1, c2 = st.columns(2)
                with c1: st.image(original, caption="Original", use_column_width=True)
                with c2: st.image(enhanced_img, caption="Enhanced", use_column_width=True)

            st.download_button(
                "Download PNG",
                data=png_bytes,
                file_name="image-enhanced-4k.png",
                mime="image/png",
                type="primary",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Enhancement failed: {e}")
            st.stop()
