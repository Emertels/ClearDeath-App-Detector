# ClearDeath App Detector

**Version:** 1.0.0  
**Interface languages:** Brazilian Portuguese, English, Spanish, French, German, Italian, Japanese, Korean, Simplified Chinese, and Russian. The interface follows the Windows UI language and falls back to Brazilian Portuguese when the language is unsupported.

## What it does

Inspect uninstall registry entries and identify applications whose files or uninstallers may be missing.

## Files

clear_death_app_detector.py, ClearDeath-App-Detector.ps1, and Session-Header.ps1 (required by the PowerShell version)

## Usage

1. Download or clone the complete repository.
2. Choose one version: `clear_death_app_detector.py` (Python) or `ClearDeath-App-Detector.ps1` (PowerShell). Run your preferred version and approve the UAC prompt when requested.

## Requirements

Windows 10 or Windows 11; Python 3.7+ for the Python version or Windows PowerShell 5.1 for the PowerShell version. Removal requires administrator privileges for selected entries.

## Safety and limitations

The project must not remove personal data, credentials, or content outside paths defined by the tool. Command and feature availability depends on Windows edition and version. Review CHANGELOG.md before updating.

## Development

See AGENTS-PT-BR.md and AGENTS-EN.md. The default interface language follows Windows UI culture; Brazilian Portuguese is the fallback.

## Languages, purpose, and tips

Menus, reports, warnings, confirmations, and safety messages are available in all ten languages. Removal confirmations use a localized word or phrase; type the exact text shown. To prevent accidental changes, the tool creates a Registry backup before deleting any entry.

Review each orphaned entry and publisher before removal. Registry backups are in %LOCALAPPDATA%\Emertels\ClearDeath\Backups; keep them until apps are confirmed to work.

### Idiomas disponíveis / Available languages

| Language | Locale | Used for |
|---|---|---|
| Brazilian Portuguese | pt-BR | Brazilian Windows; fallback for unsupported locales |
| English | en | English Windows |
| Spanish | es | Spanish Windows |
| French | fr | French Windows |
| German | de | German Windows |
| Italian | it | Italian Windows |
| Japanese | ja | Japanese Windows |
| Korean | ko | Korean Windows |
| Simplified Chinese | zh-CN | Simplified Chinese Windows |
| Russian | ru | Russian Windows |

## 👨‍💻 About the Author

Developed and maintained by **Emerson Teles** (known in the community as **Emertels**).

Technology, computing, gaming, system maintenance, and software translation/localization enthusiast. Focused on practical utilities, productivity tools, intelligent PowerShell automation, and technical localization solutions that make modern tools more accessible to Brazilian users.

### 🛠️ Projects & Contributions

- [AI-Chat-Vault](https://github.com/Emertels/AI-Chat-Vault) — Portable backup and recovery for local conversations from 20+ AI tools and assistants.
- [Antigravity — Brazilian Portuguese Translation](https://github.com/Emertels/Antigravity-Traducao-PTBR) — Complete localization of Google Antigravity Desktop into Brazilian Portuguese.
- [Codex Router — Brazilian Portuguese Translation](https://github.com/Emertels/CodexRouter-Traducao-PTBR) — Translation and localization package for Codex Router Control Center.
- [Cursor AI — Brazilian Portuguese Translation](https://github.com/Emertels/Cursor-Traducao-PTBR) — Complete, in-depth localization of Cursor AI into Brazilian Portuguese.
- [GPU Tweak III — Brazilian Portuguese Translation](https://github.com/Emertels/GPU-Tweak-III-Traducao-PTBR) — Brazilian Portuguese translation and automated installer for ASUS GPU Tweak III.
- [Microsoft Photos Fix](https://github.com/Emertels/Microsoft-Photos-Fix) — PowerShell and C# fix for startup routing and image viewing in Windows Photos.
- [PSBBN-Translator](https://github.com/Emertels/PSBBN-Translator) — Localization suite for the PSBBN Definitive Project (PlayStation 2) in 40 languages.
- [Silent Hill: Homecoming — Brazilian Portuguese Translation](https://github.com/Emertels/Silent-Hill-Homecoming-Traducao-PTBR) — Complete PC translation and review into Brazilian Portuguese.
- [Suite-Emuladores](https://github.com/Emertels/Suite-Emuladores) — PowerShell suite for downloading and updating 56 emulators and frontends on Windows.
- [ZCode — Brazilian Portuguese Translation](https://github.com/Emertels/ZCode-Traducao-PTBR) — Complete localization of ZCode Desktop into Brazilian Portuguese.

### 🌐 Connect with me & Official Communities

<div align="left">

[![GitHub](https://img.shields.io/badge/GitHub-Emertels-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/emertels)
[![Website](https://img.shields.io/badge/Website-Emerson_Teles-0070F3?style=for-the-badge&logo=googlechrome&logoColor=white)](https://emertels.github.io)
[![Discord](https://img.shields.io/badge/Discord-Emertels%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://emertels.github.io/discord)
[![X / Twitter](https://img.shields.io/badge/X_Twitter-@emertels-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/emertels)
[![YouTube](https://img.shields.io/badge/YouTube-Emerson_Teles-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@emersonteles2379)
[![Telegram](https://img.shields.io/badge/Telegram-Aplicativos%20Mods-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/apksmodsandroid)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support_the_Project-FF5E5B?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/emertels)

</div>
