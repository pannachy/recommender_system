from datetime import datetime
import hashlib
import os
import pandas as pd
import pickle
from sqlalchemy import create_engine

'''
выгрузка моделей и фичей из базы, получение предсказаний
'''


# функция загрузки модели из рабочей директории

def load_models():
    model_path_test = r"/models/model_test.pkl"
    model_test = pickle.load(open(model_path_test, 'rb'))

    model_path_control = r"/models/model_control.pkl"
    model_control = pickle.load(open(model_path_control, 'rb'))

    return model_test, model_control


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 500_000
    engine = create_engine(
        "postgresql://user:password@host:dbname"
    )
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)

# функция загрузки признаков из БД
def load_features():  # -> pd.DataFrame
    query_load_user = f"SELECT * FROM chann_user_features_lesson_10"
    user_features = batch_load_sql(query_load_user)

    query_load_post = f"SELECT * FROM chann_post_features_lesson_10"
    post_features = batch_load_sql(query_load_post)

    query_liked_post = f"SELECT DISTINCT user_id, post_id from public.feed_data WHERE action = 'like'"
    liked_posts = batch_load_sql(query_liked_post)

    return user_features, post_features, liked_posts


# загрузка фичей и модели из БД

user_features, post_features, liked_posts = load_features()
model_test, model_control = load_models()


# определение тестовой группы пользователя + константы

SALT = 'my_super_salt'
GROUPS_DIV = 100

def get_exp_group(id: int) -> str:
    value_str = str(id) + SALT
    value_num = int(hashlib.md5(value_str.encode()).hexdigest(), 16)
    percent = value_num % GROUPS_DIV
    if percent < 50:
        return "control"
    elif percent < 100:
        return "test"
    return "unknown"


#  функция предсказания

def get_recommended_posts(id: int, time: datetime, limit: int):
    exp_group = get_exp_group(id)
    if exp_group == 'test':
        model = model_test
    elif exp_group == 'control':
        model = model_control
    else:
        raise ValueError('unknown group')

    all_ids = user_features.user_id.values

    if id in all_ids:
        # загружаем user_features, мерджим c post_features
        features_for_preds = user_features[user_features.user_id == id] \
            .merge(post_features, how='cross') \
            .drop('user_id', axis=1)

        # добавляем фичи времени
        features_for_preds['hour'] = time.hour
        features_for_preds['day_of_week'] = time.weekday()

        # делаем предсказания
        predictions = pd.Series(model.predict_proba(features_for_preds.drop('post_id', axis=1))[:, 1])

        # выбираем limit лучших, сохраняем в список
        best_posts = features_for_preds.join(predictions.rename('preds'))[['post_id', 'preds']] \
                        .sort_values(by='preds', ascending=False)[:limit] \
                        .drop('preds', axis=1)
        best_posts = best_posts['post_id'].tolist()

    else:
        best_posts = liked_posts.groupby('post_id').count().sort_values(by='user_id')[-limit:].reset_index().post_id.values

    return best_posts, exp_group