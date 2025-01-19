{
  "openapi": "3.0.0",
  "info": {
    "title": "Fast Epost API",
    "version": "1.0.0",
    "description": "API documentation for the Fast Epost application."
  },
  "paths": {
    "/users/{userId}": {
      "get": {
        "summary": "Get user profile",
        "parameters": [
          {
            "name": "userId",
            "in": "path",
            "required": true,
            "description": "ID of the user to fetch",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "User profile retrieved successfully",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "email": {
                      "type": "string"
                    },
                    "phone": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "User not found"
          }
        }
      }
    },
    "/shipments": {
      "get": {
        "summary": "Get shipment data",
        "parameters": [
          {
            "name": "userId",
            "in": "query",
            "required": true,
            "description": "ID of the user to fetch shipments for",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Shipment data retrieved successfully",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "date": {
                        "type": "string"
                      },
                      "count": {
                        "type": "integer"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
