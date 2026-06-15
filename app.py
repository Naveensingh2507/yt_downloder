import streamlit as st
import yt_dlp
import os
import imageio_ffmpeg

# 1. Custom CSS Theme Injection
st.markdown("""
    <style>
    /* Main App Background & Font styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Center and Style Main Headers */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    /* Premium Container Card for Inputs */
    .ui-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    /* Target Input Box Focus Animations */
    div.stTextInput > div > div > input {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease;
    }
    div.stTextInput > div > div > input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
    }
    
    /* Primary Processing Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #38bdf8 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(56, 189, 248, 0.6) !important;
    }
    
    /* Native Download Button Styling (Green Success Variant) */
    div.stDownloadButton > button:first-child {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border-radius: 10px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
        margin-top: 1rem !important;
        transition: all 0.3s ease !important;
    }
    div.stDownloadButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(16, 185, 129, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Render Text Headers using Custom HTML Classes
st.markdown('<h1 class="main-title">Apex Stream Puller</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">High-fidelity 4K video extraction engine with integrated digital audio transcoding</p>', unsafe_allow_html=True)

# 3. Wrap Layout Elements inside a Visual Component Card
st.markdown('<div class="ui-card">', unsafe_allow_html=True)

video_url = st.text_input("YouTube Stream URL Location:", placeholder="Paste link here (e.g., https://www.youtube.com/...)")

st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

if st.button("⚡ Run Extraction Engine"):
    if video_url:
        with st.spinner("Executing system processes... Resolving formats and multiplexing audio streams..."):
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
                    info = ydl.extract_info(video_url, download=True)
                    file_path = ydl.prepare_filename(info)
                    
                    if not file_path.endswith('.mp4'):
                        file_path = os.path.splitext(file_path)[0] + '.mp4'

                st.balloons() # Visual celebration drops across the screen
                st.success("Target media multiplexed successfully onto cloud architecture.")
                
                with open(file_path, "rb") as video_file:
                    st.download_button(
                        label="💾 Download Asset to Client Machine",
                        data=video_file,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"Hardware/Network runtime intercept: {e}")
    else:
        st.warning("Input registry empty. Provide valid uniform resource locator (URL).")

st.markdown('</div>', unsafe_allow_html=True) # Closes the custom ui-card container div