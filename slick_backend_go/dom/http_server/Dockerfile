# Start from a Debian-based image with the latest version of Go installed
FROM golang:latest

# Set the Current Working Directory inside the container
WORKDIR /app/dom
# # Copy go mod and sum files
# COPY go.mod ../
# COPY go.sum ../
# COPY ../proto/gen/pb-go/slick_backend_go/proto/*.go ../
# # Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
# RUN go mod download

# Copy the source code into the container
#COPY ../proto/gen/pb-go/slick_backend_go/*.go /app
COPY proto/ /app/proto
COPY dom/ /app/dom
COPY go.mod /app/
COPY go.sum /app/

# Build the Go app
# RUN cd /app/dom/
RUN go build -o main .

# Command to run the executable
CMD ["./main"]
# CMD ["ls .."]
# ENTRYPOINT ["tail", "-f", "/dev/null"]


