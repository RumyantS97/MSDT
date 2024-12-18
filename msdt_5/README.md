# Современные средства разработки ПО
## Лабораторная 5 "Unit tests"
В рамках данной лабораторной работы требуется продемонстрировать свой талант к покрытию кода тестами.
## Задание на лабораторную работу
1. Сделать [форк](https://docs.github.com/en/get-started/quickstart/fork-a-repo) данного репозитория.
2. Подобрать код проекта, который вы будете покрывать юнит-тестами. Он может быть как вашим собственным, так и опесорсным.
2. Покрыть код юнит-тестами, руководствуясь материалом [лекции](https://github.com/xtrueman/prog_instruments/blob/main/presentations/UnitTests.pptx).
4. Открыть [пул-риквест](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) в иcходный репозиторий
5. Удостовериться, что github action успешно обнаружил и запустил ваши юнит-тесты, после чего ожидать ревью.

## Условия сдачи
* Использовать разрешено только **[pytest](https://docs.pytest.org/en/7.4.x/)**.
* Минимальное количество тестов - **7** штук.
* Как минимум **2** теста должны быть менее примитивными, чем основная масса, и использовать помимо ассертов параметризованное тестирование, моки, стабы и т.д.

## Ремарки:
* Очевидно, что при реализации юнит-тестов вы должны стремиться покрыть как можно больший процент кода тестами.
* Выбирайте в качестве исходного кода что-то более сложное, чем одинокий модуль с двумя функциями, считающими сумму чисел.
* Помните о правилах [test discovery](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#conventions-for-python-test-discovery).
* При работе с тестами называйте файл с тестами чем-то вроде **test_ВашеНазвание** чтобы github action работал

<details>
  <summary> Немного про github action в этом репозитории </summary>
  <br>

Этот action выполняет крайне простой набор действий:
* Чекаутит код вашего форка,
* Устанавливает зависимости из `requirements.txt`,
* Запускает юнит-тесты,
* Подсчитывает процент покрытия кода тестами.
  <br>
</details>

Если вы столкнулись с непреодолимыми трудностями в ходе выполнения лабораторной работы, вы можете задать вопрос в:
* телеграм-чате предмета,
* телеграм-чате вашего курса