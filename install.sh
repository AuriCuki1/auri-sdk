#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=========================================="
echo "   Installing Auri SDK for Termux..."
echo "=========================================="

# 1. Ensure dependencies are installed
echo "[1/4] Checking Python and Git..."
pkg update -y -q
pkg install -y -q python git

# 2. Clone or update the SDK repository
INSTALL_DIR="$HOME/.auri-sdk"
echo "[2/4] Downloading Auri SDK to $INSTALL_DIR..."
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi
git clone -q https://github.com/AuriCuki1/auri-sdk.git "$INSTALL_DIR"

# 3. Create the global 'auri' command in $PREFIX/bin
echo "[3/4] Setting up global 'auri' command..."
BIN_PATH="$PREFIX/bin/auri"
cat << 'WRAPPER' > "$BIN_PATH"
#!/data/data/com.termux/files/usr/bin/bash
export AURI_HOME="$HOME/.auri-sdk"
python "$AURI_HOME/auri.py" "$@"
WRAPPER
chmod +x "$BIN_PATH"

# 4. Run the core benchmark test to verify
echo "[4/4] Running core verification test..."
if [ -f "$INSTALL_DIR/core_test.auri" ]; then
    auri "$INSTALL_DIR/core_test.auri"
fi

echo "=========================================="
echo "   Auri SDK Installed Successfully! "
echo "   Usage: auri <your_script.auri>"
echo "=========================================="
