#!/bin/bash

# docker_build_and_run.sh
# Builds the Docker image and runs a smoke test to verify Streamlit starts

set -e

PROJECT_ROOT="/Users/prasadt1/ai-photography-coach-rag"
IMAGE_NAME="photo-coach"
IMAGE_TAG="latest"
CONTAINER_NAME="photo-coach-test"
TIMEOUT=30

echo "🐳 Docker Build & Run Test"
echo "================================"
echo "Project: $PROJECT_ROOT"
echo "Image: $IMAGE_NAME:$IMAGE_TAG"
echo ""

# Check if Dockerfile exists
if [ ! -f "$PROJECT_ROOT/Dockerfile" ]; then
    echo "❌ Dockerfile not found at $PROJECT_ROOT/Dockerfile"
    exit 1
fi

echo "📦 Building Docker image..."
cd "$PROJECT_ROOT"
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✓ Docker image built successfully"
echo ""

# Check if API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  GOOGLE_API_KEY not set. Using placeholder for smoke test."
    GOOGLE_API_KEY="placeholder_key_for_smoke_test"
fi

echo "🚀 Running container..."
# Start container in background
docker run \
    -d \
    --name "$CONTAINER_NAME" \
    -e GOOGLE_API_KEY="$GOOGLE_API_KEY" \
    -p 8501:8501 \
    "$IMAGE_NAME:$IMAGE_TAG" \
    sh -c "python3 -m streamlit run agents_capstone/app_streamlit.py --logger.level=debug" \
    &> /tmp/docker_run.log

CONTAINER_ID=$!

# Wait a bit for container to start
echo "⏳ Waiting for Streamlit to start (max ${TIMEOUT}s)..."
START_TIME=$(date +%s)

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "❌ Timeout: Streamlit did not respond within ${TIMEOUT}s"
        echo ""
        echo "📋 Container logs:"
        docker logs "$CONTAINER_NAME" 2>&1 || true
        docker rm "$CONTAINER_NAME" 2>&1 || true
        exit 1
    fi
    
    # Check if container is running
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        echo "❌ Container exited prematurely"
        echo ""
        echo "📋 Container logs:"
        docker logs "$CONTAINER_NAME" 2>&1 || true
        docker rm "$CONTAINER_NAME" 2>&1 || true
        exit 1
    fi
    
    # Check if port is listening
    if curl -s http://localhost:8501 > /dev/null 2>&1; then
        echo "✓ Streamlit is running on http://localhost:8501"
        break
    fi
    
    sleep 1
done

echo ""
echo "✅ Smoke test passed!"
echo ""
echo "Container is running. To access the app:"
echo "  http://localhost:8501"
echo ""
echo "To stop the container:"
echo "  docker stop $CONTAINER_NAME"
echo "  docker rm $CONTAINER_NAME"
echo ""
echo "To run with real API key:"
echo "  export GOOGLE_API_KEY='your_actual_key'"
echo "  docker run -e GOOGLE_API_KEY=\"\$GOOGLE_API_KEY\" -p 8501:8501 $IMAGE_NAME:$IMAGE_TAG"
