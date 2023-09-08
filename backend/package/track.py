class Track:
    def __init__(self, query="", title="", artist="", id="",
                 timestamps=None, lyrics=None, matched_section_id=-1,
                 matched_section="", similarity=0):
        self.query = query
        self.title = title
        self.artist = artist
        self.id = id
        self.timestamped_lyrics = timestamps or []
        self.lyrics = lyrics or []
        self.matched_section_id = matched_section_id
        self.matched_section = matched_section
        self.similarity = similarity

    def set_timestamp(self, timestamp):
        self.timestamped_lyrics = timestamp
        self.lyrics = [segment['words'] for segment in self.timestamped_lyrics]
        self.calculate_similarity()
    
    def _jaccard_similarity(set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union

    def calculate_similarity(self):
        query_tokens = set(filter(lambda token: len(token)>2, self.query.split()))

        if(len(query_tokens)==0):
            return
        
        max_similarity = -1
        most_similar_index = -1

        # checks each segment of the lyrics to find which one matches the query most
        for i, string in enumerate(self.lyrics):
            string_tokens = set(string.split())
            similarity = Track._jaccard_similarity(query_tokens, string_tokens)

            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_index = i

        # sets the value of other attributes based on the segment found
        # if index is lower than 1 set to 1
        self.matched_section_id = 1 if (most_similar_index < 1) else most_similar_index
        self.similarity = max_similarity

        # sets the previous, the current and the next segments as the matched section
        self.matched_section = "\n".join(
            self.lyrics[self.matched_section_id-1:self.matched_section_id+2]
        )

    def __str__(self):
        return f"Matched '{self.title}' by '{self.artist}' on {self.timestamped_lyrics[self.matched_section_id]['startTimeMs']} Ms of https://open.spotify.com/track/{self.id}:\n{self.matched_section}"