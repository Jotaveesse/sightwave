from  .lyrics_search import search_track_by_lyrics
from  .image_describer import get_image_description

def search_track_by_image(image, pool=5):
    description = "a big building in a city"
    tags = ['sky', 'outdoor', 'city', 'background', 'harbor', 'skyscraper']

    # ===========================================================================
    # SÓ DESCOMENTE SE REALMENTE PRECISAR PRA NAO GASTAR OS CREDITOS DA API
    # ===========================================================================
    #(description, tags) = get_image_description(image)

    matched_track = search_track_by_lyrics(f"{description} {' '.join(tags)})", pool, False)

    return matched_track