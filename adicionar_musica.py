import painel
import requests
from bs4 import BeautifulSoup
import pickle

def generate_mp3(youtube_url, nome_arquivo):
    url = 'https://www.easymp3converter.com/models/convertProcess.php'
    payload = { 'type': 'mp3',
                'search_txt': youtube_url
                }
    r = requests.post(url, data=payload)
    soup = BeautifulSoup(r.content,'html.parser')
    link = soup.find_all('option')[-1].get('data-link')
    duration = soup.find(class_='video_duration').string
    minutos, segundos = duration.split(':')
    length = int(minutos) * 60 + int(segundos)
    song_data = '1:'+nome_arquivo.split('_')[-1]+','+str(length)
    return  download_mp3(link, nome_arquivo), song_data, nome_arquivo
    
        

def download_mp3(link, nome_arquivo):
    r = requests.get(link, stream=True, verify=False)
    path = 'temp/' + nome_arquivo + '.mp3'
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=None):
            f.write(chunk)
    return path


def get_file_number():
    with open('music_ids', 'rb') as f:
        file_number, song_id, furni_id = pickle.load(f)
        file_number += 1
        with open('music_ids', 'wb') as w:
            pickle.dump((file_number, song_id, furni_id), w)
    return str(file_number)


def get_song_id():
    with open('music_ids', 'rb') as f:
        file_number, song_id, furni_id = pickle.load(f)
        song_id += 1
        with open('music_ids', 'wb') as w:
            pickle.dump((file_number, song_id, furni_id), w)
    return str(song_id)


def get_furni_id():
    with open('music_ids', 'rb') as f:
        file_number, song_id, furni_id = pickle.load(f)
        furni_id += 1
        with open('music_ids', 'wb') as w:
            pickle.dump((file_number, song_id, furni_id), w)
    return str(furni_id)


#print(get_file_number(), get_song_id(), get_furni_id())
def update_ids(file_number, song_id, furni_id):
    with open('music_ids', 'wb') as f:
        pickle.dump((file_number, song_id, furni_id), f)



if __name__ == '__main__':
    update_ids(1247, 182, 69430)
    '''nome_musica, artista = 'Blood Eagle', 'Wardruna'
    mp3, song_data, nome_arquivo = generate_mp3('https://www.youtube.com/watch?v=nsHb6Ycu51M', f"sound_machine_sample_{get_file_number()}")
    painel.login()
    painel.adicionar_musica(mp3, song_data, nome_arquivo, nome_musica, artista, get_song_id(), get_furni_id())'''

