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

# MAIN FUNCTION CALLS

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
