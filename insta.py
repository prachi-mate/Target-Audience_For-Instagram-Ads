#importing libraries
import pandas as pd
from pandas.io.json import json_normalize
from InstagramAPI import InstagramAPI
import time

#LOGIN
def login_to_instagram(username, password):
    api = InstagramAPI(username, password)
    api.login()
    return api

api = login_to_instagram('enter_your_username_here','enter_your_password_here')

#Retriving Posts
def get_my_posts(api):
    '''Retrieve all posts from own profile'''
    my_posts = []
    has_more_posts = True
    max_id= ''

    while has_more_posts:
        api.getSelfUserFeed(maxid=max_id)
        if api.LastJson['more_available'] is not True:
            has_more_posts = False #stop condition

        max_id = api.LastJson.get('next_max_id','')
        my_posts.extend(api.LastJson['items']) #merge lists
        time.sleep(2) # slows down to avoid flooding

        if has_more_posts:
            print(str(len(my_posts)) + ' posts retrieved so far...')

    print('Total posts retrieved: ' + str(len(my_posts)))
    
    return my_posts
    len(my_posts)
    my_posts[2]

my_posts = get_my_posts(api)

#Retrive Post Likers
def get_posts_likers(api, my_posts):
    '''Retrieve all likers on all posts'''
    
    likers = []
    
    print('wait %.1f minutes' % (len(my_posts)*2/60.))
    for i in range(len(my_posts)):
        m_id = my_posts[i]['id']
        api.getMediaLikers(m_id)
        
        likers += [api.LastJson]
        
        # Include post_id in likers dict list
        likers[i]['post_id'] = m_id
        
        time.sleep(2)
    print('done')
    
    return likers


likers = get_posts_likers(api, my_posts)


#Likers to pandas df
def posts_likers_to_df(likers):
    '''Transforms likers list of dicts into pandas DataFrame'''
    
    # Normalize likers by getting the 'users' list and the post_id of each like
    df_likers = json_normalize(likers, 'users', ['post_id'])
    
    # Add 'content_type' column to know the rows are likes
    df_likers['content_type'] = 'like'
    
    return df_likers

df_likers = posts_likers_to_df(likers)

print('Total posts: ' + str(len(my_posts)))
print('---------')
print('Total likes on profile: ' + str(df_likers.shape[0])) #shape[0] represents number of rows
print('Distinct users that liked your posts: ' +str(df_likers.username.nunique())) # nunique() will count distinct values of a col
print('---------')


#Top 30 likers
df_likers.username.value_counts()[:30]
df_likers.username.value_counts()[:30].plot(kind='bar', title='Top 30 media likers', grid=True, figsize=(12,6))
df_likers.username.value_counts()[:30].plot(kind='pie', title='Top 30 media likers distribution', autopct='%1.1f%%', figsize=(12,6))



#how many of my topfans are female ?

import pandas

df=pd.read_csv("C:\\Users\\prach\\OneDrive\\Desktop\\COLLEGE\\TY\\Machine Learning\\Project\\instadata.csv")

df.head()

#SVM
x=df.drop("label", axis=1)
x=x.drop("location", axis=1)
x=x.drop("gender",axis=1)
x=x.drop("id",axis=1)
y=df["label"]

from sklearn.model_selection import train_test_split
x_train,x_test,y_train, y_test = train_test_split(x,y, test_size=0.4)
z=list(y_train)
ytest=list(y_test)

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

svclassifier = SVC(kernel='linear')
svclassifier.fit(x_train,z)
output=list(svclassifier.predict(x_test))
output

accs=accuracy_score(ytest,output)
print("Accuracy score=", accs)


#Testing Unknown Data
df1=pd.read_csv("C:\\Users\\prach\\OneDrive\\Desktop\\COLLEGE\\TY\\Machine Learning\\Project\\instatest.csv")

p=df1.drop("location", axis=1)
p=p.drop("gender",axis=1)
p=p.drop("id",axis=1)

output=list(svclassifier.predict(p))
predicted=list(output)

ids=list(df1["id"])
print("id       class");

for x in range(0,len(predicted)):
    print(ids[x] +"    ------>   " +predicted[x])


