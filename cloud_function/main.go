package main

import (
	"bytes"
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"strings"

	"cloud.google.com/go/firestore"
	"cloud.google.com/go/storage"
	vision "cloud.google.com/go/vision/apiv1"
)

// GCSEvent is the payload of a GCS event. Please refer to the docs for
// additional information regarding GCS events.
type GCSEvent struct {
	Bucket string `json:"bucket"`
	Name   string `json:"name"`
}

func GCStoOCR(ctx context.Context, e GCSEvent) error {
	log.Printf("Processing file: %s", e.Name)
	pathes := strings.Split(e.Name, "/")
	user_id := pathes[0]
	group_id := pathes[1]
	file_name := pathes[2]

	// create storage client
	client, err := storage.NewClient(ctx)
	if err != nil {
		return fmt.Errorf("storage.NewClient: %v", err)
	}
	defer client.Close()

	// get image from GCS
	rc, err := client.Bucket(e.Bucket).Object(e.Name).NewReader(ctx)
	if err != nil {
		return fmt.Errorf("Object(%q).NewReader: %v", e.Name, err)
	}
	defer rc.Close()
	b, err := ioutil.ReadAll(rc)
	if err != nil {
		return fmt.Errorf("ioutil.ReadAll: %v", err)
	}
	
	// use vision API to extract text from image
	annotationClient, err := vision.NewImageAnnotatorClient(ctx)
	if err != nil {
		return fmt.Errorf("NewImageAnnotatorClient: %v", err)
	}
	defer annotationClient.Close()
	image, err := vision.NewImageFromReader(bytes.NewReader(b))
	if err != nil {
		return fmt.Errorf("NewImageFromReader: %v", err)
	}
	annotations, err := annotationClient.DetectTexts(ctx, image, nil, 10)
	if err != nil {
		return fmt.Errorf("DetectTexts: %v", err)
	}
	log.Printf("Extracted text: %q", annotations[0].Description)

	// create image path and text to Firestore
	projectID := "test-gke-360717"
	firestoreClient, err := firestore.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer firestoreClient.Close()
	// NOte: set() will overwrite the document if it already exists. or create document if it doesn't exist.
	_, err = firestoreClient.Collection(user_id).Doc(group_id).Set(ctx,
		map[string]interface{}{
		"title": file_name,
		"path": e.Name,
		"text": annotations[0].Description,
	})

	return nil
}

func main(){
	log.Print("Hello World")
}