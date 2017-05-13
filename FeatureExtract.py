import numpy as np
import pandas as pd
from temproal import ppkr_features_t


base_path = 'F:\Study\weiboPredict\data'

print('读取源微博...')
origin = pd.read_csv(base_path + '\WeiboProfile.train',
                     index_col='w_id',
                     sep='\001',
                     encoding='utf-8',
                     quoting=3)
print('读取转发...')
repo = pd.read_csv(base_path + '\\repo_tt.csv',
                   sep='\001',
                   encoding='utf-8',
                   quoting=3).fillna(value='', axis=1)
# 统计总转发量
index,counts = np.unique(repo.w_id.values,return_counts=True)
origin['repo_num'] = pd.DataFrame(data=counts,index=index).reindex(origin.index.values).values
# 只取datetime中的time
origin.time = [t.time() for t in pd.to_datetime(origin.time)]


# 取一周内的转发
repo = repo[repo['arrive_wt']<3600*24*7]

# 统计一周转发量
index,counts = np.unique(repo.w_id.values,return_counts=True)
origin['repo_num_1w'] = pd.DataFrame(data=counts,index=index).reindex(origin.index.values).values

# 取一周内转发不少于75的原微博
origin = origin[origin['repo_num_1w']>=75]
repo = repo[repo['w_id'].isin(origin.index)]
repo.arrive_tt = repo.arrive_tt.astype(int)

# obsobservate size k
k = 75

# 时间特征
t_columns = ['arrive_tt_' + str(i) for i in range(k)]+['max_interval_tt','mean_interval_tt','mean_interval_fhk_tt','mean_interval_lhk_tt']
features_t = pd.DataFrame(index=origin.index, columns=t_columns)

print('开始抽取时序特征, k='+str(k)+' ...')
features_t = features_t.apply(ppkr_features_t,axis=1,repo=repo,k=k)
print('时序特征抽取完成')
features_t.describe()
features_t.head()
print('存储时序特征...')
features_t_path = base_path + '\\features\ppkr_'+str(k)+'_features_t.csv'
features_t.to_csv(features_t_path,
                    index_label='w_id',
                    sep='\001',
                    encoding='utf-8',
                    quoting=3)
print('存储完毕, 路径为: ' + features_t_path)

# TODO: more features






