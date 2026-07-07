# 🛠️ Guia de Instalação e Configuração: Claude Code & OpenCode Token Efficiency Stack

Esta versão foi estruturada especificamente para otimizar os dois maiores agentes CLI de 2026 usando o terminal Git Bash no Windows.

---

## 🛑 Pré-requisitos do Sistema
* Git Bash configurado como terminal principal.
* Node.js / NPM e Python / PIP ativos no PATH do Windows.
* Claude Code instalado (`npm install -g @anthropic-ai/claude-code`)
* OpenCode CLI instalado (`npm install -g opencode-ai`)

---

## 📦 Bloco 1: Instalação das Ferramentas (No Git Bash)

Execute os comandos abaixo sequencialmente para instalar todos os otimizadores globais:

# 1. Instalar o codebase-memory-mcp (Grafo de Código Local)
curl -fsSL https://mcp.sh | bash

# 2. Instalar o RTK AI (Filtro de Terminal via PIP para Windows)
pip install rtk-ai

# 3. Instalar o Headroom AI (Proxy de Rede de Alta Performance)
npm install -g @headroomlabs/cli

# 4. Instalar o context-mode (Sandbox para saídas pesadas)
npm install -g context-mode

# 5. Instalar o Harmony MCP (Gerenciador de Memória persistente)
npm install -g @deusdata/harmony-mcp

---

## ⚙️ Bloco 2: Integração de Servidores MCP

### Para o Claude Code:
Abra ou crie o arquivo de configurações do Claude Code executando `nano ~/.claude/config.json` e adicione os servidores MCP:

{
  "mcpServers": {
    "codebase-memory": {
      "command": "codebase-memory-mcp"
    },
    "harmony-memory": {
      "command": "harmony-mcp",
      "args": ["--persistence-dir", "~/.claude/memory_store"]
    }
  }
}

### Para o OpenCode:
O OpenCode centraliza as configurações em um arquivo JSON próprio. Execute `nano ~/.opencode/openCode.json` e adicione a seção de servidores:

{
  "mcp": {
    "codebase-memory": {
      "command": "codebase-memory-mcp"
    },
    "harmony-memory": {
      "command": "harmony-mcp",
      "args": ["--persistence-dir", "~/.opencode/memory_store"]
    }
  }
}

---

## 🔄 Bloco 3: Inicialização do Proxy e Aliases (Headroom & RTK)

Como o Windows gerencia processos de forma diferente, envelopamos os executáveis por meio de aliases estáveis dentro do perfil do Git Bash.

### Inicializar os interceptadores de terminal no repositório:
Na pasta raiz do seu projeto atual, execute o comando de hook correspondente para que os agentes usem o RTK:
rtk init --claude
rtk init --opencode

### Configurar os Envelopamentos de Rede:
Abra o arquivo de configuração do seu Git Bash executando `nano ~/.bashrc` e insira as seguintes instruções para forçar ambos os agentes a passarem pelo Headroom:

alias claude="headroom wrap claude"
alias opencode="headroom wrap opencode"

Salve o arquivo (Ctrl+O, Enter, Ctrl+X) e atualize a sessão do terminal:
source ~/.bashrc

---

## 🩻 Bloco 4: Sandboxing de Ferramentas (context-mode)

Impeça que dumps gigantescos gerados pelos comandos internos entrem na janela de chat. Crie o arquivo `.contextmoderc.json` na raiz do projeto:

{
  "max_character_limit": 2000,
  "action": "sandbox_and_summarize",
  "storage_dir": "./.context_sandbox/",
  "allowed_extensions": [".json", ".txt", ".log", ".sql", ".dom"]
}

---

## 🧠 Bloco 5: Alinhamento de Prefixo de Cache e Dialeto (Caveman)

Tanto o Claude Code quanto o OpenCode interpretam arquivos de instruções locais automáticos. Crie ou modifique o arquivo **`CLAUDE.md`** (usado pelo Claude Code) e o arquivo **`AGENTS.md`** (usado pelo OpenCode) na raiz do projeto com o seguinte prefixo enxuto:

# PROMPT CACHING ALIGNED PREFIX - STACK CBM DETECTED

[CAVEMAN MODE ACTIVATED]
- Rule 1: Speak like a caveman. 
- Rule 2: Why use many token when few token do trick.
- Rule 3: NEVER explain code unless asked. No greetings.
- Rule 4: Output code differences immediately.

[PROJECT CONTEXT]
- Architecture: Tree-sitter graph local.
- Terminal: Intercepted by RTK proxy.
- Outputs: Sandboxed via context-mode.

### Passo de Compressão Final:
Utilize a variação específica do Caveman para limpar redundâncias textuais dos arquivos de instrução criados:
caveman-compress --file CLAUDE.md
caveman-compress --file AGENTS.md

---

## 🚀 Como testar a eficiência nos novos ambientes

Para validar o funcionamento completo da stack, utilize qualquer um dos dois comandos abaixo no seu Git Bash:

# Para o Claude Code:
claude "Rode os testes e verifique erros estruturais"

# Para o OpenCode:
opencode "Busque o fluxo de login e faça uma analise de erros rápidos"
