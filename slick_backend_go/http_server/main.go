package main

import (
	"context"
	"fmt"
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
	fmt.Println("Starting http server")
	// Define a handler function for the "/" route
	// mux := http.NewServeMux()
	// mux.HandleFunc("/", entry) // Set a client's cookies here.
	// mux.HandleFunc("/get", getCookieHandler)
	fmt.Println("Dialing grpc server")
	conn, err := grpc.Dial("grpc_service:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))

	if err != nil {
		fmt.Print(err)
	}
	defer conn.Close()

	// Start the HTTP server on port 8080
	// fmt.Println("Server is listening on port 8080...")
	client := pb.NewDOMServerClient(conn)
	id := &pb.ID{
		Id: "Jim",
	}
	server := NewHttpServer(client)
	record, err := client.ReadDb(context.Background(), id)
	if err != nil {
		fmt.Println("Error:", err)
	}
	val := record.GetVal()
	fmt.Println(val)

	//err = http.ListenAndServe(":8080", mux)
	err = server.ListenAndServe()
	if err != nil {
		fmt.Println("Error:", err)
	}
}
