# 获取用户所有歌单的音乐
import time

import sql
from chromedriver import get_driver


def save_musics_by_playlist(playlist_id, driver):
    try:
        driver.get('https://music.163.com/playlist?id=' + str(playlist_id))
        # time.sleep(1 + random.random())
        driver.switch_to.frame('g_iframe')
        songs = driver.find_elements_by_xpath('//*[@class="txt"]/a')
        musics = {}
        for song in songs:
            link = song.get_attribute('href')
            song_id = link[str(link).find('=') + 1:]
            song_name = song.find_element_by_tag_name('b').get_attribute('title')
            musics[song_id] = song_name
        sql.insert_playlist_music(playlist_id, musics)
        print('保存歌单成功：playlist_id:' + str(playlist_id))

    except Exception as e:
        print(e)
        driver.quit()
        return


def get_musics_by_user(user_id):
    driver = get_driver()
    playlist_id_list = sql.get_playlists(user_id)
    for playlist_id in playlist_id_list:
        save_musics_by_playlist(playlist_id['playlist_id'], driver)
    print('所有歌单保存完毕,user:' + str(user_id))


if __name__ == '__main__':
    start = time.time()
    get_musics_by_user(11111)
    cost = (time.time() - start)
    print('耗时：' + str(cost) + '秒')
