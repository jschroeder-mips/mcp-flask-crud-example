#!/bin/bash
#
# Futurama Quotes MCP Server Launcher
# ===================================
#
# This script launches the Futurama Quotes MCP server using a pre-configured
# Python virtual environment. 
#
# Prerequisites (run the setup tutorial first):
#   - Python virtual environment at .venv/
#   - All dependencies installed in the virtual environment
#   - Flask API server running (optional, but recommended)
#
# Usage:
#   ./run_mcp_server.sh
#
# Author: GitHub Copilot
# License: MIT

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="${SCRIPT_DIR}"
readonly VENV_PYTHON="${PROJECT_ROOT}/.venv/bin/python"
readonly MCP_SERVER_SCRIPT="${PROJECT_ROOT}/mcp_server/server.py"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Simple validation
validate_setup() {
    if [[ ! -f "${VENV_PYTHON}" ]]; then
        log "ERROR: Python virtual environment not found at: ${PROJECT_ROOT}/.venv/"
        log "Please run the setup tutorial first - see README.md"
        exit 1
    fi

    if [[ ! -f "${MCP_SERVER_SCRIPT}" ]]; then
        log "ERROR: MCP server script not found at: ${MCP_SERVER_SCRIPT}"
        exit 1
    fi
}

# Main execution
main() {
    log "Starting Futurama Quotes MCP Server"
    
    # Change to project directory
    cd "${PROJECT_ROOT}"
    
    # Validate setup
    validate_setup
    
    log "Using Python: ${VENV_PYTHON}"
    log "Python version: $(${VENV_PYTHON} --version 2>/dev/null || echo 'Unable to determine')"
    
    # Launch the MCP server using the virtual environment Python
    log "Launching MCP server..."
    exec "${VENV_PYTHON}" "${MCP_SERVER_SCRIPT}"
}

# Handle script interruption gracefully
trap 'log "MCP server interrupted"; exit 130' INT TERM

# Run main function
main "$@"
