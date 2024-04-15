[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/michaelwnau/codex/streamlit_app.py/)

# Codex

## Overview

This document provides detailed instructions for setting up and running the Codex app using Docker. Codex app is a Streamlit GUI designed for document query, generation, and Retrieval-Augmented Generation (RAG) use cases.

## Prerequisites

Ensure Docker is installed on your machine. If not, you can download it from [Docker's official website](https://www.docker.com/get-started).

## Building the Docker Container

### Clone the Repository

Clone the repository to your local machine with:

```bash
git clone https://github.com/michaelwnau/codex
cd codex
```

### Run the container
`docker build -t codex .`

`docker run -p 8501:8501 codex`

Open a browser to http://localhost:8501
