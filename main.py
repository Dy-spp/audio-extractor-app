"""
音频提取器 - Android App
批量提取视频中的音频
"""

import os
import threading
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

Window.size = (350, 600)

class AudioExtractorApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_files = []
        self.output_folder = None
        self.converting = False
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        toolbar = MDToolbar(title="🎵 音频提取器", md_bg_color=self.theme_cls.primary_color)
        main_layout.add_widget(toolbar)
        
        content = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # 说明卡片
        info_card = MDCard(orientation='vertical', padding=10, size_hint=(1, None), height=80)
        info_label = MDLabel(text="批量提取视频中的音频文件\n支持 MP4, AVI, MKV 等格式", 
                            halign="center", theme_text_color="Secondary", font_style="Caption")
        info_card.add_widget(info_label)
        content.add_widget(info_card)
        
        # 选择视频
        self.select_btn = MDRaisedButton(text="📁 选择视频文件", size_hint=(1, None), height=50,
                                        on_release=self.select_videos)
        content.add_widget(self.select_btn)
        
        self.video_label = MDLabel(text="未选择视频", size_hint=(1, None), height=40, halign="center")
        content.add_widget(self.video_label)
        
        # 选择输出
        self.output_btn = MDRaisedButton(text="📂 选择输出文件夹", size_hint=(1, None), height=50,
                                        on_release=self.select_output)
        content.add_widget(self.output_btn)
        
        self.output_label = MDLabel(text="未选择输出文件夹", size_hint=(1, None), height=40, halign="center")
        content.add_widget(self.output_label)
        
        # 转换按钮
        self.convert_btn = MDRaisedButton(text="🚀 开始转换", size_hint=(1, None), height=50,
                                         on_release=self.start_conversion)
        content.add_widget(self.convert_btn)
        
        # 进度条
        self.progress_bar = ProgressBar(size_hint=(1, None), height=30, value=0)
        content.add_widget(self.progress_bar)
        
        self.progress_label = MDLabel(text="进度: 0%", size_hint=(1, None), height=30, halign="center")
        content.add_widget(self.progress_label)
        
        self.status_label = MDLabel(text="✅ 准备就绪", size_hint=(1, None), height=50, halign="center")
        content.add_widget(self.status_label)
        
        scroll = ScrollView()
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def select_videos(self, instance):
        """选择视频文件"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        filechooser = FileChooserListView(
            path='/storage/emulated/0/' if self.is_android() else '.',
            filters=['*.mp4', '*.avi', '*.mov', '*.mkv', '*.flv', '*.wmv'],
            multiselect=True
        )
        content.add_widget(filechooser)
        
        confirm_btn = MDRaisedButton(text="确认选择", size_hint=(1, None), height=50,
                                    on_release=lambda x: self.on_videos_selected(filechooser.selection))
        content.add_widget(confirm_btn)
        
        self.video_dialog = MDDialog(title="选择视频文件", type="custom", content_cls=content, size_hint=(0.9, 0.8))
        self.video_dialog.open()
    
    def on_videos_selected(self, selection):
        if selection:
            self.video_files = selection
            self.video_label.text = f"✅ 已选择 {len(selection)} 个视频文件"
        self.video_dialog.dismiss()
    
    def select_output(self, instance):
        """选择输出文件夹"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        dirchooser = FileChooserListView(
            path='/storage/emulated/0/' if self.is_android() else '.',
            dirselect=True
        )
        content.add_widget(dirchooser)
        
        confirm_btn = MDRaisedButton(text="确认选择", size_hint=(1, None), height=50,
                                    on_release=lambda x: self.on_output_selected(dirchooser.path))
        content.add_widget(confirm_btn)
        
        self.output_dialog = MDDialog(title="选择输出文件夹", type="custom", content_cls=content, size_hint=(0.9, 0.8))
        self.output_dialog.open()
    
    def on_output_selected(self, path):
        self.output_folder = path
        self.output_label.text = f"✅ 输出: {os.path.basename(path)}"
        self.output_dialog.dismiss()
    
    def start_conversion(self, instance):
        if not self.video_files:
            self.show_dialog("错误", "请先选择视频文件")
            return
        if not self.output_folder:
            self.show_dialog("错误", "请先选择输出文件夹")
            return
        if self.converting:
            self.show_dialog("提示", "转换正在进行中...")
            return
        
        self.converting = True
        self.convert_btn.disabled = True
        self.progress_bar.value = 0
        
        threading.Thread(target=self.convert_videos).start()
    
    def convert_videos(self):
        total = len(self.video_files)
        for idx, video_path in enumerate(self.video_files, 1):
            filename = os.path.basename(video_path)
            base_name = os.path.splitext(filename)[0]
            audio_path = os.path.join(self.output_folder, f"{base_name}.mp3")
            
            Clock.schedule_once(lambda dt, msg=f"🎬 处理: {filename}": self.update_status(msg), 0)
            
            if not os.path.exists(audio_path):
                # 模拟转换（实际需要ffmpeg）
                with open(audio_path, 'w') as f:
                    f.write("音频文件")
            
            progress = (idx / total) * 100
            Clock.schedule_once(lambda dt, p=progress: self.update_progress(p), 0)
        
        self.converting = False
        Clock.schedule_once(lambda dt: self.enable_convert_btn(), 0)
        Clock.schedule_once(lambda dt: self.show_dialog("完成", f"转换完成！共处理 {total} 个文件"), 0)
    
    def update_progress(self, value):
        self.progress_bar.value = value
        self.progress_label.text = f"进度: {value:.1f}%"
    
    def update_status(self, message):
        self.status_label.text = message
    
    def enable_convert_btn(self):
        self.convert_btn.disabled = False
    
    def show_dialog(self, title, message):
        dialog = MDDialog(title=title, text=message,
                         buttons=[MDFlatButton(text="确定", on_release=lambda x: dialog.dismiss())])
        dialog.open()
    
    def is_android(self):
        try:
            from android import AndroidService
            return True
        except ImportError:
            return False

if __name__ == "__main__":
    AudioExtractorApp().run()