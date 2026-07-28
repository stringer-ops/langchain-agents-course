from pydantic import BaseModel, Field

class Participants(BaseModel):
    """names of the participants that appear in a meeting"""
    participants: list[str] = Field(description="List of names of teh participants. E.g ['Louis', 'Paola']")

class Topics(BaseModel):
    """Topics of the different tasks or things that are discussed in the meeting"""
    topics: list[str] = Field(description="List of the different topics. E.g ['Adding new use case mortages for banking', 'Calling the manager']")

class ActionItem(BaseModel):
    """Actions that is going to be taken by one or several participants"""
    action: str = Field(description="Task that is going to be performed")
    participants: list[str] = Field(description="Participants that will perform the task")

class ActionsItems(BaseModel):
    """Actions that are going to be taken by participants of the meeting"""
    actions_items: list[ActionItem] = Field(description="""List that contains the actions taken by one or more participants.
        E.g [
            {'Calling the manager': ['Louis']},
            {'Writing meeting record': ['Paola', 'Sarah']}
        ]""")

