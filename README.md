# 1. Deployment instructions

## 1.1. Deploy with Docker

Make sure [Docker](https://docs.docker.com/get-docker/) is installed. Then, in the folder where this _README.md_ file is, run:

```bash
docker build -t url_shortener_image .
```

This creates the Docker Image for the URL Shortener. After this, you can run the container by writing:

```bash
docker run -d --name url_shortener_container -p 8000:8000 url_shortener_image
```

## 1.2.- Deploy without virtualization

To deploy it without virtualization, you should follow the following steps. First, you should make sure you have Python 3.11.0 installed, as it is the version on which this implementation was tested (you can use conda for this). Then, open a terminal in the folder where this _README.md_ file is situated, and create a virtual environment to install the dependencies:

**Windows**

```bash
python -m venv <env_name>
.\<env_name>\Scripts\activate
```

**Linux + macOS**

```bash
python3 -m venv <env_name>
source <env_name>/bin/activate
```

Then, install the python libraries:

```bash
pip install -r requirements.txt
```

Finally, deploy the app:

```bash
uvicorn shortener_app.main:app
```

# 2. Interact with app

Following the previous sections instructions, will deploy the app on [**http://127.0.0.1:8000/**](http://127.0.0.1:8000/). To explore the automatically generated documentation for the endpoints, as well as testing the functionality (except the redirection feature), go to [**http://127.0.0.1:8000/docs**](http://127.0.0.1:8000/docs).

# 3. Test

To test the app with the pytest app, you have to activate the environment created in **1.2**, go to the _shortener_app_ directory and run

```bash
pytest
```
