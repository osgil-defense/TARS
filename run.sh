spacer() {
	echo
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo
}

#########################[MAIN FUNCTION CALLS]#########################

cat <<EOF
 ____  _   _ _   _ _   _ ___ _   _  ____ 
|  _ \| | | | \ | | \ | |_ _| \ | |/ ___|
| |_) | | | |  \| |  \| || ||  \| | |  _ 
|  _ <| |_| | |\  | |\  || || |\  | |_| |
|_|_\_\\___/|_|_\_|_|_\_|___|_| \_|\____|
 _____  _    ____  ____
|_   _|/ \  |  _ \/ ___|                 
  | | / _ \ | |_) \___ \                 
  | |/ ___ \|  _ < ___) |                
  |_/_/   \_\_| \_\____/                 
 
*User-Input Required!

EOF

spacer

# check if Docker is installed
if ! command -v docker &>/dev/null; then
	echo "Docker could not be found"
	exit 1
fi

# ask user if they want to rebuild the Docker image
read -p "Do you want to rebuild the Docker image? (Y/n): " rebuild_response
case "$rebuild_response" in
[yY][eE][sS] | [yY])
	echo "Building the Docker image..."
	docker build -t klinux . || {
		echo "Docker build failed"
		exit 1
	}
	;;
*)
	echo "Skipping Docker build..."
	;;
esac

spacer

# grab stable Zaproxy Docker Image
echo "Pulling the zaproxy image..."
docker pull ghcr.io/zaproxy/zaproxy:stable || {
	echo "Failed to pull zaproxy image"
	exit 1
}

spacer

# check if container already exists
if [ "$(docker ps -aq -f name=^klinux$)" ]; then
	# prompt user for action: remove, stop, or exit
	read -p "Container named 'klinux' already exists. Remove old one? (Y/n): " response
	case "$response" in
	[yY][eE][sS] | [yY])
		echo "Removing existing container..."
		docker rm -f klinux
		;;
	*)
		echo "Exiting script"
		exit 1
		;;
	esac
fi

spacer

# run Docker container
echo "Running the Docker container..."
docker run -it -p 8501:8501 --name klinux --privileged -v /var/run/docker.sock:/var/run/docker.sock klinux || {
	echo "Failed to run container"
	exit 1
}

spacer

echo "Setup completed successfully"
