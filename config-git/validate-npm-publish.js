const { execSync } = require("child_process");
const semver = require("semver");
const pkg = require("../package.json");

const packageName = pkg.name;
const currentVersion = pkg.version;

const registry =
  process.env.NPM_REGISTRY ||
  process.env.npm_config_registry ||
  "https://nexus.seudominio.com/repository/npm-hosted/";

const branch =
  process.env.CI_COMMIT_BRANCH ||
  process.env.GIT_BRANCH ||
  getCurrentGitBranch();

function getCurrentGitBranch() {
  try {
    return execSync("git rev-parse --abbrev-ref HEAD", {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"]
    }).trim();
  } catch {
    return "";
  }
}

function npmView(command) {
  return execSync(command, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"]
  }).trim();
}

function fail(message) {
  console.error(`\n❌ ${message}\n`);
  process.exit(1);
}

function success(message) {
  console.log(`✅ ${message}`);
}

console.log("Validando publicação NPM...");
console.log(`Pacote: ${packageName}`);
console.log(`Versão atual: ${currentVersion}`);
console.log(`Branch: ${branch || "não identificada"}`);
console.log(`Registry: ${registry}`);

if (!semver.valid(currentVersion)) {
  fail(`A versão "${currentVersion}" não é uma versão semver válida.`);
}

const isReleaseBranch = /^release\/.+/.test(branch);
const isPrerelease = semver.prerelease(currentVersion);

if (isReleaseBranch && isPrerelease) {
  fail(
    `Branch release não pode publicar versão pre-release: ${currentVersion}`
  );
}

if (isReleaseBranch && /-(alpha|beta|rc)(\.|\d|$)/i.test(currentVersion)) {
  fail(
    `Branch release não pode publicar versões alpha, beta ou rc: ${currentVersion}`
  );
}

let publishedVersions = [];

try {
  const result = npmView(
    `npm view "${packageName}" versions --json --registry="${registry}"`
  );

  publishedVersions = JSON.parse(result);

  if (!Array.isArray(publishedVersions)) {
    publishedVersions = [publishedVersions];
  }
} catch {
  success("Pacote ainda não existe no Nexus. Primeira publicação permitida.");
  process.exit(0);
}

const validPublishedVersions = publishedVersions
  .filter(version => semver.valid(version))
  .sort(semver.compare);

const latestVersion = validPublishedVersions.at(-1);

if (!latestVersion) {
  success("Nenhuma versão válida encontrada no Nexus. Publicação permitida.");
  process.exit(0);
}

console.log(`Última versão publicada: ${latestVersion}`);

if (publishedVersions.includes(currentVersion)) {
  fail(`A versão ${currentVersion} já está publicada no Nexus.`);
}

if (semver.lte(currentVersion, latestVersion)) {
  fail(
    `Downgrade ou versão igual não permitido. Atual: ${currentVersion}, última publicada: ${latestVersion}`
  );
}

const diff = semver.diff(latestVersion, currentVersion);

if (
  ![
    "patch",
    "minor",
    "major",
    "prepatch",
    "preminor",
    "premajor",
    "prerelease"
  ].includes(diff)
) {
  fail(
    `Incremento inválido. Atual: ${currentVersion}, última publicada: ${latestVersion}`
  );
}

if (
  isReleaseBranch &&
  ["prepatch", "preminor", "premajor", "prerelease"].includes(diff)
) {
  fail(
    `Branch release só pode publicar versões estáveis patch, minor ou major. Incremento detectado: ${diff}`
  );
}

success(`Versão válida para publicação. Incremento detectado: ${diff}`);
