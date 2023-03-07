# ChatGPT Web [Demo](https://simplegpt.io)

<div style="font-size: 1.5rem;">
  <a href="./README.md">中文</a> |
  <a href="./README.en.md">English</a>
</div>
</br>

![cover3](./docs/c3.png)
![cover](./docs/c1.png)
![cover2](./docs/c2.png)

- [ChatGPT Web](#chatgpt-web)
	- [Introduction](#Introduction)
	- [Fast Deployment](#Fast Deployment)
	- [Development Environment Setup](#Development Environment Setup)
		- [Node](#Node)
		- [PNPM](#PNPM)
		- [Python](#Python)
	- [Starting the Project in Development Environment](#Starting the Project in Development Environment)
		- [Backend](#Backend)
		- [Frontend](#Frontend)
	- [Building Docker Containers](#Building Docker Containers)
		- [Frontend Build](#Frontend Build)
		- [Backend Build](#Backend Build)
	- [Starting with Docker Compose](#Starting with Docker Compose)
		- [Starting with DockerHub](#Starting with DockerHub)
		- [FAQ](#FAQ)
		- [Build](#Build)
		- [Support](#Support)
		- [License](#license)

## Introduction

The `ChatGPT Web` page can be deployed on your own server, forked and modified
from [Chanzhaoyu/chatgpt-web](https://github.com/Chanzhaoyu/chatgpt-web/)，It uses the official OpenAI API to connect to
the `gpt-3.5-turbo` model to achieve a conversation effect similar to `ChatGPT Plus`.

Compared to the paid version `ChatGPT Plus` provided by OpenAI, `ChatGPT Web` has the following advantages:

1. **Can help you save money**. You can experience almost the same conversation service as `ChatGPT Plus` for about 10% of the cost.
	 For daily learning and work use, you don't need to spend $20 per month to purchase the Plus service. The usage cost
	 of `ChatGPT Web` page to connect to the API by yourself is about 1/10 of `ChatGPT Plus`.
2. **Easy to share**. You can share your own `ChatGPT Web` site with family and friends, and they no longer need to go
	 through the tedious process of "solving network problems"-"logging in"-"entering passwords"-"selecting captchas" to
	 easily enjoy the productivity improvement brought by `ChatGPT Plus`.

Compared to the [original version of Chanzhaoyu](https://github.com/Chanzhaoyu/chatgpt-web/), the differences are:

1. Can recognize voice messages: achieved by integrating the `whisper-1` API.
2. Can fine-tune parameters: by adjusting settings, you can save token consumption and improve the accuracy of ChatGpt's
	 responses.
3. ChatGpt now remembers more context: chat records are persistently stored on the server.
4. Removed `ChatGPTUnofficialProxyAPI` and reverse proxy functionality: to ensure stability, we encourage the use of
	 ChatGpt through forward proxies and the official API.

Other updates:

1. Random avatar generation is now available.
2. Added a Japanese interface.
3. Improved the mobile experience.
4. The backend has been rewritten in Python (because I can't use Node.js).

## Fast Deployment

If you don't need to develop, and just want to deploy and use, you can skip
to [Starting with DockerHub](#Starting with DockerHub)

## Development Environment Setup

### Node

`node` version `^16 || ^18` is required (`node >= 14` needs to
install [fetch polyfill](https://github.com/developit/unfetch#usage-as-a-polyfill)），You can manage multiple `node`
versions on your local machine using [nvm](https://github.com/nvm-sh/nvm)

```shell
node -v
```

### PNPM

If you don't have `pnpm`

```shell
npm install pnpm -g
```

### Python

The `python` version needs to be `3.10` or higher. go to the `/service` folder and run the following command:

```shell
pip install --no-cache-dir -r requirements.txt
```

## Starting the Project in Development Environment

### Backend

Only `OPENAI_API_KEY` must required, you need to register an account on [OpenAI](https://platform.openai.com/) and
obtain your API key [here](https://platform.openai.com/account/api-keys)

```shell
# You can run the following command in the /service directory:
python main.py --openai_api_key="$OPENAI_API_KEY" --api_model="$API_MODEL" --socks_proxy="$SOCKS_PROXY" --host="$HOST" --port="$PORT"
# The default port number for the backend service is 3002, which can be modified using the --port parameter.
```

### Frontend

Run the following command in the root directory.

```shell
# The default port for the frontend web page is 1002 and the default port for the backend service is 3002. You can modify them in the .env and .vite.config.ts files.
pnpm bootstrap
pnpm dev
```

## Building Docker Containers

### Frontend Build (Requires Node, Docker, and Docker Compose)

1. Run the following command at the root of the project:

	```shell
	pnpm run build
	```


2. Copy the built `dist` folder to `/docker-compose/nginx` and rename it to `html`:

	```shell
	cp dist/ docker-compose/nginx/html -r
	```

3. Edit the `/docker-compose/nginx/nginx.conf` file and replace the server_name with **your server IP**.

4. Run the following command at `/docker-compose/nginx`:

	```shell
	 docker build -t chatgpt-web-frontend .
	```


### Backend Build

1. Enter the `/service` directory and run the following command

	```shell
	docker build -t chatgpt-web-backend .
	```

### Starting with Docker Compose

- Go to the folder `/docker-compose` and modify the `docker-compose.yml` file

	```
  version: '3'
  services:
    app:
      image: chatgpt-web-backend # the name of your backend service image here
      ports:
        - 3002:3002
      environment:
        OPENAI_API_KEY: your_openai_api_key
        # Optional, default value is gpt-3.5-turbo
        API_MODEL: gpt-3.5-turbo
        # Socks proxy, optional, format is http://127.0.0.1:10808
        SOCKS_PROXY: xxxx
        # HOST, optional, default value is 0.0.0.0
        HOST: 0.0.0.0
        # PORT, optional, default value is 3002
        PORT: 3002
    nginx:
      build: nginx
      image: chatgpt-web-frontend # the name of your frontend service image here
      ports:
        - '80:80'
      expose:
        - '80'
      volumes:
        - ./nginx/html/:/etc/nginx/html/
      links:
        - app
	```

- Go to the folder `/docker-compose` and run:

	```shell
	docker-compose up
	# or
	docker-compose up -d
	```

## Starting with DockerHub

- If you don't want to package the image yourself, you can directly use the image I have already packaged.

- First, you still need to package the frontend resources yourself. Let's review the process:
	1.  install nodejs `^16 || ^18`
	2. `npm install pnpm -g`
	3. `pnpm bootstrap`
	4. `pnpm run build`

- And then copy the packaged dist folder to the `./docker-compose/nginx` directory, and rename it to `html`.
  ```shell
	cp dist/ docker-compose/nginx/html -r
	```
- Then modify the `./docker-compose/docker-compose.yml` file.

	Other than filling in the `OPENAI_API_KEY`, you also need to modify the tag of the image according to your system environment.

	```
	version: '3'

	services:
	  app:
      # According to your system, choose either x86_64 or aarch64.
      image: wenjing95/chatgpt-web-backend:x86_64
      # image: wenjing95/chatgpt-web-backend:aarch64
      ports:
        - 3002:3002
      environment:
        # Remember to fill in your OPENAI_API_KEY.
        OPENAI_API_KEY: your_openai_api_key
        # Optional, with a default value of gpt-3.5-turbo.
        API_MODEL: gpt-3.5-turbo
        # Socks proxy, optional, format as http://127.0.0.1:10808.
        SOCKS_PROXY: “”
        # HOST, optional, with a default value of 0.0.0.0.
        HOST: 0.0.0.0
        # PORT, optional, with a default value of 3002.
        PORT: 3002
    nginx:
      build: nginx
      # According to your system, choose either x86_64 or aarch64.
      image: wenjing95/chatgpt-web-frontend:x86_64
      # image: wenjing95/chatgpt-web-frontend:aarch64
      ports:
        - '80:80'
      expose:
        - '80'
      volumes:
        - ./nginx/html/:/etc/nginx/html/
      links:
        - app
	```

- Go to the folder `/docker-compose` and run:

	```shell
	docker-compose up
	# or
	docker-compose up -d
	```

## FAQ

Q: Why do I always get errors when committing to git？

A: There is a commit message validation, please follow the [Commit Guidelines](./CONTRIBUTING.md)

Q: If I only use the front-end page, where can I change the request interface?

A: In the `.env` file in the root directory, modify the `VITE_GLOB_API_URL` field.

Q: Why is the typing effect not working in the front-end?

A: For vscode, please install the recommended plugins of the project, or manually install the Eslint plugin.

Q: Why there is no typewriter effect in the frontend?

A: One possible reason is that when going through the Nginx reverse proxy, buffering is enabled, so Nginx will try to
buffer a certain amount of data from the backend before sending it to the browser. Try adding proxy_buffering off; after
the reverse proxy parameters and then reloading Nginx. The same applies to other web server configurations.

Q: Why is the recording function not working?

A: The recording function requires a secure HTTPS environment. It is recommended to use Cloudflare's free HTTPS
certificate.

Q: When building the Docker container, get the error message "exec entrypoint.sh: no such file or directory".

A: This error can occur if the entrypoint.sh file was created using an IDE with CRLF line endings instead of LF. To fix this, you can use the dos2unix tool to convert the line endings from LF to CRLF.

## Build

Thank you to the original author [Chanzhaoyu](https://github.com/Chanzhaoyu/chatgpt-web/) and all the contributors, as
well as the productivity tools `ChatGpt` and `Github Copilot`!

<a href="https://github.com/Chanzhaoyu/chatgpt-web/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Chanzhaoyu/chatgpt-web" />
</a>

## Support

If you find this project helpful, please give it a star.

If possible, please support the original author [Chanzhaoyu](https://github.com/Chanzhaoyu/chatgpt-web/)

## License

MIT © [WenJing95](./license)


> This document was translated by chatgpt
