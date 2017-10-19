class UserModel:

    def __init__(self, user_id, name, join_date=None, last_message_date=None, messages=0, rank='No Rank', active=0, update=False):
        self.user_id = user_id
        self.name = name
        self.join_date = join_date
        self.last_message_date = last_message_date
        self.messages = messages
        self.rank = rank
        self.last_rank = rank
        self.update_rank = False
        self.activity = active
        self.update = update
        self.revised = None

    def add_activity(self):

        if self.activity < 0:
            self.activity = 0
        self.activity += 1
        if self.activity == 5 and self.rank == 'No Rank':
            self.activity = 0
            self.rank = 'User'
            self.update_rank = True
        if self.activity == 10 and self.rank == 'User':
            self.activity = 0
            self.rank = 'User Plus'
            self.update_rank = True

    def sub_activity(self):
        if self.activity > 0:
            self.activity = 0
        self.activity -= 1
        if self.activity == -20 and self.rank == 'User Plus':
            self.activity = 0
            self.rank = 'User'
            self.update_rank = True
        if self.activity == -10 and self.rank == 'User':
            self.activity = 0
            self.rank = 'No Rank'
            self.update_rank = True

    def update_last(self):
        self.last_rank = self.rank
        self.update_rank = False
