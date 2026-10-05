# --- Build Stage ---
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install git for fetching dependencies.
RUN apk --no-cache add git

# Copy go.mod and go.sum if they exist, to cache dependencies.
# The 'go mod init' will create them if they don't.
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the application source code.
COPY . .

# Initialize module and tidy dependencies. This handles the case where go.mod doesn't exist.
# It also ensures all dependencies are correctly listed.
RUN go mod init go_link && go mod tidy

# Build the Go application.
# -ldflags="-w -s" strips debugging information, creating a smaller binary.
# CGO_ENABLED=0 is important for a static binary.
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-w -s" -o /app/redirector .

# --- Final Stage ---
FROM alpine:latest

WORKDIR /app

# Copy the compiled binary from the build stage.
COPY --from=builder /app/redirector .

# Copy the redirects configuration file.
COPY redirects.yaml .

# Expose the port the server will run on.
EXPOSE 8080

# Set the command to run the application.
CMD ["./redirector"]
