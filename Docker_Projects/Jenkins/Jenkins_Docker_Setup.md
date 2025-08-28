# Running Jenkins on Docker

This document describes how to run Jenkins on Docker with persistent data.

## Prerequisites

- Docker must be installed and running on your system.

## Method 1: Using `docker run`

### 1. Run Jenkins Container

Execute the following command to run a Jenkins container in detached mode:

```bash
docker run -d -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Command Breakdown:

- `-d`: Runs the container in detached mode (in the background).
- `-p 8080:8080`: Maps port 8080 on the host to port 8080 in the container (for the Jenkins web interface).
- `-p 50000:50000`: Maps port 50000 on the host to port 50000 in the container (for agent communication).
- `-v jenkins_home:/var/jenkins_home`: Creates a Docker volume named `jenkins_home` and mounts it to the `/var/jenkins_home` directory in the container. This ensures that your Jenkins data persists even if the container is removed.
- `jenkins/jenkins:lts`: The official Jenkins Long-Term Support (LTS) image from Docker Hub.

### 2. Unlock Jenkins

To unlock Jenkins, you need the initial administrator password.

1.  **Get the Container ID:**

    ```bash
    docker ps -q --filter ancestor=jenkins/jenkins:lts
    ```

2.  **Get the Initial Admin Password:**

    Replace `[container_id]` with the ID from the previous command.

    ```bash
    docker logs [container_id]
    ```

    The password will be displayed in the logs, enclosed in a block of asterisks.

### 3. Access Jenkins

Open your web browser and navigate to [http://localhost:8080](http://localhost:8080). Use the password from the previous step to unlock Jenkins and complete the setup.

## Method 2: Using `docker-compose`

Using `docker-compose` is a more manageable way to run Jenkins.

### 1. Create `docker-compose.yml`

Create a file named `docker-compose.yml` with the following content:

```yaml
version: '3.8'
services:
  jenkins:
    image: jenkins/jenkins:lts
    privileged: true
    user: root
    ports:
      - 8080:8080
      - 50000:50000
    container_name: jenkins
    volumes:
      - jenkins_home:/var/jenkins_home

volumes:
  jenkins_home:
```

### 2. Start Jenkins

Run the following command to start Jenkins in the background:

```bash
docker-compose up -d
```

### 3. Unlock Jenkins

The process for getting the initial administrator password is the same as before. You can get it from the container's logs:

```bash
docker logs jenkins
```

### 4. Access Jenkins

Open your web browser and navigate to [http://localhost:8080](http://localhost:8080). Use the password from the previous step to unlock Jenkins and complete the setup.

### 5. Stop Jenkins

To stop the Jenkins service, run:

```bash
docker-compose down
```