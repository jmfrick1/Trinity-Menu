import os
import subprocess
import sys

def create_virtual_environment(env_name):
    # Create virtual environment
    subprocess.run([sys.executable, '-m', 'venv', env_name])

def install_dependencies(env_name):
    # Install dependencies
    subprocess.run([f'{env_name}/bin/pip', 'install', 'numpy', 'opencv-python', 'torch', 'torchvision', 'requests', 'scipy', 'flask', 'flask_sqlalchemy'])

def download_openpose_models(model_dir):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    # Download pose_deploy.prototxt
    pose_deploy_url = "https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/pose/coco/pose_deploy_linevec.prototxt"
    pose_deploy_path = os.path.join(model_dir, "pose_deploy_linevec.prototxt")
    subprocess.run(["wget", pose_deploy_url, "-O", pose_deploy_path])

    # Download pose_iter_440000.caffemodel
    pose_iter_url = "http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/pose_iter_440000.caffemodel"
    pose_iter_path = os.path.join(model_dir, "pose_iter_440000.caffemodel")
    subprocess.run(["wget", pose_iter_url, "-O", pose_iter_path])

def main():
    env_name = "venv_bullseye"
    model_dir = "assets/openpose_models"
    
    create_virtual_environment(env_name)
    install_dependencies(env_name)
    download_openpose_models(model_dir)
    
    print("Environment setup complete.")

if __name__ == "__main__":
    main()
