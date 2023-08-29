from  .lyrics_search import search_track_by_lyrics
from  .image_describer import get_image_description

def search_track_by_image(image, pool=5):
    caption = "a big building in a city"
    tags = ['sky', 'outdoor', 'city', 'background', 'harbor', 'skyscraper']

    # ===========================================================================
    # SÓ DESCOMENTE SE REALMENTE PRECISAR PRA NAO GASTAR OS CREDITOS DA API
    # ===========================================================================
    result = get_image_description(image)

    caption = result.caption.content
    tags= [tag.name for tag in result.tags]

    query =f"{caption} {' '.join(tags)})"
    print(query)
    matched_track = search_track_by_lyrics(query, pool, False)

    return matched_track

print(search_track_by_image("https://akm-img-a-in.tosshub.com/businesstoday/images/story/202307/ezgif-sixteen_nine_531.jpg"))