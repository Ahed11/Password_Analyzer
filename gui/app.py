# gui/app.py
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from core.password_generator import generate_password
from core.password_analyzer import analyze_password
from core.dictionary_check import check_weak_password
from core.entropy_calculator import calculate_entropy
from core.password_rules import evaluate_strength
from core.bruteforce_time import calculate_bruteforce_time, format_time
from core.patterns_check import check_patterns

class PasswordApp(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.root.title("Password Analyzer")
        self.root.geometry("500x400")

        #self.create_widgets()

        self.welcomeFrame = tk.Frame(self.root)
        self.passwordAnalyzerFrame = tk.Frame(self.root)
        self.passwordGeneratorFrame = tk.Frame(self.root)


        #Фрейм окна приветствия
        tk.Label(self.welcomeFrame, text = "Выберите нужный инструмент", font=("Arial", 20)).pack(pady = 20)
        tk.Button(self.welcomeFrame,
                  text="Анализ пароля",
                  command=self.show_passwordAnalyzerFrame,
                  activebackground="blue", 
                  activeforeground="white",
                  anchor= "center",
                  cursor="hand2",
                  height = 3,
                  width = 20,
                  font = ("Arial", 15)).pack(anchor = "center", pady = 5) 
        tk.Button(self.welcomeFrame,
                  text="Генерация пароля",
                  command=self.show_passwordGeneratorFrame,
                  activebackground="blue", 
                  activeforeground="white",
                  anchor= "center",
                  cursor="hand2",
                  height = 3,
                  width = 20,
                  font = ("Arial", 15)).pack(anchor = "center", pady = 5)
        self.welcomeFrame.pack(fill="both", expand=True)
        tk.Button(self.welcomeFrame,
                  text="Выход",
                  command=self.root.destroy,
                  activebackground="blue", 
                  activeforeground="white",
                  anchor= "center",
                  cursor="hand2",
                  height = 3,
                  width = 20,
                  font = ("Arial", 15)).pack(anchor = "center", pady = 5)
        self.welcomeFrame.pack(fill="both", expand=True)

        #Фрейм окна анализатора
        tk.Label(self.passwordAnalyzerFrame, text = "Введите пароль", font=("Arial", 12)).pack(pady = 5)

        #Фрейм окна генератора
        tk.Label(self.passwordGeneratorFrame, text = "Выберите длину и параметры пароля", font=("Arial", 12), justify="center").pack(pady = 5)

    widgets = []

    def show_passwordAnalyzerFrame(self):
        global widgets
        
        self.welcomeFrame.forget()
        self.passwordAnalyzerFrame.pack(fill = "both")

        self.password_entry = tk.Entry(self.root, width=40, font=("Arial", 12), justify = LEFT)
        self.password_entry.pack(pady=10)    

        # Кнопки
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        
        analyzeButton = tk.Button(frame,
                  text="Анализировать", 
                  command=self.analyze_password_gui,
                  activebackground="blue", 
                  activeforeground="white", 
                  height= 3,
                  width=20,
                  anchor= "center",
                  cursor="hand2",
                  font = ("Arial", 11))
        analyzeButton.pack(side=tk.LEFT, padx=5)

        returnToWelcomeButton = tk.Button(frame,
                  text="Назад", 
                  command=self.show_welcomeFrame,
                  activebackground="blue", 
                  activeforeground="white", 
                  height= 3,
                  width=20,
                  anchor= "center",
                  cursor="hand2",
                  font = ("Arial", 11))
        returnToWelcomeButton.pack(side=tk.LEFT, padx=5)

        # Результаты
        self.result_text = tk.Text(self.root, height=15, width=60, font=("Consolas", 10))
        self.result_text.pack(pady=10)

        widgets = [frame, self.password_entry, self.result_text]

    def show_passwordGeneratorFrame(self):
        global widgets

        self.welcomeFrame.forget()
        self.passwordGeneratorFrame.pack(fill="both")

        self.password_entry = tk.Entry(self.root, width=40, font=("Arial", 12), justify = LEFT)
        self.password_entry.pack(pady=10)

        checkbutton_frame = tk.Frame(self.root, width=400)
        checkbutton_frame.pack(pady = 5)

        self.Checkbutton1 = IntVar() 
        self.Checkbutton2 = IntVar() 
        self.Checkbutton3 = IntVar() 
        self.Checkbutton4 = IntVar() 

        Button1 = Checkbutton(checkbutton_frame, text = "Прописные латинские буквы", 
                              variable = self.Checkbutton1, 
                              onvalue = 1, 
                              offvalue = 0, 
                              height = 2, 
                              width = 30) 

        Button2 = Checkbutton(checkbutton_frame, text = "Строчные латинские буквы ", 
                              variable = self.Checkbutton2, 
                              onvalue = 1, 
                              offvalue = 0, 
                              height = 2, 
                              width = 30) 

        Button3 = Checkbutton(checkbutton_frame, text = "Цифры", 
                              variable = self.Checkbutton3, 
                              onvalue = 1, 
                              offvalue = 0, 
                              height = 2, 
                              width = 30)
        
        Button4 = Checkbutton(checkbutton_frame, text = "Специальные символы",
                              variable = self.Checkbutton4,
                              onvalue = 1,
                              offvalue = 0,
                              height= 2,
                              width = 30)
            
        Button1.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        Button2.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        Button4.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        Button3.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        generateButton = tk.Button(frame,
                  text="Генерировать", 
                  command=self.generate_password_gui,
                  activebackground="blue", 
                  activeforeground="white", 
                  height= 3,
                  width=20,
                  anchor= "center",
                  cursor="hand2",
                  font = ("Arial", 11))
        generateButton.pack(side=tk.LEFT, padx=5)

        returnToWelcomeButton = tk.Button(frame,
                  text="Назад", 
                  command=self.show_welcomeFrame,
                  activebackground="blue", 
                  activeforeground="white", 
                  height= 3,
                  width=20,
                  anchor= "center",
                  cursor="hand2",
                  font = ("Arial", 11))
        returnToWelcomeButton.pack(side=tk.LEFT, padx=5)

        self.result_text = tk.Text(self.root, height=15, width=60, font=("Consolas", 10))
        self.result_text.pack(pady=10)

        widgets = [checkbutton_frame, frame, self.password_entry, self.result_text]

    def show_welcomeFrame(self):
        global widgets

        if self.passwordAnalyzerFrame.winfo_ismapped():
            self.passwordAnalyzerFrame.forget()
            for widget in widgets:
                widget.forget()
        else:
            self.passwordGeneratorFrame.forget()
            for widget in widgets:
                widget.forget()

        self.welcomeFrame.pack(fill="both", expand=True)

    def analyze_password_gui(self):

        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Предупреждение", "Введите пароль!")
            return
        
        analysis = analyze_password(password)

        weak = check_weak_password(password)

        if not weak:
            seconds = calculate_bruteforce_time(password, analysis)
            time_str = format_time(seconds)

        patterns_found = check_patterns(password)

        entropy = calculate_entropy(password, analysis)

        strength = evaluate_strength(analysis, weak)

        self.result_text.delete(1.0, tk.END)

        self.result_text.insert(tk.END, f"Длина: {analysis['length']}\n")
        self.result_text.insert(tk.END, f"Строчные: {analysis['lowercase']}\n")
        self.result_text.insert(tk.END, f"Заглавные: {analysis['uppercase']}\n")
        self.result_text.insert(tk.END, f"Цифры: {analysis['digits']}\n")
        self.result_text.insert(tk.END, f"Спецсимволы: {analysis['special']}\n")
        self.result_text.insert(tk.END, f"{'⚠ Пароль найден в словаре слабых паролей\nПредполагаемое время взлома: < 1 секунды' if weak else f'Примерное время brute-force: {time_str} '}\n")
        self.result_text.insert(tk.END, f"{'⚠ Найдены известные паттерны: ' + ', '.join(patterns_found) if patterns_found else 'Известные паттерны не найдены'}\n")
        self.result_text.insert(tk.END, f"Энтропия: {entropy:.2f}\n")
        self.result_text.insert(tk.END, f"Оценка: {strength}\n")

    def generate_password_gui(self):

        length = self.password_entry.get()

        try:
            length = int(length)
        except ValueError:
            messagebox.showerror("Ошибка", "введите целое число!")
            return
            
        if 1 <= length <= 160:
            length = length
        else:
            messagebox.showerror("Ошибка", "введите число от 1 до 160")
            return
        
        use_upper = 0
        use_lower = 0
        use_digits = 0
        use_special = 0
        
        use_upper = self.Checkbutton1.get()
        use_lower = self.Checkbutton2.get()
        use_digits = self.Checkbutton3.get()
        use_special = self.Checkbutton4.get()

        if not (use_upper or use_lower or use_digits or use_special):
            use_upper = use_lower = use_digits = 1
        
        password = generate_password(length, use_upper, use_lower, use_digits, use_special)

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        self.analyze_password_gui()