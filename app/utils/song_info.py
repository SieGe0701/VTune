import pprint

def extract_song_info(api_response):
    try:
        metadata = api_response['metadata']
        
        # Check if it's a music or humming response
        if 'music' in metadata:
            first_result = metadata['music'][0]
        elif 'humming' in metadata:
            first_result = metadata['humming'][0]
        else:
            return None
            
        title = first_result['title']
        artist = first_result['artists'][0]['name']
        
        return {
            'title': title,
            'artist': artist
        }
        
    except Exception as e:
        return {
            'title': 'Error processing response',
            'artist': 'Error processing response',
            'error': str(e)
        }