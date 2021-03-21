# EMOTIONS
SIMPLE_EMOTIONS = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
COMPLEX_EMOTIONS = ['alert', 'tired', 'non_vigilant']

singled_responses = {
    'anger': [
        "Maybe talking to a friend would help out?",
        "Shall we take a short break, maybe that would ease things out?"
    ],
    'contempt': [ 
        "In contempt......."
    ],
    'fear': [
        "We hope everything is alright!",
        "Discussing & talking about problems gives us a peace of mind."
    ],
    'disgust': [
        "Try switching to something different?",
        "Oof! That might have been something hard to watch!",
        "Ewwww !??? That's what we thought too!"
    ], 
    'happiness': [
        "Studies show that our bodies relax out when we get happy!",
        "Kudos! Glad to see that smile!",
        "Woah! Keep it up!"
    ], 
    'neutral': [
        "We can't really comprehend anything, maybe everything's just normal?",
        "Hmmmmmmmmmmmmmmmmm"
    ],
    'sadness': [
        "Feeling low? We've all been there! Take a moment to appreciate what you see",
        "Ahhhh that sucks, Just let it all go, relax and connect with your own being",
        "I know something that always cheers me up, give a call to that old friend you haven't talked to for a while"
    ],
    'surprise': [
        "WOOOOOAAAAAAHHH!!!",
        "Surprise! Surprise!"
    ],
    'tired': [
        "Oooof!!!! You seem a bit overworked! Maybe take a break?",
        "Plan of action: For now just relax and listen to some music",
        "Feeling Tired how about some coffee or a power nap?"
    ],
    'alert': [
        "Glad to see someone so engrossed in their work!", 
        "We notice some serious concentration! Keep it up!"
    ],
    'non_vigilant': [
        "Feeling a bit distracted ?",
        "Are we going off track ? Let's pause and figure that out!"
    ]
}

coupled_responses = {
	('anger', 'contempt'): '', 
	('anger', 'disgust'): 'Woah! We recommend you to chill out a bit!', 
	('anger', 'fear'): '', 
	('anger', 'happiness'): 'I cant comprehend what you are going through right now!', 
	('anger', 'neutral'): '', 
	('anger', 'sadness'): '', 
	('anger', 'surprise'): 'I cant comprehend what you are going through right now!', 
	('anger', 'alert'): '', 
	('anger', 'tired'): '', 
	('anger', 'non_vigilant'): '', 
	('contempt', 'disgust'): '', 
	('contempt', 'fear'): '', 
	('contempt', 'happiness'): '',
	('contempt', 'neutral'): '',
	('contempt', 'sadness'): '',
	('contempt', 'surprise'): '',
	('contempt', 'alert'): '',
	('contempt', 'tired'): '',
	('contempt', 'non_vigilant'): '',
	('disgust', 'fear'): '',
	('disgust', 'happiness'): '',
	('disgust', 'neutral'): '',
	('disgust', 'sadness'): '',
	('disgust', 'surprise'): '',
	('disgust', 'alert'): '',
	('disgust', 'tired'): '',
	('disgust', 'non_vigilant'): '',
	('fear', 'happiness'): '',
	('fear', 'neutral'): '',
	('fear', 'sadness'): '',
	('fear', 'surprise'): '',
	('fear', 'alert'): '',
	('fear', 'tired'): '',
	('fear', 'non_vigilant'): '',
	('happiness', 'neutral'): '',
	('happiness', 'sadness'): '',
	('happiness', 'surprise'): '',
	('happiness', 'alert'): '',
	('happiness', 'tired'): '',
	('happiness', 'non_vigilant'): '',
	('neutral', 'sadness'): '',
	('neutral', 'surprise'): '',
	('neutral', 'alert'): '',
	('neutral', 'tired'): '',
	('neutral', 'non_vigilant'): '',
	('sadness', 'surprise'): '',
	('sadness', 'alert'): '',
	('sadness', 'tired'): '',
	('sadness', 'non_vigilant'): '',
	('surprise', 'alert'): '',
	('surprise', 'tired'): '',
	('surprise', 'non_vigilant'): '',
	('alert', 'tired'): '',
	('alert', 'non_vigilant'): '',
	('tired', 'non_vigilant'): ''
}