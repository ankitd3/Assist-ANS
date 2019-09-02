# Assist-ANS
A mobile-first grievances web-app using NLP

Download the source code and "Google pre-trained vectors" (link: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) and provide the path to it in the file "NLP/distance.py" to the variable: "wordmodelfile". 

Install PyEmd, sklearn, pandas, gensim, flask via PIP

Go to the directory and run:
export FLASK_DEBUG=1 (Optional)
export FLASK_APP=assist_ans.py
flask run

Go to "localhost:5000" in your browser.
