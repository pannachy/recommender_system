# Рекомендательная система на основе контентного подхода

Проект представлет собой разработку рекомендательной системы для постов юзерам симулированной социальной сети.

### Алгоритм: 
На вход подается id пользователя, нужно выдать в ответ 5 постов, наиболее релевантных для данного юзера.

### Входные данные 
<details>
<summary>Описание базы данных</summary>

| Таблица     | Описание                                                                                                          |
|------------:|-------------------------------------------------------------------------------------------------------------------|
|user_data    | описание юзеров (id, пол, возрастб город, страна и др.                                                            |
|post_text_df | описание постов (id, текс, топик (тема))                                                                          |
|feed_post    | содержит историю о просмотренных постах для каждого юзера в изучаемый период (id юзера, id поста, действие (лайк/просмотр), таргет (1 у просмотров, если почти сразу после просмотра был совершен лайк, иначе 0. У действий like пропущенное значение.)                                                                                          |
</details>

### Исследование данных, обучение модели, оценка качества
__recommend_system_EDA+FI.ipynb__ - джупитер ноутбук, содержащий разведовательный анализ данных, генерирование новых фичей на основе текущих данных и текста, обучение и оценку модели

__recommend_system_ABtest.ipynb__ - джупитер ноутбук с проведенным AB-тестом

### Рабочие файлы эндпойнта
__database.py__ - код поделючения к базе данных

__schemas.py__ - модели pydentic

__model.py__ - модели SQLAlchemy

__endpoint.py__  - ендпойнт: получаем в качестве запроса id пользователя, формируем фичи для модели, отдаем ей на предсказание, затем возвращаем предсказания и № группы для A/B тестирования

### A/B тестирование
Для проведения A/B тестирования было обучено две модели:

__catboost_model.pkl__ - основная модель, дающая хороший скор 

__catboost_model_control.pkl__ - контрольная модель с немного измененными параметрами

Id юзера на входе через хэширование попадает в тестовую либо контрольную группу. В зависимости от этого ему делает предсказание *основная*, либо *контрольная* модель. Данные модели сделали предсказания определенной выборке пользователей, которая и оспользовалась для проведения A/B-тестирвания.

