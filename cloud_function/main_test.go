package main

import (
	"context"
	"io/ioutil"
	"log"
	"os"
	"testing"

	"cloud.google.com/go/functions/metadata"
)

func TestGCStoOCR(t *testing.T) {
	log.Print("TestGCStoOCR")
	meta := &metadata.Metadata{
		EventID: "event ID",
	}
	ctx := metadata.NewContext(context.Background(), meta)

	type args struct {
		ctx context.Context
		e   GCSEvent
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
	}{
		{
			name:    "SUCCESS",
			args:    args{
				ctx: ctx,
				e:   GCSEvent{
					Bucket: "test-bucket",
					Name:   "user_id/group_id/file_name",
				},
			},
			wantErr: false,
		},
	}
	for _, tt := range tests {
		tt := tt // capture range variable
		t.Run(tt.name, func(t *testing.T) {
			r, w, _ := os.Pipe()
			log.SetOutput(w)
			originalFlags := log.Flags()
			log.SetFlags(log.Flags() &^ (log.Ldate | log.Ltime))
			_, err := ioutil.ReadAll(r)
			if err != nil {
					t.Fatalf("ReadAll: %v", err)
			}
			if err := GCStoOCR(tt.args.ctx, tt.args.e); (err != nil) != tt.wantErr {
				t.Errorf("GCStoOCR() error = %v, wantErr %v", err, tt.wantErr)
			}

			w.Close()
			log.SetOutput(os.Stderr)
			log.SetFlags(originalFlags)
		})
	}
}
