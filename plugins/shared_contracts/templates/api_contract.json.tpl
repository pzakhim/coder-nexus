{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "{{ApiTitle}} Contract",
  "version": "{{Version}}",
  "status": "DRAFT_BY_FE",
  "feature_slug": "{{FeatureSlug}}",
  "endpoint": "{{EndpointPath}}",
  "method": "{{HttpMethod}}",
  "auth_required": true,
  "headers": {
    "Authorization": "Bearer <jwt>",
    "Content-Type": "application/json"
  },
  "query_parameters": {
    "type": "object",
    "properties": {},
    "required": []
  },
  "request_body": {
    "type": "object",
    "properties": {},
    "required": []
  },
  "responses": {
    "200": {
      "description": "Success response",
      "body": {
        "type": "object",
        "properties": {
          "code": { "type": "integer", "example": 200 },
          "data": { "type": "object" },
          "message": { "type": "string" }
        },
        "required": ["code", "data"]
      }
    },
    "400": {
      "description": "Validation error",
      "body": {
        "type": "object",
        "properties": {
          "code": { "type": "integer", "example": 400 },
          "error": { "type": "string" }
        }
      }
    }
  }
}
