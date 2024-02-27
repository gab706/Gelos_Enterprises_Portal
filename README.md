# Gelos Enterprises Portal

An assignment I had to create for my Certificate 3 in IT at Tafe NSW.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using Docker](#using-docker)
  - [Using Python](#using-python)
- [License](#license)

## Prerequisites

Ensure you have the following installed on your machine:

- Docker (if using Docker)
- Python 3.x (if running without Docker)

## Installation

Clone the repository to your local machine:

```shell
git clone https://github.com/gab706/Gelos_Enterprises_Portal.git
cd Gelos_Enterprises_Portal
```

## Using Docker

Build and run the Docker image:

```shell
docker build -t gelos_enterprises_portal .
docker run -p 4000:80 gelos_enterprises_portal
```

## Using Python

Create a virtual environment:

```shell
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:
```shell
.\venv\Scripts\activate
```

- On MacOS:
```shell
source venv/bin/activate
```

Run the application:

```shell
python3 src/main.py
```

## License
This project is licensed under MIT 2024 - see the LICENSE file for details.