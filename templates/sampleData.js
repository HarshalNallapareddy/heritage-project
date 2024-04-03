{
    "nodes": [
      {
        "id": "1",
        "name": "John Doe",
        "dateOfBirth": "1970-01-01",
        "hobbies": ["gardening", "reading"]
      },
      {
        "id": "2",
        "name": "Jane Doe",
        "dateOfBirth": "1975-05-15",
        "hobbies": ["painting", "cycling"]
      },
      {
        "id": "3",
        "name": "Jimmy Doe",
        "dateOfBirth": "2000-03-12",
        "hobbies": ["video games", "soccer"]
      }
      // Additional family members...
    ],
    "connections": [
      {
        "type": "spouse",
        "source": "1",
        "target": "2"
      },
      {
        "type": "parent-child",
        "source": "1",
        "target": "3"
      },
      {
        "type": "parent-child",
        "source": "2",
        "target": "3"
      }
      // Additional relationships...
    ]
  }