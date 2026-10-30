from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
# read API key from env
app.config['OPENAI_KEY'] = os.getenv('OPENAI_API_KEY')

@app.route('/v1/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt','')
    if not app.config['OPENAI_KEY']:
        return jsonify(error='OpenAI key not set'), 500
    try:
        openai.api_key = app.config['OPENAI_KEY']
        response = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user', 'content':prompt}])
        return jsonify(text=response['choices'][0]['message']['content'])
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
