"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [
            {
                "id": self._generateId(),
                "first_name": "John",
                "last_name": self.last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generateId(),
                "first_name": "Jane",
                "last_name": self.last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generateId(),
                "first_name": "Jimmy",
                "last_name": self.last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    # ID aleatorio entre 0 y 99,999,999
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        if "id" not in member:
            member["id"] = self._generateId()
        if "last_name" not in member:
            member["last_name"] = self.last_name
        self._members.append(member)

    def delete_member(self, id):
        for index, m in enumerate(self._members):
            if m["id"] == id:
                del self._members[index]
                return True
        return False

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def update_member(self, id, updated_data):
        for member in self._members:
            if member["id"] == id:
                member["first_name"] = updated_data.get("first_name", member["first_name"])
                member["age"] = updated_data.get("age", member["age"])
                member["lucky_numbers"] = updated_data.get("lucky_numbers", member["lucky_numbers"])
                return member
        return None

    def get_all_members(self):
        return self._members
