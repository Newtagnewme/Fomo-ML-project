import requests
import os 
import shutil

sub_generes = {
    "Reggaeton" : ["Reggaeton", "Alternative Reggaeton", "Bachatón", "Cubaton", "Neoperreo", "Moombahton", "Trapeton"],
    "House" : [ "Acid House","Chicago House","Deep Deep House","Deep House","Electro House","Funky House","Progressive House","Tech House","Vocal House"],
    "Rock": ["Abstractro","Acid Rock","Album Rock","Alternative Rock","Art Rock","Classic Rock","Dance Rock","Folk Rock","Glam Rock","Indie Rock","Math Rock","Pop Rock","Prog Rock","Punk Rock","Rock Steady","Rockabilly","Soft Rock","Soul Christmas"],
    "Blues": ["Acoustic Blues","Blues Rock","Delta Blues","Electric Blues","Jazz Blues","Louisiana Blues","Piano Blues","Traditional Blues"],
    "Jazz" : ["Acid Jazz","Avant-garde Jazz","Electro Jazz","Free Jazz","Funk Jazz","Gypsy Jazz","Jazz Fusion","Jazz Metal","Jazz Trio","Soul Jazz"],
    "Classical": ["Classical Christmas","Classical Performance","Classical Period","Modern Classical"],
    "Country": ["Alternative Country","Americana Country","Bluegrass Country","Country Blues","Country Dawn","Country Gospel","Country Rock","Outlaw Country","Traditional Country"],
    "Electronic": ["Electronic","Electronicore"],
    "Pop": ["Acid Pop","Dance Pop","Deep Pop Punk","Indie Pop","K-pop","Pop Punk","Pop Rap","Power-pop Punk","Spanish Pop"],
    "Metal": ["Alternative Metal","Black Metal","Death Metal","Doom Metal","Groove Metal","Heavy Metal","Metalcore","Progressive Metal","Speed Metal","Thrash Metal"],
    "Techno": ["Acid Techno","Dark Minimal Techno","Deep Tech House","Dub Techno","Minimal Techno","Techno"],
    "Hip-Hop": ["Abstract Hip Hop","Alternative Hip Hop","East Coast Hip Hop","Hardcore Hip Hop","Hip Hop","West Coast Rap"],
    "Reggae": ["Reggae Fusion","Reggae Rock","Rock Steady"],
    "Soul": ["Acid Jazz","Blue-eyed Soul","Deep Soul House","Neo Soul","Northern Soul","Soul Jazz"],
    "Punk": ["Anarcho-punk","Crust Punk","Folk Punk","Hardcore Punk","Indie Punk","Punk Blues","Punk Rock","Ska Punk"],
    "Folk": ["Alternative Folk","British Folk","Folk Metal","Folk Punk","Folk Rock","Indie Folk","Neofolk","Traditional Folk"],
}

DATASET_PATH = "..."


def generate_spotify_token():
    data = {
        'grant_type': '',
        'client_id': '',
        'client_secret': '',
    }   

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    if response.status_code != 200:
        print(f"Failed to generate token, status code {response.status_code}")
        return None
    
    j = response.json()
    return j["access_token"]

def make_request():
    token = generate_spotify_token()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}" 
    }

    for g, sg in sub_generes.items():
        print(f"Downloading images for genre {g}")
        for s in sg:
            url = f"https://api.spotify.com/v1/search?q={s}&type=track"
            response = requests.get(url, headers=headers)
            if response.status_code == 401:
                print("[FATAL] Token expired, exiting")
                os.exit(1)

            if response.status_code != 200:
                print(f"Request failed with status code {response.status_code} for genre {g} and subgenre {s}")
                continue

            j = response.json()
            tracks = j["tracks"]["items"]
            for track in tracks: 
                image = track["album"]["images"][1]["url"] #we get the 1 because it's the 300x300 image
                if download_image(image, f"{DATASET_PATH}/{g}/{track['id']}.jpg"): 
                    print(f"Downloaded image for {track['name']} and saved in {DATASET_PATH}/{g}/{track['id']}.jpg")

def download_image(url, destination):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        return True
    else:
        print(f"failed to download image, status code {response.status_code}")
        return False

if __name__ == "__main__":
    make_request()