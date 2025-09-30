import streamlit as st
from pytubefix import YouTube
import moviepy.editor as mpe
import os

st.title("YouTube 视频下载与合成")

# 输入 YouTube 链接
link = st.text_input("请输入 YouTube 视频链接:")

if link:
    try:
        video = YouTube(link, use_po_token=True)
        st.write(f"视频标题: {video.title}")
        st.write(f"发布日期: {video.publish_date.strftime('%Y-%m-%d')}")

        if st.button("下载并合成视频"):
            st.info("正在下载视频和音频，请稍候...")

            # 获取视频流和音频流
            b = video.streams.filter(mime_type="video/mp4").order_by('resolution').desc().first()
            a = video.streams.filter(only_audio=True).first()

            # 下载并重命名
            vname = "clip.mp4"
            aname = "audio.mp3"
            final_name = video.publish_date.strftime('%Y-%m-%d') + '_' + video.title + '_Youtube.mp4'

            b.download()
            os.rename(b.default_filename, vname)
            a.download()
            os.rename(a.default_filename, aname)

            # 合成音频到视频
            vid = mpe.VideoFileClip(vname)
            aud = mpe.AudioFileClip(aname)
            final = vid.set_audio(aud)
            final.write_videofile(final_name)

            # 删除中间文件
            os.remove(vname)
            os.remove(aname)

            st.success("下载和合成完成！")
            st.download_button("下载视频", data=open(final_name, "rb"), file_name=final_name)

    except Exception as e:
        st.error(f"出现错误: {e}")
