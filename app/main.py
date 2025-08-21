from flask import Flask, render_template, request
import random
from livereload import Server

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text', '')
    words = text.split(' ')
    num_words = len(words)

    # Temporarily mark words with chunk info
    word_meta_list = [{'text': w, 'color': None, 'chunk_id': None} for w in words]
    analysis_results = []
    max_probability = 0
    chunk_counter = 0

    i = 0
    while i < num_words:
        if random.random() < 0.2 and (num_words - i) > 2:
            chunk_length = random.randint(2, 6)
            end_index = min(i + chunk_length, num_words)
            chunk_id = f"chunk-{chunk_counter}"

            is_strong_suspicion = random.random() < 0.5
            color = "red" if is_strong_suspicion else "orange"
            suspicion_level = "강하게" if is_strong_suspicion else "조금"
            probability = random.randint(71, 100) if is_strong_suspicion else random.randint(30, 70)
            if probability > max_probability: max_probability = probability

            for j in range(i, end_index):
                word_meta_list[j]['color'] = color
                word_meta_list[j]['chunk_id'] = chunk_id

            chunk_text = " ".join(words[i:end_index])
            reason_number = random.randint(1, 1000)
            reason_text = f"부분은 AI가 작성한 특정 패턴과 {reason_number}가지 유사점이 발견되어 {suspicion_level} 의심됩니다."
            analysis_results.append({
                'chunk_text': chunk_text,
                'reason_text': reason_text,
                'color': color,
                'chunk_id': chunk_id
            })
            chunk_counter += 1
            i = end_index
        else:
            i += 1
    
    # Create a clean list for display, grouping chunks together
    display_list = []
    i = 0
    while i < num_words:
        meta = word_meta_list[i]
        if meta['color']:
            chunk_id = meta['chunk_id']
            chunk_words = []
            while i < num_words and word_meta_list[i]['chunk_id'] == chunk_id:
                chunk_words.append(word_meta_list[i]['text'])
                i += 1
            display_list.append({'text': " ".join(chunk_words), 'color': meta['color'], 'chunk_id': chunk_id})
        else:
            display_list.append({'text': meta['text'], 'color': None, 'chunk_id': None})
            i += 1

    if max_probability == 0:
        max_probability = random.randint(0, 29)

    return render_template(
        'index.html',
        original_text=text,
        display_list=display_list,
        analysis_results=analysis_results,
        probability=max_probability
    )

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.watch('C:/Users/tails/Capstone_toy/app/')
    server.serve(port=5000)