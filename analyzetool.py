import re
import linecache


class RelationFinder(object):

    def __init__(self, path = 'F:\\Study\\weiboPredict\\data\\weibo_dc_parse2015_link_filter'):
        self.__path = path

    # 在文件中逐行匹配，并返回符合条件的行
    def __find_lines(self, token):

        pattern = re.compile(token)
        f = open(self.__path,encoding='utf-8')

        for line in f:
            match = pattern.match(line)
            if match:
                yield list(map(int,line.replace('\t','\001').replace('\n','').split('\001')))
        f.close()

    mode_find_all = 0
    mode_find_sub = 1
    mode_find_fans = 2

    def __token_generator(self, id_list, mode):

        token = r''
        if mode == 0:
            for id in id_list:
                token += r'.*' + str(id) + r'.*|'
            token = token[:len(token) - 1]
        if mode == 1:
            for id in id_list:
                token += r'^' + str(id) + '\s.*|'
            token = token[:len(token) - 1]
        if mode == 2:
            for id in id_list:
                token += '.*\s' + str(id) + '\001.*|' \
                      + '.*\001' + str(id) + '\001.*|' \
                      + '.*\001' + str(id) + '\n|'
            token = token[:len(token) - 1]
        return  token



    def find_user_relations(self, id_list, mode):

        token = self.__token_generator(id_list,mode)
        lines = self.__find_lines(token)
        lines = list(lines)
        print(len(lines),'lines matched:')
        print(lines)
        return lines



f = open('F:\\Study\\weiboPredict\\data\\weibo_dc_parse2015_link_filter', encoding='utf-8' )
f2 = open('F:\\Study\\weiboPredict\\data\\adjlist.csv', encoding='utf-8',mode='w')
for line in f:
    line = line.replace('\t', ',').replace('\001',',')
    f2.write(line)
f.close()