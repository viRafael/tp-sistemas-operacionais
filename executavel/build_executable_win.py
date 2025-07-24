# build_executable.py
# Compatível com Windows, Linux e Mac

import subprocess
import sys
import os
import venv
import platform

VENV_DIR = "venv"

def create_virtualenv():
    """Cria o ambiente virtual se não existir"""
    if not os.path.exists(VENV_DIR):
        print("🐍 Criando ambiente virtual...")
        venv.create(VENV_DIR, with_pip=True)
        print("✅ Ambiente virtual criado!")

def get_python_path():
    """Retorna o caminho do Python dentro do venv conforme o SO"""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def get_pyinstaller_path():
    """Retorna o caminho do PyInstaller dentro do venv conforme o SO"""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pyinstaller.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "pyinstaller")

def run_in_venv(cmd):
    """Executa comandos dentro do ambiente virtual"""
    python_bin = get_python_path()
    subprocess.check_call([python_bin, "-m"] + cmd)

def install_requirements():
    """Instala os pacotes necessários dentro do venv"""
    print("📦 Instalando PyInstaller no ambiente virtual...")
    run_in_venv(["pip", "install", "--upgrade", "pip"])
    run_in_venv(["pip", "install", "pyinstaller"])
    print("✅ PyInstaller instalado no ambiente virtual!")

def create_executable():
    """Cria o executável usando PyInstaller dentro do venv"""
    print("\n🔨 Criando executável...")

    pyinstaller_bin = get_pyinstaller_path()

    cmd = [
        pyinstaller_bin,
        "--clean", # Adicionado para limpar o cache do PyInstaller
        "--onefile",
        "--console",
        "--name=SimuladorCAV",
        "--icon=NONE",
        "--hidden-import=collections.abc", # Força a inclusão de collections.abc
        "--hidden-import=os", # Força a inclusão de os
        "simulador_cav_gui.py"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("✅ Executável criado com sucesso!")
        print("📁 Arquivo gerado: dist/SimuladorCAV")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")
        print("💡 Tente executar manualmente com PyInstaller")

def main():
    print("🚀 CRIADOR DE EXECUTÁVEL - SIMULADOR CAV")
    print("=" * 50)

    if not os.path.exists("simulador_cav_gui.py"):
        print("❌ Arquivo 'simulador_cav_gui.py' não encontrado!")
        return

    create_virtualenv()
    install_requirements()
    create_executable()

    print("\n🎉 PRONTO! Seu executável está na pasta 'dist'")
    print("=" * 50)

if __name__ == "__main__":
    main()
