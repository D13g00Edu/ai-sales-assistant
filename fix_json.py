import os
path = "frontend/package.json"
json_content = """{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint"
  },
  "dependencies": {
    "lucide-react": "^0.460.0",
    "next": "15.1.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "recharts": "^2.13.3"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "eslint": "^9",
    "eslint-config-next": "15.1.0",
    "typescript": "^5"
  }
}
"""
with open(path, "wb") as f:
    f.write(json_content.encode("utf-8"))
