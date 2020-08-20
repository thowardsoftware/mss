__author__ = "christopherdavidson"

import uuid
from common.database import Database

#############################################
# ROOM CLASS: Keeps track of Rooms available for meetings
#############################################

class Room(object):

    def __init__(self, meetings, roomNum, _id=None):
        self.meetings = dict() if meetings is None else meetings
        self.roomNum = None if roomNum is None else roomNum
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
         return {
             'meetings': self.meetings,
             'roomNum': self.roomNum,
             '_id': self._id
         }

    #### INSTANCE METHODS ####
    def save_to_mongo(self):
        Database.insert(collection='room', data=self.json())

    def get_room_number(self):
        return self.roomNum

    #### CLASS METHODS ####
    @classmethod
    def delete_room_base(cls, room_id):
        Database.remove_one(collection='room', searchVal=room_id)

    @classmethod
    def get_from_mongo(cls, id):
        room = Database.find_one('room', {'_id': id})
        if room is not None:
            return cls(**room)
        return False

    # UPDATE MEMBERS OF MEETING
    @classmethod
    def update_meetings(cls, room_id, newKey, newVal):
        if room_id is not None:
            Database.update_meeting(room_id, newKey, newVal)
            return True
        return False

    ########## Find Room by Meeting ID #############
    @classmethod
    def find_by_meeting(cls, meeting_id, searchKey):
        room = Database.find_one('room', {'meetings.'+searchKey: meeting_id})
        if room is not None:
            return cls(**room)
        return False

    @classmethod
    def erase_meeting(cls, searchKey, room_id):
        Database.erase_replace_meeting_from_room(room_id=room_id, newKey=searchKey)
