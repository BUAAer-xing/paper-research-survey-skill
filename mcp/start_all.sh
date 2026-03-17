#!/usr/bin/env bash
# 统一启动三个 MCP 服务：arxiv / semantic-scholar / google-scholar

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── 配置 ──
ARXIV_DIR="$SCRIPT_DIR/arxiv-mcp-server"
ARXIV_STORAGE="$ARXIV_DIR/storages"

SEMANTIC_DIR="$SCRIPT_DIR/semantic-scholar-mcp-server"
SEMANTIC_SCHOLAR_API_KEY="${SEMANTIC_SCHOLAR_API_KEY:-}"

GOOGLE_DIR="$SCRIPT_DIR/google-scholar-mcp-server"

# ── 确保 arxiv 存储目录存在 ──
mkdir -p "$ARXIV_STORAGE"

echo "Starting arxiv-mcp-server ..."
uv --directory "$ARXIV_DIR" run arxiv-mcp-server --storage-path "$ARXIV_STORAGE" &
PID_ARXIV=$!

echo "Starting semantic-scholar-mcp-server ..."
SEMANTIC_SCHOLAR_API_KEY="$SEMANTIC_SCHOLAR_API_KEY" \
  uv --directory "$SEMANTIC_DIR" run server.py &
PID_SEMANTIC=$!

echo "Starting google-scholar-mcp-server ..."
uv --directory "$GOOGLE_DIR" run google_scholar_server.py &
PID_GOOGLE=$!

echo ""
echo "All MCP servers started:"
echo "  arxiv-mcp-server        PID=$PID_ARXIV"
echo "  semantic-scholar-mcp    PID=$PID_SEMANTIC"
echo "  google-scholar-mcp      PID=$PID_GOOGLE"
echo ""
echo "Press Ctrl+C to stop all servers."

# 捕获 SIGINT/SIGTERM，统一关闭子进程
cleanup() {
    echo ""
    echo "Stopping all MCP servers ..."
    kill "$PID_ARXIV" "$PID_SEMANTIC" "$PID_GOOGLE" 2>/dev/null
    wait "$PID_ARXIV" "$PID_SEMANTIC" "$PID_GOOGLE" 2>/dev/null
    echo "All servers stopped."
}
trap cleanup SIGINT SIGTERM

wait
