# -*- coding: utf-8 -*-
"""
说明：次定义的一级分发词库可自行根据各自模块的需求进行修改、库命名形式为 业务_lib.
"""
domain_atmosphere_lib = ['氛围灯', '颜色', '亮度', '气氛', '氛围', '亮一点', '暗一点']
domain_phone_lib = ['电话', '呼叫', "回电话", "拨打"]
domain_dis_phone_lib = ['座椅', '加热', '通风', '空调', '温度', '度', 'pm2.5', "音乐"]
domain_air_conditioners_lib = ['空调', '风速', '风扇', '暖风', '冷风']
domain_moon_roof_lib = ['天窗', '星星', '太阳', '月亮', '打开天窗说亮话']
domain_shade_screens_lib =['遮阳帘', '天窗遮阳', '遮阳网', '遮阳布', '遮阳板',  '遮光板']
domain_seat_lib = ['座椅', '座位', '主驾', '主驾驶', '副驾', '副驾驶', '驾驶座']
domain_music_lib = ['音乐', '听音乐','播放', '来首', '我想听', '听', '我要听', 'U盘', 'u盘', '蓝牙音乐', '歌曲', '放', '来一首', '一首',
                    '放首', '放一首', '帮我找一下', '帮我放一首', '播放歌曲', '请播', '主题曲', '片头曲', '片尾曲', '钢琴曲', '插曲', '请放',
                    '上一首', '上一曲', '下一首', '下一曲']
domain_novel_lib = ['小说']
domain_radio_lib = ['调频', 'FM', 'fm', '收音机', 'am', '99']
domain_navigation_lib = ['导航', '想去', '想到', "渴了", '饿了', '想喝水']
soc_lib = ['soc']
domain_energy_lib = ['能量']
domain_total_libs = domain_atmosphere_lib + domain_air_conditioners_lib + domain_moon_roof_lib + \
                    domain_shade_screens_lib + domain_seat_lib + domain_phone_lib + domain_music_lib + \
                    domain_novel_lib + domain_navigation_lib + domain_radio_lib + soc_lib + domain_energy_lib
