package main

import (
	"context"
	"fmt"
	"log"
	"net"
	pb "slick_backend_go/proto/gen/pb-go/slick_backend_go/proto"

	"google.golang.org/grpc"
)

type Server struct {
}

func (s *Server) ReadDb(ctx context.Context, id *pb.ID) (*pb.Record, error) {
	return &pb.Record{
		Val: fmt.Sprintf("The Id you gave was: %d", id.Id),
	}, nil
}

func main() {
	lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", 12345))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	fmt.Println("Listening...")
	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)
	pb.RegisterDOMServerServer(grpcServer, &Server{})
	grpcServer.Serve(lis)
}
