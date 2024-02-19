# Start from a Debian-based image with the latest version of Go installed
FROM golang:latest

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod .
COPY go.sum .

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code into the container
COPY *.go ./
COPY ./messages/*.go src/

# Build the Go app
RUN go build -o main .

# Command to run the executable
CMD ["./main"]
