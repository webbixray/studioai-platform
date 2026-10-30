from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def hello():
    return jsonify(message='Hello from StudioAI backend')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


from llm_client import get_llm_response
from security_scan import scan_code
import black

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    lang = data.get('lang', 'python')
    brief = data.get('brief', '')
    # Generate code
    code = get_llm_response(brief, model='gpt-4o-mini')
    findings = scan_code(lang, code)
    # Auto-remediation for Python
    if lang == 'python':
        try:
            formatted = black.format_str(code, mode=black.Mode())
            code = formatted
        except Exception:
            pass
    return jsonify({'lang': lang, 'generated': code, 'findings': findings})

