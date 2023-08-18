import pandas as pd
import numpy as np

import joblib
from flask import Flask, render_template, request
import shap
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("divorce-prediction-by-jihar-2dd31151c0d5.json", scope)
client = gspread.authorize(credentials)

sheet = client.open_by_key("1rVrqeW6nDs-WNCIP2Wl4qqXBYmm4wfQw8Xyb1uks6Qo")
worksheet = sheet.get_worksheet(0)  # Assuming you want to use the first worksheet

app = Flask(__name__)

# Load the pickled model

model = joblib.load('model_randomforest_treatment6.pkl')
explainer = shap.TreeExplainer(model)

questions = {
        1  : "If one of us apologizes when our discussion deteriorates, the discussion ends.",
        2  : "I know we can ignore our differences, even if things get hard sometimes.",
        3  : "When we need it, we can take our discussions with my spouse from the beginning and correct it.",
        4  : "When I discuss with my spouse, to contact him will eventually work.",
        5  : "The time I spent with my wife is special for us.",
        6  : "We don't have time at home as partners.",
        7  : "We are like two strangers who share the same environment at home rather than family.",
        8  : "I enjoy our holidays with my wife.",
        9  : "I enjoy traveling with my wife.",
        10 : "Most of our goals are common to my spouse.",
        11 : "I think that one day in the future, when I look back, I see that my spouse and I have been in harmony with each other.",
        12 : "My spouse and I have similar values in terms of personal freedom.",
        13 : "My spouse and I have similar sense of entertainment.",
        14 : "Most of our goals for people (children, friends, etc.) are the same.",
        15 : "Our dreams with my spouse are similar and harmonious.",
        16 : "We're compatible with my spouse about what love should be.",
        17 : "We share the same views about being happy in our life with my spouse",
        18 : "My spouse and I have similar ideas about how marriage should be",
        19 : "My spouse and I have similar ideas about how roles should be in marriage",
        20 : "My spouse and I have similar values in trust.",
        21 : "I know exactly what my wife likes.",
        22 : "I know how my spouse wants to be taken care of when she/he sick.",
        23 : "I know my spouse's favorite food.",
        24 : "I can tell you what kind of stress my spouse is facing in her/his life.",
        25 : "I have knowledge of my spouse's inner world.",
        26 : "I know my spouse's basic anxieties.",
        27 : "I know what my spouse's current sources of stress are.",
        28 : "I know my spouse's hopes and wishes.",
        29 : "I know my spouse very well.",
        30 : "I know my spouse's friends and their social relationships.",
        31 : "I feel aggressive when I argue with my spouse.",
        32 : "When discussing with my spouse, I usually use expressions such as ‘you always’ or ‘you never’ .",
        33 : "I can use negative statements about my spouse's personality during our discussions.",
        34 : "I can use offensive expressions during our discussions.",
        35 : "I can insult my spouse during our discussions.",
        36 : "I can be humiliating when we discussions.",
        37 : "My discussion with my spouse is not calm.",
        38 : "I hate my spouse's way of open a subject.",
        39 : "Our discussions often occur suddenly.",
        40 : "We're just starting a discussion before I know what's going on.",
        41 : "When I talk to my spouse about something, my calm suddenly breaks.",
        42 : "When I argue with my spouse, ı only go out and I don't say a word.",
        43 : "I mostly stay silent to calm the environment a little bit.",
        44 : "Sometimes I think it's good for me to leave home for a while.",
        45 : "I'd rather stay silent than discuss with my spouse.",
        46 : "Even if I'm right in the discussion, I stay silent to hurt my spouse.",
        47 : "When I discuss with my spouse, I stay silent because I am afraid of not being able to control my anger.",
        48 : "I feel right in our discussions.",
        49 : "I have nothing to do with what I've been accused of.",
        50 : "I'm not actually the one who's guilty about what I'm accused of.",
        51 : "I'm not the one who's wrong about problems at home.",
        52 : "I wouldn't hesitate to tell my spouse about her/his inadequacy.",
        53 : "When I discuss, I remind my spouse of her/his inadequacy.",
        54 : "I'm not afraid to tell my spouse about her/his incompetence."
}

# Load Google Sheets credentials and authenticate
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("divorce-prediction-by-jihar-2dd31151c0d5.json", scope)
client = gspread.authorize(credentials)


@app.route('/', methods=['GET'])
def index():
    return render_template('form.html', questions=questions)

@app.route('/predict', methods=['POST'])
def predict():
    # Gather user details
    name = request.form.get('name')
    email = request.form.get('email')
    time_spent = int(request.form.get('time_spent'))  # Get the calculated time spent

    user_details = [name, email, time_spent]  # Remove start_time and end_time

    # Open the Google Sheet using its ID
    sheet = client.open_by_key("1rVrqeW6nDs-WNCIP2Wl4qqXBYmm4wfQw8Xyb1uks6Qo")

    try:
        user_details_worksheet = sheet.worksheet("User Details")
    except gspread.exceptions.WorksheetNotFound:
        user_details_worksheet = sheet.add_worksheet(title="User Details", rows="100", cols="3")  # Adjust cols to 3
        user_details_worksheet.append_row(["user_name", "user_email", "time_spent"])  # Remove start_time and end_time

    # Check the number of rows in the User Details worksheet
    current_rows = user_details_worksheet.row_count

    # Set a threshold for when to add more rows (e.g., 80% of the initial limit)
    row_threshold = 0.8 * 100  # Change 100 to your initial row limit

    if current_rows >= row_threshold:
        # Add more rows to the worksheet to accommodate more data
        rows_to_add = 100  # Adjust the number of rows to add as needed
        user_details_worksheet.add_rows(rows_to_add)

    # Append user details to the User Details worksheet
    user_details_worksheet.append_row(user_details)

    # Gather user responses
    responses = []
    for qid in questions:
        response = request.form.get(f'q{qid}')
        if response is not None and response != '':
            responses.append(response)
        else:
            responses.append(0)

    try:
        responses_worksheet = sheet.worksheet("Responses")
    except gspread.exceptions.WorksheetNotFound:
        responses_worksheet = sheet.add_worksheet(title="Responses", rows="100", cols="55")  # Adjust cols to 55
        header_row = list(questions.keys())
        header_row.extend(["User Name", "User Email", "Predicted Divorce Probability"])
        responses_worksheet.append_row(header_row)

    # Calculate predicted divorce probability
    X = [responses]
    prediction = model.predict_proba(X)[0][0] * 100
    shap_values = explainer.shap_values(pd.DataFrame(X, columns=questions.keys()))
    abs_shap_values = np.abs(shap_values[1][0])
    top_feature_indices = np.argsort(abs_shap_values)[::-1][:5]

    # Retrieve the top feature names from the questions dictionary
    top_feature_names = [questions[qid] for qid in top_feature_indices]
    top_feature_values = [responses[i] for i in top_feature_indices]
    top_feature_shap_values = shap_values[1][0][top_feature_indices]

    # Append user responses to the Responses worksheet along with user name, email, and predicted probability
    responses.append(name)  # Add user name to responses
    responses.append(email)  # Add user email to responses
    responses.append(prediction)  # Add predicted divorce probability to responses
    responses_worksheet.append_row(responses)

    # Rest of your shap_values code here...

    return render_template('result.html', 
                           prediction=prediction,
                           user_name=name,
                           user_email=email,
                           time_spent=time_spent,
                           top_feature_names=top_feature_names, 
                           top_feature_values=top_feature_values, 
                           top_feature_shap_values=top_feature_shap_values)

if __name__ == '__main__':
    app.run()
