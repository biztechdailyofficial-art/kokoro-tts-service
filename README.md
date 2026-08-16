# Kokoro TTS Service

Standalone HTTP wrapper around Kokoro TTS (voices: `sarah`, `james`, `emma`, `oliver`).
Built to run somewhere with real CPU (Railway) instead of the 1-vCPU VPS payledgr-backend
runs on, where Kokoro inference took 16-20s per line — too slow for a live phone call.

## Deploy on Railway

1. Push this repo to GitHub.
2. Railway → New Project → Deploy from GitHub repo → select this repo.
3. Set an environment variable `API_KEY` to a random secret string (this locks down
   `/synthesize` so nobody else can run up your compute bill).
4. Railway builds the Dockerfile automatically. Wait for the `/health` check to pass.
5. Settings → Networking → Generate Domain, and copy the public URL it gives you.

## API

```
POST /synthesize
Headers: X-API-Key: <your API_KEY>
Body:    { "text": "Hello there", "voice": "sarah", "speed": 0.95 }
Returns: audio/wav bytes
```

```
GET /health -> { "status": "ok" }
```

## Connecting it to payledgr-backend

Once deployed, send me the Railway URL and the `API_KEY` you set — I'll point
`kokoro-tts.js` at it instead of the local `/home/payledgr/tts` process.
