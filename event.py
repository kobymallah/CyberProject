class Event:

    LOST_COMMUNICATION = 'LOST_COMMUNICATION'
    RISK_CHANGE = 'RISK_CHANGE'
    SHOT_DOWN = 'SHOT_DOWN'
    DAMAGED = 'DAMAGED'

    def __init__(self, event_type, entities, entities_attributes=None):
        """
        Initialize an event with the given arguments. Depending on the event type,
         the entities_attributes can be discarded
        :param event_type: the type of event, the possible values are defined above
        :param entities: the entities involved in this event
        :param entities_attributes: the attributes that are changed after the event
        """
        self.type = event_type
        self.entities = entities
        self.entities_attributes = entities_attributes
