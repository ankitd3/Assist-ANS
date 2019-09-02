from flask import Flask, render_template, url_for, request
from NLP import distance

app = Flask(__name__)
#Dataset: https://github.com/MrJay10/banking-faq-bot/blob/master/BankFAQs.csv
department = ['security', 'loans', 'accounts', 'insurance', 'investments',
       'fundstransfer', 'cards']
'''
['Mortgage','Credit reporting','Consumer Loan'
     ,'Debt collection','Student loan','Bank account or service'
     ,'Other financial service','Money transfers'
     ,'Credit repair services, or other personal consumer reports'
     ,'Payday loan','Checking or savings account'
     ,'Virtual currency or money service'
     ,'Credit card or prepaid card','Vehicle loan or lease'
     ,'Payday loan, title loan, or personal loan']
'''
process = ['Choose language','Record and submit your query','Review automated solution','Your query will be posted under a department','Department is assigned automatically','Please keep the query ID for tracking']

@app.route("/")
@app.route('/query')
def query():
    return render_template('query.html', title = 'Query', process = process)

@app.route('/query', methods=['POST'])
def query_post():
    similar_q, dept, query_found = [0,0,0]
    elaborate = False
    text = request.form['text']
    satisfied = request.form['satisfied']
    #processed_text = text.upper()
    if(satisfied == "True"):
        dept = distance.find_department(text, True)
        if(dept != False):
            query_found = False
        elif(dept == False):
            elaborate = True
    else:
        similar_q = distance.find_department(text, False)
        if(similar_q != False):
            if(len(similar_q[0])==7):
                #We actually found a similar question
                query_found = True
            else:
                #We couldn't find a similar question hence, we stored the query
                dept = similar_q
                query_found = False
        elif(similar_q == False):
            elaborate = True

    return render_template('query.html', department = dept, title = 'Query', similar_query = similar_q, query_found = query_found, text = text, elaborate = elaborate, process = process)

@app.route('/track')
def track():
    process = ['Enter your query ID','Check if it has been resolved or not']
    return render_template('track.html', title = 'Track', solution = "NA", process = process)

@app.route('/track', methods=['GET', 'POST'])
def track_post():

    process = ['Enter your query ID','Check if it has been resolved or not']

    q_id = request.form['q_id']

    solution = distance.fetch_query_details('',int(q_id),'resolved')

    return render_template('track.html', title = 'Track', solution = solution, process = process)

@app.route('/solve')
def solve():

    process = ['Choose your department','Click on the query card you wish to solve','Enter your ID and solution','You may change the department of the query as well']

    unresolved_queries = distance.fetch_query_details('all',0,'unresolved')

    return render_template('solve.html', title = 'Solve', success = 0, queries = unresolved_queries, departments = department, process = process)

@app.route('/solve', methods=['GET', 'POST'])
def solve_post():

    process = ['Choose your department','Click on the query card you wish to solve','Enter your ID and solution','You may change the department of the query as well']

    q_id = request.form['q_id']
    e_id = request.form['e_id']
    solution = request.form['solution']
    new_department = request.form['new_department']

    unresolved_queries = distance.fetch_query_details('all',0,'unresolved')

    if(new_department!='0'):
        distance.change_department(int(q_id),new_department)
        success = 2      
    else:
        distance.resolve_query(int(q_id),int(e_id),solution)
        success = 1

    return render_template('solve.html', title = 'Solve', success = success, queries = unresolved_queries, departments = department, process = process)

if __name__ == '__main__':
    app.run(debug=True)