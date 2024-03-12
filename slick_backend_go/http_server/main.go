package main

import (
	"context"
	"fmt"
	"net/http"
	pb "slick_backend_go/proto/gen/pb-go/slick_backend_go/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type Server struct {
}

func (s *Server) ReadDb(ctx context.Context, id *pb.ID) (*pb.Record, error) {
	return &pb.Record{
		Val: fmt.Sprintf("The Id you gave was: %d", id.Id),
	}, nil
}

func main() {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("Recovered from err: ", err)
		}
	}()
	fmt.Print("Hello!!")
	// Define a handler function for the "/" route
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello, World!") // Send response to the client

	})
	//var opts []grpc.DialOption
	fmt.Println("Dialing")
	conn, err := grpc.Dial("grpc_service:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))

	if err != nil {
		fmt.Print(err)
	}
	defer conn.Close()

	fmt.Println("Creating client")
	// Start the HTTP server on port 8080
	// fmt.Println("Server is listening on port 8080...")
	client := pb.NewDOMServerClient(conn)
	id := &pb.ID{
		Id: 10,
	}
	fmt.Println("Sending req")
	record, err := client.ReadDb(context.Background(), id)
	if err != nil {
		fmt.Println("Error:", err)
	}
	val := record.GetVal()
	fmt.Println(val)

	err = http.ListenAndServe("localhost:8080", nil)
	if err != nil {
		fmt.Println("Error:", err)
	}
}
