# Docker Tips and Tricks 

## Run a container with name and ports 
docker run --name blue-app -p 38282:8080 kodekloud/simple-webapp:blue

## Most Common Docker Commands

*   **`docker run`**: Creates and starts a new container from an image. You can specify options like running in detached mode (`-d`), mapping ports (`-p`), and setting environment variables (`-e`).
*   **`docker pull <image>`**: Downloads a Docker image from a registry like Docker Hub. If no tag is specified, it defaults to `:latest`.
*   **`docker ps`**: Lists running containers. Use `docker ps -a` to show all containers, including stopped ones.
*   **`docker stop <container>`**: Stops one or more running containers.
*   **`docker start <container>`**: Starts one or more stopped containers.
*   **`docker restart <container>`**: Restarts a container.
*   **`docker exec -it <container> <command>`**: Executes a command inside a running container. The `-it` flags provide an interactive terminal.
*   **`docker logs <container>`**: Displays the logs of a container, useful for troubleshooting.
*   **`docker build -t <image_name> .`**: Builds a Docker image from a Dockerfile in the current directory. The `-t` flag tags the image with a name.
*   **`docker images`**: Lists all local Docker images.
*   **`docker rmi <image>`**: Removes one or more Docker images.
*   **`docker commit <container> <new_image_name>`**: Creates a new image from a container's changes.
*   **`docker login`**: Logs in to a Docker registry.
*   **`docker push <image>`**: Pushes an image to a configured registry.
*   **`docker network`**: Commands for managing Docker networks (e.g., `create`, `connect`, `ls`).
*   **`docker volume`**: Commands for managing Docker volumes (e.g., `create`, `ls`, `rm`), used for persistent data.
*   **`docker info`**: Displays system-wide information about Docker.
*   **`docker --version`**: Shows the Docker version installed.

## Docker Tips and Tricks

*   **Optimize Dockerfiles for Caching**: Arrange instructions in your Dockerfile so that frequently changing commands are placed lower down. This allows Docker to reuse cached layers for the stable parts of your build, significantly speeding up build times.
*   **Use Multi-Stage Builds**: Separate your build environment from the runtime environment within the same Dockerfile. This reduces the final image size and minimizes the attack surface by excluding unnecessary build tools and files from the production image.
*   **Choose Minimal Base Images**: Opt for lightweight base images like Alpine Linux or Distroless instead of full operating system images (e.g., Ubuntu, Debian). These images have fewer packages, which reduces the attack surface and improves performance.
*   **Use `.dockerignore`**: Similar to `.gitignore`, a `.dockerignore` file excludes unnecessary files and directories from the build context sent to the Docker daemon. This speeds up the build process and keeps image sizes smaller.
*   **Minimize Layers**: Each command in a Dockerfile creates a new layer. Combine multiple commands into a single `RUN` instruction using `&&` to reduce the number of layers and image size.
*   **Run Containers as Non-Root Users**: Avoid running containers as the root user to enhance security. Create a non-root user in your Dockerfile.
*   **Use Volumes for Persistent Data**: For data that needs to persist beyond the container's lifecycle, use Docker volumes. They are stored outside the container's filesystem and can be shared among containers.
*   **Use Docker Compose for Multi-Container Applications**: For applications with multiple services, Docker Compose simplifies the management of interconnected containers.
*   **Pin Base Image Versions**: Always specify exact versions of base images and dependencies (e.g., `ubuntu:22.04` instead of `ubuntu:latest`) to ensure consistency and reproducibility.
*   **Scan Images for Vulnerabilities**: Regularly scan your Docker images for security vulnerabilities using tools like Trivy, Clair, or Snyk.
*   **Automate Workflow with CI/CD**: Integrate Docker into your Continuous Integration/Continuous Deployment pipelines to automate builds, tests, and deployments.
*   **Squashing Image Layers**: This technique reduces the number of layers in your Docker images by merging them into one, which can help minimize the image size.