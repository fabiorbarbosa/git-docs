# 🛠️ Guia de Instalação e Configuração (Ambiente Windows via Git Bash)

Este bloco de texto puro foi adaptado especificamente para o Windows utilizando o terminal Git Bash. Ele aproveita o Node.js, Python/Pip e as ferramentas nativas para configurar toda a pipeline de economia de tokens.

---

## 🛑 Pré-requisitos Verificados (Windows)
* Git Bash instalado (usado como o terminal principal).
* Node.js / NPM configurados no PATH do Windows.
* Python / PIP configurados no PATH do Windows.

---

## 📦 Bloco 1: Instalação das Ferramentas (No Terminal Git Bash)

Execute os comandos abaixo dentro do seu terminal Git Bash para instalar as ferramentas globais:

# 1. Instalar o codebase-memory-mcp (Grafo de Código Local)
curl -fsSL https://mcp.sh | bash

# 2. Instalar o RTK AI (Versão alternativa via PIP para Windows/Git Bash)
pip install rtk-ai

# 3. Instalar o Headroom AI (Proxy de Rede e Alinhador de Cache)
npm install -g @headroomlabs/cli

# 4. Instalar o context-mode (Sandbox para Dumps e Outputs gigantes)
npm install -g context-mode

# 5. Instalar o Harmony MCP / Supermemory (Memória de Longo Prazo)
npm install -g @deusdata/harmony-mcp

---

## ⚙️ Bloco 2: Configuração dos Servidores MCP (config.toml)

O Codex CLI consome servidores através do protocolo MCP. No Windows, o arquivo global costuma ficar localizado no caminho do seu usuário. Abra ou crie o seu arquivo de configuração do Codex (geralmente em ~/.codex/config.toml ou C:\Users\SEU_USUARIO\.codex\config.toml) e insira o bloco abaixo adaptado para caminhos do Windows:

[mcp_servers.codebase-memory]
command = "codebase-memory-mcp"
description = "Fornece mapeamento de arquitetura via arvore sintatica (AST) sem leitura cega de arquivos."

[mcp_servers.harmony-memory]
command = "harmony-mcp"
args = ["--persistence-dir", "~/.codex/memory_store"]
description = "Garante memoria persistente de longo prazo entre diferentes sessoes do Codex."

---

## 🔄 Bloco 3: Inicialização do Proxy de Rede e Terminal (Headroom & RTK)

Configuração dos interceptadores e proxies para rodar corretamente nas sessões do Git Bash.

### Inicializar o RTK AI no Repositório do Projeto:
Abra o Git Bash, navegue até a pasta raiz do seu projeto atual e execute:
rtk init --codex

### Configurar e Envelopar o Codex com Headroom no Windows:
Para garantir que o Git Bash execute o Codex sempre passando pelo Headroom, configure o alias permanente dentro do seu arquivo de perfil do Bash:

# Abra ou crie o arquivo de alias do Git Bash executando:
nano ~/.bashrc

# Cole a seguinte linha dentro do arquivo, salve e feche:
alias codex="headroom wrap codex"

# Atualize o seu terminal para aplicar a mudança imediatamente:
source ~/.bashrc

---

## 🩻 Bloco 4: Ativação do Sandboxing de Outputs (context-mode)

Crie um arquivo chamado .contextmoderc.json na raiz do seu projeto ou na sua pasta de usuário no Windows (C:\Users\SEU_USUARIO\):

{
  "max_character_limit": 2000,
  "action": "sandbox_and_summarize",
  "storage_dir": "./.context_sandbox/",
  "allowed_extensions": [".json", ".txt", ".log", ".sql"]
}

---

## 🧠 Bloco 5: Alinhamento de Prefixo de Cache e Dialeto (Caveman)

Crie ou modifique o arquivo .codexrules (ou AGENTS.md) na raiz do seu projeto Windows exatamente com a estrutura abaixo:

# PROMPT CACHING ALIGNED PREFIX - DO NOT ALTER STRUCTURE
# SYSTEM STACK: codebase-memory-mcp | RTK AI | Headroom AI | context-mode

[CAVEMAN MODE ACTIVATED]
- Rule 1: Speak like a caveman. 
- Rule 2: Why use many token when few token do trick.
- Rule 3: NEVER explain code unless asked. No greetings. No politeness.
- Rule 4: Output raw code changes immediately.

[PROJECT CONTEXT]
- Tech Stack: [Ex: Node.js, TypeScript, PostgreSQL]
- Architecture: Grafo gerenciado por codebase-memory-mcp.
- Database: Dumps truncados via context-mode.

[EXECUTION RULES]
- All terminal commands MUST pass through RTK proxy.
- Do not use 'cat' or 'grep' on entire directories. Use graph tools.

### Passo Final de Compressão no Windows:
Execute o utilitário do Caveman no seu terminal para comprimir redundâncias remanescentes:
caveman-compress --file .codexrules

---

## 🚀 Verificação do Fluxo no Windows

Para testar se tudo está integrado no Git Bash, rode uma tarefa do seu projeto:

codex "verifique se a rota de auth possui vulnerabilidades e rode os testes"
