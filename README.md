# Rezzi - Your Personal Resume Assistant 

My team and I built a 100% voice-driven resume builder to tackle literacy challenges at the 2018  [AngelHack](https://angelhack.com/)  Silicon Valley Hackathon. AngelHack proposed two challenges that we wanted to try to tackle in the 24-hour period: build tech to solve homelessness and make a social impact.

### Our solution

We built Rezzi, an interactive resume assistant. It'll ask you questions relevant for a job search and resume, listen to your answers, then generate a resume to send to local homless job assistance workshops.

![test](https://raw.githubusercontent.com/nikrom17/Rezzi/master/rezzi/static/img/rezzi_screenshot.png =305x)

The PWA works by:

1.  Get user voice as audio file
2.  Analyze language
3.  Respond to user in audio
4.  Repeat 1-3 till end, gathering data
5.  Build a resume

The users audio input was sent to the Dialogflow API for NLP and NLU analysis. The relevant entities such as job titles, names, and languages are stored in a local database while the chatbot's text response is used for further interaction.

For our case, the user will be asked questions such as:
1. "What's your name?"
2. "Which languages do you speak?"
3. "What skills do you have?"
4. "What was your last job title?"
5. "What did you do at your last job?"

The benefit of NLU is that we can build a rich context and provide better feedback to the user. Instead of responding with a static script we can make the chatbots responses more dynamic:

Q: "What was your last job title?"
A: "I was a cashier"
Q: "Where did you work as a cashier?"
A: "At SuperMart"
Q: "When did you work at SuperMart?"

## Awards

We won the  [Code For A Cause](http://codeforacause.co/)  Impact Award Challenge: "Build technology that solves a social or environmental problem and positively impacts your local community."

##  Using Rezzi

1. `git clone https://github.com/nikrom17/Rezzi.git rezzi`
2. `cd rezzi/rezzi`
3. `python3 app.py`
4. This will launch the server. Navigate to `http://127.0.0.1:5000`
5. Click on the microphone icon at the bottom and say hello. Then Rezzi will start asking questions.
