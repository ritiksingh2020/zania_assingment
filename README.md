# E-Commerce Platform RESTful API

## Overview

This project is a production-grade RESTful API for a simple e-commerce platform built with FastAPI. It allows users to view available products, add new products, and place orders. The application includes comprehensive testing, exception handling, and is containerized using Docker for easy deployment.

## Features

- **View Products:** Retrieve a list of all available products.
- **Add Products:** Add new products with details like name, description, price, and stock quantity.
- **Place Orders:** Place orders for selected products with stock validation.
- **Exception Handling:** Graceful error responses for various error scenarios.
- **Testing:** Unit and integration tests to ensure reliability.
- **Dockerized:** Easy deployment using Docker.

## Technology Stack

- **Programming Language:** Python 3.11
- **Web Framework:** FastAPI
- **Database:** SQLite (default)
- **ORM:** SQLAlchemy
- **Testing Framework:** pytest
- **Containerization:** Docker

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/ritiksingh2020/zania_assingment.git
cd ecommerce-api
```

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate  # For Linux/MacOS
.venv\Scripts\activate     # For Windows
pip install -r requirements.txt  # to install requirements
uvicorn app.main:app --host 0.0.0.0 --port 8000 # to run the server
pytest # to run the testcases
```

## Run with docker

``` bash
Build the Docker Image:
docker build -t ecommerce-api .

Run the Docker Container:
docker run -d -p 8000:8000 --name ecommerce-api ecommerce-api

Run Tests Inside Docker:
docker exec -it ecommerce-api pytest
```

