# Verificador ClearDeath de Aplicativos

**Versão:** 1.0.0  
**Idiomas da interface:** PT-BR, inglês, espanhol, francês, alemão, italiano, japonês, coreano, chinês simplificado e russo. O idioma é detectado pela configuração de idioma do Windows; PT-BR é usado como alternativa quando o idioma não é compatível.

## O que faz

Analisa entradas de desinstalação e identifica aplicativos cujos arquivos ou desinstaladores podem estar ausentes.

## Arquivos

clear_death_app_detector.py, ClearDeath-App-Detector.ps1 e Session-Header.ps1 (necessário para a versão PowerShell)

## Como usar

1. Baixe ou clone o repositório completo.
2. Escolha uma das versões: `clear_death_app_detector.py` (Python) ou `ClearDeath-App-Detector.ps1` (PowerShell). Execute a versão escolhida e aceite o UAC quando solicitado.

## Requisitos

Windows 10 ou Windows 11; Python 3.7+ para a versão Python ou Windows PowerShell 5.1 para a versão PowerShell. A remoção exige privilégios de administrador conforme as entradas selecionadas.

## Segurança e limitações

O projeto não deve apagar dados pessoais, credenciais ou conteúdo fora dos caminhos definidos pela ferramenta. A disponibilidade de comandos e recursos depende da edição e versão do Windows. Revise CHANGELOG.md antes de atualizar.

## Desenvolvimento

Consulte AGENTS-PT-BR.md e AGENTS-EN.md. O idioma padrão da interface é detectado pela cultura do Windows; quando ela não for compatível, use PT-BR como fallback.

## Idiomas, finalidade e dicas

Menus, relatórios, avisos, confirmações e mensagens de segurança estão disponíveis nos dez idiomas. As confirmações de remoção usam uma palavra ou frase localizada; digite exatamente o texto exibido. Para evitar remoções acidentais, a ferramenta cria um backup do Registro antes de excluir qualquer entrada.

Revise cada entrada órfã e o fabricante antes de remover. A cópia do registro fica em %LOCALAPPDATA%\Emertels\ClearDeath\Backups; mantenha-a até confirmar que os aplicativos continuam funcionando.

### Idiomas disponíveis / Available languages

| Idioma | Código | Indicação |
|---|---|---|
| Português (Brasil) | pt-BR | Brasil |
| Inglês | en | Sistemas em inglês |
| Espanhol | es | Sistemas em espanhol |
| Francês | fr | Sistemas em francês |
| Alemão | de | Sistemas em alemão |
| Italiano | it | Sistemas em italiano |
| Japonês | ja | Sistemas em japonês |
| Coreano | ko | Sistemas em coreano |
| Chinês simplificado | zh-CN | Sistemas em chinês simplificado |
| Russo | ru | Sistemas em russo |







## Sobre Emerson Teles

Emerson Teles (Emertels) desenvolve ferramentas para Windows, automação, emulação e localização de software. Veja os projetos e acompanhe os canais oficiais:

- [Site oficial](https://emertels.github.io) · [GitHub](https://github.com/Emertels) · [Discord](https://emertels.github.io/discord)
- [YouTube](https://www.youtube.com/@emersonteles2379) · [X](https://x.com/emertels) · [Telegram](https://t.me/apksmodsandroid) · [Ko-fi](https://ko-fi.com/emertels)

### Outros projetos

- [AI-Chat-Vault](https://github.com/Emertels/AI-Chat-Vault) — backup portátil e recuperação de conversas locais de ferramentas de IA.
- [Suite-Emuladores](https://github.com/Emertels/Suite-Emuladores) — gerenciamento de download e atualização de emuladores e frontends no Windows.
- [Microsoft-Photos-Fix](https://github.com/Emertels/Microsoft-Photos-Fix) — correção de inicialização e papel de parede do app Fotos do Windows.
- [PSBBN-Translator](https://github.com/Emertels/PSBBN-Translator) — localização do PSBBN Definitive Project em 40 idiomas.
- [GPU-Tweak-III-Traducao-PTBR](https://github.com/Emertels/GPU-Tweak-III-Traducao-PTBR), [Cursor-Traducao-PTBR](https://github.com/Emertels/Cursor-Traducao-PTBR), [CodexRouter-Traducao-PTBR](https://github.com/Emertels/CodexRouter-Traducao-PTBR), [Antigravity-Traducao-PTBR](https://github.com/Emertels/Antigravity-Traducao-PTBR) e [ZCode-Traducao-PTBR](https://github.com/Emertels/ZCode-Traducao-PTBR) — projetos de localização para PT-BR.
- [Silent-Hill-Homecoming-Traducao-PTBR](https://github.com/Emertels/Silent-Hill-Homecoming-Traducao-PTBR) — tradução e revisão para PC.


