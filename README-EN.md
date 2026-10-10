# 🛡️ ClearDeath App Detector — Orphaned App Registry Scanner

<div align="center">

**🌐 Idiomas / Languages:**  
[![Documentação PT-BR](https://img.shields.io/badge/Documenta%C3%A7%C3%A3o-Portugu%C3%AAs%20(Brasil)-green?style=for-the-badge)](README.md)
[![Documentation EN](https://img.shields.io/badge/Documentation-English-0070F3?style=for-the-badge)](README-EN.md)

![Version](https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D4?style=for-the-badge)
![Languages](https://img.shields.io/badge/Languages-10%20Native-2ea44f?style=for-the-badge)
![Languages](https://img.shields.io/badge/Languages-10%20Native-2ea44f?style=for-the-badge)

</div>

---

Scans Windows Registry uninstall entries and detects programs whose files or uninstallers are missing or corrupted, featuring automated preventive backup.

## 🚀 Key Features
- **Safe Residue Audit:** Detects orphaned entries left behind by incomplete application uninstallations.
- **Automated Backup:** Exports Registry backups to `%LOCALAPPDATA%\Emertels\ClearDeath\Backups` prior to any removal.
- **Dual Engine:** Available both as a PowerShell script (`ClearDeath-App-Detector.ps1`) and standalone Python (`clear_death_app_detector.py`).
- **Multilingual Support:** 10 auto-detected system languages with Brazilian Portuguese fallback.

## 📦 Usage
1. Download the portable zip package from the [Releases](https://github.com/Emertels/ClearDeath-App-Detector/releases/latest) section.
2. Run `ClearDeath-App-Detector.ps1` in PowerShell as Administrator or launch `clear_death_app_detector.py`.
3. Follow the interactive menu to inspect, review, or safely clean orphaned entries.

> [!TIP]
> Prior to confirming deletion of any registry keys, the tool prompts for an explicit confirmation phrase to prevent accidental removals.

---
## 🌐 Multilingual Support (10 Native Languages)

This tool features full built-in support for **10 native languages**, automatically detecting the UI culture configured in your Windows operating system:

| Language | Code | Detection |
| :--- | :--- | :--- |
| 🇧🇷 **Portuguese (Brazil)** | `pt-BR` | Default / Automatic |
| 🇺🇸 **English** | `en` | Automatic |
| 🇪🇸 **Spanish** | `es` | Automatic |
| 🇫🇷 **French** | `fr` | Automatic |
| 🇩🇪 **German** | `de` | Automatic |
| 🇮🇹 **Italian** | `it` | Automatic |
| 🇯🇵 **Japanese** | `ja` | Automatic |
| 🇰🇷 **Korean** | `ko` | Automatic |
| 🇨🇳 **Simplified Chinese** | `zh-CN` | Automatic |
| 🇷🇺 **Russian** | `ru` | Automatic |

### 💡 Forcing or Changing the Language
If you want to run the tool in a language different from your Windows system UI, simply set the `EMERTELS_LANGUAGE` environment variable:

**In Command Prompt (CMD / Batch):**
```cmd
set EMERTELS_LANGUAGE=en
powershell -ExecutionPolicy Bypass -File ClearDeath-App-Detector.ps1
```

**In PowerShell:**
```powershell
$env:EMERTELS_LANGUAGE = "en"
.\ClearDeath-App-Detector.ps1
```

> [!TIP]
> If your system language is not among the 10 supported cultures, the application safely falls back to **Portuguese (Brazil)** or **English**.

---
## 👨‍💻 About the Author

Developed and maintained by **Emerson Teles** (known in the community as **Emertels**).

Technology, computing, gaming, and system maintenance enthusiast dedicated to software localization into Brazilian Portuguese (PT-BR). Developer focused on practical utilities, productivity tools, intelligent PowerShell automation, and complete technical localization solutions that make modern software accessible to Brazilian users.

### 🛠️ Projects & Contributions

- [AI-Chat-Vault](https://github.com/Emertels/AI-Chat-Vault) — Portable backup and recovery tool for local chat histories across 20+ AI assistants.
- [Antigravity — PT-BR Translation](https://github.com/Emertels/Antigravity-Traducao-PTBR) — Complete Brazilian Portuguese localization package for Google Antigravity Desktop.
- [Codex Router — PT-BR Translation](https://github.com/Emertels/CodexRouter-Traducao-PTBR) — Portable translation and localization package for Codex Router Control Center in PT-BR.
- [Cursor AI — PT-BR Translation](https://github.com/Emertels/Cursor-Traducao-PTBR) — Deep Brazilian Portuguese localization and update suite for Cursor AI.
- [GPU Tweak III — PT-BR Translation](https://github.com/Emertels/GPU-Tweak-III-Traducao-PTBR) — Full PT-BR translation and automated installer for ASUS GPU Tweak III.
- [Microsoft Photos Fix](https://github.com/Emertels/Microsoft-Photos-Fix) — Advanced PowerShell & C# solution fixing fast route startup and photo viewing on Windows.
- [PSBBN-Translator](https://github.com/Emertels/PSBBN-Translator) — Enterprise translation and localization suite for the PS2 PSBBN Definitive Project in 40 languages.
- [Silent Hill: Homecoming — PT-BR Translation](https://github.com/Emertels/Silent-Hill-Homecoming-Traducao-PTBR) — Complete Brazilian Portuguese translation and revision for PC.
- [Suite-Emuladores](https://github.com/Emertels/Suite-Emuladores) — Intelligent PowerShell suite for automated downloads and updates of 56 game emulators & frontends on Windows.
- [ZCode — PT-BR Translation](https://github.com/Emertels/ZCode-Traducao-PTBR) — Full Brazilian Portuguese visual translation and localization for ZCode Desktop.

### 🌐 Connect with Me & Official Communities

<div align="left">

[![GitHub](https://img.shields.io/badge/GitHub-Emertels-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/emertels)
[![Website](https://img.shields.io/badge/Website-Emerson_Teles-0070F3?style=for-the-badge&logo=googlechrome&logoColor=white)](https://emertels.github.io)
[![Discord](https://img.shields.io/badge/Discord-Emertels%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://emertels.github.io/discord)
[![X / Twitter](https://img.shields.io/badge/X_Twitter-@emertels-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/emertels)
[![YouTube](https://img.shields.io/badge/YouTube-Emerson_Teles-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@emersonteles2379)
[![Telegram](https://img.shields.io/badge/Telegram-Aplicativos%20Mods-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/apksmodsandroid)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/emertels)

</div>
