using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace analyzer
{
    public partial class Form1 : Form
    {
        enum State { S, A, B, C, D, H, E, F }; //состояния анализатора
        List<string> list = new List<string>();

        bool log = false;
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e) //функционал кнопки ввод строки
        {
            richTextBox1.Clear();
            richTextBox1.DeselectAll();
            textBox2.Text = "";
            textBox1.Text = "";

        }

        private void analysis_Click(object sender, EventArgs e) // функционал кнопки анализ
        {
            textBox2.Clear();
            textBox1.Clear();
            richTextBox1.Text += " ";
            string str; //анализируемая входная строка
            str = richTextBox1.Text.ToLower(); //приведение к нижнему регистру всех символов
            int len_str = str.Length; //длина входной строки
            string error = "";
            string message = "";
            int vr = 0; //позиция начального символа в слове, в котором допущена ошибка

            message = "";
            error = "";
            textBox2.Text = "";
            string stroka = ""; // строка для символов идентификатора 
            int position_symbol = 0; //позиция текущего символа в строке
            State sta = State.S; //текущее состояние анализатора

            List<string> identTable = new List<string>(); //Список идентификаторов
            List<string> typeTable = new List<string>(); //Список типов


            while (sta != State.E && sta != State.F && position_symbol < len_str)
            {
                char str_current = str[position_symbol];

                switch (sta)//начало проверки строки
                {
                    case State.S: // пробелы и var
                        if (str_current == ' ')
                        {
                            position_symbol++;

                            sta = State.S;
                        }
                        else if (str_current == 'v')
                        {
                            position_symbol++;
                            str_current = str[position_symbol];
                            if (str_current == 'a')
                            {
                                position_symbol++;
                                str_current = str[position_symbol];
                                if (str_current == 'r')
                                {
                                    position_symbol++;
                                    str_current = str[position_symbol];
                                    if (str_current == ' ')
                                    {
                                        sta = State.A;
                                    }
                                    else
                                    {
                                        error = "Синтаксическая ошибка: недопустимый символ. Ожидался оператор 'var' ";
                                        richTextBox1.Select(position_symbol, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                                else
                                {
                                    error = "Синтаксическая ошибка: ожидалось - 'r' ";
                                    richTextBox1.Select(position_symbol, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                            }
                            else
                            {
                                error = "Синтаксическая ошибка: ожидалось - 'a' ";
                                richTextBox1.Select(position_symbol, 1);
                                richTextBox1.SelectionBackColor = Color.Coral;
                                richTextBox1.DeselectAll();
                                sta = State.F;
                            }
                        }
                        else
                        {
                            error = "Синтаксическая ошибка: ожидалось - 'var' ";
                            richTextBox1.Select(position_symbol, 1);
                            richTextBox1.SelectionBackColor = Color.Coral;
                            richTextBox1.DeselectAll();
                            sta = State.F;
                        }
                        break;

                    case State.A://проверка пробелы
                        if (str_current == ' ')
                        {
                            position_symbol++;
                            sta = State.A;
                        }
                        else if (Char.IsLetter(str_current) == true)
                        {
                            position_symbol++;
                            vr = position_symbol;
                            stroka = "" + str_current;
                            sta = State.B;
                        }
                        else
                        {
                            error = "Синтаксическая ошибка: идентификатор должен начинаться с буквы.";
                            richTextBox1.Select(position_symbol, 1);
                            richTextBox1.SelectionBackColor = Color.Coral;
                            richTextBox1.DeselectAll();
                            sta = State.F;
                        }
                        break;

                    case State.B://проверка идентификатора
                        if (stroka.Length <= 8)
                        {
                            if (Char.IsLetterOrDigit(str_current) == true)
                            {
                                position_symbol++;
                                stroka += str_current;
                                sta = State.B;
                            }
                            //cemantika
                            else if (str_current == ' ')
                            {
                                if (stroka == "byte" || stroka == "word" || stroka == "integer" || stroka == "real" || stroka == "char" || stroka == "double" || stroka == "var")
                                {
                                    error = "Семантическая ошибка: совпадение с зарезервированным словом.";
                                    richTextBox1.Select(vr - 1, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                                else
                                {
                                    if (identTable.Contains(stroka) == false)
                                    {
                                        identTable.Add(stroka);
                                        position_symbol++;
                                        sta = State.C;
                                    }
                                    else
                                    {
                                        error = "Семантическая ошибка: повторное объявление переменной.";
                                        richTextBox1.Select(vr - 1, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                            }
                            else if (str_current == ',')
                            {
                                if (stroka == "var" || stroka == "byte" || stroka == "word" || stroka == "integer" || stroka == "real" || stroka == "char" || stroka == "double")
                                {
                                    error = "Семантическая ошибка: совпадение с зарезервированным словом.";
                                    richTextBox1.Select(vr - 1, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                                else
                                {
                                    if (identTable.Contains(stroka) == false)
                                    {
                                        identTable.Add(stroka);
                                        position_symbol++;
                                        sta = State.A;
                                    }
                                    else
                                    {
                                        error = "Семантическая ошибка: повторное объявление переменной.";
                                        richTextBox1.Select(vr - 1, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                            }
                            else if (str_current == ':')
                            {
                                if (stroka == "var" || stroka == "byte" || stroka == "word" || stroka == "integer" || stroka == "real" || stroka == "char" || stroka == "double")
                                {
                                    error = "Семантическая ошибка: совпадение с зарезервированным словом.";
                                    richTextBox1.Select(vr - 1, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                                else
                                {
                                    if (identTable.Contains(stroka) == false)
                                    {
                                        identTable.Add(stroka);
                                        position_symbol++;
                                        sta = State.D;
                                    }
                                    else
                                    {
                                        error = "Семантическая ошибка: повторное объявление переменной.";
                                        richTextBox1.Select(vr - 1, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                            }
                            else
                            {
                                error = "Синтаксическая ошибка: недопустимый символ.";
                                richTextBox1.Select(position_symbol, 1);
                                richTextBox1.SelectionBackColor = Color.Coral;
                                richTextBox1.DeselectAll();
                                sta = State.F;
                            }
                        }
                        else
                        {
                            error = "Семантическая ошибка: длина идентификатора превышает 8.";
                            richTextBox1.Select(vr - 1, 1);
                            richTextBox1.SelectionBackColor = Color.Coral;
                            richTextBox1.DeselectAll();
                            sta = State.F;
                        }

                        break;

                    case State.C:
                        if (str_current == ' ')
                        {
                            position_symbol++;
                            sta = State.C;
                        }
                        else if (str_current == ',')
                        {
                            position_symbol++;
                            sta = State.A;
                        }
                        else if (str_current == ':')
                        {
                            position_symbol++;
                            sta = State.D;
                        }
                        else
                        {
                            error = "Синтаксическая ошибка: недопустимый символ. Ожидалась запятая или двоеточие.";
                            richTextBox1.Select(position_symbol, 1);
                            richTextBox1.SelectionBackColor = Color.Coral;
                            richTextBox1.DeselectAll();
                            sta = State.F;
                        }
                        break;

                    case State.D:
                        if (str_current == 'b' || str_current == 'w' || str_current == 'i' || str_current == 'r' || str_current == 'c' || str_current == 'd')
                        {
                            if (str_current == 'b')
                            {
                                position_symbol++;
                                str_current = str[position_symbol];
                                if (str_current == 'y')
                                {
                                    position_symbol++;
                                    str_current = str[position_symbol];
                                    if (str_current == 't')
                                    {
                                        position_symbol++;
                                        str_current = str[position_symbol];
                                        if (str_current == 'e')
                                        {
                                            position_symbol++;
                                            str_current = str[position_symbol];
                                            if (str_current == ',')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("byte");
                                                }
                                                position_symbol++;
                                                sta = State.A;
                                            }
                                            else if (str_current == ';')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("byte");
                                                }
                                                sta = State.E; //конец
                                            }
                                            else if (str_current == ' ')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("byte");
                                                }
                                                position_symbol++;
                                                sta = State.H;
                                            }
                                            else
                                            {
                                                error = "Синтаксическая ошибка: ожидался тип 'byte'";
                                                richTextBox1.Select(position_symbol, 1);
                                                richTextBox1.SelectionBackColor = Color.Coral;
                                                richTextBox1.DeselectAll();
                                                sta = State.F;
                                            }

                                        }
                                        else
                                        {
                                            error = "Синтаксическая ошибка: ожидалось 'e'";
                                            richTextBox1.Select(position_symbol, 1);
                                            richTextBox1.SelectionBackColor = Color.Coral;
                                            richTextBox1.DeselectAll();
                                            sta = State.F;
                                        }
                                    }
                                    else
                                    {
                                        error = "Синтаксическая ошибка: ожидалось 't'";
                                        richTextBox1.Select(position_symbol, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                                else
                                {
                                    error = "Синтаксическая ошибка: ожидалось 'y'";
                                    richTextBox1.Select(position_symbol, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                            }

                            else if (str_current == 'w')
                            {
                                position_symbol++;
                                str_current = str[position_symbol];
                                if (str_current == 'o')
                                {
                                    position_symbol++;
                                    str_current = str[position_symbol];
                                    if (str_current == 'r')
                                    {
                                        position_symbol++;
                                        str_current = str[position_symbol];
                                        if (str_current == 'd')
                                        {
                                            position_symbol++;
                                            str_current = str[position_symbol];
                                            if (str_current == ',')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("word");
                                                }
                                                position_symbol++;
                                                sta = State.A;
                                            }
                                            else if (str_current == ';')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("word");
                                                }
                                                sta = State.E; //конец
                                            }
                                            else if (str_current == ' ')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("word");
                                                }
                                                position_symbol++;
                                                sta = State.H;
                                            }
                                            else
                                            {
                                                error = "Синтаксическая ошибка: ожидался тип 'word'";
                                                richTextBox1.Select(position_symbol, 1);
                                                richTextBox1.SelectionBackColor = Color.Coral;
                                                richTextBox1.DeselectAll();
                                                sta = State.F;
                                            }

                                        }
                                        else
                                        {
                                            error = "Синтаксическая ошибка: ожидалось 'd'";
                                            richTextBox1.Select(position_symbol, 1);
                                            richTextBox1.SelectionBackColor = Color.Coral;
                                            richTextBox1.DeselectAll();
                                            sta = State.F;
                                        }
                                    }
                                    else
                                    {
                                        error = "Синтаксическая ошибка: ожидалось 'r'";
                                        richTextBox1.Select(position_symbol, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                                else
                                {
                                    error = "Синтаксическая ошибка: ожидалось 'o'";
                                    richTextBox1.Select(position_symbol, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                            }

                            else if (str_current == 'r')
                            {
                                position_symbol++;
                                str_current = str[position_symbol];
                                if (str_current == 'e')
                                {
                                    position_symbol++;
                                    str_current = str[position_symbol];
                                    if (str_current == 'a')
                                    {
                                        position_symbol++;
                                        str_current = str[position_symbol];
                                        if (str_current == 'l')
                                        {
                                            position_symbol++;
                                            str_current = str[position_symbol];
                                            if (str_current == ',')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("real");
                                                }
                                                position_symbol++;
                                                sta = State.A;
                                            }
                                            else if (str_current == ';')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("real");
                                                }
                                                sta = State.E; //конец
                                            }
                                            else if (str_current == ' ')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("real");
                                                }
                                                position_symbol++;
                                                sta = State.H;
                                            }
                                            else
                                            {
                                                error = "Синтаксическая ошибка: ожидался тип 'real'";
                                                richTextBox1.Select(position_symbol, 1);
                                                richTextBox1.SelectionBackColor = Color.Coral;
                                                richTextBox1.DeselectAll();
                                                sta = State.F;
                                            }

                                        }
                                        else
                                        {
                                            error = "Синтаксическая ошибка: ожидалось 'l'";
                                            richTextBox1.Select(position_symbol, 1);
                                            richTextBox1.SelectionBackColor = Color.Coral;
                                            richTextBox1.DeselectAll();
                                            sta = State.F;
                                        }
                                    }
                                    else
                                    {
                                        error = "Синтаксическая ошибка: ожидалось 'a'";
                                        richTextBox1.Select(position_symbol, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                                else
                                {
                                    error = "Синтаксическая ошибка: ожидалось 'e'";
                                    richTextBox1.Select(position_symbol, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                            }

                            else if (str_current == 'c')
                            {
                                position_symbol++;
                                str_current = str[position_symbol];
                                if (str_current == 'h')
                                {
                                    position_symbol++;
                                    str_current = str[position_symbol];
                                    if (str_current == 'a')
                                    {
                                        position_symbol++;
                                        str_current = str[position_symbol];
                                        if (str_current == 'r')
                                        {
                                            position_symbol++;
                                            str_current = str[position_symbol];
                                            if (str_current == ',')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("char");
                                                }
                                                position_symbol++;
                                                sta = State.A;
                                            }
                                            else if (str_current == ';')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("char");
                                                }
                                                sta = State.E; //конец
                                            }
                                            else if (str_current == ' ')
                                            {
                                                for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                {
                                                    typeTable.Add("char");
                                                }
                                                position_symbol++;
                                                sta = State.H;
                                            }
                                            else
                                            {
                                                error = "Синтаксическая ошибка: ожидался тип 'char'";
                                                richTextBox1.Select(position_symbol, 1);
                                                richTextBox1.SelectionBackColor = Color.Coral;
                                                richTextBox1.DeselectAll();
                                                sta = State.F;
                                            }

                                        }
                                        else
                                        {
                                            error = "Синтаксическая ошибка: ожидалось 'r'";
                                            richTextBox1.Select(position_symbol, 1);
                                            richTextBox1.SelectionBackColor = Color.Coral;
                                            richTextBox1.DeselectAll();
                                            sta = State.F;
                                        }
                                    }
                                    else
                                    {
                                        error = "Синтаксическая ошибка: ожидалось 'a'";
                                        richTextBox1.Select(position_symbol, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                                else
                                {
                                    error = "Синтаксическая ошибка: ожидалось 'h'";
                                    richTextBox1.Select(position_symbol, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                            }
                            else if (str_current == 'i')
                            {
                                position_symbol++;
                                str_current = str[position_symbol];
                                if (str_current == 'n')
                                {
                                    position_symbol++;
                                    str_current = str[position_symbol];
                                    if (str_current == 't')
                                    {
                                        position_symbol++;
                                        str_current = str[position_symbol];
                                        if (str_current == 'e')
                                        {
                                            position_symbol++;
                                            str_current = str[position_symbol];
                                            if (str_current == 'g')
                                            {
                                                position_symbol++;
                                                str_current = str[position_symbol];
                                                if (str_current == 'e')
                                                {
                                                    position_symbol++;
                                                    str_current = str[position_symbol];
                                                    if (str_current == 'r')
                                                    {
                                                        position_symbol++;
                                                        str_current = str[position_symbol];
                                                        if (str_current == ',')
                                                        {
                                                            for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                            {
                                                                typeTable.Add("integer");
                                                            }
                                                            position_symbol++;
                                                            sta = State.A;
                                                        }
                                                        else if (str_current == ';')
                                                        {
                                                            for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                            {
                                                                typeTable.Add("integer");
                                                            }
                                                            sta = State.E; //конец
                                                        }
                                                        else if (str_current == ' ')
                                                        {
                                                            for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                            {
                                                                typeTable.Add("integer");
                                                            }
                                                            position_symbol++;
                                                            sta = State.H;
                                                        }
                                                        else
                                                        {
                                                            error = "Синтаксическая ошибка: ожидался тип 'integer'";
                                                            richTextBox1.Select(position_symbol, 1);
                                                            richTextBox1.SelectionBackColor = Color.Coral;
                                                            richTextBox1.DeselectAll();
                                                            sta = State.F;
                                                        }
                                                    }
                                                    else
                                                    {
                                                        error = "Синтаксическая ошибка: ожидалось 'r'";
                                                        richTextBox1.Select(position_symbol, 1);
                                                        richTextBox1.SelectionBackColor = Color.Coral;
                                                        richTextBox1.DeselectAll();
                                                        sta = State.F;
                                                    }
                                                }
                                                else
                                                {
                                                    error = "Синтаксическая ошибка: ожидалось 'e'";
                                                    richTextBox1.Select(position_symbol, 1);
                                                    richTextBox1.SelectionBackColor = Color.Coral;
                                                    richTextBox1.DeselectAll();
                                                    sta = State.F;
                                                }
                                            }
                                            else
                                            {
                                                error = "Синтаксическая ошибка: ожидалось 'g'";
                                                richTextBox1.Select(position_symbol, 1);
                                                richTextBox1.SelectionBackColor = Color.Coral;
                                                richTextBox1.DeselectAll();
                                                sta = State.F;
                                            }

                                        }
                                        else
                                        {
                                            error = "Синтаксическая ошибка: ожидалось 'e'";
                                            richTextBox1.Select(position_symbol, 1);
                                            richTextBox1.SelectionBackColor = Color.Coral;
                                            richTextBox1.DeselectAll();
                                            sta = State.F;
                                        }
                                    }
                                    else
                                    {
                                        error = "Синтаксическая ошибка: ожидалось 't'";
                                        richTextBox1.Select(position_symbol, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                                else
                                {
                                    error = "Синтаксическая ошибка: ожидалось 'n'";
                                    richTextBox1.Select(position_symbol, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                            }
                            else if (str_current == 'd')
                            {
                                position_symbol++;
                                str_current = str[position_symbol];
                                if (str_current == 'o')
                                {
                                    position_symbol++;
                                    str_current = str[position_symbol];
                                    if (str_current == 'u')
                                    {
                                        position_symbol++;
                                        str_current = str[position_symbol];
                                        if (str_current == 'b')
                                        {
                                            position_symbol++;
                                            str_current = str[position_symbol];
                                            if (str_current == 'l')
                                            {
                                                position_symbol++;
                                                str_current = str[position_symbol];
                                                if (str_current == 'e')
                                                {
                                                    position_symbol++;
                                                    str_current = str[position_symbol];
                                                    if (str_current == ',')
                                                    {
                                                        for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                        {
                                                            typeTable.Add("double");
                                                        }
                                                        position_symbol++;
                                                        sta = State.A;
                                                    }
                                                    else if (str_current == ';')
                                                    {
                                                        for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                        {
                                                            typeTable.Add("double");
                                                        }
                                                        position_symbol++;
                                                        sta = State.E; //конец
                                                    }
                                                    else if (str_current == ' ')
                                                    {
                                                        for (int i = typeTable.Count + 1; i < identTable.Count + 1; i++)
                                                        {
                                                            typeTable.Add("double");
                                                        }
                                                        position_symbol++;
                                                        sta = State.H;
                                                    }
                                                    else
                                                    {
                                                        error = "Синтаксическая ошибка: ожидался тип 'double'";
                                                        richTextBox1.Select(position_symbol, 1);
                                                        richTextBox1.SelectionBackColor = Color.Coral;
                                                        richTextBox1.DeselectAll();
                                                        sta = State.F;
                                                    }
                                                }
                                                else
                                                {

                                                    error = "Синтаксическая ошибка: ожидалось 'e'";
                                                    richTextBox1.Select(position_symbol, 1);
                                                    richTextBox1.SelectionBackColor = Color.Coral;
                                                    richTextBox1.DeselectAll();
                                                    sta = State.F;
                                                }
                                            }
                                            else
                                            {
                                                error = "Синтаксическая ошибка: ожидалось 'l'";
                                                richTextBox1.Select(position_symbol, 1);
                                                richTextBox1.SelectionBackColor = Color.Coral;
                                                richTextBox1.DeselectAll();
                                                sta = State.F;
                                            }

                                        }
                                        else
                                        {
                                            error = "Синтаксическая ошибка: ожидалось 'b'";
                                            richTextBox1.Select(position_symbol, 1);
                                            richTextBox1.SelectionBackColor = Color.Coral;
                                            richTextBox1.DeselectAll();
                                            sta = State.F;
                                        }
                                    }
                                    else
                                    {
                                        error = "Синтаксическая ошибка: ожидалось 'u'";
                                        richTextBox1.Select(position_symbol, 1);
                                        richTextBox1.SelectionBackColor = Color.Coral;
                                        richTextBox1.DeselectAll();
                                        sta = State.F;
                                    }
                                }
                                else
                                {
                                    error = "Синтаксическая ошибка: ожидалось 'o'";
                                    richTextBox1.Select(position_symbol, 1);
                                    richTextBox1.SelectionBackColor = Color.Coral;
                                    richTextBox1.DeselectAll();
                                    sta = State.F;
                                }
                            }

                        }
                        else if (str_current == ' ')
                        {
                            position_symbol++;
                            sta = State.D;
                        }
                        else
                        {
                            error = "Синтаксическая ошибка: такого типа не существует!";
                            richTextBox1.Select(position_symbol, 1);
                            richTextBox1.SelectionBackColor = Color.Coral;
                            richTextBox1.DeselectAll();
                            sta = State.F;
                        }
                        break;

                    case State.H:
                        if (str_current == ' ')
                        {
                            position_symbol++;
                            sta = State.H;
                        }
                        else if (str_current == ';')
                        {
                            sta = State.E;
                        }
                        else if (str_current == ',')
                        {
                            position_symbol++;
                            sta = State.A;
                        }
                        else
                        {
                            error = "Синтаксическая ошибка: недопустимый символ. Ожидалось: ';' или ','";
                            richTextBox1.Select(position_symbol, 1);
                            richTextBox1.SelectionBackColor = Color.Coral;
                            richTextBox1.DeselectAll();
                            sta = State.F;
                        }
                        break;
                }
            }
            if (sta == State.E)
            {
                message = "Цепочка принадлежит языку";
                textBox2.Text = message;
            }
            else if (sta == State.F)
            {
                textBox2.Text = error;
                log = true;
            }
            else if (sta != State.F && sta != State.E)
            {
                richTextBox1.Select(position_symbol, 1);
                richTextBox1.SelectionBackColor = Color.Coral;
                richTextBox1.DeselectAll();
                message = "Синтаксическая ошибка: у цепочки нет конечного символа. Ожидается ';'";
                textBox2.Text = message;
            }
            if (textBox2.Text == "Цепочка принадлежит языку")
            {
                for (int i = 0; i < identTable.Count; i++)
                {
                    list.Add(identTable[i]);
                    list.Add(typeTable[i]);
                }
            }

        }

        private void semanticsoutput_Click(object sender, EventArgs e) // функционал кнопки вывод семантики
        {
            textBox1.Clear();
            if (richTextBox1.Text == "")
            {
                textBox1.Text = "Ошибка: строка пустая.";
            }
            else
            {
                if (textBox2.Text != "Цепочка принадлежит языку")
                {
                    textBox1.Text = "Цепочка не принадлежит языку";
                }
                else
                {
                    textBox1.AppendText($"Таблица идентификаторов и соответствующих типов: \r\n\n");
                    for (int i = 0; i < list.Count; i = i + 2)
                    {
                        textBox1.AppendText($" " + list[i] + " тип: " + list[i + 1] + "\r\n");
                    }
                    list.Clear();
                }
            }
        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {
            if (log)
            {
                log = false;
                int cursorPos = richTextBox1.SelectionStart;
                richTextBox1.Select(0, richTextBox1.Text.Length);
                richTextBox1.SelectionBackColor = Color.White;
                richTextBox1.DeselectAll();
                richTextBox1.SelectionStart = cursorPos;
            }

        }
    }
}
