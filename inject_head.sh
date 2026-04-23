#!/bin/bash

# Find Streamlit's index.html in site-packages
STREAMLIT_INDEX=$(python -c "import streamlit; import os; print(os.path.join(os.path.dirname(streamlit.__file__), 'static', 'index.html'))")

echo "Found Streamlit index at: $STREAMLIT_INDEX"

# Inject AdSense script into <head>
sed -i 's|<head>|<head><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4881378862565200" crossorigin="anonymous"></script>|' "$STREAMLIT_INDEX"

echo "AdSense injected successfully!"