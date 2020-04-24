# Find_Love_MusicCloud
这是一个然并卵的项目。
可以查找Ta在网易云音乐评论，通过用户收藏和创建的歌单下所有歌曲的评论中查找到TA的评论。可以尽情满足我们的窥探欲望，从而使我们心有戚戚，立即升仙。
使用本源码造成的任何感情伤害概不负责。
This project is useless.
you can find his/her commones on MusicCloud By his/her playlists and its songs。So you are a pussy。
This Source is not to harm ,but make the world a better place. 
示例：

![preview](https://static.perhamer.com/img/music_cloud_demo.png)

# musicCloud获取用户评论
    由于数据量的问题，仅提供查询用户所有歌单及收藏的歌单下所有歌曲的评论
    待优化：只查询用户注册时间之后的评论
	需要下载chromeDriver.exe

执行顺序

    1、playlist_by_user.py 输入用户ID查找用户创建的、收藏的歌单
    2、musics_by_playlist.py 获取上一步歌单下的所有歌曲
    3、comment_by_music.py 获取上一步歌曲下的所有评论并筛选
    
    
# sql init:


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `music_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reply_comment_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '回复的评论id',
  `reply_content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `liked_count` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `comment_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
-- Table structure for playlist_music
-- ----------------------------
DROP TABLE IF EXISTS `playlist_music`;
CREATE TABLE `playlist_music`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `playlist_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `music_id` bigint(255) NOT NULL,
  `music_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `playlist_id`, `music_id`) USING BTREE,
  INDEX `playlist_id`(`playlist_id`, `music_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4442 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;


-- ----------------------------
-- Table structure for user_playlist
-- ----------------------------
DROP TABLE IF EXISTS `user_playlist`;
CREATE TABLE `user_playlist`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `playlist_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `playlist_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `user_id`, `playlist_id`) USING BTREE,
  INDEX `user_id`(`user_id`, `playlist_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 62 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
