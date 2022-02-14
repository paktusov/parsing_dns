<h1 align="center"><a target="_blank"  href="http://beeb08c902a0.sn.mynetname.net/">Parsing DNS</a></h1>

## Описание

<p<>.>Parsing DNS - это проект для отслеживания появления новых товаров или снижения их цены в разделе "Уценённые товары" магазина DNS. Благодаря этому проекту у пользователя появляется возможность оперативно приобрести товар по выгодной цене. В нем я отрабатываю все стадии цикла разработки приложения.</p> 

Каждый новый функционал появляется после постановки задачи в Jira (изначально использовался упрощенный инструмент notion), путем создания новой ветки в репозитории, ее ревью (выполняется наставником) с последующим слиянием. Каждый этап автоматически отражается в Jira.

Основой данного проекта является платформа Scrapy для извлечения данных с веб-страниц. Для обхода защиты от Variti был использован эмулятор браузера Selenium. Хранение информации осуществляется в нереляционной СУБД MongoDB. Изначально хранилась локально, а в последующем была перенесена в облако. Для отображения информации из базы данных был использован фреймворк Flask. Для отработки навыков в проекте не была использована SQLAlchemy. Также в проект было добавлено SMS и Telegram оповещение. В проекте используется менеджер управления зависимостями Poetry, для передачи настроек используется классы модуля Pydantic. Все приложения запакованы в Docker контейнеры и запускаются вместе через Docker Compose.

## Установка
