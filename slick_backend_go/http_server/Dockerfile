# Start from a Debian-based image with the latest version of Go installed
FROM golang:latest

# Set the Current Working Directory inside the container
WORKDIR /app/http_server

COPY go.mod /app/
COPY go.sum /app/
RUN go mod download

# Copy the source code into the container
COPY proto/ /app/proto
COPY http_server/ /app/http_server
EXPOSE 8080
# Build the Go app
# RUN cd /app/dom/
RUN go build -o main .

# Command to run the executable
CMD ["./main"]


