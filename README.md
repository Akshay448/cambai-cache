# Camb AI - Backend/Infrastructure Engineer Challenge

**Develop a key-value store using Kubernetes (k8s), FastAPI, 
and Huey as a REDIS queue that can scale reliably across multiple pods/deployments**

## Getting Started

To keep things simple and get started using the key value store
1. Clone the repository to your local machine.
2. Ensure Docker Desktop is installed with Kubernetes enabled.
3. Execute the deployment script to apply Kubernetes configurations: `$ ./deploy.sh`.
4. Import the provided [Postman collection](Cambiai-cache.postman_collection.json) in postman client to interact with the key-value store endpoints.


# INDEX
1. [Project Structure](#project-structure)
2. [Building Image and Running with Kubernetes](#building-image-and-running-with-kubernetes)
3. [Components Used in the System](#components-used-in-the-system)
4. [Architecture Diagram (HLD)](#architecture-diagram-hld)
5. [Implementation Ideas for Scalability and Robustness](#implementation-ideas-for-scalability-and-robust-system-)
6. [Code Implementation (LLD)](#code-implementation-lld)

## Project Structure

- **/cambai-cache/**
  - **/kubernetes/**: Contains Kubernetes deployment and service configurations.
    - `fastapi-deployment.yaml`: Deployment for FastAPI app, pulling a pre-built Docker image.
    - `fastapi-service.yaml`: Exposes FastAPI endpoints over localhost through a LoadBalancer.
    - `huey-worker-deployment.yaml`: Initializes Huey workers for task processing.
    - `redis-huey-deployment.yaml`: Deploys a Redis instance for Huey's task queue.
    - `redis-huey-service.yaml`: Exposes Redis port for Huey.
    - `redis-kv-deployment.yaml`: Deploys a Redis instance for the key-value store.
    - `redis-kv-service.yaml`: Exposes Redis port for the key-value store.
  - `deploy.sh`: Script to deploy all Kubernetes components.
  - `Dockerfile`: Containerizes the FastAPI endpoints.
  - `huey_config.py`: Defines tasks for the Huey queue.
  - `main.py`: FastAPI endpoints and Redis connection initialization.
  - `README.md`: Project documentation.

## Building image and running with kubernetes

### Prerequisites - Docker desktop installed and kubernetes enabled
1. (Optional) Build and push the Docker image if modifications are made:
```bash
docker build -t <your-dockerhub-username>/redis-huey-app .
docker push <your-dockerhub-username>/redis-huey-app
```
2. Enable Kubernetes in Docker Desktop and wait for initialization.
3. Optional commands to make sure kubernetes is working
```bash
kubectl config use-context docker-desktop
kubectl config get-contexts 
```
4. Once the kubernetes is up and running, run the below command from root directory 
```bash
chmod +x deploy.sh
.deploy.sh
```
5. Use Postman to interact with the API endpoints provided in the [collection](Cambiai-cache.postman_collection.json).

## Components Used in the system
* FastAPI: For creating RESTful endpoints.
* Huey: As a task queue with Redis for asynchronous task processing.
* Redis: Two instances used, one for key value store and other for huey task queue.
* Kubernetes: For orchestrating and scaling the deployments across multiple pods.

## Architecture diagram (HLD)
Find the architecture diagram here at - [cambi-cache-draw](https://drive.google.com/file/d/1MdwTCM_XtEvDMn5jXlZEtqE2KzUkwPT3/view?usp=sharing)

![cambai-cache](https://github.com/Akshay448/cambai-cache/assets/30473155/26fcd9bf-7621-4e51-af37-6b18bae49e0d)


## Implementation ideas for scalability and robust system 

### Notes for task queue and workers
a task queue interacting with multiple workers for efficient workload distribution
1. task queue setup - huey with redis, different processes send tasks to queue
2. workers subscribe - workers listen or poll to queue for tasks, many workers
3. tasks distribution - round robin, random, least busy, categories of tasks
4. with kubernetes HPA, workers can scale based on certain metrics
5. fault tolerance - if a task fails, task returns to the queue or to dead letter queue
6. rate limiting - to prevent too much load on workers
7. task prioritization
8. The Redis instance serves as the storage and messaging system for Huey's tasks

### Scaling redis instances
1. redis needs data persistance, replication, has a stateful nature
2. statefulset deployment for redis for persistent data storage
3. pvcs - to persists data even when pod crashes or restarts
4. redis cluster - multiple nodes, gives high availability
5. redis sentinal - master slave setup, has more read capacity
6. use prometheus and grafana for monitoring
7. redis operator - helps to manage the redis cluster

### huey and fastapi deployments and services
1. stateless pods can be scaled independently with given number of replicas
2. using hpa to scale based on cpu or memory use
3. use readiness and liveness probes so that request goes to healthy pods

### More notes
* Microservices Architecture: separating the FastAPI application, Huey workers, and Redis into distinct service. each component can be scaled independently
* Asynchronous Processing with Huey: To ensure the FastAPI application remains responsive, heavy operations are offloaded to Huey. This reduces the API's latency, especially under heavy load, by not blocking client requests.
* Containerization with Docker: huey and fastapi endpoints


## Code Implementation (LLD)
The project's code is mostly covered in main.py and huey_config.py

**Pydantic Model for Data Validation**
  * KeyValue Model: Pydantic for data validation through the KeyValue class. 
  * This class defines the structure of the key-value pairs, with key and value as required fields.
  * Help with data validation at the api layer

**Try catch for error handling**
  * Error Handling in Tasks: Each Huey task 
  * (create_key_with_huey, update_key_with_huey, delete_key_with_huey) within huey_config.py incorporates try-catch blocks to handle exceptions, particularly RedisError

**Retries**
  * Retry Logic in Reading: The read_key function in main.py employs the retry decorator from tenacity.

**Dependency Injection for Flexibility and Testing**
  * Redis Client as a Dependency: use of FastAPI's dependency injection feature to provide a Redis client (get_redis_client) for interacting with the Redis key-value store.












