sudo apt-get update
sudo apt-get install -y git ffmpeg build-essential python3 python3-venv python-pip python-setuptools git-core tmux
sudo chown -R ubuntu:ubuntu /srv/
python3 -m venv /srv/venv/

cd /srv/
git clone git@github.com:dancelogue/dance-datasets-downloader.git
cd dance-datasets-downloader/

source /srv/venv/bin/activate
pip install wheel
pip install -r requirements.txt
pip install -r server/requirements.txt
