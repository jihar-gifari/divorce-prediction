
# Divorce Probability Prediction 🤖💔
Hey there! Welcome to my Divorce Probability Prediction project. 🚀 In this journey, I'll give you a sneak peek into how I tinkered with data, trained a machine learning model, 
interpreted its mystical workings, and even managed to deploy it into the wilds of the internet using Flask, GCP, and Heroku. So, buckle up, and let's dive in!

## 1. EDA - Let's Get Our Sherlock Hats On 🕵️‍♂️
Before doing predictions, I put on my detective cap and delved into the data. I know, not as cool as Benedict Cumberbatch, but I tried! I peeked into the Turkish Relationship Survey dataset
like a nosy neighbor (without the gossip, of course). This was the stage where I tamed the unruly data, cleaned it up, and uncovered its quirks. Ah, the joy of spotting suspicious data, missing values and outliers - it's like finding the last piece of chocolate cake in the fridge!

In the EDA phase, my main goals are : 
- Understanding each variable's nature, 
- Exploring how its link to divorce status, and 
- Identifying necessary cleaning steps.

### Key Findings : 
- Variables mostly show distinct scoring patterns. For example, in question 18 ("My spouse and I have similar ideas about how marriage should be"), divorced individuals strongly disagree (low score), while non-divorced tend to agree. This highlights the significance of shared marital ideals.
- Yet, a few variables display odd result. Take Question 41: "When I talk to my spouse about something, my calm suddenly breaks." Non-divorced couples report significantly higher numbers than divorced couple. This counters expectations, as sudden calm disruption during conversation doesn't align with a happy marriage. This odd results also appear on several other variables. This kind of variable will be specially treated as "suspicious data".
- No missing values, duplicated data, or imbalanced target detected. However, There is a small percentage of outliers detected in question 6 & 7
  
## 2. Data Preprocessing - The Art of Transformation 🧙‍♀️
As noted in previous EDA, no missing values, duplicates, or imbalanced target variables exist. Only minor outliers appear and certain variables yield unusual results (read: suspicious data), requiring special treatment. Here are the approaches I used:

![Cleaning Treatments](https://github.com/jihar-gifari/divorce-prediction/blob/main/divorce_treatments.png)
- Exclusion 1 : Exclude Very Suspicious Variable Only
- Exclusion 2 : Exclude All Suspicious Variable 
- Manipulation 1 : Manipulate value in Very Suspicious variable only
- Manipulation 2 : Manipulate value in All Suspicious variable


Manipulation : replace 0->4, 1->3, 4->0, 3->1

very_suspicious = 'Q6', 'Q7', 'Q32', 'Q35', 'Q36', 'Q37', 'Q38', 'Q39', 'Q41', 'Q46'

suspicious = 'Q6', 'Q7', 'Q32', 'Q35', 'Q36', 'Q37', 'Q38', 'Q39', 'Q41', 'Q46', 
             'Q31', 'Q40', 'Q45', 'Q48', 'Q50', 'Q51', 'Q52', 'Q54'
             

Totally, there were 8 different treatments. Each treatments will be used to train models using various algorithm, best treatment and algorithm will be selected


## 3. Modelling and Evaluation - The "Aha!" Moment 🌟
Across the 8 data treatments, I experimented with approximately 17 algorithms, leading to 136 model combinations. Initially, I assessed models using accuracy, precision, recall, F1-Score, and AUC/ROC. 
Surprisingly, many models performed exceptionally well on the test set. To mitigate the risk of overfitting, I selected the model with the best cross-validation score while prioritizing higher interpretability.

## 4. Model Interpretation (SHAP) - Decoding the Enigma 🕵️‍♀️
Ever heard of SHAP (SHapley Additive exPlanations)? It's like magic glasses that help you understand how your model thinks. I put them on and deciphered the cryptic reasoning behind the model's predictions. It was like translating a cat's meow into English! 🐱🔍

### Key Interpretation (From Top 5 Variable) :
- When both partners share similar views on marriage roles and concepts (Questions 19 & 18), divorce chances diminish.
- Having aligned values on personal freedom (Question 12) is linked to a lowered predicted divorce probability.
- A higher likelihood of initiating discussions or arguments in a relationships without knowing what's going on (Question 40) corresponds to an increased risk of divorce.


## 5. Deployment Using Flask, GCP, and Heroku - Let's Go Live! 🌐
A model that can't see the world is like a superhero stuck in a phone booth. I gave my model wings and deployed it using Flask, GCP, and Heroku. It's now out there, predicting divorce probabilities like a fortune teller with a Ph.D. in relationships! 🚀💑

So, there you have it! My whirlwind journey from data detective to model magician, topped with a sprinkle of code and a dash of humor. Feel free to check out the code, play with the app, and remember: predicting divorce might be complex, but understanding the journey doesn't have to be! Enjoy the nerdy adventure! 🤓🚀
