import requests
from pprint import pprint


with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()


class VKinder:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def users_search(self, version, af, at, s, c, st,hph):
        search_url = self.url + 'users.search'
        self.token = token
        self.version = version
        params = {
            'age_from': af,
            'age_to': at,
            'sex': s,
            'city': c,
            'status': st,
            'has_photo': hph,
            'count': 5,
            'fields': 'bdate, city, relation, sex'
        }
        res = requests.get(search_url, params={**self.params, **params})
        return res.json()

    def get_all_photos(self, vk_id):
        photos_url = self.url + 'photos.get'
        params = {
            'owner_id': vk_id,
            'count': 5, #переменная
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'photos': 1,
        }
        res = requests.get(photos_url, params={**self.params, **params})
        return res.json()

    def candidates_list(self):
        candidates_list = []
        candidates = self.users_search('5.130', 25, 30, '2', '1', '1', '1')['response']['items']
        for candidate in candidates:
            candidate_dict = {}
            photo_list = []
            vk_id = candidate['id']
            candidate_dict['vk_id'] = vk_id
            candidate_dict['first_name'] = candidate['first_name']
            candidate_dict['last_name'] = candidate['last_name']
            candidate_dict['sex'] = candidate['sex']
            candidate_dict['bdate'] = candidate['bdate']
            if 'city' in candidate.keys():
                candidate_dict['city'] = candidate['city']['title']
            else:
                continue
            if 'relation' in candidate.keys():
                candidate_dict['status'] = candidate['relation']
            else:
                continue
            candidate_dict['profile_url'] = f'https://vk.com/id{vk_id}'
            photos = self.get_all_photos(vk_id)['response']['items']
            for photo in photos:
                photo_dict = {}
                # url = photo['sizes'][-1]['url']
                owner_id = photo['owner_id']
                photo_id = photo['id']
                photo_dict['url'] = f'photo{owner_id}_{photo_id}'
                photo_dict['likes'] = photo['likes']['count']
                # photo_dict['date'] = datetime.utcfromtimestamp(int(photo['date'])).strftime('%Y-%m-%d %H-%M-%S')
                # photo_dict['file_name'] = f'{photo_dict["likes"]}_{photo_dict["date"]}'
                photo_list.append(photo_dict)
                candidate_dict['photos'] = photo_list
            candidates_list.append(candidate_dict)
        return candidates_list


# vk = VKinder(token, '5.130')
# pprint(vk.get_all_photos('53890585'))

