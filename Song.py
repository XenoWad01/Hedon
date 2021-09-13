class Song:
    def __init__(self, data, played_by):
        self.url = data.get("url", None)
        self.name = data.get("title", None)
        self.youtube_id = data.get('id', None)
        self.played_by = played_by
    def __str__(self):
        return f"**Song:** {self.name}\n**URL:** 'https://www.youtube.com/watch?v={self.youtube_id}',\n**Played by:** *{self.played_by}*"
