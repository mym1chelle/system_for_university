# Тестовое задание «Система управления университетом»

1. [Информация о выполненных частях задания](#title0)
2. [Описание сущностей](#title1)
3. [Инструкции по использованию API](#title2)
4. [Инструкции по установке и запуску приложения.](#title3)

## <a id="title0">Информация о выполненных частях задания</a>
ER-диаграма находится в файле [ER_diagram.pdf](./ER_diagram.pdf) в корне проекта.

SQL скрипт, который создаёт все таблицы с полями, их типами данных, ключами и связями расположен в файле [tables.sql](./tables.sql) в корне проекта.


SQL запросы из второй части задания расположены в файле [query_for_task.sql](./query_for_task.sql) в корне проекта.

В третьей части задания нет ограничений на использование ORM или инструментов для миграции БД. Но я решил использовать данные из предыдущих частей задания, а именно SQL-запросы.
Во всем проекте используются «сырые» SQL-запросы и движок `psycopg2-binary`, для того чтобы продемострировать корректность создаваемых таблиц в БД из предыдущих частей задания.

«Сырые» SQL-запросы имеют место быть, но для более комфортного написания кода, я бы предпочел использовать связку `SQLAlchemy`, `Alembic`, `asyncpg`.

## <a id="title1">Описание сущностей</a>

#### факультет (faculty)
Поля:
- Название факультета (name)

#### учебный план (curriculum)
Поля:
- Название учебного плана (name)
- Ссылка на файл с учебным планом (link_by_file)

#### отделение (department)
Поля:
- Название отделения (name)
- Связь **o2m** с таблицей **факультет**, так как отделение может принадлежать только одному факультету, но на факультете может быть несколько отделений.
- Связь **o2m** с таблицей **учебный план**, так как отделение может иметь только один учебный план, но данный учебный план может быть у нескольких отделений.

#### группа (students_group)
Поля:
- Код группы (code)
- Связь **o2m** с таблицей **отделение**, так как группа может принадлежать только одному отделению, но в этом отделении может быть несколько групп.

#### студент (student)
Поля:
- Фамилия (surname)
- Имя (name)
- Отчество — не обязательное поле (fathers_name)
- Дата рождения (date_of_birth)
- Связь **o2m** с таблицей **группа**, так как студент может обучаться только в одной группе, но в этой группе может быть несколько студентов.

#### семестр (semester)
Поля:
- Начало семестра (start_date)
- Окончание семестра (end_date)

Эти поля уникальные, так как не должно быть двух одинаковых семестров, которые начинаются и заканчиваются в одни и те же даты.

#### расписание (schedule)
Поля:
- Связь **o2o** с таблицей **семестр**, так как в расписании не должно быть одинаковых семестров.

#### здание (building)
Поля:
- номер здания (number)
- адрес здания (address)

#### аудитория (classroom)
Поля:
- номер аудитории (number)
- Связь **o2m** с таблицей **здание**, так как аудитория может находиться только в определенном здании, но в этом здании может быть несколько аудиторий

#### оценка (grade)
Поля:
- оценка (grade)
Поле имеет тип VARCHAR для того, чтобы установить градацию оценок: «Отлично», «Хорошо» и т.д. В дальнейшем может изменяться в зависимости от принятой системы оценивания.

#### преподаватель (teacher)
Поля:
- Фамилия (surname)
- Имя (name)
- Отчество — не обязательное поле (fathers_name)

#### программа курса (course_programme)
Поля:
- Название программы (name)
- Ссылка на файл с программой курса (link_by_file)

#### курс (course)
Поля:
- название курса (name)
- Связь **o2m** с таблицей **программа курса**, так как у некоторых курсов могут быть одинаковые программы.
- Связь **o2m** с таблицей **преподаватель**, так как курс должен вести один преподаватель, но этот преподаватель может вести несколько курсов.

#### студент — курс (student_to_course)
Промежуточная таблица, для связи **m2m** между таблицами **студент** и **курс**, так как студент может посещать неограниченное количество курсов, так и курс могут посетить неограниченное количество студентов.

В данной таблице добавленно ограничение, которое не дает студенту выбрать один и тот же курс дважды.

#### учебный план —  курс (curriculum_to_course)
Промежуточная таблица, для связи **m2m** между таблицами **учебный план** и **курс**, так как в учебном плане может быть несколько курсов, так и курс может быть в нескольких учебных планах.

В данной таблице добавленно ограничение, которое не дает внести в учебный план два одинаковых курса

#### семестр — курс (semester_to_course)
Промежуточная таблица, для связи **m2m** между таблицами **семестр**, **курс** и **аудитория**, так как в семестре может быть несколько курсов, так и курс может быть в нескольких семестрах. Соответсвенно и в аудитории могут проходить несколько курсов, так и курс может проходить в разных аудиториях.

В данной таблице добавленно ограничение, которое запрещает в одном семестре вносить несколько одинаковых курсов

#### задание для самостоятельной работы (task)
Поля:
- Задание (task)
- Связь **o2m** с таблицей **курс**, так как задание может быть только в одном курсе, но у курса может быть несколько заданий
- Дата создания задания (created_at)

#### экзамен (exam)
Поля:
-  Связь **o2m** с таблицей **курс**, так как экзамен может быть только в одном курсе, но у курса может быть несколько экзаменов
- Дата проведения экзамена (date)


### таблицы с оценками
Так как система оценивания может быть разной, я решил реализовать выставление оценок для экзамена, задания для самостоятельно работы и курса в целом.

#### Оценка за задание для самостоятельной работы (task_grade)
Промежуточная таблица, для связи **m2m** между таблицами **студент**, **задание для самостоятельной работы** и **оценка**, так как студенты могут выполнить несколько заданий и по всем ним получить оценки.

В данной таблице добавленно ограничение, которое запрещает одному студенту выполнять несколько раз одно и тоже задание

#### Оценка за экзамен (exam_grade)
Промежуточная таблица, для связи **m2m** между таблицами **студент**, **экзамен* и **оценка**, так как студенты могут сдавать несколько экзаменов и по всем ним получить оценки.

В данной таблице добавленно ограничение, которое запрещает одному студенту сдавать несколько раз один и тоже экзамен

#### Оценка за курс (course_grade)
Промежуточная таблица, для связи **m2m** между таблицами **студент**, **курс** и **оценка**, так как студенты могут изучить несколько курсов и по всем ним получить оценки.

В данной таблице добавленно ограничение, которое запрещает одному студенту изучать один и тот же курс несколько раз




## <a id='title2'>Инструкция по использованию API</a>

Пройдя по ссылке:
```
http://localhost:8000/docs#/
```
вы попадете на страницу с документацией к проекту. 
На этой странице содержится информация:
* о эндпоинтах и типах запросов к ним
* о параметрах запросов, их типах и ограничениях
* о результатах запросов в случае успешного выполнения или ошибок

Далее я подробно описываю работу каждого эндпоинта:

#### POST /students
С помощью данного эндпоинта осуществляется добавление студента в базу данных. В теле запроса передаются следующие параметры в виде JSON:
* surname (**обязательный ключ**) — фамилия
* name (**обязательный ключ**) — имя
* fathers_name — отчество
* date_of_birth (**обязательный ключ**) — дата рождения
* group_code — код группы

Все необязательные параметры можно удалить из тела запроса, тогда эти поля будут иметь значение по умолчанию (`None`).

В случае передачи неверных значений или (в случае с group_code) значений, которых нет в базе данных, будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса в базе данных создастся новая запись. А результатом запроса будет JSON который содержит всю информацию о новой записи.

#### GET /students/{student_id}
С помощью данного эндпоинта осуществляется выбор записи о студенте из базы данных. В качестве параметра запроса передается `studen_id`, который соответсвует ID записи в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке. В случае успешного выполнения запроса, его результатом будет JSON который содержит всю информацию о выбранной записи.  

Так как данные о группе, в которой состоит студент хранятся в другой таблице, то вместо ID группы в результат передается код группы, в которой состоит студент. Если студент не состоит в группе, то данное поле будет содержать `None`.

#### PUT /students/{student_id}
С помощью данного эндпоинта осуществляется редактирование записи о студенте в базе данных. В качестве параметра запроса передается `studen_id`, который соответсвует ID записи в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.  

В теле запроса передаются следующие параметры в виде JSON:
* surname  — фамилия
* name  — имя
* fathers_name  — отчество
* date_of_birth  — дата рождения
* group_code  — код группы  

Все параметры являюся **необязательными**, поэтому можно изменять одновременно несколько данных студента или выборочно изменить значение какого-то поля.

В случае успешного выполнения запроса, его результатом будет JSON который содержит всю актуальную информацию о выбранной записи. 

#### DELETE /students/{student_id}
С помощью данного эндпоинта осуществляется удаление записи о студенте из базе данных. В качестве параметра запроса передается `studen_id`, который соответсвует ID записи в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.  

В случае успешного выполения запроса будет выведено сообщение об удалении выбранной записи.

#### GET /teachers
С помощью данного эндпоинта осуществляется выбор всех записей в базе данных с данными преподавателей. В качестве параметра запроса передаются `limit` (по-умолчанию равен 15) и `offset` (по-умолчанию равен 0). С помощью этих параметров осуществляется перемещение по списку преподавателей.

В случае успешного выполения запроса будет выведен список словарей, в которых содержится вся информация о преподавателях. Если преподавателей в базе данных нет, то вернется пустой список.


#### POST /courses
С помощью данного эндпоинта осуществляется добавление курса в базу данных. В теле запроса передаются следующие параметры в JSON:

Данные о курсе:
* course_name (**обязательный ключ**) — название курса
* course_programme_name  — название программы для курса

Данные о преподавателе:
* id — ID записи в базе данных с нужным преподавателем

Все необязательные параметры можно удалить из тела запроса, тогда эти поля будут иметь значение по умолчанию (`None`).

В случае передачи неверных значений или (в случае с course_programme_name и id) значений, которых нет в базе данных, будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса в базе данных создастся новая запись. А результатом запроса будет JSON с информацией о новой записи, в которой содержится вложенность нескольких таблиц (курс, программа курса, преподаватель).

#### GET /courses/{courses_id}
С помощью данного эндпоинта осуществляется выбор записи о курсе из базы данных.

В качестве параметра запроса передается `course_id`, который соответсвует ID записи в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке. В случае успешного выполнения запроса, его результатом будет JSON с информацией о новой записи, в которой содержится вложенность нескольких таблиц (курс, программа курса, преподаватель).

#### GET /courses/{courses_id}/students
С помощью данного эндпоинта осуществляется выбор всех студентов, которые посещают заданный курс.

В качестве параметра запроса передается `course_id`, который соответсвует ID записи в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.Также передаются праметры `limit` (по-умолчанию равен 15) и `offset` (по-умолчанию равен 0). С помощью этих параметров осуществляется перемещение по списку студентов.

В случае успешного выполения запроса будет выведен список словарей, в которых содержится вся информация о студентах. Если студентов, которые изучают выбранный курс в базе данных нет, то вернется пустой список.

#### POST /grades/add
*Этот эндпоинт я добавил сверх задания в силу специфики структуры базы данных.*

С помощью данного эндпоинта осуществляется добавление новой оценки в базу данных. В теле запроса передается следующий параметр в виде JSON:

* grade (**обязательный ключ**) — оценка, напр. «Отлично»

В случае передачи неверного значения или уже существующего, будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса в базе данных создастся новая запись. А результатом запроса будет JSON с информацией о новой записи.

#### POST /grades
С помощью данного эндпоинта осуществляется добавление новой оценки студенту за курс в базу данных. В теле запроса передаются следующие параметры в виде JSON:

* grade (**обязательный ключ**) — название оценки
* student_id (**обязательный ключ**) — ID студента, которому будет выставленна оценка
* course_id (**обязательный ключ**) — курс, за который студент получит оценку

В случае передачи неверных значений или (в случае с grade) значений, которых нет в базе данных, будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса в базе данных создастся новая запись. А результатом запроса будет JSON в которой содержится вложенность нескольких таблиц (курс, оценка, студент).

#### PUT /grades/{grade_id}
С помощью данного эндпоинта осуществляется редактирование оценки, выставленной студенту за курс. В качестве параметра запроса передается `grade_id`, который соответсвует ID записи о выставленной оценке в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.  

В теле запроса передается следующий параметр в виде JSON:
* grade (**обязательный ключ**) — название оценки

В случае передачи неверных значений или (в случае с grade) значений, которых нет в базе данных, будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса, его результатом будет JSON который содержит всю актуальную информацию о выбранной записи.

## <a id='title3'>Инструкция установке и запуску приложения</a>

1. [Установить Docker](https://www.docker.com)
2. [Установить Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. Клонировать проект в локальную директорию:
```
https://github.com/mym1chelle/system_for_university.git
```
4. Переименовать файл [.env.example](./.env.example) в `.env`
5. В директории клонированного проекта запусть сбор образов и запуск контейнеров Docker:

```
docker compose up --build
```