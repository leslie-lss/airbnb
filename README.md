# airbnb
爬取airbnb的房源信息及评价信息，并存入mongodb中

# 网站分析

## 房源网址列表
https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&map_toggle=false&s_tag=Yz8-d_Fe&section_offset=5&items_offset=18

每页有18条房源信息，大约只显示17页，共300多条房源

利用xpath可以提取到相应的房源的链接，如：/room/xxxxxx，后边的xxxxxx是房源的id号码，唯一

## 房源信息：

利用开发者工具分析后发现它返回有json格式的房源的全部信息，直接利用下边这个网址来获取房源的json信息：

https://zh.airbnb.com/api/v2/pdp_listing_details/443684?_format=for_rooms_show&request_url=https%3A%2F%2Fzh.airbnb.com%2Frooms%2F443684&&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&

选取其中的部分信息来进行保存。

## 评论信息

房源中的评论是异步加载的，但是同样也返回了相应的json信息，相应网址如下：

https://zh.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=zh&listing_id=443684&role=guest&_format=for_p3&_limit=7&_offset=7&_order=language_country

每页只显示7条评论，通过offset来控制：0、7、14、21、28、35……
