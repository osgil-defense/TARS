# docker build -t klinux .

# docker pull ghcr.io/zaproxy/zaproxy:stable

docker run -it --name klinux --privileged -v /var/run/docker.sock:/var/run/docker.sock klinux

