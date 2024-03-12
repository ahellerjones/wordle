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
	fmt.Println("Got the request from grpc!")
	return &pb.Record{
		Val: fmt.Sprintf("The Id you gave was: %d", id.Id),
	}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)
	fmt.Println("Created server ...")
	pb.RegisterDOMServerServer(grpcServer, &Server{})
	fmt.Println("Serving cunt...")
	err = grpcServer.Serve(lis)
	if err != nil {
		fmt.Println(err)
	}

}
