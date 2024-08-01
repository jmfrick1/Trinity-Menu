# Environment setup script
import os
import subprocess
import sys

def create_virtual_environment(env_name):
    # Create virtual environment
    subprocess.run([sys.executable, '-m', 'venv', env_name])

def install_dependencies(env_name):
    # Install dependencies
    if os.name == 'nt':
        pip_path = os.path.join(env_name, 'Scripts', 'pip')
    else:
        pip_path = os.path.join(env_name, 'bin', 'pip')

    subprocess.run([pip_path, 'install', '--upgrade', 'pip'])
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    subprocess.run([pip_path, 'install', '-r', 'server-requirements.txt'])

def main():
    env_name = "ASTS_env"

    create_virtual_environment(env_name)
    install_dependencies(env_name)

    print("Environment setup complete.")

if __name__ == "__main__":
    main()
