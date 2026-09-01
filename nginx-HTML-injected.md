# Arquitetura de Injeção de Componentes Legados via Servidor (Nginx SSI)

Este documento descreve a estratégia técnica para injetar o HTML renderizado de um widget de chat autônomo (hospedado em um subdomínio) diretamente nas páginas de uma aplicação principal (Angular e telas legadas em ASP Clássico) utilizando **Server-Side Includes (SSI)** no Nginx.

Esta abordagem elimina completamente a necessidade de `iframes`, abas adicionais ou injeção dinâmica via JavaScript (`document.appendChild`), realizando a montagem de forma transparente no lado do servidor.

---

## 🏗️ Fluxo da Arquitetura

1. O usuário requisita uma página no domínio principal (`meu-dominio.com.br`).
2. O Nginx repassa a requisição para o servidor da aplicação correspondente (Angular ou IIS/ASP).
3. A aplicação responde com o HTML contendo uma tag de comentário especial do SSI: `<!--# include virtual="..." -->`.
4. O Nginx intercepta esse HTML, identifica a tag e faz uma chamada interna ultrarrápida para o subdomínio do chat (`://meu-dominio.com.br`).
5. O subdomínio devolve apenas o pedaço de HTML renderizado do chat.
6. O Nginx substitui o comentário pelo HTML do chat e entrega o código unificado final para o navegador do cliente.

---

## 🛠️ Passo 1: Preparação no HTML das Aplicações

Tanto no arquivo principal do Angular (`index.html`) quanto nas páginas legadas do ASP Clássico (`.asp`), adicione a linha de marcação abaixo exatamente no local onde o fragmento do widget deve ser embutido (geralmente logo antes do fechamento da tag `</body>`):

```html
<!--# include virtual="/internal-chat-widget/" -->
```

*Nota: Por se tratar de um comentário HTML padrão, se o SSI for desativado por algum motivo, os navegadores ignorarão a linha sem quebrar o layout do sistema.*

---

## ⚙️ Passo 2: Configuração do Nginx (`nginx.conf`)

No arquivo de configuração do bloco de servidor do seu domínio principal (`meu-dominio.com.br`), aplique as diretivas de SSI e crie a rota interna protegida:

```nginx
server {
    listen 80;
    server_name meu-dominio.com.br;

    # 1. Ativa o processamento de Server-Side Includes
    ssi on;
    ssi_silent_errors off; # Defina como 'on' em produção para ocultar erros caso o chat fique fora do ar

    # 2. Rota padrão para as aplicações (Angular ou ASP Clássico)
    location / {
        proxy_pass http://seu_servidor_principal; 
        
        # OBRIGATÓRIO: Força o backend a não responder compactado (Gzip)
        # para que o Nginx consiga ler o HTML e processar a tag SSI antes do envio
        proxy_set_header Accept-Encoding ""; 
    }

    # 3. Rota Interna e Protegida para Injeção do Widget
    location /internal-chat-widget/ {
        # Garante que esta rota não pode ser acessada externamente via URL direta
        internal; 

        # Busca o HTML bruto processado diretamente no subdomínio do chat
        proxy_pass http://://meu-dominio.com.br/; 
        
        proxy_set_header Host ://meu-dominio.com.br;
        proxy_set_header X-Real-IP \$remote_addr;

        # Evita compressão no tráfego do fragmento de HTML do chat
        proxy_set_header Accept-Encoding ""; 
    }
}
```

---

## 💻 Passo 3: Estrutura do HTML do Subdomínio do Chat

O servidor responsável por responder pelo subdomínio `://meu-dominio.com.br` deve retornar **apenas o fragmento bruto do chat**, sem as tags estruturais globais (`<html>`, `<head>`, `<body>`). 

Para garantir o carregamento correto dos estilos e scripts do chat de dentro da página hospedeira, utilize **URLs absolutas** apontando para o subdomínio:

```html
<!-- Retorno limpo e isolado do subdomínio do chat -->
<link rel="stylesheet" href="http://://meu-dominio.com.br/css/chat.css">

<div class="meu-chat-container-fixo">
    <button class="botao-chat-flutuante">💬 Conversar</button>
</div>

<script src="http://://meu-dominio.com.br/js/chat-core.js" defer></script>
```

---

## 🔒 Boas Práticas e Cuidados Importantes

1. **Escopo de CSS (Scoping):** Como o HTML do chat compartilhará o mesmo DOM do sistema hospedeiro, utilize classes com prefixos únicos (ex: `.mw-chat-button`, `.mw-chat-window`) ou encapsule o fragmento utilizando **Shadow DOM** via JavaScript para evitar que o CSS do chat altere o estilo do Angular ou do ASP legando.
2. **CORS (Cross-Origin Resource Sharing):** Como o Nginx mascara a chamada do chat através da rota local `/internal-chat-widget/`, o HTML principal e o fragmento compartilham a mesma origem aos olhos do navegador. Contudo, se o script do seu chat (`chat-core.js`) fizer requisições AJAX para um endpoint de API (ex: `://meu-dominio.com.br`), certifique-se de configurar as permissões de CORS na API para aceitar requisições de `meu-dominio.com.br`.
3. **Módulo SSI Ativo:** Certifique-se de que o Nginx foi compilado com o módulo `http_ssi_module` (habilitado por padrão nas distribuições Linux mais populares como Ubuntu, Debian e Alpine).
