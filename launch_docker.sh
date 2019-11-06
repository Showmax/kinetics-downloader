#!/bin/bash
# sudo nvidia-docker build -t dancelogue:st-gnc .
# docker build -t gcr.io/dancelogue-ai-demo/dancelogue-deep-sort:1.0 .

xhost +
docker run --rm -ti \
	--volume=$(pwd):/dancelogue:rw \
	--volume="/media/gitumarkk/Extreme SSD/Dancelogue/DATASETS/":/DATASETS:rw \
	--volume="/home/gitumarkk/Desktop/DANCELOGUE AI/DATASETS/st-gcn":/DATASETS_DESKTOP:rw \
	--workdir=/ \
	--ipc=host \
	-p 8097:8097 \
	-p 8006:8006 \
	-p 8007:8007 \
	-p 8008:8008 \
	-p 8009:8009 \
	dancelogue:st-gnc /bin/bash
