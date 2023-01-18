# ==============================================================================
# title              : main_app.py
# description        : This is the flask app for BERT QNA Italian DEMO which receives the request and provide response.
# author             : Pragnakalp Techlabs
# email              : letstalk@pragnakalp.com
# website            : https://www.pragnakalp.com
# python_version     : 3.x
# ==============================================================================

# import required Libraries
import logging
from flask import Flask, render_template, request, make_response, jsonify, current_app, Response
import json
import os
import csv
import pytz
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# json_json() function is used to convert the input data i.e paragraph and question into the SQUAD like format, then we will be storing this data in a file named input_italian.json which is used as prediction file in run_squad command that you will see further in submitted_form() function.

def json_json():
    false = "" 
    json_data= {
        "version": "v2.0",
        "data": [
            {
                "title": "Google",
                "paragraphs": [
                    {
                        "qas": [
                            {
                                "question": request.form['Question1'],
                                "id":"56ddde6b9a695914005b9628",
                                "is_impossible":false
                            },
                            {
                                "question": request.form['Question2'],
                                "id":"56ddde6b9a695914005b9629",
                                "is_impossible":false
                            },
                            {
                                "question": request.form['Question3'],
                                "id":"56ddde6b9a695914005b962a",
                                "is_impossible":false
                             },
                            {
                                "question": request.form['Question4'],
                                "id":"5ad39d53604f3c001a3fe8d3",
                                "is_impossible":false
                             },
                            {
                                "question": request.form['Question5'],
                                "id":"5ad39d53604f3c001a3fe8d4",
                                "is_impossible":false
                            }
                        ],
                        "context":request.form['Paragraph']
                    }
                ]
            }
        ]
    }
    return json_data

# csvsave() function is used for logging, that is a log file is created which will store paragraph, questions, answers, IP adrress and current time for each request.
def csvsave(p, q, a, IP, now):
    fieldnames = ['p', 'q', 'a', 'IP', 'time']
    with open('bert_log.csv', 'a') as inFile:
        # DictWriter will help you write the file easily by treating the
        # csv as a python's class and will allow you to work with
        # dictionaries instead of having to add the csv manually.
        writer = csv.DictWriter(inFile, fieldnames=fieldnames)

        # writerow() will write a row in your csv file
        writer.writerow({'p': p, 'q': q, 'a': a, 'IP': IP, 'time': now})

# This is used to render the Question Answering form, in which we will take the paragraph and questions entered by user and then submitted_form() function is called on submit event.
@app.route('/', methods=['GET'])
def form():
    return render_template('form_bert_qna.html')

# submitted_form() Contains the code for performing the prediction using the run_squad file of BERT.
@app.route('/submitted', methods=['POST','GET','OPTIONS'])
def submitted_form():
    intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(intz)
    if request.method == 'POST':
        # Dumping the input in json format in the file using the json_json() function as discussed above.
        with open('input_italian.json', 'w') as f:
            json.dump(json_json(), f)
    
    # Fetching the paragraph and questions from the Request.
    para = request.form['Paragraph']
    q1 = request.form['Question1']
    q2 = request.form['Question2']
    q3 = request.form['Question3']
    q4 = request.form['Question4']
    q5 = request.form['Question5']

    

    # Below is the code to perform the prediction, for which model is required, our fine-tuned model is stored in bert/model folder. Fine-Tuned model contains three main files i) model.ckpt file is a TensorFlow checkpoint that contains the weights. ii) vocab.txt is a vocab file which maps WordPiece to word id. iii) bert_config.json is a config file which specifies the hyperparameters of the model.

    # You can even change the rest of the hyper-parameter:-
    # max_seq_length: The maximum total input sequence length after WordPiece tokenization, Sequences longer than this will be truncated, and sequences shorter will be padded. Default is 128.
    # output_dir: directory where the output files will be stored
    # predict_file: the file on which predict is performed
    # doc_stride: When splitting up a long document into chunks, how much stride to take between chunks
    # max_query_length: The maximum number of tokens for the question. Questions longer than this will be truncated to this length.
    # do_train: Whether to run training.
    # do_predict: Whether to perform prediction.
    # n_best_size: The total number of n-best predictions to generate in the nbest_predictions.json output file.
    os.system("python bert/run_squad.py \
  --bert_config_file=bert/model/bert_config.json \
  --vocab_file=bert/model/vocab.txt \
  --output_dir=bert/model/output/ \
  --predict_file=input_italian.json \
  --init_checkpoint=bert/model/italian_model.ckpt-20446 \
  --do_lower_case=False \
  --max_seq_length=384 \
  --doc_stride=128 \
  --do_train=False \
  --do_predict=True \
  --n_best_size=3")

    # prediction files are stored at output_dir which we have mentioned in run_squad command
    # Here we have read the predictions.json file, fetch predicted answers from it and submitted that to submitted_form_bert.html page
    with open("bert/model/output/predictions.json", "r") as read_file:
        output = json.load(read_file)

    if not q1:
        a11 = "No question entered"
    else:
        a11 = output["56ddde6b9a695914005b9628"]

    if not q2:
        a22 = "No question entered"
    else:
        a22 = output["56ddde6b9a695914005b9629"]

    if not q3:
        a33 = "No question entered"
    else:
        a33 = output["56ddde6b9a695914005b962a"]

    if not q4:
        a44 = "No question entered"
    else:
        a44 = output["5ad39d53604f3c001a3fe8d3"]

    if not q5:
        a55 = "No question entered"
    else:
        a55 = output["5ad39d53604f3c001a3fe8d4"]

    # Fetched the IP address from the Request
    IP = request.remote_addr
    # Called the csvsave() to Store the details in log file.
    csvsave(para, [q1, q2, q3, q4, q5], [a11, a22, a33, a44, a55], IP, now)

    # called the submitted_form_bert.html page
    return render_template(
                'submitted_form_bert.html',
                para = para,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                a1 = a11,
                a2 = a22,
                a3 = a33,
                a4 = a44,
                a5 = a55
            )

# submitted_api() contains the code for performing the prediction through api
@app.route('/submitted_api', methods=['POST','GET','OPTIONS'])
def submitted_api():
    intz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(intz)
    if request.method == 'POST':
        print("************** Request Receieved ------------------------")
        # Dumping the input in json format in the file using the json_json() function as discussed above.
        with open('input_chinese.json', 'w') as f:
            json.dump(json_json(), f)

    para = request.form['Paragraph']
    q1 = request.form['Question1']
    q2 = request.form['Question2']
    q3 = request.form['Question3']
    q4 = request.form['Question4']
    q5 = request.form['Question5']

    os.system("python bert/run_squad.py \
  --bert_config_file=bert/model/bert_config.json \
  --vocab_file=bert/model/vocab.txt \
  --output_dir=bert/model/output/ \
  --predict_file=input_spansih.json \
  --init_checkpoint=bert/italian_model.ckpt-20446 \
  --do_lower_case=False \
  --max_seq_length=384 \
  --doc_stride=128 \
  --do_train=False \
  --do_predict=True \
  --n_best_size=3")

    with open("bert/model/output/predictions.json", "r") as read_file:
        output = json.load(read_file)
        # return make_response(jsonify(output))
        # returning templetes and viewing data on page
    if not q1:
        a11 = "No question entered"
    else:
        a11 = output["56ddde6b9a695914005b9628"]

    if not q2:
        a22 = "No question entered"
    else:
        a22 = output["56ddde6b9a695914005b9629"]

    if not q3:
        a33 = "No question entered"
    else:
        a33 = output["56ddde6b9a695914005b962a"]

    if not q4:
        a44 = "No question entered"
    else:
        a44 = output["5ad39d53604f3c001a3fe8d3"]

    if not q5:
        a55 = "No question entered"
    else:
        a55 = output["5ad39d53604f3c001a3fe8d4"]
        
    # Fetched the IP address from the Request
    IP = request.remote_addr
    # Called the csvsave() to Store the details in log file.
    csvsave(para, [q1, q2, q3, q4, q5], [a11, a22, a33, a44, a55], IP, now)

    result = {
        'paragraph': para,
        'question_1': {
            'question': q1,
            'answer': a11
        },
        'question_2': {
            'question': q2,
            'answer': a22
        },
        'question_3': {
            'question': q3,
            'answer': a33
        },
        'question_4': {
            'question': q4,
            'answer': a44
        },
        'question_5': {
            'question': q5,
            'answer': a55
        }
    }

    # return make_response(jsonify(result))
    data = json.dumps(result)
    resp = Response(data, status=200, mimetype='application/json')        
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = True
    print("--------------- Response --------------------",resp)
    return resp

if __name__ == '__main__':
    app.run(debug=True)