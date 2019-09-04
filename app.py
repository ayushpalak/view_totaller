from flask import Flask,render_template,request
import pandas as pd

app = Flask(__name__)

def findSum(filename, content_id):
    df = pd.read_csv(filename)
    df2 = df
    df['Views'] = (df['Views'].astype(str).str.replace(",","")).astype(int)
    df = df.groupby(['Content Id'])['Views'].agg('sum')
    df = dict(df)
    ids = [int(i.strip()) for i in content_id.split(",")] 
    result = {}
    for i in ids:
        print(i,df[i])
        a = df2.loc[df2['Content Id'] == i].values
        result[i] = [a[0][1],df[i]]
    return result

@app.route('/')  
def upload():  
    return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        content_id = request.form['content_id']
        print(content_id)
        f = request.files['file']  
        f.save(f.filename)
        result = findSum(f.filename,content_id)  
        return render_template("success.html", name = f.filename, result = result)  
  
if __name__ == '__main__':  
    app.run(debug = True)  