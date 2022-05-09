import discord


class Queue:
    def __init__(self):
        print('Queue initiated')
        self.queue = []

    def get_current(self):
        return self.queue[len(self.queue)-1]

    def get_next(self):
        next_song = self.queue[len(self.queue)-2]
        return next_song

    def cycle_next(self):
        self.queue.pop()
        if not self.isEmpty():
            return self.queue[len(self.queue)-1]
        else:
            return None


# hahahah




    def add(self, song):
        self.queue.append(song)

    def clear(self):
        self.queue = []

    def isEmpty(self):
        if len(self.queue) == 0:
            return True
        return False

    def __str__(self):
        if not self.isEmpty():
            s = "__**Queue:**__\n"
            s += '<I===========================================II\n'
            for song in self.queue:
                s += str(song) + '\n'
                s += '<I===========================================II\n'
            return s
        else:
            return "Queue is empty"
