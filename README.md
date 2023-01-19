# BERT-QnA-Italian

## Instructions to set up the Bert QNA Italian Demo on Local system

1. Clone the repository in your system.
2. Download the model file from https://drive.google.com/file/d/1eSkw0zMnOd13WvdAi_9sOwaDz9HbPkrJ/view?usp=sharing and unzip it in /bert directory.
3. Install and create a virtual environment by the following step. You'll need <b>python <= 3.6</b> to set it up.
```shell
sudo apt install virtualenv
virtualenv venv --python=python3.6
source venv/bin/activate
```
4. Install the dependencies from requirement.txt file (it will install all the required packages)
```shell
pip install -r requirement.txt
```
5. Run the flask app by the following command (by default the app is running on port 5000)
```shell
python main_app.py 
```
6. You can access the Bert QNA at http://127.0.0.1:5000/ 

7. We have also included API to enable access of the QnA from third-party application. You can make call to http://127.0.0.1:5000/submitted_api with paragraph and questions from HTML form.

If you have any other questions or face issues in setting the demo up then kindly reach out to us at letstalk@pragnakalp.com 

For all your Natural Language Processing (NLP) requirements, we are here to help you. Email us your requirement at letstalk@pragnakalp.com and don't forget to check out more interesting <a href="https://www.pragnakalp.com/services/natural-language-processing-services/" target="_blank">NLP services</a> we are offering. 