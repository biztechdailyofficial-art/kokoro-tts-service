import io
import os

import numpy as np
import soundfile as sf
from flask import Flask, jsonify, request, send_file
from kokoro import KPipeline

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')

VOICES = {
    'sarah':  ('af_heart',   'a'),
    'james':  ('am_michael', 'a'),
    'emma':   ('bf_emma',    'b'),
    'oliver': ('bm_george',  'b'),
}

print('Loading Kokoro pipelines...', flush=True)
pipelines = {
    'a': KPipeline(lang_code='a'),
    'b': KPipeline(lang_code='b'),
}
print('Kokoro ready', flush=True)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/synthesize')
def synthesize():
    if API_KEY and request.headers.get('X-API-Key') != API_KEY:
        return jsonify({'error': 'unauthorized'}), 401

    data = request.get_json(force=True, silent=True) or {}
    text = (data.get('text') or '').strip()
    voice_name = data.get('voice', 'sarah')
    speed = float(data.get('speed', 0.95))

    if not text:
        return jsonify({'error': 'text is required'}), 400

    voice_id, lang = VOICES.get(voice_name, VOICES['sarah'])
    generator = pipelines[lang](text, voice=voice_id, speed=speed)
    chunks = [chunk.audio.numpy() for chunk in generator]
    audio = np.concatenate(chunks)

    buf = io.BytesIO()
    sf.write(buf, audio, 24000, format='WAV')
    buf.seek(0)
    return send_file(buf, mimetype='audio/wav')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
