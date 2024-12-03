## Задание 
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на учебном конфигурационном языке принимается из
стандартного ввода. Выходной текст на языке yaml попадает в стандартный
вывод.

Однострочные комментарии:

% Это однострочный комментарий

Многострочные комментарии:

/*
Это многострочный
комментарий
*/

Массивы:

[ значение, значение, значение, ... ]

Словари:

{
 имя = значение,
 имя = значение,
 имя = значение,
 ...

}

Имена:

[_A-Z][_a-zA-Z0-9]*

Значения:

* Числа
* Массивы
* Словари

Объявление константы на этапе трансляции:

def имя = значение;

Вычисление константы на этапе трансляции:

^(имя)

Результатом вычисления константного выражения является значение.
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2
примера описания конфигураций из разных предметных областей.

## О программе
Эта программа парсит полученный на вход текст и преобразует его в формат yaml.

YAML - это язык для сериализации данных, который отличается простым синтаксисом и позволяет хранить ложно организованные данные в компактном и читаемом формате. 
Этот язык похож на XML и JSON, но использует более минималистичный синтаксис при сохранении аналогичных возможностей. YAML обычно применяют для создания конфигурационных
файлов или для управления контейнерами. Часто используется среди DevOps и Data-Science разработчиков.

Программа может работать в двух режимах:
1. Парсить текст, введенный с клавиатуры (модуль readFromCommandLine.py)
2. Парсить текст, читая файл (модуль readFromFile.py и файл config.txt, хранящий текст)
   
## Запуск
Запуск программы происходит в обоих случаях из командной строки

Для первого режима запуск производится следующим образом:
1. В командной строке переходим в папку с проектом (в моем случае это C:\Python\homework3)

  ![Screenshot 1](https://github.com/whiteicesky/yaml-parser/blob/main/Screenshot_1.png)
   
2. Запускаем программу командой

  ```
    python readFromCommandLine.py
  ```
3. Начинаем вводить наш текст
4. Завершение ввода осуществляется через нажатие Ctrl+Z на Windows и Ctrl+D на Linux/MacOS

  ![Screenshot 2](https://github.com/whiteicesky/yaml-parser/blob/main/Screenshot_2.png)
   
5. Вывод в формате YAML
   
  ![Screenshot 3](https://github.com/whiteicesky/yaml-parser/blob/main/Screenshot_3.png)

Для работы второго режима программы необходим конфигурационный файл. В моем случае он выглядит вот так:

  ![Screenshot 4](https://github.com/whiteicesky/yaml-parser/blob/main/Screenshot_4.png)

А также библиотека yaml. Ее можно установить следующей командой: 

  ```
    pip install pyyaml
  ```

Запуск осуществляется слеюдущим образом:
1. Также в командной строке переходим в папку с проектом

  ![Screenshot 1](https://github.com/whiteicesky/yaml-parser/blob/main/Screenshot_1.png)
   
2. Запускаем программу командой

  ```
    type config.txt | python readFromFile.py
  ```

  Где "config.txt" - название файла конфигурации
3. Вывод в формате YAML

  ![Screenshot 5](https://github.com/whiteicesky/yaml-parser/blob/main/Screenshot_5.png)

## Тесты
В консоли в директории проекта запустить тесты командой
   
   ```
    python -m unittest test.py
   ```
Результат:

![Screenshot 6](https://github.com/whiteicesky/yaml-parser/blob/main/Screenshot_6.png)

