[app]
title = 音频提取器
package.name = audioextractor
package.domain = com.dyspp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.9.7,kivy==2.2.1,kivymd==1.1.1
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30
android.arch = arm64-v8a
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
