from  lyrics_searcher import get_matching_tracks
import image_describer
import sys

def main(image):
    description = "a big building in a city"
    tags = ['sky', 'outdoor', 'city', 'background', 'harbor', 'skyscraper']

    # ===========================================================================
    # SÓ DESCOMENTE SE REALMENTE PRECISAR PRA NAO GASTAR OS CREDITOS DA API
    # ===========================================================================
    #(description, tags) = image_describer.get_image_description(image)
    
    if(description == None):
        return
    
    # just testing 3 different methods to see whats better
    matched_track_by_desc = get_matching_tracks(description, 4, False)
    matched_track_by_tags = get_matching_tracks(" ".join(tags), 4, False)
    matched_track_by_both = get_matching_tracks(f"{description} {' '.join(tags)})", 4, False)

    print('\nDescription Match')
    print(matched_track_by_desc)
    print('\nTag Match')
    print(matched_track_by_tags)
    print('\nBoth Match')
    print(matched_track_by_both)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python image_to_lyrics.py <image_url>")
        main("https://cdn.britannica.com/73/114973-050-2DC46083/Midtown-Manhattan-Empire-State-Building-New-York.jpg")
    else:
        image = sys.argv[1]
        main(image)