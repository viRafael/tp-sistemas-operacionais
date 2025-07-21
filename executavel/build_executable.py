# build_executable.py
# Corrigido para ambientes gerenciados (como Ubuntu 23+)

import subprocess
import sys
import os
import venv

VENV_DIR = "venv"

def create_virtualenv():
    """Cria o ambiente virtual se não existir"""
    if not os.path.exists(VENV_DIR):
        print("🐍 Criando ambiente virtual...")
        venv.create(VENV_DIR, with_pip=True)
        print("✅ Ambiente virtual criado!")

def run_in_venv(cmd):
    """Executa comandos dentro do ambiente virtual"""
    python_bin = os.path.join(VENV_DIR, "bin", "python")
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

    pyinstaller_bin = os.path.join(VENV_DIR, "bin", "pyinstaller")
    
    cmd = [
        pyinstaller_bin,
        "--onefile",
        "--windowed",
        "--name=SimuladorCAV",
        "--icon=NONE",
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
