# The Caffeinated Odyssey ☕️

## Test Task: The Caffeinated Odyssey

### Objective
Implement a whimsical yet robust HTTP server for our caffeinated haven using **FastAPI**. The goal is to keep things simple—no external services, databases, queues, or buses. This server will support three essential routes, catering to both our caffeine-craving clients and our dedicated baristas.

### Routes
- **/order/** - Where our beloved clients demand their americano.
- **/start/** - Where baristas begin crafting the magic brew.
- **/finish/** - Where baristas triumphantly declare the coffee ready and summon the client.

---

## The Tale of the Caffeinated Clients

Our clients? Let's just say they're an "interesting" bunch:

- **Single Shot Sensation**: They exclusively drink americano. Variety is not their spice of life.
- **The Perfectionist**: These clients detest HTTP errors. Their motto: "200 or nothing". They're as patient as they are picky—happy to wait indefinitely for their order confirmation at `/order/`.
- **Groupie Gatherings**: They love company! Groups of 100-200 clients are common. But fear not—we only have 10 baristas. Thankfully, our clients' patience knows no bounds.
- **Brewing Time**: Each americano takes **30-60 seconds** to prepare. Perfection takes time!
- **Dual Server Madness**: Our clients are so special that they insist clients and workers interact with different FastAPI servers on separate ports within the same Python application. Eccentric? Absolutely. Unfathomable? Never.
- **The Delusional DDoSer**: There's a peculiar client who orders thousands of americanos in one go. He's crafty but always comes from the same address. It's fine to cut him off after a while—just ensure your regulars stay happy and caffeinated.

---

## Additional Requirements

- **GitHub Repository**: Host your code in a GitHub repository.
- **Deployment Instructions**: Either deploy the service somewhere, provide a Docker file, or offer crystal-clear instructions for setup and execution.
- **Defend Against The Delusional**: The DDoSer is a classic denial-of-service attack from a single IP address. Use Nginx or any other straightforward solution to protect the service.

---

## Example Workflow

1. **Client**: Sends a `POST` request to `/order/` and waits for a `200 OK` response when their Americano is ready.
2. **Worker**: Checks the queue with `GET /start/`, picks up the oldest order, starts making it, and then calls `POST /finish/` once the order is done.
3. **Anti-DDoS**: Implement a rule to block or throttle requests from the mischievous DDoSer's IP address, ensuring regular clients get their brew without delay.

---

# Solution

The application is deployed on an EC2 instance, served by NGINX on port 80, and can be accessed via the following URL:

[http://ec2-16-171-38-125.eu-north-1.compute.amazonaws.com](http://ec2-16-171-38-125.eu-north-1.compute.amazonaws.com)

The API is defined as follows, according to the requirements:

### Customer App:
- **POST** `/order/`

### Barista App:
- **GET** `/start/`
- **POST** `/finish/?order_id=<ORDER_ID>`

The server runs a single-process FastAPI instance, with all data stored in memory (as per the requirements).

In addition to the server and NGINX configuration, the repository includes scripts that simulate the behavior of both a customer and a barista. You can use these scripts to interact with the hosted application over the internet. The scripts are configurable via environment variables.

Details on how to set up the development environment are described in one of the following section.

# Development Setup

1. Create new virtualenv in suitable dir, e.g. `python -m venv ~/.virtualenvs/coffee`
2. Activate venv if not activated: `. ~/.virtualenvs/coffee/bin/activate`
3. Install requirements listed in the repo: `pip install -r ./app/requirements_dev.txt`

### Run server locally

In order to run server locally:

1. Ensure that [Docker is installed](https://docs.docker.com/engine/install/) on your system
2. Navigate to the repository's root directory and execute: `docker compose up --build`
3. Once the containers are up, the server will be accessible at localhost:80

Then you would be able to run the customer and barista scripts:
- `BASE_SERVER_URL=<SERVER_URL> python ./app/client/customer_simulation.py`
- `BASE_SERVER_URL=<SERVER_URL> python ./app/client/barista_simulation.py`

By default, the scripts connect to `localhost`. To point them to a different server, modify the environment variables accordingly.

## Running code formatters and linters

In order to run ruff and mypy one can run:

- `ruff format` - formats the code
- `ruff check . --fix` -  runs configured linters and applies fixes automatically
- `mypy .` - performs static type checking for Python

## Limitations of the solution

The solution is, of course, not how the production grade server ready. 
It lucks some of the functionality that I decided that is beyond the scope of this task,
but would be required for a production server:
- SSL certification and HTTPS traffic to ensure secure communication between server and client 
- Persistent storage for orders (e.g. PostgreSQL, MySQL etc.) 
- Server authorization (e.g. with the use of JWTs)
- Monitoring and alerting for server health and performance (e.g. prometheus and grafana)
- Optionally, a message broker (e.g. Kafka, RabbitMQ)
- Tests (e.g. pytest)
- Additionally, it would be beneficial to have all resources and infrastructure defined as code (IaC) (e.g. terraform) 



