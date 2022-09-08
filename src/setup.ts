import { execSync } from "child_process";
import { existsSync, readdirSync } from "fs";
import { join } from "path";
import { ExtensionContext, ProgressLocation, window, workspace} from "vscode";

export const IS_WIN = process.platform === "win32";

function createVirtualEnvironment(python: string, name: string, cwd: string): string {
  const path = join(cwd, name);
  if (!existsSync(path)) {
    const createVenvCmd = `${python} -m venv ${name}`;
    execSync(createVenvCmd, { cwd });
  }
  return path;
}

function getPython(): string {
  return workspace.getConfiguration("python").get<string>("pythonPath", getPythonCrossPlatform());
}

function getPythonCrossPlatform(): string {
  return IS_WIN ? "python" : "python3";
}

function getPythonFromVenvPath(venvPath: string): string {
  return IS_WIN ? join(venvPath, "Scripts", "python") : join(venvPath, "bin", "python");
}

function getPythonVersion(python: string): number[] | undefined {
  const getPythonVersionCmd = `${python} --version`;
  const version = execSync(getPythonVersionCmd).toString();
  return version.match(RegExp(/\d/g))?.map((v) => Number.parseInt(v));
}

function getVenvPackageVersion(python: string, name: string): boolean {
  const listPipPackagesCmd = `${python} -m pip show ${name}`;

  try {
    const packageInfo = execSync(listPipPackagesCmd).toString();
    if (packageInfo === undefined){
      return false;
    }
    return true;
  } catch (err) {
    return false;
  }
}

function installServer(python: string){
  execSync(`${python} -m pip install pyflies-ls`);
}

function* installLS(context: ExtensionContext): IterableIterator<string> {
  yield "Installing textX language server";

  // Get python interpreter
  const python = getPython();
  // Check python version (3.5+ is required)
  const [major, minor] = getPythonVersion(python) || [3, 6];
  if (major !== 3 || minor < 5) {
    throw new Error("Python 3.5+ is required!");
  }

  // Create virtual environment
  const venv = createVirtualEnvironment(python, "pyfliesls", context.extensionPath);
  yield `Virtual Environment created in: ${venv}`;

  // Install source from wheels
  const venvPython = getPythonFromVenvPath(venv);
  const wheelsPath = join(context.extensionPath, "wheels");
  installServer(venvPython);
  // installAllWheelsFromDirectory(venvPython, wheelsPath);
  yield `Successfully installed pyflies-LS.`;
}

export async function installLSWithProgress(context: ExtensionContext): Promise<string> {
  // Check if LS is already installed
  const venvPython = getPythonFromVenvPath(join(context.extensionPath, "pyfliesls"));

  if (getVenvPackageVersion(venvPython, "pyflies-ls")) {
    return Promise.resolve(venvPython);
  }

  // Install with progress bar
  return await window.withProgress({
    location: ProgressLocation.Window,
  }, (progress): Promise<string> => {
    return new Promise<string>((resolve, reject) => {

      // Catch generator errors
      try {
        // Go through installation steps
        for (const step of installLS(context)) {
          progress.report({ message: step });
        }

      } catch (err) {
        reject(err);
      }

      resolve(venvPython);
    });
  });

}
