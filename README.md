# yt-dlp GUI

> Made by **Çınar Civan**

A simple, modern downloader interface for YouTube, Twitch, Twitter and [1000+ sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).  
Supports **Turkish 🇹🇷** and **English 🇬🇧** — switch languages with one click inside the app.

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🇬🇧 English

### Features
- Video + audio, audio-only (mp3 / m4a / opus) or video-only download
- Quality selection (up to 4K)
- Container format selection (mp4, mkv, webm…)
- Subtitle, thumbnail and metadata embedding
- Playlist support
- **yt-dlp is downloaded automatically** — no manual setup needed
- **Built-in language switcher** (TR / EN button in the top-right corner)

### Usage — Ready installer (recommended)
1. Download the Windows installer from the [Releases](https://github.com/cinarcivan/yt-dlp-gui/releases) page
2. Run the installer and complete setup
3. Launch the app — `yt-dlp.exe` is downloaded automatically on first launch into `%LOCALAPPDATA%\yt-dlp-gui`
4. Paste a URL and click **Download**

### Usage — Portable .exe
1. Download `yt-dlp GUI.exe` from the [Releases](https://github.com/cinarcivan/yt-dlp-gui/releases) page
2. Run it — `yt-dlp.exe` is downloaded automatically on first launch into `%LOCALAPPDATA%\yt-dlp-gui`
3. Paste a URL and click **Download**

> First-time launch requires an internet connection to fetch yt-dlp (~10 MB).

### Usage — Run with Python
```bash
# No extra dependencies — Python 3.8+ is enough
python ytdlp_gui.py
```

### Build your own .exe / installer
```bash
git clone https://github.com/USERNAME/ytdlp-gui
cd ytdlp-gui
build.bat
```
Output:
- Portable app: `dist/yt-dlp GUI.exe`
- Installer: `dist/installer/yt-dlp-gui-setup-1.0.0.exe` (if Inno Setup is installed)

Requirements:
- Python 3.8+
- pip
- [Inno Setup](https://jrsoftware.org/isinfo.php) for installer generation

---

## 🇹🇷 Türkçe

### Özellikler
- Video + ses, yalnızca ses (mp3 / m4a / opus) veya yalnızca video indirme
- Kalite seçimi (4K'ya kadar)
- Kapsayıcı format seçimi (mp4, mkv, webm…)
- Altyazı, kapak resmi ve metadata gömme
- Playlist desteği
- **yt-dlp otomatik indirilir** — ayrıca kurulum gerekmez
- **Yerleşik dil değiştirici** (sağ üst köşedeki TR / EN butonu)

### Kullanım — Hazır installer (önerilen)
1. [Releases](https://github.com/cinarcivan/yt-dlp-gui/releases) sayfasından Windows installer dosyasını indir
2. Installer'ı çalıştırıp kurulumu tamamla
3. Uygulamayı aç — `yt-dlp.exe` ilk çalıştırmada `%LOCALAPPDATA%\yt-dlp-gui` klasörüne otomatik indirilir
4. URL'yi yapıştır ve **İndir** butonuna bas

### Kullanım — Portable .exe
1. [Releases](https://github.com/cinarcivan/yt-dlp-gui/releases) sayfasından `yt-dlp GUI.exe` dosyasını indir
2. Çalıştır — ilk açılışta `yt-dlp.exe` `%LOCALAPPDATA%\yt-dlp-gui` klasörüne otomatik indirilir
3. URL'yi yapıştır ve **İndir** butonuna bas

> İlk çalıştırma için internet bağlantısı gerekir (~10 MB).

### Kullanım — Python ile çalıştır
```bash
# Ek bağımlılık yok — Python 3.8+ yeterli
python ytdlp_gui.py
```

### Kendi .exe / installer paketini oluştur
```bash
git clone https://github.com/KULLANICI_ADI/ytdlp-gui
cd ytdlp-gui
build.bat
```
Çıktı:
- Portable uygulama: `dist/yt-dlp GUI.exe`
- Installer: `dist/installer/yt-dlp-gui-setup-1.0.0.exe` (Inno Setup kuruluysa)

Gereksinimler:
- Python 3.8+
- pip
- Installer üretmek için [Inno Setup](https://jrsoftware.org/isinfo.php)

---

## License / Lisans

MIT
