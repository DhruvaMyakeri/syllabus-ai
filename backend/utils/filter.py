def is_relevant(video, query):
    title = video["title"].lower()
    query_words = query.lower().split()

    match_count = sum(1 for w in query_words if w in title)

    # at least 1-2 important words must match
    return match_count >= max(1, len(query_words)//2)