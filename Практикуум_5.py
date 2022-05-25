# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 16:54:48 2021

@author: Anastasia
"""

import numpy as np
class ChessBoard:
    count = 0 # счетчик отслеживания ходов
    def __init__(self):
        self.objectboard = self.form_board()
    def __str__(self): 
        board = self.draw_board(self.objectboard.T) 
        string = ''
        for i in reversed(range(8)): #переворачиваем массив, чтобы белые были снизу
            string += str(board[i])  + '\n'
        return string
    def form_board(self): 
        board = np.zeros((8,8), dtype = object) # заполняем массив нулями
        # расставляем белые фигуры на доску, кроме пешек
        WhiteRook1=Rook(0,0,'w',board)
        WhiteRook2 = Rook(7, 0, 'w', board)
        WhiteKnight1 = Knight(1, 0, 'w', board)
        WhiteKnight2 = Knight(6, 0, 'w', board)
        WhiteBishop1 = Bishop(2, 0, 'w', board)
        WhiteBishop2 = Bishop(5, 0, 'w', board)
        WhiteQueen = Queen(3, 0, 'w', board)
        WhiteKing = King(4, 0, 'w', board)
        # расставляем пешек
        for i in range(8):
            exec("WPawn" + str(i+1)  + "= Pawn(i, 1, 'w', board)")  
        # расставляем черные фигуры на доску, кроме пешек
        BlackRook1 = Rook(0, 7, 'b', board)
        BlackRook2 = Rook(7, 7, 'b', board)
        BlackKnight1 = Knight(1, 7, 'b', board)
        BlackKnight2 = Knight(6, 7, 'b', board)
        BlackBishop1 = Bishop(2, 7, 'b', board)
        BlackBishop2 = Bishop(5, 7, 'b', board)
        BlackQueen = Queen(3, 7, 'b', board)
        BlackKing = King(4, 7, 'b', board)
        # расставляем пешек
        for i in range(8):
            exec("BPawn" + str(i+1)  + "= Pawn(i, 6, 'b', board)")  
        return board 
    
    def draw_board(self, board):
        func_sym_col = np.vectorize(self.retrieve_piece) # векторизированная версия функции
        symbolic_board = func_sym_col(board)
        return symbolic_board

    def retrieve_piece(self, piece):
        if isinstance(piece, ChessPiece):
            return str(piece.symbol+piece.color) # выводим названия объектов на экран
        else:
            return '0 '

    def rules(self, piece, i, j, m, n):
        board = self.objectboard
        if ((self.__class__.count % 2) == 0):
            if (piece.color == 'b'):
                raise Exception('Ходит белый')
        else:
            if (piece.color == 'w'):
                raise Exception('Ходит черный')
        # проверяем корректность ходов фигур
        piece_type = piece.symbol 
        check_new_pos = 0 
        opponent_king = 0 
        auxboard = []
        if ((m - i) >= 0):
            check1 = 1
        else:
            check1 = 0
        if ((n - j) >= 0):
            check2 = 1
        else:
            check2 = 0

        if piece_type == 'K':
            if (abs(i - m) > 1):
                raise Exception('Не верный ход для короля')
            elif (abs(j - n) > 1) :
                raise Exception('Не верный ход для короля')
            elif check_new_pos:
                raise Exception('Король не может перейти на поле с угрозой')
            elif opponent_king:
                raise Exception('Вы не можете подходить слишком близко к королю противника')

        elif piece_type == 'Q':
            if not ((abs((i - m) / (j - n)) == 1) or ((i - m) == 0) or ((j - n) == 0)):
                raise Exception('Не верный ход для королевы')
            if (i - m) == 0:
                if check2:
                    auxboard = board[i][j+1:n]
                else:
                    auxboard = board[i][n+1:j]
            elif (j - n) == 0:
                if check1:
                    auxboard = board[i+1:m][j]
                else:
                    auxboard = board[m+1:i][j]
            else:
                if check1 and check2:
                    for ct in range(m - i - 1):
                        auxboard.append(board[i + 1 + ct][j + 1 + ct])
                elif check1 and (not check2):
                    for ct in range(m - i  - 1):
                        auxboard.append(board[i + 1 + ct][j + 1 - ct])
                elif (not check1) and check2:
                    for ct in range(i - m - 1):
                        auxboard.append(board[i + 1 - ct][j +1 + ct])
                elif (not check1) and (not check2):
                    for ct in range(i - m - 1):
                        auxboard.append(board[i + 1 - ct][j + 1 - ct])
            if not (all(p == 0 for p in auxboard)):
                raise Exception('Путь закрыт')

        elif piece_type == 'R':
            if not (((i - m) == 0) or ((j - n) == 0)):
                raise Exception('Не верный ход для ладьи')
            if (i - m) == 0:
                if check2:
                    auxboard = board[i][j+1:n]
                else:
                    auxboard = board[i][n+1:j]
            elif (j - n) == 0:
                if check1:
                    auxboard = board[i+1:m][j]
                else:
                    auxboard = board[m+1:i][j]
            if not (all(p == 0 for p in auxboard)):
                raise Exception('Путь закрыт')

        elif piece_type == 'B':
            if not (abs((i - m) / (j - n)) == 1):
                raise Exception('Не верный ход для слона')
            if check1 and check2:
                for ct in range(m - i - 1):
                    auxboard.append(board[i + 1 + ct][j + 1 + ct])
            elif check1 and (not check2):
                for ct in range(m - i  - 1):
                    auxboard.append(board[i + 1 + ct][j + 1 - ct])
            elif (not check1) and check2:
                for ct in range(i - m - 1):
                    auxboard.append(board[i + 1 - ct][j +1 + ct])
            elif (not check1) and (not check2):
                for ct in range(i - m - 1):
                    auxboard.append(board[i + 1 - ct][j + 1 - ct])
                    print(board[i + 1 - ct][j + 1 - ct])
            if not (all(p == 0 for p in auxboard)):
                raise Exception('Путь закрыт')
        elif piece_type == 'N': 
            if not (((abs(i - m) == 2) and (abs(j - n) == 1)) or  ((abs(i - m) == 1) and (abs(j - n) == 2))):
                raise Exception('Не верный ход для коня')

        elif piece_type == 'P':
            if piece.color == 'w': # условие для белых пешек
                if piece.count == 0:
                    if not(((n - j) == 2) or ((n - j) == 1) and ((i - m) == 0)):
                        raise Exception('Неверный ход для пешки')
                elif piece.count != 0:
                    if not((n - j) == 1):
                        raise Exception('Неверный ход для пешки')
            else: # условие для черных пешек
                if piece.count == 0:
                    if not(((n - j) == -2) or ((n - j) == -1) and ((i - m) == 0)):
                        raise Exception('Неверный ход для пешки')
                elif piece.count != 0:
                    if not((n - j) == -1):
                        raise Exception('Неверный ход для пешки')

        # Ограничение на переход к квадрату, который занят фишкой того же цвета
        if board[m][n] != 0: # Есть фигура в конечной позиции
            if board[i][j].color == board[m][n].color:# Фигура того же цвета
                raise Exception("В этой позиции уже стоит ваша фигура")
            elif board[m][n].symbol == 'K':
                raise Exception("Вы не можете занять место короля")
        if ((piece_type == 'P') or (piece_type == 'K')):
            piece.count += 1
        return 1 

    def move(self, position):
        #вводим координаты доски
        letstr = 'abcdefgh'
        numstr = '12345678'
        board = self.objectboard
        if not (len(position) == 4):
            raise ValueError('Введите 4 символа для хода, например: e2e3');
        # Конечная и начальная позиции
        initial_pos = position[:2]
        final_pos = position[-2:]
        if not (str == type(initial_pos) and (str == type(final_pos))):     # Проверяем что аргументы-строка
            raise TypeError('Позиции должны быть строкой')
        elif not ((initial_pos[0] in letstr) and (initial_pos[1] in numstr)): # Проверка есть ли начальная клетка на доске
            raise ValueError('Позиция дожна быть от a1 до h8')
        elif not ((final_pos[0] in letstr) and (final_pos[1] in numstr)): # Проверка есть ли конечная клетка на доске
            raise ValueError('Позиция дожна быть от a1 до h8')
        elif initial_pos == final_pos: # проверяем не совпадают ли начальная и конечная позиции
            raise ValueError('Конечная позиция должна отличаться от начальной')
        # Определяем есть ли на начальном квадрате фигура
        i = letstr.index(initial_pos[0]) ; j = numstr.index(initial_pos[1]) # Начальная позиция в числовом виде
        m = letstr.index(final_pos[0]); n = numstr.index(final_pos[1]) # Финальная позиция в числовом виде
        if not (isinstance(board[i][j], ChessPiece)):
            raise Exception('В этой клетке нет фигуры')
        piece = board[i][j]
        if self.rules(piece, i, j, m, n) != 1:
            raise('Этот ход не разрешен')
        # Перемещаем фигуру по доске
        piece.movepiece(i, j, m, n, board)
        self.__class__.count += 1 # подсчитываем ходы
        print("count=", self.__class__.count)
        
class ChessPiece: # базовый класс
    def __init__(self, x, y, color): 
        self.pos_x = x
        self.pos_y = y
        self.color = color
       
    def movepiece(self, i, j, m, n, chessboard):  # реализация хода
        self.pos_x = i
        self.pos_y = j
        chessboard[i][j] = 0 # предыдущая позиция становится равна 0
        chessboard[m][n] = self

class King(ChessPiece):
        def __init__(self, x, y, color, chessboard):
            ChessPiece.__init__(self, x, y, color)
            self.symbol = 'K'
            self.count = 0
            chessboard[self.pos_x][self.pos_y] = self

class Queen(ChessPiece):
        def __init__(self, x, y, color, chessboard):
            ChessPiece.__init__(self, x, y, color)
            self.symbol = 'Q'
            chessboard[self.pos_x][self.pos_y] = self

class Rook(ChessPiece):
        def __init__(self, x, y, color, chessboard):
            ChessPiece.__init__(self, x, y, color)  
            self.symbol = 'R'
            chessboard[self.pos_x][self.pos_y] = self

class Bishop(ChessPiece):
        def __init__(self, x, y, color, chessboard):
            ChessPiece.__init__(self, x, y, color)
            self.symbol = 'B'
            chessboard[self.pos_x][self.pos_y] = self

class Knight(ChessPiece):
        def __init__(self, x, y, color, chessboard):
            ChessPiece.__init__(self, x, y, color)
            self.symbol = 'N'
            chessboard[self.pos_x][self.pos_y] = self

class Pawn(ChessPiece):
        def __init__(self, x, y, color, chessboard):
            ChessPiece.__init__(self, x, y, color)
            self.symbol = 'P'
            self.count = 0 # для отслеживания начала движения
            chessboard[self.pos_x][self.pos_y] = self
 # вывод доски
chessboard = ChessBoard()
print(chessboard)
while True:
    XOD=input("Введите ваш ход в формате начальная позиция-конечная позиция, например e2e3:")
    print(XOD)
    chessboard.move(XOD)
    print(chessboard)