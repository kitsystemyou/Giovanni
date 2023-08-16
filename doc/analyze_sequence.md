Analyze Flow

```mermaid
sequenceDiagram
    participant W as Web
    participant A as API
    participant CS as Cloud Sorage
    participant CF as Cloud Function
    participant CV as Cloud Vision API
    participant FS as Fire Store

    W ->> A: File Upload
    A ->> CS: File Upload
    CS ->> CF: Triggered
    CF ->> CS: Get File
    CS -->> CF: Response
    CF ->> CV: Analyze Request
    CV -->> CF: Response
    CF ->> FS: Store Analyzed Data
```

    A->>+John: Hello John, how are you?
    John->>-A: I feel great!