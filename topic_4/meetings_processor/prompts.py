PARTICIPANTS_EXTRACTOR = """
    You are a helpful assistant that extracts the participants from a meeting transcript. 
    The participants are the people who take part in the meeting.
    Your task is to identify and list the participants mentioned in the transcript.
    Write the names of the participantes in a list format, without any additional text or explanation.

    Meeting transcript: {transcript}
"""

TOPICS_EXTRACTOR = """
    You are a helpful assistant that extracts the topics discussed in a meeting transcript.
    You have to identify and out put as a list the topics mentioned in the meeting.
    Avoid too general or too specific categories.

    Meeting transcript: {transcript}
"""

ACTIONS_ITEMS_EXTRACTOR = """
    You are a helpful assistant that extracts the action items from a meeting transcript.
    Your task is to identify and list the action items mentioned in the transcript and assign each
    of them to a given participant. Notice not only the explicit tasks but also the implicit ones.
    The action items should be output as a dictionary where the keys are the action 
    items and the values are the participants responsible for them.

    Meeting transcript: {transcript}
    Participants: {participants}
"""

RECORD_GENERATOR = """
    You are a helpful assistant that generates a record of a meeting based on the transcript.
    Your task is to create a record that summarizes the key points and decisions made during the meeting.
    The maximum amount of words that the record can have is 150.

    Meeting transcript: {transcript}
"""

SUMMARY_GENERATOR = """
    You are a helpful assistant that generates a summary of a meeting based on the transcript.
    Your task is to create a summary that provides an overview of the meeting.
    The maximum amount of words that the summary can have is 30.
    
    Meeting transcript: {transcript}"""