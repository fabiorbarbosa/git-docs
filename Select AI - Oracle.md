# Padrão de Comentários de Colunas para Oracle Select AI

Para garantir a máxima precisão do **Select AI**, os comentários devem ser curtos, diretos e focados em regras de negócio. Evite descrições óbvias e foque em esclarecer códigos, unidades de medida e relacionamentos.

---

## 📋 Exemplos Práticos de Padrões

### 1. Colunas de Status ou Código (Crítico)
*Identifica o significado exato de cada sigla ou número armazenado.*

```sql
COMMENT ON COLUMN pedidos.status IS 'Status do pedido. Valores: A = Ativo, I = Inativo, C = Cancelado, P = Pendente de Pagamento.';
```

### 2. Colunas de Valores Monetários ou Numéricos
*Informa a unidade de medida para evitar erros de cálculo pela IA.*

```sql
COMMENT ON COLUMN produtos.preco_venda IS 'Preço de venda unitário do produto em Reais (BRL). Sempre armazenado com duas casas decimais.';
```

### 3. Colunas de Chaves Estrangeiras (Relacionamentos)
*Ajuda o modelo a entender como realizar os JOINs corretamente entre as tabelas.*

```sql
COMMENT ON COLUMN vendas.id_cliente IS 'Chave estrangeira que conecta ao ID da tabela CLIENTES. Identificador único do comprador.';
```

### 4. Colunas de Datas e Horários
*Especifica o padrão de fuso horário ou regras de preenchimento.*

```sql
COMMENT ON COLUMN usuarios.data_cadastro IS 'Data e hora em que o usuário criou a conta. Salvo no padrão UTC.';
```

---

## 🚫 O que EVITAR nos comentários

* **Redundância óbvia:** `COMMENT ON COLUMN clientes.nome IS 'Nome do cliente.';` (A IA já deduz isso pelo nome da coluna).
* **Histórico ou dados administrativos:** "Coluna criada pelo João em 2024 para resolver o bug X". Isso confunde o modelo de linguagem.



## PROMPT
Atue como um Administrador de Banco de Dados especialista em Oracle e IA (Select AI). 

Analise a estrutura de tabela fornecida abaixo. Com base no nome da coluna (identificando siglas comuns como ID, DT, FLG, VLR, CD, STATUS, TP) e no tipo de dado (NUMBER, VARCHAR2, DATE, etc.), gere os comandos SQL `COMMENT ON COLUMN` seguindo as melhores práticas para o Oracle Select AI.

### Regras para os comentários:
1. Devem ser em português, curtos, diretos e sem redundâncias óbvias.
2. Para colunas com nomes como 'STATUS', 'TP' ou 'FLG', crie um exemplo de dicionário de valores (ex: 'Valores: A = Ativo, I = Inativo').
3. Para colunas 'ID', especifique se é uma chave primária ou chave estrangeira padrão.
4. Para colunas de valores/valores monetários, inclua a unidade de medida padrão (Reais/BRL).
5. Se a tabela não for especificada no input, utilize o placeholder 'NOME_DA_TABELA'.

### Entrada da Estrutura:
Name.                Type.            Nullable.     Default.     Comments
ID_CLIENTE      NUMBER      N

### Formato de Saída esperado:
Retorne apenas o bloco de código SQL contendo os comandos COMMENT ON COLUMN gerados.


--

Atue como um Administrador de Banco de Dados especialista em Oracle e IA (Select AI). 

Analise a estrutura de tabela fornecida abaixo. Com base no nome da coluna, sufixos, prefixos e no tipo de dado (NUMBER, VARCHAR2, DATE, TIMESTAMP, etc.), gere os comandos SQL `COMMENT ON COLUMN` seguindo rigorosamente as melhores práticas para o Oracle Select AI (enriquecimento de metadados para modelos LLM).

### Regras Gerais para os comentários:
1. Devem ser em português do Brasil, curtos, diretos e sem redundâncias óbvias (ex: nunca diga apenas 'Nome do cliente' se a coluna chamar 'NOME').
2. Se a tabela não for especificada explicitamente no input, utilize o placeholder 'NOME_DA_TABELA'.

### Dicionário Expandido de Siglas, Prefixos/Sufixos e Regras Específicas:

1. IDENTIFICADORES (ID_... / ..._ID / CD_... / COD_...):
   - Se o nome coincidir com o contexto da tabela (ex: ID_CLIENTE na tabela Clientes), determine como 'Chave primária e identificador único'.
   - Se referenciar outra entidade (ex: ID_CIDADE na tabela Clientes), determine como 'Chave estrangeira que conecta à tabela correspondente'.

2. ESTADOS, TIPOS E FLAGS (STATUS / SITUACAO / TP_... / TIPO_... / FLG_... / IND_... / IS_...):
   - STATUS / SITUACAO: Adicione um exemplo descritivo de dicionário de valores (ex: 'Valores: A = Ativo, I = Inativo, C = Cancelado').
   - TP / TIPO: Crie uma inferência lógica de tipos (ex: 'Tipo de registro. Valores: F = Física, J = Jurídica' ou 'O = Operacional, A = Administrativo').
   - FLG / IND / IS (Flags Booleanas): Identifique como indicador booleano. Defina o mapeamento de valores padrão baseado no tipo do dado (ex: VARCHAR2(1)/CHAR(1) -> 'Valores: S = Sim, N = Não'; se NUMBER -> 'Valores: 1 = Sim, 0 = Não').

3. DADOS MONETÁRIOS E QUANTIDADES (VLR_... / VL_... / PRECO / TOTAL / SALDO / QTD_... / QUANT_...):
   - Valores monetários (NUMBER com decimais): Explicite que o valor é monetário e está armazenado na moeda corrente (Reais / BRL).
   - QTD / QUANT: Defina como 'Quantidade numérica de unidades' ou insira uma unidade de medida lógica se aplicável (ex: quilos, litros, unidades).

4. CRONOLOGIA (DT_... / DATA_... / ..._DATE / TS_... / ..._TIME):
   - DATE / TIMESTAMP: Explique o evento temporal (ex: 'Data e hora em que o registro foi criado/modificado'). Se for apenas data sem hora, especifique 'Armazena apenas a data do evento (DD/MM/AAAA)'.

5. DADOS FISCAIS, DOCUMENTOS E LOCALIZAÇÃO (CPF / CNPJ / CPF_CNPJ / INSCRICAO / CEP / UF / BAIRRO / ENDERECO):
   - CPF/CNPJ: Especifique se armazena apenas números, se possui máscara e se valida o documento oficial.
   - CEP / TEL / TELEFONE / EMAIL: Detalhe que armazena a informação textual formatada para auxiliar buscas exatas da IA.
   - UF: Especifique 'Sigla da Unidade Federativa com dois caracteres (ex: SP, RJ)'.

6. AUDITORIA E LOGS (USER_... / USUARIO_... / OPERACAO / LOG_...):
   - Colunas de controle: Identifique como metadados de auditoria interna (ex: 'Usuário do sistema responsável pela última alteração do registro').

7. INTEGRAÇÕES (ID_INTEGRACAO / GUID / LEGADO_... / EXT_...):
   - Identifique como chaves ou códigos de sincronização com sistemas externos, ERPs, APIs ou bases legadas.

8. TEXTO LIVRE (OBS / DSC / DESCRICAO / COMENTARIO):
   - Indique que aceita texto alfanumérico livre para observações ou descrições detalhadas do registro.

### Entrada da Estrutura:
Name.                Type.            Nullable.     Default.     Comments
ID_CLIENTE      NUMBER      N

### Formato de Saída esperado:
Retorne apenas o bloco de código SQL contendo os comandos COMMENT ON COLUMN gerados, sem blocos de texto antes ou depois e sem as marcações de crases (```sql).



## PYTHON

import os
import sys
from anthropic import Anthropic

# 1. Inicializa o cliente com a chave de API das variáveis de ambiente
# No terminal: export ANTHROPIC_API_KEY="sua-chave-aqui"
if "ANTHROPIC_API_KEY" not in os.environ:
    print("Erro: A variável de ambiente ANTHROPIC_API_KEY não foi definida.")
    sys.exit(1)

client = Anthropic()

# 2. Configurações de arquivos e contexto
ARQUIVO_ENTRADA = "estrutura.txt"      # Arquivo onde você colou a estrutura do banco
ARQUIVO_SAIDA = "comentarios_gerados.sql" # Arquivo .sql que será criado
NOME_TABELA = "CLIENTES"               # Altere para o nome da sua tabela real

# 3. Leitura do arquivo de entrada
try:
    with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
        estrutura_texto = f.read()
except FileNotFoundError:
    print(f"Erro: Crie o arquivo '{ARQUIVO_ENTRADA}' e cole a estrutura da tabela nele antes de rodar.")
    sys.exit(1)

# 4. Prompt do Sistema Expandido com Dicionário de Siglas e Regras de Negócio
PROMPT_SISTEMA = (
    "Atue como um Administrador de Banco de Dados especialista em Oracle e IA (Select AI).\n"
    "Seu objetivo é ler uma estrutura de tabela e gerar comandos SQL 'COMMENT ON COLUMN' focados "
    "em enriquecer os metadados para que modelos de LLM realizem Text-to-SQL sem ambiguidade.\n\n"
    
    "### DIRETRIZES DE ESCRITA:\n"
    "- Escreva estritamente em português brasileiro.\n"
    "- Seja curto, direto e evite redundâncias óbvias (ex: nunca descreva 'NOME' apenas como 'Nome do cliente').\n"
    "- Se o nome da coluna não der pistas claras de regras de negócio complexas, deduza uma descrição profissional e útil baseada no contexto da tabela.\n\n"
    
    "### REGRAS PARA RECONHECIMENTO DE SIGLAS E TIPOS:\n"
    "1. ID_... / ..._ID / CD_...: Identifique como identificadores. Especifique se parece uma Chave Primária (PK) ou Chave Estrangeira (FK).\n"
    "2. STATUS / SITUACAO: Adicione um dicionário fictício de valores de exemplo coerentes (ex: 'Valores: A = Ativo, I = Inativo, C = Cancelado').\n"
    "3. TP_... / ..._TP / TIPO_...: Adicione uma lista explicativa de tipos de exemplo (ex: 'Tipo de operação. Valores: F = Física, J = Jurídica').\n"
    "4. FLG_... / IND_... / IS_...: Identifique como flags booleanas armazenadas como VARCHAR/CHAR ou NUMBER. Indique os valores padrão (ex: 'Valores: S = Sim, N = Não' ou '1 = Sim, 0 = Não').\n"
    "5. DT_... / ..._DATA: Explique que armazena a data e/ou hora da ocorrência do evento especificado.\n"
    "6. VLR_... / VL_... / PRECO / TOTAL / SALDO: Se o tipo for numérico com decimais, explicite que o valor é monetário armazenado em Reais (BRL).\n"
    "7. CPF / CNPJ / CPF_CNPJ: Documente se exige máscara, se aceita apenas números ou se varia pelo tamanho do campo.\n"
    "8. CEP / TEL / TELEFONE / EMAIL: Detalhe o formato esperado do dado armazenado para auxiliar filtros de busca textuais da IA.\n"
    "9. OBS / DSC / DESCRICAO: Indique que armazena texto livre ou observações detalhadas sobre o registro.\n\n"
    
    "### FORMATO DE SAÍDA:\n"
    "Retorne APENAS o bloco de código SQL limpo com as declarações 'COMMENT ON COLUMN', sem marcações de markdown adicionais (sem ```sql) e sem nenhuma mensagem introdutória ou conclusiva."
)

PROMPT_CONTEUDO = f"""
Gere os comentários SQL para a tabela '{NOME_TABELA}' analisando detalhadamente os nomes e tipos da seguinte estrutura:

{estrutura_texto}
"""

print(f"Enviando dados de '{ARQUIVO_ENTRADA}' para o Claude...")

try:
    # 5. Chamada à API utilizando o Claude 3.5 Sonnet
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2500,
        system=PROMPT_SISTEMA,
        messages=[
            {"role": "user", "content": PROMPT_CONTEUDO}
        ]
    )
    
    # Limpa possíveis blocos markdown residuais caso a IA inclua por engano
    sql_gerado = response.content[0].text.strip()
    if sql_gerado.startswith("```"):
        sql_gerado = "\n".join(sql_gerado.split("\n")[1:-1])

    # 6. Gravação do arquivo .sql de saída
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f_out:
        f_out.write(sql_gerado)
        
    print(f"Sucesso! O arquivo '{ARQUIVO_SAIDA}' foi gerado perfeitamente com os comentários SQL.")

except Exception as e:
    print(f"Ocorreu um erro durante a execução: {e}")


export ANTHROPIC_API_KEY="sua_chave_real_aqui"
python gerador_sql_select_ai.py