import gradio as gr
import pandas as pd

with gr.Blocks() as demo:
    dataset_df = {}
    state = gr.State(value=0)
    with gr.Row():
        gr.Markdown("# Distributed Evaluation Parallel 😎")
    with gr.Row():
        upload = gr.UploadButton(label="Upload a file")
        prev = gr.Button(value="Previous")
        next = gr.Button(value="Next")
        download = gr.Button(value="Download")
    with gr.Row():
        with gr.Column():
            question = gr.Textbox(label="Question")
        with gr.Column():
            ground_truth = gr.Textbox(label="GT")
        with gr.Column():
            prediction = gr.Textbox(label="Prediction")
            score = gr.Radio(["Incorrect", "Correct"], label="Score")
    with gr.Row():
        todos = gr.DataFrame()
        done = gr.DataFrame()
    

    def csv2df(file):
        df = pd.read_csv(file.name)
        dataset_df.update(dict(df=df))
        return update()

    def prev_func():
        state.value = max(state.value - 1, 0)
        return update()
    
    def next_func():
        state.value = min(state.value + 1, len(dataset_df['df']) - 1)
        return update()

    def update():
        q = dataset_df['df'].question.to_list()[state.value]
        g = dataset_df['df'].answer.to_list()[state.value]
        p = dataset_df['df'].prediction.to_list()[state.value]
        return q, g, p, dataset_df['df'], dataset_df['df']
    upload.upload(csv2df, upload, [question, ground_truth, prediction, todos, done])
    prev.click(prev_func, None, [question, ground_truth, prediction, todos, done])
    next.click(next_func, None, [question, ground_truth, prediction, todos, done])

demo.queue()
demo.launch(share=True)