from flask import Flask, render_template, g, request
import config
from twitter_handler import twitter_handler
from pre_processing import pre_processing

app = Flask(__name__)
app.config.from_object("config")
twitter_request = twitter_handler(app)
pre_process = pre_processing()

#default homepage, routed from home and the base url
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

#default homepage, routed from home and the base url
@app.route("/tweet_test/<tweet_id>",methods=["GET"])
def test(tweet_id=None):
    tweet = twitter_request.retrieve_tweet(tweet_id)
    predictions = pre_process.test(tweet.text)
    return predictions

#default homepage, routed from home and the base url
@app.route("/plain_text",methods=["POST"])
def plain_test():
    text = request.form['plain_text']
    predictions = pre_process.test(text)
    return predictions


#runs servlet, debug=true if you want to test running code
if __name__ == "__main__":

    app.run(host= '0.0.0.0',debug=True)
