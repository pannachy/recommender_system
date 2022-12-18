# Рекомендательная система на основе контентного подхода

Проект представлет собой разработку рекомендательной системы для постов юзерам симулированной социальной сети.
Алгоритм: на вход подается id пользователя, нужно выдать в ответ 5 постов, наиболее релевантных для данного юзера.

Входные данные представляют собой три датасета: /n
```
*user_data* - описание юзеров (id, пол, возрастб город, страна и др., /n
*post_text_df* - описание постов (id, текс, топик (тема)), /n
*feed_post* - содержит историю о просмотренных постах для каждого юзера в изучаемый период (id юзера, id поста, действие (лайк/просмотр), таргет (1 у просмотров, если почти сразу после просмотра был совершен лайк, иначе 0. У действий like пропущенное значение.)
```
Файл __recommend_system_EDA+FI__ - это джупитер ноутбук, содержащий разведовательный анализ данных, генерирование новых фичей на основе текущих данных и текста,
обучение и оценку модели

Файл __database.py__ - код поделючения к базе данных

Файл __schemas.py__ - модели pydentic

Файл __model.py__ - модели SQLAlchemy

Файл __endpoint.py__  - ендпойнт: получаем в качестве запроса id пользователя, формируем фичи для модели, отдаем ей на предсказание, затем возвращаем предсказания и № группы для A/B тестирования


