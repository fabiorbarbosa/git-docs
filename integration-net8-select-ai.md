# Integração .NET 8 + LinqToDB (DataContext) + Oracle Select AI com Paginação

Este guia unifica a configuração necessária para expor um endpoint que aceita filtros em linguagem natural, executa a consulta via Oracle Select AI e retorna os dados paginados de forma dinâmica.

---

## 1. Banco de Dados: Stored Procedure com Paginação

Crie ou atualize a Stored Procedure no Oracle para aceitar os parâmetros de **página** (`p_pagina`) e **quantidade de registros** (`p_tamanho_pagina`). O cálculo do `OFFSET` garante que apenas as linhas solicitadas sejam trafegadas pela rede.

```sql
CREATE OR REPLACE PROCEDURE sp_obter_dados_ia_paginado (
    p_filtro         IN VARCHAR2,
    p_pagina         IN NUMBER,
    p_tamanho_pagina IN NUMBER,
    p_resultado      OUT SYS_REFCURSOR
) AS
    v_sql          CLOB;
    v_offset       NUMBER;
BEGIN
    -- Configura o perfil ativo do Select AI
    DBMS_CLOUD_AI.SET_PROFILE('MEU_PERFIL_IA');
    
    -- Calcula o deslocamento de linhas para a paginação
    v_offset := (p_pagina - 1) * p_tamanho_pagina;

    -- Monta o SQL dinâmico injetando as cláusulas de paginação nativas do Oracle 12c+
    v_sql := 'SELECT AI runsql ''' || p_filtro || ''' ' ||
             'OFFSET ' || v_offset || ' ROWS ' ||
             'FETCH NEXT ' || p_tamanho_pagina || ' ROWS ONLY';

    -- Abre o cursor dinâmico para o LinqToDB ler
    OPEN p_resultado FOR v_sql;
END sp_obter_dados_ia_paginado;
/
```

---

## 2. Código .NET 8 (C#)

### Models (DTOs)
Estrutura para receber o request com paginação e envelopar a resposta com metadados básicos.

```csharp
namespace SuaAplicacao.Models;

public class ConsultaAiRequest
{
    public string Filtro { get; set; } = string.Empty;
    public int Pagina { get; set; } = 1;
    public int TamanhoPagina { get; set; } = 10;
}

public class PagedResult<T>
{
    public int PaginaAtual { get; set; }
    public int TamanhoPagina { get; set; }
    public List<T> Dados { get; set; } = new();
}
```

### Contexto LinqToDB (DataContext)
Implementação do contexto herdando de `DataContext`. Utilizamos o `CreateDataConnection()` para abrir uma conexão física temporária e ler o `RefCursor` dinâmico com segurança, fechando-a automaticamente ao final do bloco.

```csharp
namespace SuaAplicacao.Data;

using LinqToDB;
using LinqToDB.Data;
using LinqToDB.DataProvider.Oracle;
using Oracle.ManagedDataAccess.Client;
using System.Data;

public class DbOracleContext : DataContext
{
    public DbOracleContext(string connectionString) 
        : base(OracleTools.GetDataProvider(OracleVersion.v12), connectionString)
    {
    }

    public async Task<List<Dictionary<string, object>>> ExecutarSelectAiPaginadoAsync(string filtro, int pagina, int tamanhoPagina)
    {
        var resultados = new List<Dictionary<string, object>>();

        // Extrai uma DataConnection do DataContext para gerenciar o comando ADO.NET nativo
        using (var dataConnection = this.CreateDataConnection())
        {
            if (dataConnection.Connection.State != ConnectionState.Open)
                await dataConnection.EnsureConnectionAsync();

            using (var cmd = (OracleCommand)dataConnection.Connection.CreateCommand())
            {
                cmd.CommandText = "sp_obter_dados_ia_paginado";
                cmd.CommandType = CommandType.StoredProcedure;

                // Parâmetros de entrada e saída da procedure
                cmd.Parameters.Add("p_filtro", OracleDbType.Varchar2, filtro, ParameterDirection.Input);
                cmd.Parameters.Add("p_pagina", OracleDbType.Int32, pagina, ParameterDirection.Input);
                cmd.Parameters.Add("p_tamanho_pagina", OracleDbType.Int32, tamanhoPagina, ParameterDirection.Input);
                cmd.Parameters.Add("p_resultado", OracleDbType.RefCursor, ParameterDirection.Output);

                // Executa e lê as colunas dinâmicas retornadas pela IA
                using (var reader = await cmd.ExecuteReaderAsync())
                {
                    while (await reader.ReadAsync())
                    {
                        var linha = new Dictionary<string, object>();
                        for (int i = 0; i < reader.FieldCount; i++)
                        {
                            linha[reader.GetName(i)] = reader.GetValue(i);
                        }
                        resultados.Add(linha);
                    }
                }
            }
        }

        return resultados;
    }
}
```

### Program.cs (Configuração DI)
Configuração do ciclo de vida do contexto no container de Injeção de Dependência da API.

```csharp
using SuaAplicacao.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

// Registra o DataContext como Scoped
builder.Services.AddScoped(provider => 
{
    var connectionString = builder.Configuration.GetConnectionString("OracleDb")!;
    return new DbOracleContext(connectionString);
});

var app = builder.Build();
app.MapControllers();
app.Run();
```

### API Controller
Endpoint REST que recebe o payload JSON, repassa os filtros ao contexto e monta o objeto paginado de resposta.

```csharp
namespace SuaAplicacao.Controllers;

using Microsoft.AspNetCore.Mvc;
using SuaAplicacao.Data;
using SuaAplicacao.Models;

[ApiController]
[Route("api/[controller]")]
public class AiController : ControllerBase
{
    private readonly DbOracleContext _context;

    public AiController(DbOracleContext context)
    {
        _context = context;
    }

    [HttpPost("consultar")]
    public async Task<IActionResult> ConsultarComIA([FromBody] ConsultaAiRequest request)
    {
        // Validações básicas de entrada
        if (string.IsNullOrWhiteSpace(request.Filtro))
            return BadRequest("O filtro enviado na requisição não pode estar vazio.");

        if (request.Pagina < 1) request.Pagina = 1;
        if (request.TamanhoPagina < 1) request.TamanhoPagina = 10;

        try
        {
            // Executa a busca paginada
            var dadosId = await _context.ExecutarSelectAiPaginadoAsync(
                request.Filtro, 
                request.Pagina, 
                request.TamanhoPagina
            );

            // Monta o envelope paginado
            var resposta = new PagedResult<Dictionary<string, object>>
            {
                PaginaAtual = request.Pagina,
                TamanhoPagina = request.TamanhoPagina,
                Dados = dadosId
            };

            return Ok(resposta);
        }
        catch (Exception ex)
        {
            // Logar o erro interno apropriadamente aqui
            return StatusCode(500, \$"Erro na execução do Select AI: {ex.Message}");
        }
    }
}
```

---

## 3. Exemplo de Requisição (Payload)

Para testar a paginação na sua API, envie uma requisição `POST` para `http://localhost:suaporta/api/ai/consultar`:

```json
{
  "filtro": "Quais foram os 50 clientes que mais compraram no ano passado?",
  "pagina": 1,
  "tamanhoPagina": 5
}
```
