#!/bin/bash
#
# Futurama Quotes System Setup Script
# ===================================
#
# This script sets up everything you need to run the Futurama quotes
# system with AI integration. No special tools required - just Python!
#
# Usage:
#   ./setup.sh
#
# Author: GitHub Copilot  
# License: MIT

set -euo pipefail

# Colors for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[✅]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $*"
}

log_error() {
    echo -e "${RED}[❌]${NC} $*"
}

# Check Python version
check_python() {
    log_info "Checking Python installation..."
    
    if ! command -v python3 >/dev/null 2>&1; then
        log_error "Python 3 is not installed"
        log_info "Please install Python 3.10+ from https://python.org"
        exit 1
    fi
    
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log_success "Found Python ${python_version}"
    
    # Check if version is at least 3.10
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
        log_success "Python version is compatible"
    else
        log_warning "Python 3.10+ recommended, but continuing with ${python_version}"
    fi
}

# Set up virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    cd "${PROJECT_DIR}"
    
    if [[ -d ".venv" ]]; then
        log_info "Virtual environment already exists, using it"
    else
        python3 -m venv .venv
        log_success "Created virtual environment"
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    log_success "Updated pip"
    
    # Install dependencies
    log_info "Installing Python dependencies..."
    pip install -r requirements.txt
    log_success "Installed all dependencies"
    
    # Verify installation
    if python -c "import flask, httpx, mcp; print('Dependencies verified')" >/dev/null 2>&1; then
        log_success "All dependencies working correctly"
    else
        log_error "Dependency verification failed"
        exit 1
    fi
}

# Test Flask API
test_flask() {
    log_info "Testing Flask API setup..."
    
    cd "${PROJECT_DIR}"
    source .venv/bin/activate
    
    # Test import
    if python -c "import futurama_api.app; print('Flask app import OK')" >/dev/null 2>&1; then
        log_success "Flask API can be imported"
    else
        log_error "Flask API import failed"
        exit 1
    fi
}

# Test MCP server
test_mcp() {
    log_info "Testing MCP server setup..."
    
    cd "${PROJECT_DIR}"
    source .venv/bin/activate
    
    # Test import
    if python -c "import mcp_server.server; print('MCP server import OK')" >/dev/null 2>&1; then
        log_success "MCP server can be imported"
    else
        log_error "MCP server import failed"
        exit 1
    fi
    
    # Make launcher executable
    chmod +x run_mcp_server.sh
    log_success "Made MCP launcher executable"
}

# Show next steps
show_instructions() {
    log_success "Setup complete! Here's how to run everything:"
    echo
    echo "📋 STEP 1: Start the Flask API"
    echo "   cd $(pwd)"
    echo "   source .venv/bin/activate"
    echo "   python futurama_api/app.py"
    echo
    echo "📋 STEP 2: Configure Claude Desktop"
    echo "   Add this to your Claude config file:"
    echo 
    echo -e "${BLUE}   {" 
    echo "     \"mcpServers\": {"
    echo "       \"futurama-quotes\": {"
    echo "         \"command\": \"$(pwd)/run_mcp_server.sh\","
    echo "         \"cwd\": \"$(pwd)/\""
    echo "       }"
    echo "     }"
    echo -e "   }${NC}"
    echo
    echo "📋 Config file locations:"
    echo "   • macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
    echo "   • Windows: %APPDATA%/Claude/claude_desktop_config.json" 
    echo "   • Linux: ~/.config/claude/claude_desktop_config.json"
    echo
    echo "📋 STEP 3: Restart Claude Desktop"
    echo
    echo "📋 STEP 4: Test with Claude"
    echo "   Ask: 'Can you list all the Futurama quotes?'"
    echo
    log_info "For detailed instructions, see TUTORIAL.md"
}

# Offer to start Flask API
offer_start_api() {
    echo
    read -p "🚀 Start the Flask API now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Starting Flask API..."
        log_warning "Press Ctrl+C to stop the server when you're done"
        sleep 2
        cd "${PROJECT_DIR}"
        source .venv/bin/activate
        python futurama_api/app.py
    fi
}

# Main setup function
main() {
    echo -e "${GREEN}🚀 Futurama Quotes System Setup${NC}"
    echo "=================================="
    echo
    
    check_python
    setup_venv
    test_flask
    test_mcp
    show_instructions
    offer_start_api
}

# Handle interrupts
trap 'log_warning "Setup interrupted"; exit 130' INT TERM

# Run setup
main "$@"
