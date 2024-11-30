'''
В данном проекте представлена часть моего pet-проекта
по вычислению оптимальной стратегии в игре Buckshoot Roulette
(часть потому что оригинальный код написан на C#, а переписывать все лень.
Несмотря на это оригинальный вариант я вставил без правок по стилям)
Оригинал: https://github.com/Daytel/Roulette
'''


# Класс хранящий результат вычислений стратегии
class Choice:
    def __init__( self, path: str, ev: float, win: float, lose: float ):

        # Путь выборов
        self.path = path

        # Урон в раунде (EV > 0 - дилер получил больше урона, иначе игрок)
        self.ev = ev

        # Шанс победить в раунде
        self.win = win

        # Шанс програть
        self.lose = lose


# Класс вычисления наилучшей стратегии
class Solution:

    # Сбор результатов
    def __init__( self, max_hp ):

        # Путь выборов
        self.choice = [] 

        # Численные коеффициенты
        self.ev = []
        self.win = []
        self.lose = []
        
        # Максимум здоровья
        self.max_hp = max_hp 

    '''
    self - результаты, YHP - здоровье игрока, DHP - здоровье дилера, LR - боевые патроны, BL - холостые патроны,
    ch - вероятность события, path - путь действий, MI - предметы игрока, HI - предметы дилера,
    BM - знания игроком патронов, BD - знания дилером патронов, FM - первый ход,
    ind - номер текущего патрона, capt - наличие на руках наручников
    '''

    # Задача 1. Добавить расклад для боевые + холостые
    def me_calculate( self, YHP, DHP, LR, BL, ch, path, MI, HI, BM, BD, FM, ind, capt ):
        
        # Условия завершения рекурсии
        # 1. Кто-то умер
        if YHP < 1:
            self.lose[ self.choice.index(path) ] += ch
        elif DHP < 1:
            self.win[ self.choice.index(path) ] += ch
        
        # 2. Кончились патроны
        elif LR + BL != 0:
            
            # Иначе считаем стратегию
            # Если первый ход - создаём новую ветвь
            if FM and path == "":
                self.choice.append(path)
                self.ev.append(0)
                self.win.append(0)
                self.lose.append(0)

            # 1. Процесс хила

            # Использование "Лекарства" экстренно
            if MI["Cigarettes"] == 0 and ( MI["Adrenalin"] == 0 and HI["Cigarettes"] == 0 and
                                         Simulation.KillMe( YHP, LR, BL, MI, HI ) > 0.5 and
                                         Simulation.can_kill( DHP, LR, BL, MI, HI )
                                         ) < 0.5:
                
                # Нам выгодно есть таблетку
                if FM:
                    self.choice[-1] += "Medicine "
                    path += "Medicine "
                MI["Medicine"] -= 1
                self.me_calculate( YHP + 2, DHP, LR, BL, ch * 0.5, path, MI, HI, BM, BD, FM, ind, capt )
                self.me_calculate( YHP - 1, DHP, LR, BL, ch * 0.5, path, MI, HI, BM, BD, FM, ind, capt )

            # Обычное использование сигарет и таблеток
            if YHP != self.max_hp:

                # Таблетки
                if MI["Medicine"] != 0 and YHP == 2 and self.max_hp == 4:
                    if FM:
                        self.choice[-1] += "Medicine "
                        path += "Medicine "
                    MI["Medicine"] -= 1
                    self.me_calculate( YHP + 2, DHP, LR, BL, ch * 0.5, path, MI, HI, BM, BD, FM, ind, capt )
                    self.me_calculate( YHP - 1, DHP, LR, BL, ch * 0.5, path, MI, HI, BM, BD, FM, ind, capt )
                
                # Сигареты
                elif MI["Cigarettes"] != 0:
                    if FM:
                        self.choice[-1] += "Cigarettes "
                        path += "Cigarettes "
                    MI["Cigarettes"] -= 1
                    self.me_calculate( YHP + 1, DHP, LR, BL, ch, path, MI, HI, BM, BD, FM, ind, capt )

            # Использование патронов
            # Остались холостые
            if LR == 0:
                
                # Проверка на условие 100% победы
                if DHP == 1:
                    if MI["Inverter"] != 0 or ( MI["Adrenalin"] != 0 and HI["Inverter"] != 0 ):
                        if FM:
                            self.choice[-1] += "Inverter Dealer"
                            path += "Inverter Dealer"
                        self.ev[-1] += ch
                        self.dealer_calculate( YHP, DHP - 1, LR, BL - 1, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                    else:
                        if FM:
                            self.choice[-1] += "Me"
                            path += "Me"
                        self.me_calculate( YHP, DHP, LR, 0, ch, path, MI, HI, BM, BD, FM, ind, capt )

                elif DHP == 2:

                    # Наручники + 2 Инвертора
                    if BL >= 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and
                                     MI["Inverter"] + min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Saw"] ) ) > 1
                                   ):
                        if FM:
                            self.choice[-1] += "Handcuffs Inverter Dealer Inverter Dealer"
                            path += "Handcuffs Inverter Dealer Inverter Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR, BL - 2, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                    
                    # Пила + Инвертор
                    elif MI["Saw"] + min( MI["Adrenalin"], HI["Saw"] ) != 0 and MI["Inverter"] + min( MI["Adrenalin"] -\
                                          Simulation.use_adrenalin( 1, MI["Saw"] ), HI["Inverter"]
                                        ) != 0:
                        if FM:
                            self.choice[-1] += "Inverter Saw Dealer"
                            path += "Inverter Saw Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR, BL - 2, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                    # На последний патрон Инвертор
                    elif BL == 1 and ( MI["Inverter"] != 0 or ( MI["Adrenalin"] != 0 and HI["Adrenalin"] != 0 ) ):
                        if FM:
                            self.choice[-1] += "Inverter Dealer"
                            path += "Inverter Dealer"
                        self.ev[-1] += ch
                        self.dealer_calculate( YHP, DHP - 1, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                    else:
                        if FM:
                            self.choice[-1] += "Me "
                            path += "Me "
                        self.MeCalculete( YHP, DHP, LR, BL - 1, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                
                elif DHP == 3:

                    # Наручники + Пила + 2 Инвертора
                    if BL >=2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and MI["Saw"] + \
                                    min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Handcuffs"]), HI["Saw"] ) != 0 and
                                    MI["Inverter"] + min( MI["Adrenalin"] - Simulation.use_adrenalin( 2, MI["Handcuffs"] + \
                                    MI["Saw"] ), HI["Inverter"] ) > 1
                                  ):
                        if (FM):
                            self.choice[-1] += "Handcuffs Inverter Saw Dealer Inverter Dealer"
                            path += "Handcuffs Inverter Saw Dealer Inverter Dealer"
                        self.ev[-1] += ch * 3
                        self.dealer_calculate( YHP, DHP - 3, LR, BL - 2, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                    
                    # На 2 патрона Наручники + 2 инвертора
                    elif BL == 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and
                                       MI["Inverter"] + min( MI["Adrenalin"] -\
                                       Simulation.use_adrenalin( 1, MI["Saw"] ), HI["Inverter"] ) > 1
                                     ):
                        if FM:
                            self.choice[-1] += "Handcuffs Inverter Dealer Inverter Dealer"
                            path += "Handcuffs Inverter Dealer Inverter Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                    # На последний патрон Пила + Инвертор
                    elif BL == 1 and ( MI["Saw"] + min( MI["Adrenalin"], HI["Saw"] ) != 0 and MI["Inverter"] + \
                                       min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Saw"]), HI["Inverter"] ) != 0
                                     ):
                        if FM:
                            self.choice[-1] += "Inverter Saw Dealer"
                            path += "Inverter Saw Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                    # На последний Инвертор
                    elif BL == 1 and ( MI["Inverter"] != 0 or ( MI["Adrenalin"] != 0 and HI["Inverter"] != 0 ) ):
                        if FM:
                            self.choice[-1] += "Inverter Dealer"
                            path += "Inverter Dealer"
                        self.ev[-1] += ch
                        self.dealer_calculate( YHP, DHP - 1, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                    else:
                        if FM:
                            self.choice[-1] += "Me... "
                            path += "Me... "
                        self.me_calculate( YHP, DHP, LR, BL - 1, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                # DHP == 4
                else:  

                    # Наручники + 2 Пилы + 2 Инвертора
                    if BL >= 2 and ( MI["Handcuffs"] + min(MI["Adrenalin"], HI["Handcuffs"]) != 0 and MI["Saw"] + \
                                     min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Handcuffs"] ), HI["Saw"] ) > 1 and \
                                     MI["Inverter"] + min( MI["Adrenalin"] - Simulation.use_adrenalin( 3, MI["Handcuffs"] +\
                                     MI["Saw"] ), HI["Inverter"] ) > 1
                                   ):
                        if FM:
                            self.choice[-1] += "Handcuffs Inverter Saw Dealer Inverter Saw Dealer"
                            path += "Handcuffs Inverter Saw Dealer Inverter Saw Dealer"
                        self.ev[-1] += ch * 4
                        self.dealer_calculate( YHP, DHP - 4, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                    
                    # На 2 патрона Наручники + Пила + 2 Инвертора
                    elif BL == 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and \
                                       MI["Saw"] + min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Handcuffs"]), HI["Saw"] ) != 0 and \
                                       MI["Inverter"] + min( MI["Adrenalin"] - Simulation.use_adrenalin( 2, MI["Handcuffs"] + MI["Saw"] ), HI["Inverter"] ) > 1
                                     ):
                        if FM:
                            self.choice[-1] += "Handcuffs Inverter Saw Dealer Inverter Dealer"
                            path += "Handcuffs Inverter Saw Dealer Inverter Dealer"
                        self.ev[-1] += ch * 3
                        self.dealer_calculate( YHP, DHP - 3, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                    
                    # На 2 патрона Наручники + 2 инвертора
                    elif BL == 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and MI["Inverter"] + \
                                       min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Saw"] ), HI["Inverter"] ) > 1
                                     ):
                        if FM:
                            self.choice[-1] += "Handcuffs Inverter Dealer Inverter Dealer"
                            path += "Handcuffs Inverter Dealer Inverter Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                    # На последний патрон Пила + Инвертор
                    elif BL == 1 and ( MI["Saw"] + min( MI["Adrenalin"], HI["Saw"] ) != 0 and MI["Inverter"] + min( MI["Adrenalin"] - \
                                       Simulation.use_adrenalin( 1, MI["Saw"] ), HI["Inverter"] ) != 0
                                     ):
                        if FM:
                            self.choice[-1] += "Inverter Saw Dealer"
                            path += "Inverter Saw Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                    
                    # На последний Инвертор
                    elif BL == 1 and ( MI["Inverter"] != 0 or ( MI["Adrenalin"] != 0 and HI["Inverter"] != 0 ) ):
                        if FM:
                            self.choice[-1] += "Inverter Dealer"
                            path += "Inverter Dealer"
                        self.ev[-1] += ch
                        self.dealer_calculate( YHP, DHP - 1, LR, 0, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                    else:
                        if FM:
                            self.choice[-1] += "Me "
                            path += "Me "
                        self.me_calculate( YHP, DHP, LR, BL - 1, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

            elif BL == 0: # Остались боевые
                
                # Проверка на условие 100% победы
                if DHP == 1:
                    if FM:
                        self.choice[-1] += "Dealer"
                        path += "Dealer"
                    self.ev[-1] += ch
                    self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                elif DHP == 2:

                    # 2 патрона + Наручники
                    if LR >= 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 ):
                        if FM:
                            self.choice[-1] += "Handcuffs Dealer Dealer"
                            path += "Handcuffs Dealer Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                    
                    # Пила
                    elif MI["Saw"] + min( MI["Adrenalin"], HI["Saw"] ) != 0:
                        if FM:
                            self.choice[-1] += "Saw Dealer"
                            path += "Saw Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                    
                    # На последний патрон - просто бьём
                    elif LR == 1:
                        if FM:
                            self.choice[-1] += "Dealer"
                            path += "Dealer"
                        self.ev[-1] += ch
                        self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                    
                    # Тратим предметы, пытаясь пропустить раунд
                    else:

                        # Если дилер не убивает на своём ходе
                        if Simulation.can_kill( YHP, LR - 1, BL, MI, HI ) == 0:

                            # По EV мы впереди: 2 в него 1 в себя
                            if LR == 3 and HI["Handcuffs"] == 0:
                                if FM:
                                    self.choice[-1] += "Dealer"
                                    path += "Dealer"
                                self.ev[-1] += ch
                                self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                            # Иначе скипаем патрон для норм ситуации (не тратим адреналин)
                            elif MI["Beer"] != 0:
                                if FM:
                                    self.choice[-1] += "Beer "
                                    path += "Beer "
                                MI["Beer"] = MI["Beer"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                            
                            elif MI["Inverter"] != 0:
                                if FM:
                                    self.choice[-1] += "Inverter "
                                    path += "Inverter "
                                MI["Inverter"] = MI["Inverter"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            # Иначе просто стреляем
                            else:
                                if FM:
                                    self.choice[-1] += "Dealer"
                                    path += "Dealer"
                                self.ev[-1] += ch
                                self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                        # Пытаемся выжить
                        else:
                            if MI["Beer"] != 0:
                                if FM:
                                    self.choice[-1] += "Beer "
                                    path += "Beer "
                                MI["Beer"] = MI["Beer"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                            
                            elif MI["Inverter"] != 0:
                                if FM:
                                    self.choice[-1] += "Inverter "
                                    path += "Inverter "
                                MI["Inverter"] = MI["Inverter"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                            
                            elif HI["Inverter"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Inverter "
                                    path += "Inverter "
                                MI["Adrenalin"] = MI["Adrenalin"] - 1
                                HI["Inverter"] = HI["Inverter"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                            
                            elif HI["Beer"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Beer "
                                    path += "Beer "
                                MI["Adrenalin"] = MI["Adrenalin"] - 1
                                HI["Beer"] = HI["Beer"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            else:

                                # Увы и ах
                                if FM:
                                    self.choice[-1] += "Dealer"
                                    path += "Dealer"
                                self.ev[-1] += ch
                                self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                
                elif DHP == 3:

                    # Наручники + Пила
                    if LR >= 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and MI["Saw"] + \
                                     min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Handcuffs"] ), HI["Saw"] ) != 0
                                   ):
                        if FM:
                            self.choice[-1] += "Handcuffs Saw Dealer Dealer"
                            path += "Handcuffs Saw Dealer Dealer"
                        self.ev[-1] += ch * 3
                        self.dealer_calculate( YHP, DHP - 3, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                    # На 2 последних патрона Наручники
                    elif LR == 2 and MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0:
                        if FM:
                            self.choice[-1] += "Handcuffs Dealer Dealer"
                            path += "Handcuffs Dealer Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                    
                    # На последний патрон Пила
                    elif LR == 1 and ( MI["Saw"] + min( MI["Adrenalin"], HI["Saw"] ) != 0 ):
                        if FM:
                            self.choice[-1] += "Saw Dealer"
                            path += "Saw Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                    
                    else: # Тратим предметы для скипа

                         # Если диллер не убивает на своём ходе
                        if Simulation.can_kill( YHP, LR - 1, BL, MI, HI ) == 0:

                            # Наручники сразу используем т.к. их использование всегда выгодно
                            if HI["Handcuffs"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Handcuffs Dealer Dealer"
                                    path += "Handcuffs Dealer Dealer"
                                HI["Handcuffs"] = HI["Handcuffs"] - 1
                                MI["Adrenalin"] = MI["Adrenalin"] - 1
                                self.ev[-1] += ch * 2
                                self.dealer_calculate( YHP, DHP - 2, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                            
                            elif HI["Handcuffs"] != 0:
                                if FM:
                                    self.choice[-1] += "Handcuffs Dealer Dealer"
                                    path += "Handcuffs Dealer Dealer"
                                MI["Handcuffs"] = MI["Handcuffs"] - 1
                                self.ev[-1] += ch * 2
                                self.dealer_calculate( YHP, DHP - 2, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                            # Используем пилу или просто бьём когда патронов нечётно
                            elif LR == 3 and HI["Handcuffs"] == 0:

                                # Используем пилу
                                if HI["Saw"] != 0 and MI["Adrenalin"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    HI["Saw"] = HI["Saw"] - 1
                                    MI["Adrenalin"] = MI["Adrenalin"] - 1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                                elif MI["Saw"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    MI["Saw"] = MI["Saw"] - 1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                                
                                # Просто бьём
                                else:
                                    if FM:
                                        self.choice[-1] += "Dealer"
                                        path += "Dealer"
                                    self.ev[-1] += ch
                                    self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                            
                            # Иначе пробуем скипнуть патрон
                            else:
                                if MI["Beer"] != 0:
                                    if FM:
                                        self.choice[-1] += "Beer "
                                        path += "Beer "
                                    MI["Beer"] = MI["Beer"] - 1
                                    self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                                elif MI["Inverter"] != 0:
                                    if FM:
                                        self.choice[-1] += "Inverter "
                                        path += "Inverter "
                                    MI["Inverter"] = MI["Inverter"] - 1
                                    self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                                
                                # Если не получилось используем пилу/стреляем
                                elif HI["Saw"] != 0 and MI["Adrenalin"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    HI["Saw"] = HI["Saw"] - 1
                                    MI["Adrenalin"] = MI["Adrenalin"] - 1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                                
                                elif MI["Saw"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    MI["Saw"] = MI["Saw"] - 1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                                # Просто бьём
                                else:
                                    if FM:
                                        self.choice[-1] += "Dealer"
                                        path += "Dealer"
                                    self.ev[-1] += ch
                                    self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                        # Пробуем выжить
                        else:
                            if MI["Beer"] != 0:
                                if FM:
                                    self.choice[-1] += "Beer "
                                    path += "Beer "
                                MI["Beer"] = MI["Beer"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            elif MI["Inverter"] != 0:
                                if FM:
                                    self.choice[-1] += "Inverter "
                                    path += "Inverter "
                                MI["Inverter"] = MI["Inverter"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            elif HI["Inverter"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Inverter "
                                    path += "Inverter "
                                MI["Adrenalin"] = MI["Adrenalin"] - 1
                                HI["Inverter"] = HI["Inverter"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            elif HI["Beer"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Beer "
                                    path += "Beer "
                                MI["Adrenalin"] = MI["Adrenalin"] - 1
                                HI["Beer"] = HI["Beer"] - 1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            else:
                                if FM:
                                    self.choice[-1] += "Dealer"
                                    path += "Dealer"

                                # Надеемся на лучшее
                                self.ev[-1] += ch
                                self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                else: # DHP == 4

                    # Наручники + 2 Пилы
                    if LR >= 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and MI["Saw"] + \
                                     min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Handcuffs"] ), HI["Saw"] ) > 1
                                   ):
                        if FM:
                            self.choice[-1] += "Handcuffs Saw Dealer Saw Dealer"
                            path += "Handcuffs Saw Dealer Saw Dealer"
                        self.ev[-1] += ch * 4
                        self.dealer_calculate( YHP, DHP - 4, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                    # На 2 патрона Наручники + Пила
                    elif BL == 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and \
                         MI["Saw"] + min( MI["Adrenalin"] - Simulation.use_adrenalin(1, MI["Handcuffs"] ), HI["Saw"] ) != 0 ):
                        if FM:
                            self.choice[-1] += "Handcuffs Saw Dealer Dealer"
                            path += "Handcuffs Saw Dealer Dealer"
                        self.ev[-1] += ch * 3
                        self.dealer_calculate( YHP, DHP - 3, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                    # На 2 патрона Наручники
                    elif BL == 2 and ( MI["Handcuffs"] + min( MI["Adrenalin"], HI["Handcuffs"] ) != 0 and MI["Inverter"] + \
                                      min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Saw"] ), HI["Inverter"] ) > 1 ):
                        if FM:
                            self.choice[-1] += "Handcuffs Dealer Dealer"
                            path += "Handcuffs Dealer Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                    
                    # На последний патрон Пила
                    elif BL == 1 and ( MI["Saw"] + min( MI["Adrenalin"], HI["Saw"] ) != 0 and MI["Inverter"] + \
                                       min( MI["Adrenalin"] - Simulation.use_adrenalin( 1, MI["Saw"] ), HI["Inverter"] ) != 0
                                     ):
                        if FM:
                            self.choice[-1] += "Saw Dealer"
                            path += "Saw Dealer"
                        self.ev[-1] += ch * 2
                        self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                    
                    # Пробуем скипнуть патроны для комбы
                    else:

                        # Если диллер не убивает на своём ходе
                        if Simulation.can_kill( YHP, LR - 1, BL, MI, HI ) == 0:

                            # Используем наручники и пилу поскольку это всегда выгодно
                            if HI["Handcuffs"] != 0 and HI["Saw"] != 0 and MI["Adrenalin"] > 1:
                                if FM:
                                    self.choice[-1] += "Handcuffs Saw Dealer Dealer"
                                    path += "Handcuffs Saw Dealer Dealer"
                                HI["Handcuffs"] = HI["Handcuffs"] - 1
                                HI["Saw"] = HI["Handcuffs"] - 1
                                MI["Adrenalin"] -= 2
                                self.ev[-1] += ch * 3
                                self.dealer_calculate( YHP, DHP - 3, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                            elif HI["Handcuffs"] != 0 and MI["Saw"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Handcuffs Saw Dealer Dealer"
                                    path += "Handcuffs Saw Dealer Dealer"
                                HI["Handcuffs"]-=1
                                MI["Saw"]-=1
                                MI["Adrenalin"]-=1
                                self.ev[-1] += ch * 3
                                self.dealer_calculate( YHP, DHP - 3, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                            elif MI["Handcuffs"] != 0 and HI["Saw"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Handcuffs Saw Dealer Dealer"
                                    path += "Handcuffs Saw Dealer Dealer"
                                MI["Handcuffs"]-=1
                                HI["Saw"]-=1
                                MI["Adrenalin"]-=1
                                self.ev[-1] += ch * 3
                                self.dealer_calculate( YHP, DHP - 3, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                            
                            elif MI["Handcuffs"] != 0 and MI["Saw"] != 0:
                                if FM:
                                    self.choice[-1] += "Handcuffs Saw Dealer Dealer"
                                    path += "Handcuffs Saw Dealer Dealer"
                                MI["Handcuffs"]-=1
                                MI["Saw"]-=1
                                self.ev[-1] += ch * 3
                                self.dealer_calculate( YHP, DHP - 3, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                            # Используем наручники
                            elif HI["Handcuffs"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Handcuffs Dealer Dealer"
                                    path += "Handcuffs Dealer Dealer"
                                HI["Handcuffs"]-=1
                                MI["Adrenalin"]-=1
                                self.ev[-1] += ch * 2
                                self.dealer_calculate( YHP, DHP - 2, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )

                            elif HI["Handcuffs"] != 0:
                                if FM:
                                    self.choice[-1] += "Handcuffs Dealer Dealer"
                                    path += "Handcuffs Dealer Dealer"
                                MI["Handcuffs"]-=1
                                self.ev[-1] += ch * 2
                                self.dealer_calculate( YHP, DHP - 2, LR - 2, BL, ch, path, MI, HI, BM, BD, False, ind + 2, capt )
                            
                            # Используем пилу и просто бьём когда патроно нечётно
                            elif LR == 3 and HI["Handcuffs"] == 0:

                                # Используем пилу
                                if HI["Saw"] != 0 and MI["Adrenalin"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    HI["Saw"]-=1
                                    MI["Adrenalin"]-=1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                                elif MI["Saw"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    MI["Saw"]-=1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                                
                                # Просто бьём
                                else:
                                    if FM:
                                        self.choice[-1] += "Dealer"
                                        path += "Dealer"
                                    self.ev[-1] += ch
                                    self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                            # Пробуем скипнуть патрон
                            else:
                                if MI["Beer"] != 0:
                                    if FM:
                                        self.choice[-1] += "Beer "
                                        path += "Beer "
                                    MI["Beer"]-=1
                                    self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                                elif MI["Inverter"] != 0:
                                    if FM:
                                        self.choice[-1] += "Inverter "
                                        path += "Inverter "
                                    MI["Inverter"]-=1
                                    self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                                
                                # Если не получилось используем пилу/стреляем
                                elif HI["Saw"] != 0 and MI["Adrenalin"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    HI["Saw"]-=1
                                    MI["Adrenalin"]-=1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                                
                                elif MI["Saw"] != 0:
                                    if FM:
                                        self.choice[-1] += "Saw Dealer"
                                        path += "Saw Dealer"
                                    MI["Saw"]-=1
                                    self.ev[-1] += ch * 2
                                    self.dealer_calculate( YHP, DHP - 2, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )
                                
                                # Просто бьём
                                else:
                                    if FM:
                                        self.choice[-1] += "Dealer"
                                        path += "Dealer"
                                    self.ev[-1] += ch
                                    self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

                        # Пробуем скипнуть патрон
                        else:
                            if MI["Beer"] != 0:
                                if FM:
                                    self.choice[-1] += "Beer "
                                    path += "Beer "
                                MI["Beer"]-=1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            elif MI["Inverter"] != 0:
                                if FM:
                                    self.choice[-1] += "Inverter "
                                    path += "Inverter "
                                MI["Inverter"]-=1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )
                            
                            elif HI["Inverter"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Inverter "
                                    path += "Inverter "
                                    MI["Adrenalin"]-=1
                                    HI["Inverter"]-=1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            elif HI["Beer"] != 0 and MI["Adrenalin"] != 0:
                                if FM:
                                    self.choice[-1] += "Beer "
                                    path += "Beer "
                                MI["Adrenalin"]-=1
                                HI["Beer"]-=1
                                self.me_calculate( YHP, DHP, LR - 1, BL, ch, path, MI, HI, BM, BD, FM, ind + 1, capt )

                            else:

                                # Надеемся на лучшее
                                if FM:
                                    self.choice[-1] += "Dealer"
                                    path += "Dealer"
                                self.ev[-1] += ch
                                self.dealer_calculate( YHP, DHP - 1, LR - 1, BL, ch, path, MI, HI, BM, BD, False, ind + 1, capt )

    # Задача 1. Добавить логику предметам
    def dealer_calculate( self, YHP, DHP, LR, BL, ch, path, MI, HI, BM, BD, FM, ind, capt ):

        # Условия завершения рекурсии
        # 1. Кто-то умер
        if YHP < 1:
            self.lose[ self.choice.IndexOf(path) ] += ch
        elif DHP < 1:
            self.win[ self.choice.IndexOf(path) ] += ch

        # 2. Кончились патроны
        elif LR + BL != 0:

            # Шанс боевого патрона
            damage = LR / ( LR + BL )

            # Боевых больше холостых /1 HP при наличии боевых - в меня
            if LR > BL or ( DHP == 1 and LR != 0 ):
                self.ev[ self.choice.IndexOf(path) ] -= ch * damage
                self.me_calculate( YHP - 1, DHP, LR - 1, BL, ch * damage, path, MI, HI, BM, BD, FM, ind, capt )
                if (BL != 0):
                    self.me_calculate( YHP, DHP, LR, BL - 1, ch * ( 1 - damage ), path, MI, HI, BM, BD, FM, ind, capt )
            
            # Иначе - в себя
            else:
                self.ev[ self.choice.IndexOf(path) ] += ch * damage
                if (LR != 0):
                    self.me_calculate( YHP, DHP - 1, LR - 1, BL, ch * damage, path, MI, HI, BM, BD, FM, ind, capt )
                self.dealer_calculate( YHP, DHP, LR, BL - 1, ch * (1 - damage), path, MI, HI, BM, BD, FM, ind, capt )