Arquivo na raiz da solution como Directory.Build.targets:

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