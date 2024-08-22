# colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

format_bash() {
	local path="$1"

	# reformat a single file
	reformat_file() {
		local file_path="$1"
		if shfmt -w "$file_path"; then
			echo -e "${YELLOW}Reformatted:${NC} $file_path"
		else
			echo -e "${RED}Error formatting:${NC} $file_path"
		fi
	}

	# reformat all .sh and .zsh files in a directory
	reformat_shell_scripts() {
		local directory="$1"
		find "$directory" -type d -name "node_modules" -prune -o -type f \( -name "*.sh" -o -name "*.zsh" \) -print | while read -r file; do
			reformat_file "$file"
		done
	}

	echo -e "${BLUE}Formatting Bash/Zsh files in directory:${NC} $path"

	if [[ -d "$path" ]]; then
		reformat_shell_scripts "$path"
	elif [[ -f "$path" ]]; then
		if [[ "$path" == *.sh || "$path" == *.zsh ]]; then
			reformat_file "$path"
		else
			echo -e "${RED}Error: File '$path' is not a .sh or .zsh file.${NC}"
			return 1
		fi
	else
		echo -e "${RED}Error: Path '$path' does not exist.${NC}"
		return 1
	fi
}

format_python() {
	local path="$1"

	echo -e "${BLUE}Formatting Python files in directory:${NC} $path"

	if [[ -d "$path" ]]; then
		black "$path"
	elif [[ -f "$path" && "$path" == *.py ]]; then
		echo -e "${BLUE}Formatting Python file:${NC} $path"
		black "$path"
	else
		echo -e "${RED}Error: Path '$path' is not a Python file or directory.${NC}"
		return 1
	fi
}

format_javascript() {
	local path="$1"

	echo -e "${BLUE}Formatting JavaScript/JSON/Markdown files in directory:${NC} $path"

	if [[ -d "$path" ]]; then
		prettier --write "$path/**/*.{js,json,md,jsx,html,css}"
	elif [[ -f "$path" && ("$path" == *.js || "$path" == *.json || "$path" == *.md) ]]; then
		echo -e "${BLUE}Formatting file:${NC} $path"
		prettier --write "$path"
	else
		echo -e "${RED}Error: Path '$path' is not a JavaScript, JSON, or Markdown file or directory.${NC}"
		return 1
	fi
}

spacer() {
	echo
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo
}

env_check() {
	if [ -f .env ]; then
		echo "Found .env file. Refer to .template_env if needed"
	else
		echo "File .env not found. Refer to .template_env and create it"
		echo "'''"
		sed '${/^$/d;}' .template_env
		echo "'''"
		exit 1
	fi
}

run() {
	spacer

	echo "RUNNING TARS * User-Input Required!"

	spacer

	# make sure the .env file has been created and set
	env_check

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

	# open URL in the browser to make things easier
	url="http://0.0.0.0:8501"
	if [[ "$OSTYPE" == "darwin"* ]]; then
		open $url
	elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
		if command -v xdg-open >/dev/null; then
			xdg-open $url
		elif command -v gnome-open >/dev/null; then
			gnome-open $url
		else
			echo "No suitable command found to open the URL"
		fi
	fi

	# run Docker container
	echo "Running the Docker container..."
	docker run -it -p 8501:8501 --name klinux --privileged -v /var/run/docker.sock:/var/run/docker.sock klinux || {
		echo "Failed to run container"
		exit 1
	}

	spacer

	echo "Setup completed successfully"
}

format() {
	echo -e "${GREEN}Formatting Bash/Zsh files${NC}"
	if ! command -v shfmt &>/dev/null; then
		echo -e "${RED}Error: shfmt is not installed. You can install it from: ${BLUE}https://github.com/mvdan/sh${NC}"
		exit 1
	fi
	format_bash "$(pwd)"
	echo

	echo -e "${GREEN}Formatting Python files${NC}"
	if ! command -v black &>/dev/null; then
		echo -e "${RED}Error: black is not installed. You can install it from: ${BLUE}https://github.com/psf/black${NC}"
		exit 1
	fi
	format_python "$(pwd)"
	echo

	echo -e "${GREEN}Formatting JavaScript/JSON/Markdown files${NC}"
	if ! command -v prettier &>/dev/null; then
		echo -e "${RED}Error: prettier is not installed. You can install it from: ${BLUE}https://www.npmjs.com/package/prettier${NC}"
		exit 1
	fi
	format_javascript "$(pwd)"
}

show_help() {
	echo "Usage: $0 [-r] [-f]"
	echo "  -r  Run the TARS"
	echo "  -f  Run formatter"
}

# main function calls

if [ $# -eq 0 ]; then
	show_help
	exit 1
fi

while getopts "rfh" opt; do
	case ${opt} in
	r)
		run
		;;
	f)
		format
		;;
	h)
		show_help
		;;
	\?)
		show_help
		exit 1
		;;
	esac
done
