conda create -n yolov7 python=3.9

activate yolov7
conda install openpyxl

nvcc --version
Cuda compilation tools, release 10.2, V10.2.89

cd folder where you want to clone the repository
git clone https://github.com/WongKinYiu/yolov7.git

cd xx\yolov7
pip install --upgrade pip
pip install -r requirements.txt

pip install torch==1.10.1+cu102 torchvision==0.11.2+cu102 torchaudio==0.10.1 -f https://download.pytorch.org/whl/cu102/torch_stable.html

python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.version.cuda)" 