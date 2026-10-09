# 🛡️ ClearDeath App Detector — Verificador de Aplicativos Órfãos 🇧🇷

<div align="center">

**🌐 Idiomas / Languages:**  
[![Documentação PT-BR](https://img.shields.io/badge/Documenta%C3%A7%C3%A3o-Portugu%C3%AAs%20(Brasil)-green?style=for-the-badge)](README.md)
[![Documentation EN](https://img.shields.io/badge/Documentation-English-0070F3?style=for-the-badge)](README-EN.md)

![Versão](https://img.shields.io/badge/Vers%C3%A3o-v1.0.0-blue?style=for-the-badge)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=for-the-badge)
![Plataforma](https://img.shields.io/badge/Plataforma-Windows%2010%20%7C%2011-0078D4?style=for-the-badge)
![Idiomas](https://img.shields.io/badge/Idiomas-10%20Nativos-2ea44f?style=for-the-badge)

</div>

---

Analisa entradas de desinstalação no Registro do Windows e identifica programas cujos arquivos ou desinstaladores estão ausentes ou corrompidos, com backup automático preventivo.

## 🚀 Principais Recursos
- **Auditoria Segura de Resíduos:** Detecta entradas órfãs deixadas por desinstalações incompletas de softwares.
- **Backup Automático:** Antes de qualquer remoção, exporta o Registro para `%LOCALAPPDATA%\Emertels\ClearDeath\Backups`.
- **Duplo Motor:** Disponível em script PowerShell (`ClearDeath-App-Detector.ps1`) e Python autônomo (`clear_death_app_detector.py`).
- **Interface Multilíngue:** 10 idiomas auto-detectados com fallback em Português (Brasil).

## 📦 Como Usar
1. Baixe o pacote portátil na seção [Releases](https://github.com/Emertels/ClearDeath-App-Detector/releases/latest).
2. Execute `ClearDeath-App-Detector.ps1` no PowerShell como Administrador ou rode `clear_death_app_detector.py`.
3. Escolha as opções no menu para inspecionar, ocultar ou remover com segurança.

> [!TIP]
> Antes de confirmar a remoção de qualquer chave, o utilitário solicita uma frase de confirmação explícita para evitar qualquer exclusão acidental.

## 📋 Opções do Menu
- **1 — Mostrar entradas ocultadas:** Exibe novamente itens marcados como ignorados nesta sessão.
- **2 — Ver suspeitas:** Lista itens que apontam para diretórios inexistentes.
- **3 — Selecionar para remoção:** Permite digitar números individuais ou `ALL`.
- **4 — Remover todas:** Pré-seleciona todas as suspeitas com exigência de confirmação.
- **5 — Sair.**

---
## 👨‍💻 Sobre o Autor

Desenvolvido e mantido por **Emerson Teles** (conhecido na comunidade como **Emertels**).

Entusiasta de tecnologia, informática, jogos, manutenção de sistemas e tradução/localização de softwares para Português do Brasil (PT-BR). Desenvolvedor focado em utilitários práticos, ferramentas de produtividade, automação inteligente em PowerShell e soluções completas de localização técnica que aproximam ferramentas modernas do público brasileiro.

### 🛠️ Projetos & Contribuições

- [AI-Chat-Vault](https://github.com/Emertels/AI-Chat-Vault) — Backup portátil e recuperação de conversas locais de 20+ ferramentas e assistentes de IA.
- [Antigravity — Tradução PT-BR](https://github.com/Emertels/Antigravity-Traducao-PTBR) — Localização completa do Google Antigravity Desktop para Português do Brasil.
- [Codex Router — Tradução PT-BR](https://github.com/Emertels/CodexRouter-Traducao-PTBR) — Pacote de tradução e localização do Codex Router Control Center em PT-BR.
- [Cursor AI — Tradução PT-BR](https://github.com/Emertels/Cursor-Traducao-PTBR) — Localização completa e profunda do Cursor AI para Português do Brasil.
- [GPU Tweak III — Tradução PT-BR](https://github.com/Emertels/GPU-Tweak-III-Traducao-PTBR) — Tradução em português brasileiro e instalador automatizado para ASUS GPU Tweak III.
- [Microsoft Photos Fix](https://github.com/Emertels/Microsoft-Photos-Fix) — Solução definitiva em PowerShell e C# para rota de inicialização rápida e visualização no app Fotos do Windows.
- [PSBBN-Translator](https://github.com/Emertels/PSBBN-Translator) — Suíte corporativa de tradução e localização para o PSBBN Definitive Project (PlayStation 2) em 40 idiomas.
- [Silent Hill: Homecoming — Tradução PT-BR](https://github.com/Emertels/Silent-Hill-Homecoming-Traducao-PTBR) — Tradução e revisão completa do jogo para PC em português brasileiro.
- [Suite-Emuladores](https://github.com/Emertels/Suite-Emuladores) — Suíte inteligente em PowerShell para download e atualização autônoma de 56 emuladores e frontends no Windows.
- [ZCode — Tradução PT-BR](https://github.com/Emertels/ZCode-Traducao-PTBR) — Tradução e localização completa do ZCode Desktop para Português do Brasil.

### 🌐 Conecte-se comigo & Comunidades Oficiais

<div align="left">

[![GitHub](https://img.shields.io/badge/GitHub-Emertels-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/emertels)
[![Website](https://img.shields.io/badge/Website-Emerson_Teles-0070F3?style=for-the-badge&logo=googlechrome&logoColor=white)](https://emertels.github.io)
[![Discord](https://img.shields.io/badge/Discord-Emertels%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://emertels.github.io/discord)
[![X / Twitter](https://img.shields.io/badge/X_Twitter-@emertels-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/emertels)
[![YouTube](https://img.shields.io/badge/YouTube-Emerson_Teles-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@emersonteles2379)
[![Telegram](https://img.shields.io/badge/Telegram-Aplicativos%20Mods-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/apksmodsandroid)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Apoiar%20Projeto-FF5E5B?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/emertels)

</div>
