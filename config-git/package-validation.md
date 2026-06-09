#Validação de packages 

Arquivo na raiz da solution como Directory.Build.targets:
```xml
<Project>
  <PropertyGroup>
    <!-- GitLab -->
    <CurrentBranch Condition="'$(CI_COMMIT_REF_NAME)' != ''">$(CI_COMMIT_REF_NAME)</CurrentBranch>
    <CurrentBranch Condition="'$(CI_COMMIT_BRANCH)' != ''">$(CI_COMMIT_BRANCH)</CurrentBranch>
    <!-- Azure DevOps -->
    <CurrentBranch Condition="'$(BUILD_SOURCEBRANCHNAME)' != ''">$(BUILD_SOURCEBRANCHNAME)</CurrentBranch>
    <CurrentBranch Condition="'$(BUILD_SOURCEBRANCH)' != ''">
      $([System.String]::Copy('$(BUILD_SOURCEBRANCH)').Replace('refs/heads/', ''))
    </CurrentBranch>
    <!-- GitHub Actions -->
    <CurrentBranch Condition="'$(GITHUB_REF_NAME)' != ''">$(GITHUB_REF_NAME)</CurrentBranch>
    <CurrentBranch Condition="'$(GITHUB_REF)' != ''">
      $([System.String]::Copy('$(GITHUB_REF)').Replace('refs/heads/', ''))
    </CurrentBranch>
  </PropertyGroup>
  <Target Name="ValidateNoPreReleasePackagesOnReleaseBranch"
          BeforeTargets="Build"
          Condition="$([System.String]::Copy('$(CurrentBranch)').StartsWith('release/'))">
    <ItemGroup>
      <InvalidInternalPackages Include="@(PackageReference)"
        Condition="
          $([System.String]::Copy('%(PackageReference.Identity)').StartsWith('MinhaEmpresa.'))
          And (
            $([System.String]::Copy('%(PackageReference.Version)').Contains('-alpha'))
            Or $([System.String]::Copy('%(PackageReference.Version)').Contains('-beta'))
            Or $([System.String]::Copy('%(PackageReference.Version)').Contains('-rc'))
          )
        " />
    </ItemGroup>
    <Message Importance="High"
             Text="Validando pacotes internos para branch release/*: $(CurrentBranch)" />
    <Error
      Condition="'@(InvalidInternalPackages)' != ''"
      Text="Build bloqueado. Branch $(CurrentBranch) não permite pacotes internos alpha, beta ou rc: @(InvalidInternalPackages -> '%(Identity) %(Version)', ', ')" />
  </Target>
</Project>
```
Troque:

StartsWith('MinhaEmpresa.')

pelo prefixo real das suas libs internas, por exemplo:

StartsWith('SeuBanco.')
StartsWith('Company.')
StartsWith('Safra.')

Exemplo bloqueado em release/*:

<PackageReference Include="MinhaEmpresa.Core" Version="1.4.0-beta.2" />
<PackageReference Include="MinhaEmpresa.Auth" Version="2.1.0-rc.1" />

Exemplo permitido:


<PackageReference Include="MinhaEmpresa.Core" Version="1.4.0" />
<PackageReference Include="MinhaEmpresa.Auth" Version="2.1.0" />


No GitLab, isso funciona automaticamente porque ele expõe a branch em:

CI_COMMIT_REF_NAME
CI_COMMIT_BRANCH


Exemplo com YAML no .gitlab-ci.yml

.gitlab/ci/dotnet-build.yml
```yaml
.build-base:
  stage: build
  image: mcr.microsoft.com/dotnet/sdk:9.0
  script:
    - dotnet restore
    - dotnet build -c Release
    - dotnet test
```
No seu .gitlab-ci.yml principal:
```yaml
include:
  - local: '.gitlab/ci/dotnet-build.yml'
build:
  extends:
    - .build-base
  before_script:
    - |
      if [[ "$CI_COMMIT_BRANCH" =~ ^release/ ]]; then

        echo "Validando pacotes pre-release em branch release/*..."

        INVALID_PACKAGES=$(find . \
          \( -name "*.csproj" -o -name "*.props" \) \
          -print0 \
          | xargs -0 grep -HnE \
            '<(PackageReference|PackageVersion)[^>]+(Include|Update)="[^"]+"[^>]+Version="[^"]*-(alpha|beta|rc)' \
          || true)

        if [ -n "$INVALID_PACKAGES" ]; then
          echo "Build bloqueado. Branch release/* não permite pacotes alpha, beta ou rc:"
          echo "$INVALID_PACKAGES"
          exit 1
        fi

        echo "Validação OK."

      else
        echo "Branch não é release/*. Validação ignorada."
      fi
```
Fluxo de execução:
```textplain
build
 │
 ├── before_script (seu)
 │     └── valida alpha/beta/rc
 │
 └── script (.build-base)
       ├── dotnet restore
       ├── dotnet build
       └── dotnet test
```
⸻

Se quiser validar apenas pacotes internos com prefixo Company.:
```bash
INVALID_PACKAGES=$(find . \
  \( -name "*.csproj" -o -name "*.props" \) \
  -print0 \
  | xargs -0 grep -HnE \
    '<(PackageReference|PackageVersion)[^>]+(Include|Update)="MinhaEmpresa\.[^"]+"[^>]+Version="[^"]*-(alpha|beta|rc)' \
  || true)
```
⸻

Uma alternativa ainda mais limpa é extrair a validação para um template reutilizável:

.gitlab/ci/validate-release.yml
```yaml
.validate-release-packages:
  before_script:
    - |
      if [[ "$CI_COMMIT_BRANCH" =~ ^release/ ]]; then

        echo "Validando pacotes pre-release em branch release/*..."

        INVALID_PACKAGES=$(find . \
          \( -name "*.csproj" -o -name "*.props" \) \
          -print0 \
          | xargs -0 grep -HnE \
            '<(PackageReference|PackageVersion)[^>]+(Include|Update)="[^"]+"[^>]+Version="[^"]*-(alpha|beta|rc)' \
          || true)

        if [ -n "$INVALID_PACKAGES" ]; then
          echo "Build bloqueado. Branch release/* não permite pacotes alpha, beta ou rc:"
          echo "$INVALID_PACKAGES"
          exit 1
        fi

        echo "Validação OK."

      else
        echo "Branch não é release/*. Validação ignorada."
      fi
```
E no pipeline:
```yaml
include:
  - local: '.gitlab/ci/dotnet-build.yml'
  - local: '.gitlab/ci/validate-release.yml'
build:
  extends:
    - .validate-release-packages
    - .build-base
```
Essa segunda abordagem para um ambiente corporativo porque mantém a validação desacoplada do build e reaproveitável para qualquer projeto .NET.