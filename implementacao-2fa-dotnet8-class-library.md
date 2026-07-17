# Implementação de 2FA com TOTP em .NET 8

Guia para criar uma Class Library .NET 8 que:

- gera um segredo TOTP;
- monta a URI `otpauth://` para cadastro no Google Authenticator, Microsoft Authenticator ou app compatível;
- gera um QR Code em PNG/Base64;
- valida códigos de seis dígitos.

## 1. Criar o projeto

```bash
dotnet new classlib -n TwoFactorAuth
cd TwoFactorAuth
dotnet add package Otp.NET
dotnet add package QRCoder
```

No `.csproj`, confirme o alvo:

```xml
<TargetFramework>net8.0</TargetFramework>
```

## 2. Contratos

Crie `TwoFactorSetup.cs`:

```csharp
namespace TwoFactorAuth;

public sealed record TwoFactorSetup(
    string Secret,
    string ProvisioningUri,
    byte[] QrCodePng,
    string QrCodeBase64);
```

## 3. Serviço de 2FA

Crie `TwoFactorService.cs`:

```csharp
using OtpNet;
using QRCoder;

namespace TwoFactorAuth;

public sealed class TwoFactorService
{
    private const string Issuer = "MinhaAplicacao";

    public TwoFactorSetup CreateSetup(string accountName)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(accountName);

        var secretBytes = KeyGeneration.GenerateRandomKey(20);
        var secret = Base32Encoding.ToString(secretBytes);
        var provisioningUri = new OtpUri(
            OtpType.Totp,
            secret,
            accountName,
            issuer: Issuer).ToString();

        var qrCodePng = PngByteQRCodeHelper.GetQRCode(
            provisioningUri,
            QRCodeGenerator.ECCLevel.Q,
            pixelsPerModule: 20);

        return new TwoFactorSetup(
            secret,
            provisioningUri,
            qrCodePng,
            Convert.ToBase64String(qrCodePng));
    }

    public bool ValidateCode(
        string base32Secret,
        string code,
        VerificationWindow? window = null)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(base32Secret);

        if (code is null || code.Length != 6 || !code.All(char.IsDigit))
            return false;

        var secretBytes = Base32Encoding.ToBytes(base32Secret);
        var totp = new Totp(secretBytes);

        return totp.VerifyTotp(
            code,
            out _,
            window ?? VerificationWindow.RfcSpecifiedNetworkDelay);
    }
}
```

## 4. Uso

```csharp
var service = new TwoFactorService();

// Executar uma única vez durante o cadastro do 2FA.
var setup = service.CreateSetup("usuario@empresa.com");

// Exibir em uma página HTML:
var imageSource = $"data:image/png;base64,{setup.QrCodeBase64}";

// Persistir o segredo somente depois que o usuário confirmar o primeiro código.
var secret = setup.Secret;

// Validar um código informado pelo usuário.
var valid = service.ValidateCode(secret, "123456");
```

HTML para exibir o QR Code:

```html
<img src="data:image/png;base64,{{QrCodeBase64}}" alt="QR Code para configurar o autenticador" />
```

## 5. Fluxo recomendado

1. Usuário solicita a ativação do 2FA.
2. A aplicação chama `CreateSetup`.
3. A aplicação exibe o QR Code e, opcionalmente, o segredo como alternativa manual.
4. Usuário cadastra a conta no aplicativo autenticador.
5. Usuário informa o primeiro código.
6. A aplicação chama `ValidateCode`.
7. Somente após sucesso, persiste o segredo e marca o 2FA como ativo.
8. Nos próximos logins, exige e valida um novo código.

## 6. Armazenamento seguro

- O segredo é uma credencial: criptografe-o em repouso.
- Nunca registre o segredo, a URI ou o QR Code em logs.
- Não retorne o segredo depois que o cadastro for concluído.
- Use um cofre de segredos ou criptografia com chave protegida pelo ambiente.
- Considere salvar o último `timeStep` usado para impedir reutilização do mesmo código.
- Proteja a validação contra brute force com limite de tentativas, atraso progressivo e auditoria.
- Exija HTTPS na aplicação que consumir esta biblioteca.

## 7. Janela de tolerância

O padrão `VerificationWindow.RfcSpecifiedNetworkDelay` permite pequenas diferenças de relógio e atraso de rede. Use uma janela maior somente se houver uma justificativa operacional, pois isso aumenta o período em que um código pode ser aceito:

```csharp
var window = new VerificationWindow(previous: 1, future: 1);
var valid = service.ValidateCode(secret, code, window);
```

## 8. Testes mínimos

```csharp
var service = new TwoFactorService();
var setup = service.CreateSetup("teste@empresa.com");
var totp = new Totp(Base32Encoding.ToBytes(setup.Secret));
var currentCode = totp.ComputeTotp();

if (!service.ValidateCode(setup.Secret, currentCode))
    throw new InvalidOperationException("O código TOTP deveria ser válido.");

if (service.ValidateCode(setup.Secret, "000000"))
    throw new InvalidOperationException("Um código inválido não deveria ser aceito.");
```

## Referências

- [Otp.NET](https://github.com/kspearrin/otp.net) — TOTP/HOTP e validação de códigos.
- [QRCoder](https://github.com/codebude/QRCoder) — geração do QR Code.
- [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238) — especificação do TOTP.
