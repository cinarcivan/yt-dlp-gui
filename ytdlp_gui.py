"""
yt-dlp GUI
A simple, modern downloader GUI for Windows.
Supports Turkish and English.

Requirements: Python 3.8+  (tkinter is built-in)
yt-dlp is downloaded automatically — no manual install needed.

Made by Çınar Civan
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import sys
import shutil
import urllib.request
import urllib.error

# ─── Color Palette ───────────────────────────────────────────────────────────
BG       = "#0f0f13"
SURFACE  = "#1a1a24"
SURFACE2 = "#22223a"
ACCENT   = "#7c5cfc"
ACCENT2  = "#a87cff"
TEXT     = "#e8e6f0"
TEXT_DIM = "#8884a0"
SUCCESS  = "#4caf82"
ERROR    = "#f26b6b"
BORDER   = "#2e2b45"
# ─────────────────────────────────────────────────────────────────────────────

YTDLP_DOWNLOAD_URL = (
    "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
)

APP_NAME = "yt-dlp-gui"
APP_VERSION = "1.0.0"

# ─── Translations ─────────────────────────────────────────────────────────────
STRINGS = {
    "tr": {
        "title":             "yt-dlp GUI",
        "checking":          "yt-dlp kontrol ediliyor…",
        "ready":             "yt-dlp hazır",
        "failed":            "yt-dlp indirilemedi!",
        "downloading_ytdlp": "yt-dlp indiriliyor…",
        "sec_url":           "VİDEO / PLAYLİST URL",
        "paste":             "Yapıştır",
        "sec_options":       "İNDİRME SEÇENEKLERİ",
        "label_format":      "Format",
        "label_quality":     "Maks. Kalite",
        "label_container":   "Kapsayıcı",
        "q_best":            "En iyi",
        "c_auto":            "Otomatik",
        "sec_output":        "ÇIKTI KLASÖRÜ",
        "browse":            "Gözat…",
        "sec_extra":         "EK SEÇENEKLER",
        "chk_subs":          "Altyazıları indir",
        "chk_playlist":      "Playlist desteği",
        "chk_thumb":         "Kapak resmi göm",
        "chk_meta":          "Metadata göm",
        "btn_copy_cmd":      "Komutu Kopyala",
        "btn_download":      "  ⬇  İndir",
        "btn_cancel":        "Durdur",
        "log_label":         "LOG",
        "made_by":           "Made by Çınar Civan",
        "fmt_best":          "Video + Ses (en iyi)",
        "fmt_audio_mp3":     "Yalnızca Ses (mp3)",
        "fmt_audio_m4a":     "Yalnızca Ses (m4a)",
        "fmt_audio_opus":    "Yalnızca Ses (opus)",
        "fmt_video_only":    "Yalnızca Video (sessiz)",
        # log messages
        "log_auto_dl":       "yt-dlp bulunamadı. GitHub'dan otomatik indiriliyor…",
        "log_dl_ok":         "✔ yt-dlp başarıyla indirildi!",
        "log_dl_fail":       "İndirme başarısız (internet bağlantısı?): ",
        "log_dl_err":        "İndirme hatası: ",
        "log_cmd_copied":    "Komut panoya kopyalandı.",
        "log_need_url":      "URL giriniz.",
        "log_ytdlp_wait":    "yt-dlp henüz hazır değil. Lütfen bekleyin veya uygulamayı yeniden başlatın.",
        "log_enter_url":     "Lütfen bir URL girin.",
        "log_starting":      "▶ İndirme başlatılıyor…",
        "log_done":          "✔ İndirme tamamlandı!",
        "log_stopped":       "⏹ Durduruldu.",
        "log_error_code":    "✖ Hata (kod {})",
        "log_not_found":     "yt-dlp çalıştırılamadı. Uygulamayı yeniden başlatmayı deneyin.",
        "log_unexpected":    "Beklenmeyen hata: ",
        "log_stopping":      "Durduruluyor…",
        "dlg_title":         "yt-dlp bulunamadı",
        "dlg_msg":           (
            "yt-dlp otomatik olarak indirilemedi.\n\n"
            "Lütfen şu adımları izleyin:\n"
            "1. https://github.com/yt-dlp/yt-dlp/releases adresine gidin\n"
            "2. yt-dlp.exe dosyasını şu klasöre koyun:\n{path}\n"
            "3. Uygulamayı yeniden başlatın"
        ),
    },
    "en": {
        "title":             "yt-dlp GUI",
        "checking":          "Checking yt-dlp…",
        "ready":             "yt-dlp ready",
        "failed":            "yt-dlp download failed!",
        "downloading_ytdlp": "Downloading yt-dlp…",
        "sec_url":           "VIDEO / PLAYLIST URL",
        "paste":             "Paste",
        "sec_options":       "DOWNLOAD OPTIONS",
        "label_format":      "Format",
        "label_quality":     "Max Quality",
        "label_container":   "Container",
        "q_best":            "Best",
        "c_auto":            "Auto",
        "sec_output":        "OUTPUT FOLDER",
        "browse":            "Browse…",
        "sec_extra":         "EXTRA OPTIONS",
        "chk_subs":          "Download subtitles",
        "chk_playlist":      "Playlist support",
        "chk_thumb":         "Embed thumbnail",
        "chk_meta":          "Embed metadata",
        "btn_copy_cmd":      "Copy Command",
        "btn_download":      "  ⬇  Download",
        "btn_cancel":        "Cancel",
        "log_label":         "LOG",
        "made_by":           "Made by Çınar Civan",
        "fmt_best":          "Video + Audio (best)",
        "fmt_audio_mp3":     "Audio only (mp3)",
        "fmt_audio_m4a":     "Audio only (m4a)",
        "fmt_audio_opus":    "Audio only (opus)",
        "fmt_video_only":    "Video only (no audio)",
        # log messages
        "log_auto_dl":       "yt-dlp not found. Downloading from GitHub automatically…",
        "log_dl_ok":         "✔ yt-dlp downloaded successfully!",
        "log_dl_fail":       "Download failed (check internet connection?): ",
        "log_dl_err":        "Download error: ",
        "log_cmd_copied":    "Command copied to clipboard.",
        "log_need_url":      "Please enter a URL.",
        "log_ytdlp_wait":    "yt-dlp is not ready yet. Please wait or restart the app.",
        "log_enter_url":     "Please enter a URL.",
        "log_starting":      "▶ Starting download…",
        "log_done":          "✔ Download complete!",
        "log_stopped":       "⏹ Stopped.",
        "log_error_code":    "✖ Error (code {})",
        "log_not_found":     "yt-dlp could not be launched. Try restarting the app.",
        "log_unexpected":    "Unexpected error: ",
        "log_stopping":      "Stopping…",
        "dlg_title":         "yt-dlp not found",
        "dlg_msg":           (
            "yt-dlp could not be downloaded automatically.\n\n"
            "Please follow these steps:\n"
            "1. Go to https://github.com/yt-dlp/yt-dlp/releases\n"
            "2. Place yt-dlp.exe in this folder:\n{path}\n"
            "3. Restart the application"
        ),
    },
}
# ─────────────────────────────────────────────────────────────────────────────

# Format keys that need language-aware detection in _build_command
_FMT_AUDIO_KEYS  = ("fmt_audio_mp3", "fmt_audio_m4a", "fmt_audio_opus")
_FMT_AUDIO_EXTS  = {"fmt_audio_mp3": "mp3", "fmt_audio_m4a": "m4a", "fmt_audio_opus": "opus"}
_FMT_VIDEO_KEY   = "fmt_video_only"


def _app_install_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _user_data_dir() -> str:
    local_appdata = os.getenv("LOCALAPPDATA")
    if local_appdata:
        return os.path.join(local_appdata, APP_NAME)
    return _app_install_dir()


def _ensure_user_data_dir() -> str:
    path = _user_data_dir()
    os.makedirs(path, exist_ok=True)
    return path


def _bundled_ytdlp_path() -> str:
    return os.path.join(_app_install_dir(), "yt-dlp.exe")


def _managed_ytdlp_path() -> str:
    return os.path.join(_ensure_user_data_dir(), "yt-dlp.exe")


def _find_ytdlp():
    for local in (_managed_ytdlp_path(), _bundled_ytdlp_path()):
        if os.path.isfile(local):
            return local
    return shutil.which("yt-dlp")


class YtdlpGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self._lang = "tr"          # default language
        self._fmt_key = "fmt_best" # tracks selected format by key
        self._qual_raw = None      # tracks quality (None = "best")
        self._cont_raw = None      # tracks container (None = "auto")

        self.title(self.t("title"))

        self.geometry("800x720")
        self.minsize(680, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._process    = None
        self._running    = False
        self._ytdlp_path = None

        self._build_ui()
        self._check_ytdlp()

    # ── Translation helpers ───────────────────────────────────────────────────

    def t(self, key: str) -> str:
        return STRINGS[self._lang].get(key, key)

    # ── UI Build ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        self._style()

        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=24, pady=(20, 4))

        tk.Label(header, text="yt-dlp", font=("Segoe UI", 22, "bold"),
                 bg=BG, fg=ACCENT2).pack(side="left")
        tk.Label(header, text=" GUI", font=("Segoe UI", 22),
                 bg=BG, fg=TEXT).pack(side="left")

        # Language toggle
        self._lang_btn = tk.Button(
            header, text="EN", font=("Segoe UI", 9, "bold"),
            bg=SURFACE2, fg=ACCENT2, activebackground=SURFACE,
            activeforeground=ACCENT2, relief="flat", cursor="hand2",
            padx=10, pady=3, bd=0, command=self._toggle_language)
        self._lang_btn.pack(side="right", padx=(8, 0))

        self._status_dot = tk.Label(header, text="●", font=("Segoe UI", 12),
                                    bg=BG, fg=TEXT_DIM)
        self._status_dot.pack(side="right")
        self._status_label = tk.Label(header, text=self.t("checking"),
                                      font=("Segoe UI", 9), bg=BG, fg=TEXT_DIM)
        self._status_label.pack(side="right", padx=(0, 6))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(8, 16))

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=24)

        self._build_url_section(body)
        self._build_options_section(body)
        self._build_output_section(body)
        self._build_extra_section(body)
        self._build_buttons(body)
        self._build_log(body)

        # Footer
        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=24, pady=(0, 12))
        tk.Label(footer, text=self.t("made_by"),
                 font=("Segoe UI", 8), bg=BG, fg=TEXT_DIM).pack(side="right")

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TCombobox",
                    fieldbackground=SURFACE2, background=SURFACE2,
                    foreground=TEXT, selectbackground=ACCENT,
                    selectforeground=TEXT, bordercolor=BORDER,
                    arrowcolor=ACCENT2, padding=6)
        s.map("TCombobox", fieldbackground=[("readonly", SURFACE2)])
        s.configure("TCheckbutton", background=BG, foreground=TEXT,
                    selectcolor=ACCENT, focuscolor=BG)
        s.map("TCheckbutton", background=[("active", BG)])
        s.configure("TProgressbar", troughcolor=SURFACE2,
                    background=ACCENT, thickness=4)

    def _card(self, parent, label_key: str):
        wrapper = tk.Frame(parent, bg=BG)
        wrapper.pack(fill="x", pady=(0, 12))
        lbl = tk.Label(wrapper, text=self.t(label_key),
                       font=("Segoe UI", 8, "bold"),
                       bg=BG, fg=TEXT_DIM, anchor="w")
        lbl.pack(fill="x", pady=(0, 5))
        frame = tk.Frame(wrapper, bg=SURFACE, bd=0, highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=ACCENT)
        frame.pack(fill="x")
        return frame, lbl

    def _entry(self, parent, textvariable=None, **kw):
        return tk.Entry(parent, textvariable=textvariable,
                        bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
                        relief="flat", font=("Segoe UI", 10),
                        highlightthickness=1, highlightbackground=BORDER,
                        highlightcolor=ACCENT, **kw)

    def _btn(self, parent, text, cmd, small=False, secondary=False, danger=False):
        if danger:
            fg, bg_col, act = TEXT, "#3a1a2a", "#5a2a3a"
        elif secondary:
            fg, bg_col, act = TEXT_DIM, SURFACE2, SURFACE
        else:
            fg, bg_col, act = TEXT, ACCENT, "#6a4ce0"
        font = ("Segoe UI", 9) if small else ("Segoe UI", 10, "bold")
        pad  = (8, 4) if small else (20, 8)
        btn = tk.Button(parent, text=text, command=cmd,
                        bg=bg_col, fg=fg, activebackground=act,
                        activeforeground=fg, relief="flat", cursor="hand2",
                        font=font, padx=pad[0], pady=pad[1], bd=0)
        btn.bind("<Enter>", lambda e, b=btn, c=act: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg_col: b.config(bg=c))
        return btn

    # ── Sections ─────────────────────────────────────────────────────────────

    def _build_url_section(self, parent):
        card, self._lbl_url = self._card(parent, "sec_url")
        inner = tk.Frame(card, bg=SURFACE, padx=12, pady=12)
        inner.pack(fill="x")
        row = tk.Frame(inner, bg=SURFACE)
        row.pack(fill="x")
        self.url_var = tk.StringVar()
        self._entry(row, textvariable=self.url_var).pack(
            side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        self._paste_btn = self._btn(row, self.t("paste"), self._paste_url, small=True)
        self._paste_btn.pack(side="left")

    def _build_options_section(self, parent):
        card, self._lbl_opts = self._card(parent, "sec_options")
        inner = tk.Frame(card, bg=SURFACE, padx=12, pady=12)
        inner.pack(fill="x")
        cols = tk.Frame(inner, bg=SURFACE)
        cols.pack(fill="x")

        # Format
        left = tk.Frame(cols, bg=SURFACE)
        left.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self._lbl_fmt = tk.Label(left, text=self.t("label_format"),
                                  bg=SURFACE, fg=TEXT_DIM, font=("Segoe UI", 9))
        self._lbl_fmt.pack(anchor="w", pady=(0, 4))
        self.format_var = tk.StringVar(value=self.t("fmt_best"))
        self._fmt_box = ttk.Combobox(left, textvariable=self.format_var,
                                     state="readonly", values=self._fmt_values())
        self._fmt_box.pack(fill="x")
        self._fmt_box.bind("<<ComboboxSelected>>", self._on_fmt_change)

        # Quality
        mid = tk.Frame(cols, bg=SURFACE)
        mid.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self._lbl_qual = tk.Label(mid, text=self.t("label_quality"),
                                   bg=SURFACE, fg=TEXT_DIM, font=("Segoe UI", 9))
        self._lbl_qual.pack(anchor="w", pady=(0, 4))
        self.quality_var = tk.StringVar(value=self.t("q_best"))
        self._qual_box = ttk.Combobox(mid, textvariable=self.quality_var,
                                      state="readonly", values=self._qual_values())
        self._qual_box.pack(fill="x")
        self._qual_box.bind("<<ComboboxSelected>>", self._on_qual_change)

        # Container
        right = tk.Frame(cols, bg=SURFACE)
        right.pack(side="left", fill="x", expand=True)
        self._lbl_cont = tk.Label(right, text=self.t("label_container"),
                                   bg=SURFACE, fg=TEXT_DIM, font=("Segoe UI", 9))
        self._lbl_cont.pack(anchor="w", pady=(0, 4))
        self.container_var = tk.StringVar(value=self.t("c_auto"))
        self._cont_box = ttk.Combobox(right, textvariable=self.container_var,
                                      state="readonly", values=self._cont_values())
        self._cont_box.pack(fill="x")
        self._cont_box.bind("<<ComboboxSelected>>", self._on_cont_change)

    def _build_output_section(self, parent):
        card, self._lbl_out = self._card(parent, "sec_output")
        inner = tk.Frame(card, bg=SURFACE, padx=12, pady=12)
        inner.pack(fill="x")
        row = tk.Frame(inner, bg=SURFACE)
        row.pack(fill="x")
        self.out_var = tk.StringVar(
            value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self._entry(row, textvariable=self.out_var).pack(
            side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        self._browse_btn = self._btn(row, self.t("browse"), self._browse_output, small=True)
        self._browse_btn.pack(side="left")

    def _build_extra_section(self, parent):
        card, self._lbl_extra = self._card(parent, "sec_extra")
        inner = tk.Frame(card, bg=SURFACE, padx=12, pady=10)
        inner.pack(fill="x")
        row = tk.Frame(inner, bg=SURFACE)
        row.pack(fill="x")
        self.subtitles_var = tk.BooleanVar(value=False)
        self.playlist_var  = tk.BooleanVar(value=False)
        self.thumb_var     = tk.BooleanVar(value=False)
        self.metadata_var  = tk.BooleanVar(value=True)
        self._chk_subs  = ttk.Checkbutton(row, text=self.t("chk_subs"),  variable=self.subtitles_var)
        self._chk_pl    = ttk.Checkbutton(row, text=self.t("chk_playlist"), variable=self.playlist_var)
        self._chk_thumb = ttk.Checkbutton(row, text=self.t("chk_thumb"), variable=self.thumb_var)
        self._chk_meta  = ttk.Checkbutton(row, text=self.t("chk_meta"),  variable=self.metadata_var)
        for cb in (self._chk_subs, self._chk_pl, self._chk_thumb, self._chk_meta):
            cb.pack(side="left", padx=(0, 20))

    def _build_buttons(self, parent):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(4, 12))
        self._progress = ttk.Progressbar(row, mode="indeterminate", style="TProgressbar")
        self._progress.pack(fill="x", pady=(0, 10))
        btn_row = tk.Frame(row, bg=BG)
        btn_row.pack(fill="x")
        self.cmd_btn = self._btn(btn_row, self.t("btn_copy_cmd"),
                                 self._copy_command, secondary=True)
        self.cmd_btn.pack(side="left")
        self.dl_btn = self._btn(btn_row, self.t("btn_download"), self._start_download)
        self.dl_btn.pack(side="right")
        self.cancel_btn = self._btn(btn_row, self.t("btn_cancel"), self._cancel,
                                    secondary=True, danger=True)
        self.cancel_btn.pack(side="right", padx=(0, 8))
        self.cancel_btn.config(state="disabled")

    def _build_log(self, parent):
        self._lbl_log = tk.Label(parent, text=self.t("log_label"),
                                  font=("Segoe UI", 8, "bold"),
                                  bg=BG, fg=TEXT_DIM, anchor="w")
        self._lbl_log.pack(fill="x", pady=(0, 5))
        frame = tk.Frame(parent, bg=SURFACE, highlightthickness=1,
                         highlightbackground=BORDER)
        frame.pack(fill="both", expand=True, pady=(0, 8))
        self.log = tk.Text(frame, bg=SURFACE, fg=TEXT,
                           font=("Cascadia Code", 9), relief="flat",
                           state="disabled", wrap="word",
                           insertbackground=TEXT, padx=10, pady=8)
        scrollbar = tk.Scrollbar(frame, command=self.log.yview,
                                 bg=SURFACE2, troughcolor=SURFACE,
                                 relief="flat", bd=0)
        self.log.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True)
        self.log.tag_config("ok",   foreground=SUCCESS)
        self.log.tag_config("err",  foreground=ERROR)
        self.log.tag_config("info", foreground=ACCENT2)
        self.log.tag_config("dim",  foreground=TEXT_DIM)

    # ── Combobox change trackers (save by canonical key) ──────────────────────

    def _on_fmt_change(self, _=None):
        val = self.format_var.get()
        for key in ("fmt_best", "fmt_audio_mp3", "fmt_audio_m4a",
                    "fmt_audio_opus", "fmt_video_only"):
            if val == self.t(key):
                self._fmt_key = key
                return

    def _on_qual_change(self, _=None):
        val = self.quality_var.get()
        self._qual_raw = None if val == self.t("q_best") else val

    def _on_cont_change(self, _=None):
        val = self.container_var.get()
        self._cont_raw = None if val == self.t("c_auto") else val

    # ── Value lists for comboboxes ────────────────────────────────────────────

    def _fmt_values(self):
        return [self.t(k) for k in
                ("fmt_best", "fmt_audio_mp3", "fmt_audio_m4a",
                 "fmt_audio_opus", "fmt_video_only")]

    def _qual_values(self):
        return [self.t("q_best"), "2160p", "1440p", "1080p", "720p", "480p", "360p"]

    def _cont_values(self):
        return [self.t("c_auto"), "mp4", "mkv", "webm", "mp3", "m4a", "opus", "flac"]

    # ── Language Toggle ───────────────────────────────────────────────────────

    def _toggle_language(self):
        # Save selections before switch
        self._on_fmt_change()
        self._on_qual_change()
        self._on_cont_change()

        self._lang = "en" if self._lang == "tr" else "tr"
        self._lang_btn.config(text="TR" if self._lang == "en" else "EN")

        # Window title
        self.title(self.t("title"))

        # Header status
        self._status_label.config(text=self._current_status_text())

        # Section labels
        self._lbl_url.config(text=self.t("sec_url"))
        self._lbl_opts.config(text=self.t("sec_options"))
        self._lbl_out.config(text=self.t("sec_output"))
        self._lbl_extra.config(text=self.t("sec_extra"))
        self._lbl_log.config(text=self.t("log_label"))

        # Option labels
        self._lbl_fmt.config(text=self.t("label_format"))
        self._lbl_qual.config(text=self.t("label_quality"))
        self._lbl_cont.config(text=self.t("label_container"))

        # Buttons
        self._paste_btn.config(text=self.t("paste"))
        self._browse_btn.config(text=self.t("browse"))
        self.cmd_btn.config(text=self.t("btn_copy_cmd"))
        self.dl_btn.config(text=self.t("btn_download"))
        self.cancel_btn.config(text=self.t("btn_cancel"))

        # Checkboxes
        self._chk_subs.config(text=self.t("chk_subs"))
        self._chk_pl.config(text=self.t("chk_playlist"))
        self._chk_thumb.config(text=self.t("chk_thumb"))
        self._chk_meta.config(text=self.t("chk_meta"))

        # Comboboxes — rebuild values and restore selection
        self._fmt_box["values"] = self._fmt_values()
        self.format_var.set(self.t(self._fmt_key))

        self._qual_box["values"] = self._qual_values()
        self.quality_var.set(self._qual_raw if self._qual_raw else self.t("q_best"))

        self._cont_box["values"] = self._cont_values()
        self.container_var.set(self._cont_raw if self._cont_raw else self.t("c_auto"))

    def _current_status_text(self):
        color = self._status_dot.cget("fg")
        if color == SUCCESS: return self.t("ready")
        if color == ERROR:   return self.t("failed")
        if color == ACCENT2: return self.t("downloading_ytdlp")
        return self.t("checking")

    # ── yt-dlp Detection / Auto-Download ─────────────────────────────────────

    def _check_ytdlp(self):
        def worker():
            path = _find_ytdlp()
            if path:
                self._ytdlp_path = path
                self.after(0, self._set_status, True)
            else:
                self.after(0, self._set_status_downloading)
                self._download_ytdlp()
        threading.Thread(target=worker, daemon=True).start()

    def _set_status(self, found: bool):
        if found:
            self._status_dot.config(fg=SUCCESS)
            self._status_label.config(text=self.t("ready"), fg=SUCCESS)
        else:
            self._status_dot.config(fg=ERROR)
            self._status_label.config(text=self.t("failed"), fg=ERROR)

    def _set_status_downloading(self):
        self._status_dot.config(fg=ACCENT2)
        self._status_label.config(text=self.t("downloading_ytdlp"), fg=ACCENT2)

    def _download_ytdlp(self):
        dest = _managed_ytdlp_path()
        self.after(0, self._log, self.t("log_auto_dl"), "info")
        try:
            tmp = dest + ".tmp"
            urllib.request.urlretrieve(YTDLP_DOWNLOAD_URL, tmp)
            os.replace(tmp, dest)
            self._ytdlp_path = dest
            self.after(0, self._log, self.t("log_dl_ok"), "ok")
            self.after(0, self._set_status, True)
        except urllib.error.URLError as e:
            self.after(0, self._log, self.t("log_dl_fail") + str(e.reason), "err")
            self.after(0, self._set_status, False)
            self.after(0, self._show_manual_install_hint)
        except Exception as e:
            self.after(0, self._log, self.t("log_dl_err") + str(e), "err")
            self.after(0, self._set_status, False)

    def _show_manual_install_hint(self):
        messagebox.showerror(
            self.t("dlg_title"),
            self.t("dlg_msg").format(path=_managed_ytdlp_path()),
        )

    # ── Actions ───────────────────────────────────────────────────────────────

    def _paste_url(self):
        try:
            self.url_var.set(self.clipboard_get().strip())
        except tk.TclError:
            pass

    def _browse_output(self):
        path = filedialog.askdirectory(initialdir=self.out_var.get())
        if path:
            self.out_var.set(path)

    def _build_command(self):
        url  = self.url_var.get().strip()
        out  = self.out_var.get().strip()

        ytdlp = self._ytdlp_path or "yt-dlp"
        cmd   = [ytdlp]

        fk = self._fmt_key  # canonical key, language-independent

        if fk in _FMT_AUDIO_KEYS:
            ext = _FMT_AUDIO_EXTS[fk]
            cmd += ["-x", "--audio-format", ext, "--audio-quality", "0"]
        elif fk == _FMT_VIDEO_KEY:
            cmd += ["-f", "bestvideo"]
        else:
            if self._qual_raw is None:
                f_str = "bestvideo+bestaudio/best"
            else:
                h = self._qual_raw.replace("p", "")
                f_str = (f"bestvideo[height<={h}]+bestaudio/"
                         f"best[height<={h}]/bestvideo+bestaudio/best")
            cmd += ["-f", f_str]

        if self._cont_raw and fk not in _FMT_AUDIO_KEYS:
            cmd += ["--merge-output-format", self._cont_raw]

        if self.subtitles_var.get():
            cmd += ["--write-subs", "--sub-langs", "tr,en", "--embed-subs"]
        if not self.playlist_var.get():
            cmd += ["--no-playlist"]
        if self.thumb_var.get():
            cmd += ["--embed-thumbnail"]
        if self.metadata_var.get():
            cmd += ["--embed-metadata"]

        template = os.path.join(out, "%(title)s.%(ext)s")
        cmd += ["-o", template, "--progress", url]
        return cmd

    def _copy_command(self):
        if not self.url_var.get().strip():
            self._log(self.t("log_need_url"), "err"); return
        cmd = self._build_command()
        self.clipboard_clear()
        self.clipboard_append(" ".join(
            f'"{c}"' if " " in c else c for c in cmd))
        self._log(self.t("log_cmd_copied"), "ok")

    def _start_download(self):
        if self._running:
            return
        if not self._ytdlp_path:
            self._log(self.t("log_ytdlp_wait"), "err"); return
        if not self.url_var.get().strip():
            self._log(self.t("log_enter_url"), "err"); return

        cmd = self._build_command()
        self._log(self.t("log_starting"), "info")
        self._log("$ " + " ".join(cmd[:6]) + " …", "dim")

        self._running = True
        self.dl_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self._progress.start(12)
        threading.Thread(target=self._run, args=(cmd,), daemon=True).start()

    def _run(self, cmd):
        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=(subprocess.CREATE_NO_WINDOW
                               if sys.platform == "win32" else 0)
            )
            for line in self._process.stdout:
                line = line.rstrip()
                if not line: continue
                tag = ("ok"   if ("[download]" in line and "%" in line)
                       else "err"  if "ERROR" in line
                       else "info" if line.startswith("[")
                       else None)
                self.after(0, self._log, line, tag)

            self._process.wait()
            rc = self._process.returncode
            if rc == 0:
                self.after(0, self._log, self.t("log_done"), "ok")
            elif rc in (-1, None):
                self.after(0, self._log, self.t("log_stopped"), "dim")
            else:
                self.after(0, self._log, self.t("log_error_code").format(rc), "err")
        except FileNotFoundError:
            self.after(0, self._log, self.t("log_not_found"), "err")
        except Exception as ex:
            self.after(0, self._log, self.t("log_unexpected") + str(ex), "err")
        finally:
            self.after(0, self._finish)

    def _finish(self):
        self._running = False
        self._process = None
        self._progress.stop()
        self.dl_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def _cancel(self):
        if self._process:
            self._process.terminate()
            self._log(self.t("log_stopping"), "dim")

    def _log(self, msg, tag=None):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", tag or "")
        self.log.see("end")
        self.log.config(state="disabled")


if __name__ == "__main__":
    app = YtdlpGUI()
    app.mainloop()
