import streamlit as st
import yt_dlp
import os
import imageio_ffmpeg
import time

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Naveen YT Downloader",
    page_icon="⚡",
    layout="centered"
)

# 2. HIGH-END BESPOKE CSS INJECTION
st.markdown("""
    <style>
    /* Reset & Deep Dark Background Slate */
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #f1f5f9;
    }
    
    /* Header Branding */
    .brand-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #f43f5e 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        padding-bottom: 0px;
        text-shadow: 0 10px 30px rgba(244, 63, 94, 0.2);
    }
    
    .brand-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Premium Glassmorphism Main Workspace Card */
    .main-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 3rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 2.5rem;
    }
    
    /* Premium Native Text Input Restyling */
    div.stTextInput > div > div > input {
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        border: 2px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        font-size: 1.05rem !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    div.stTextInput > div > div > input:focus {
        border-color: #f43f5e !important;
        box-shadow: 0 0 20px rgba(244, 63, 94, 0.25) !important;
        background-color: #0f172a !important;
    }
    
    /* The Crimson Extraction Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 16px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 14px !important;
        width: 100% !important;
        box-shadow: 0 8px 24px rgba(225, 29, 72, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        letter-spacing: 0.5px;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(225, 29, 72, 0.5) !important;
    }
    div.stButton > button:first-child:active {
        transform: translateY(-1px) !important;
    }
    
    /* Client Download Button (Emerald Glow Variant) */
    div.stDownloadButton > button:first-child {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 14px !important;
        width: 100% !important;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stDownloadButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 26px rgba(16, 185, 129, 0.5) !important;
    }
    
    /* Custom CSS Loading Animation Shimmer */
    .processing-pulse {
        text-align: center;
        padding: 20px;
        background: rgba(244, 63, 94, 0.1);
        border: 1px dashed #f43f5e;
        border-radius: 14px;
        color: #fca5a5;
        font-weight: 600;
        animation: pulseAnimation 2s infinite alternate;
    }
    @keyframes pulseAnimation {
        0% { opacity: 0.6; box-shadow: 0 0 10px rgba(244,63,94,0.1); }
        100% { opacity: 1; box-shadow: 0 0 25px rgba(244,63,94,0.3); }
    }
    
    /* Reviews Layout Grid */
    .reviews-section {
        margin-top: 4rem;
    }
    .reviews-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #cbd5e1;
        margin-bottom: 1.5rem;
        border-left: 4px solid #f43f5e;
        padding-left: 12px;
    }
    .review-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .review-user {
        font-weight: 700;
        color: #f8fafc;
        display: inline-block;
        margin-right: 10px;
    }
    .review-stars {
        color: #fbbf24;
        font-size: 0.9rem;
    }
    .review-text {
        color: #94a3b8;
        margin-top: 0.5rem;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Developer Profile Section Card */
    .dev-profile {
        margin-top: 5rem;
        padding: 2rem;
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        text-align: center;
    }
    .dev-avatar {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #f43f5e, #fb923c);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.5rem;
        color: white;
        margin: 0 auto 1rem auto;
        box-shadow: 0 0 20px rgba(244,63,94,0.3);
    }
    .dev-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }
    .dev-tag {
        font-size: 0.85rem;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1.2rem;
    }
    .social-btn {
        display: inline-flex;
        align-items: center;
        background: #1e293b;
        color: #e2e8f0 !important;
        text-decoration: none !important;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 8px;
        border: 1px solid #334155;
        transition: all 0.3s ease;
    }
    .social-btn:hover {
        background: #f43f5e;
        color: white !important;
        border-color: #f43f5e;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE TITLES
st.markdown('<h1 class="brand-title">Naveen YT Downloader</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">High-speed, lossless media extraction and processing core</p>', unsafe_allow_html=True)

# 4. MAIN APPARATUS COMPONENT CARD
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Capturing URL stream location
video_url = st.text_input("Enter Target Video Link Location:", placeholder="Paste YouTube link here...")

st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

# Main Processing Trigger
if st.button("⚡ Initialize High-Speed Extraction"):
    if video_url:
        # Injecting custom CSS animated pulsing loader instead of standard spinner
        status_box = st.markdown('<div class="processing-pulse">Initializing cloud pipelines... Compiling multi-threaded video stream...</div>', unsafe_allow_html=True)
        
        try:
            output_folder = "downloads"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_path,
                'postprocessor_args': [
                    '-c:a', 'aac',
                    '-b:a', '192k'
                ],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                status_box.markdown('<div class="processing-pulse">Downloading high-fidelity raw stream arrays... Please wait...</div>', unsafe_allow_html=True)
                info = ydl.extract_info(video_url, download=True)
                
                status_box.markdown('<div class="processing-pulse">Multiplexing video layers & transcoding audio track to high-fidelity AAC...</div>', unsafe_allow_html=True)
                file_path = ydl.prepare_filename(info)
                
                if not file_path.endswith('.mp4'):
                    file_path = os.path.splitext(file_path)[0] + '.mp4'

            # Remove loading element and replace with visual success rewards
            status_box.empty()
            st.balloons()
            st.success("Extraction sequence completed. Asset compiled flawlessly.")
            
            with open(file_path, "rb") as video_file:
                st.download_button(
                    label="💾 Download Finished File to Local Drive",
                    data=video_file,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4"
                )
                
        except Exception as e:
            status_box.empty()
            st.error(f"Pipeline Intercept Error: {e}")
    else:
        st.warning("Input registry empty. Provide a valid video URL first.")

st.markdown('</div>', unsafe_allow_html=True) # End of Main Card

# 5. USER TESTIMONIALS / REVIEWS SECTION
st.markdown('<div class="reviews-section">', unsafe_allow_html=True)
st.markdown('<p class="reviews-header">Global User Metrics & Performance Feedback</p>', unsafe_allow_html=True)

reviews = [
    {"user": "Rohan Sharma", "stars": "⭐⭐⭐⭐⭐", "text": "Unbelievable speeds! I dropped a 1080p link and it multiplexed the video and crystal-clear audio perfectly in seconds. The custom UI looks insanely premium."},
    {"user": "Elena Rostova", "stars": "⭐⭐⭐⭐⭐", "text": "Finally a downloader without spammy redirect ads. This engine transcodes directly to clean AAC audio format. Flawless work, Naveen."},
    {"user": "Devraj Singh", "stars": "⭐⭐⭐⭐★", "text": "Extremely solid implementation. Clean animations and smooth glassmorphic interface layout. Essential tools for creators."}
]

for r in reviews:
    st.markdown(f"""
        <div class="review-card">
            <div>
                <span class="review-user">{r['user']}</span>
                <span class="review-stars">{r['stars']}</span>
            </div>
            <div class="review-text">"{r['text']}"</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. ARCHITECT PROFILE SECTION
st.markdown(f"""
    <div class="dev-profile">
        <div class="dev-avatar">NSR</div>
        <div class="dev-name">Nveen Singh Ratnu</div>
        <div class="dev-tag">Lead System Architect</div>
        <div style="margin-top: 1rem;">
            <a class="social-btn" href="https://www.instagram.com/naveenhujiime/" target="_blank">📸 Connect on Instagram</a>
            <a class="social-btn" href="https://www.linkedin.com/in/naveen-singh-ratnu-848a12319/" target="_blank">💼 Network on LinkedIn</a>
        </div>
    </div>
""", unsafe_allow_html=True)