import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from core.breach_check import check_pwned_password
from core.bruteforce_time import ATTACK_SCENARIOS, calculate_bruteforce_time, format_time
from core.dictionary_check import check_weak_password, dictionary_available
from core.entropy_calculator import calculate_entropy
from core.password_analyzer import analyze_password
from core.password_generator import generate_passphrase, generate_password
from core.password_rules import evaluate_strength
from core.patterns_check import check_patterns


class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Analyzer")
        self.root.geometry("760x680")
        self.root.minsize(720, 620)

        self.clipboard_clear_job = None
        self.clipboard_last_value = None

        self.analyzer_password_var = tk.StringVar()
        self.generator_password_var = tk.StringVar()
        self.generator_mode_var = tk.StringVar(value="password")
        self.generator_length_var = tk.StringVar(value="16")
        self.passphrase_separator_var = tk.StringVar(value="-")

        self.use_upper_var = tk.IntVar(value=1)
        self.use_lower_var = tk.IntVar(value=1)
        self.use_digits_var = tk.IntVar(value=1)
        self.use_special_var = tk.IntVar(value=1)

        self.container = tk.Frame(self.root, padx=16, pady=16)
        self.container.pack(fill="both", expand=True)

        self.welcome_frame = tk.Frame(self.container)
        self.analyzer_frame = tk.Frame(self.container)
        self.generator_frame = tk.Frame(self.container)

        self._build_welcome_frame()
        self._build_analyzer_frame()
        self._build_generator_frame()
        self.show_frame(self.welcome_frame)

    def _build_welcome_frame(self):
        tk.Label(
            self.welcome_frame,
            text="Выберите нужный инструмент",
            font=("Arial", 20, "bold"),
        ).pack(pady=(60, 20))

        button_options = {
            "activebackground": "#1f6feb",
            "activeforeground": "white",
            "anchor": "center",
            "cursor": "hand2",
            "height": 2,
            "width": 24,
            "font": ("Arial", 13),
        }

        tk.Button(
            self.welcome_frame,
            text="Анализ пароля",
            command=lambda: self.show_frame(self.analyzer_frame),
            **button_options,
        ).pack(pady=8)
        tk.Button(
            self.welcome_frame,
            text="Генерация пароля",
            command=lambda: self.show_frame(self.generator_frame),
            **button_options,
        ).pack(pady=8)
        tk.Button(
            self.welcome_frame,
            text="Выход",
            command=self.root.destroy,
            **button_options,
        ).pack(pady=8)

    def _build_analyzer_frame(self):
        tk.Label(self.analyzer_frame, text="Проверка пароля", font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Label(
            self.analyzer_frame,
            text="Пароль скрыт по умолчанию. Анализ не показывает его в истории и в окне результатов.",
            font=("Arial", 10),
            justify="left",
        ).pack(anchor="w", pady=(4, 14))

        entry_row = tk.Frame(self.analyzer_frame)
        entry_row.pack(fill="x")

        self.analyzer_entry = tk.Entry(
            entry_row,
            textvariable=self.analyzer_password_var,
            width=48,
            font=("Arial", 12),
            show="*",
        )
        self.analyzer_entry.pack(side="left", fill="x", expand=True)

        self.analyzer_toggle_button = tk.Button(
            entry_row,
            text="Показать",
            width=12,
            command=lambda: self.toggle_password_visibility(self.analyzer_entry, self.analyzer_toggle_button),
        )
        self.analyzer_toggle_button.pack(side="left", padx=(8, 0))

        actions = tk.Frame(self.analyzer_frame)
        actions.pack(fill="x", pady=12)

        tk.Button(actions, text="Анализировать", width=18, command=self.analyze_password_gui).pack(side="left", padx=(0, 8))
        tk.Button(actions, text="Скопировать", width=18, command=lambda: self.copy_password(self.analyzer_password_var.get())).pack(side="left", padx=8)
        tk.Button(actions, text="Сохранить...", width=18, command=lambda: self.save_password(self.analyzer_password_var.get())).pack(side="left", padx=8)
        tk.Button(actions, text="Назад", width=18, command=lambda: self.show_frame(self.welcome_frame)).pack(side="right")

        self.analyzer_result_text = ScrolledText(
            self.analyzer_frame,
            height=24,
            width=90,
            font=("Consolas", 10),
            wrap="word",
        )
        self.analyzer_result_text.pack(fill="both", expand=True)
        self._set_result_text(self.analyzer_result_text, "Результаты анализа появятся здесь.")

    def _build_generator_frame(self):
        tk.Label(self.generator_frame, text="Генератор паролей", font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Label(
            self.generator_frame,
            text="Можно генерировать как случайную строку символов, так и passphrase из 4–6 слов.",
            font=("Arial", 10),
            justify="left",
        ).pack(anchor="w", pady=(4, 12))

        mode_row = tk.Frame(self.generator_frame)
        mode_row.pack(fill="x")
        tk.Label(mode_row, text="Режим:", font=("Arial", 11, "bold")).pack(side="left")
        tk.Radiobutton(
            mode_row,
            text="Символьный пароль",
            variable=self.generator_mode_var,
            value="password",
            command=self.update_generator_mode,
        ).pack(side="left", padx=(8, 0))
        tk.Radiobutton(
            mode_row,
            text="Passphrase",
            variable=self.generator_mode_var,
            value="passphrase",
            command=self.update_generator_mode,
        ).pack(side="left", padx=(8, 0))

        config_row = tk.Frame(self.generator_frame)
        config_row.pack(fill="x", pady=(10, 6))

        self.length_label = tk.Label(config_row, text="Длина:")
        self.length_label.pack(side="left")
        self.length_entry = tk.Entry(config_row, textvariable=self.generator_length_var, width=8)
        self.length_entry.pack(side="left", padx=(8, 18))

        self.separator_label = tk.Label(config_row, text="Разделитель:")
        self.separator_label.pack(side="left")
        self.separator_entry = tk.Entry(config_row, textvariable=self.passphrase_separator_var, width=8)
        self.separator_entry.pack(side="left", padx=(8, 0))

        charset_frame = tk.LabelFrame(self.generator_frame, text="Наборы символов", padx=10, pady=10)
        charset_frame.pack(fill="x", pady=(8, 10))

        self.charset_checkbuttons = [
            tk.Checkbutton(charset_frame, text="Строчные латинские буквы", variable=self.use_lower_var),
            tk.Checkbutton(charset_frame, text="Заглавные латинские буквы", variable=self.use_upper_var),
            tk.Checkbutton(charset_frame, text="Цифры", variable=self.use_digits_var),
            tk.Checkbutton(charset_frame, text="Спецсимволы", variable=self.use_special_var),
        ]
        for index, checkbox in enumerate(self.charset_checkbuttons):
            checkbox.grid(row=index // 2, column=index % 2, sticky="w", padx=10, pady=4)

        entry_row = tk.Frame(self.generator_frame)
        entry_row.pack(fill="x", pady=(0, 10))
        self.generator_entry = tk.Entry(
            entry_row,
            textvariable=self.generator_password_var,
            width=48,
            font=("Arial", 12),
            show="*",
        )
        self.generator_entry.pack(side="left", fill="x", expand=True)
        self.generator_toggle_button = tk.Button(
            entry_row,
            text="Показать",
            width=12,
            command=lambda: self.toggle_password_visibility(self.generator_entry, self.generator_toggle_button),
        )
        self.generator_toggle_button.pack(side="left", padx=(8, 0))

        actions = tk.Frame(self.generator_frame)
        actions.pack(fill="x", pady=(0, 12))
        tk.Button(actions, text="Сгенерировать", width=18, command=self.generate_password_gui).pack(side="left", padx=(0, 8))
        tk.Button(actions, text="Скопировать", width=18, command=lambda: self.copy_password(self.generator_password_var.get())).pack(side="left", padx=8)
        tk.Button(actions, text="Сохранить...", width=18, command=lambda: self.save_password(self.generator_password_var.get())).pack(side="left", padx=8)
        tk.Button(actions, text="Назад", width=18, command=lambda: self.show_frame(self.welcome_frame)).pack(side="right")

        self.generator_result_text = ScrolledText(
            self.generator_frame,
            height=20,
            width=90,
            font=("Consolas", 10),
            wrap="word",
        )
        self.generator_result_text.pack(fill="both", expand=True)
        self._set_result_text(self.generator_result_text, "Здесь появится разбор сгенерированного пароля или passphrase.")
        self.update_generator_mode()

    def show_frame(self, frame):
        for item in (self.welcome_frame, self.analyzer_frame, self.generator_frame):
            item.pack_forget()
        frame.pack(fill="both", expand=True)

    def update_generator_mode(self):
        is_passphrase = self.generator_mode_var.get() == "passphrase"
        self.length_label.config(text="Слов (4-6):" if is_passphrase else "Длина:")
        state = "normal" if is_passphrase else "disabled"
        self.separator_label.config(state=state)
        self.separator_entry.config(state=state)
        for checkbox in self.charset_checkbuttons:
            checkbox.config(state="disabled" if is_passphrase else "normal")

    def toggle_password_visibility(self, entry_widget, button_widget):
        if entry_widget.cget("show") == "*":
            entry_widget.config(show="")
            button_widget.config(text="Скрыть")
        else:
            entry_widget.config(show="*")
            button_widget.config(text="Показать")

    def copy_password(self, password):
        if not password:
            messagebox.showwarning("Предупреждение", "Сначала введите или сгенерируйте пароль.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.clipboard_last_value = password

        if self.clipboard_clear_job:
            self.root.after_cancel(self.clipboard_clear_job)
        self.clipboard_clear_job = self.root.after(20000, self.clear_clipboard)

        messagebox.showinfo("Скопировано", "Пароль скопирован")

    def clear_clipboard(self):
        try:
            if self.root.clipboard_get() == self.clipboard_last_value:
                self.root.clipboard_clear()
        except tk.TclError:
            pass
        finally:
            self.clipboard_clear_job = None
            self.clipboard_last_value = None

    def save_password(self, password):
        if not password:
            messagebox.showwarning("Предупреждение", "Сначала введите или сгенерируйте пароль.")
            return

        confirmed = messagebox.askyesno(
            "Подтверждение",
            "Сохранение пароля в файл может быть небезопасным. Продолжить?",
        )
        if not confirmed:
            return

        target_path = filedialog.asksaveasfilename(
            title="Сохранить пароль",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=str(Path.cwd()),
        )
        if not target_path:
            return

        Path(target_path).write_text(password, encoding="utf-8")
        messagebox.showinfo("Готово", "Пароль сохранён в файл.")

    def analyze_password_gui(self):
        password = self.analyzer_password_var.get()
        if not password:
            messagebox.showwarning("Предупреждение", "Введите пароль для анализа.")
            return

        self.render_analysis(password, self.analyzer_result_text)

    def generate_password_gui(self):
        raw_value = self.generator_length_var.get()
        try:
            amount = int(raw_value)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число.")
            return

        mode = self.generator_mode_var.get()

        try:
            if mode == "passphrase":
                if not 4 <= amount <= 6:
                    messagebox.showerror("Ошибка", "Для passphrase выберите от 4 до 6 слов.")
                    return
                separator = self.passphrase_separator_var.get()
                password = generate_passphrase(amount, separator)
            else:
                if not 1 <= amount <= 160:
                    messagebox.showerror("Ошибка", "Введите длину от 1 до 160.")
                    return

                selected_groups = sum(
                    [
                        self.use_upper_var.get(),
                        self.use_lower_var.get(),
                        self.use_digits_var.get(),
                        self.use_special_var.get(),
                    ]
                )
                if selected_groups == 0:
                    messagebox.showerror("Ошибка", "Выберите хотя бы один набор символов.")
                    return
                if amount < selected_groups:
                    messagebox.showerror(
                        "Ошибка",
                        f"Для {selected_groups} выбранных наборов минимальная длина — {selected_groups}",
                    )
                    return

                password = generate_password(
                    amount,
                    self.use_upper_var.get(),
                    self.use_lower_var.get(),
                    self.use_digits_var.get(),
                    self.use_special_var.get(),
                )
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))
            return

        self.generator_password_var.set(password)
        self.generator_entry.config(show="*")
        self.generator_toggle_button.config(text="Показать")
        self.render_analysis(password, self.generator_result_text)

    def render_analysis(self, password, result_widget):
        analysis = analyze_password(password)
        weak = check_weak_password(password)
        breach = check_pwned_password(password)
        patterns_found = check_patterns(password)
        entropy = calculate_entropy(password, analysis)
        strength = evaluate_strength(analysis, weak, patterns_found, breach["count"])
        brute_force = calculate_bruteforce_time(password, analysis)

        lines = [
            f"Длина: {analysis['length']}",
            f"Уникальные символы: {analysis['unique_chars']}",
            f"Строчные буквы: {'да' if analysis['lowercase'] else 'нет'}",
            f"Заглавные буквы: {'да' if analysis['uppercase'] else 'нет'}",
            f"Цифры: {'да' if analysis['digits'] else 'нет'}",
            f"Спецсимволы: {'да' if analysis['special'] else 'нет'}",
            f"Passphrase-структура: {'да' if analysis['is_passphrase'] else 'нет'}",
            "",
            f"Словарная проверка: {'пароль найден в локальном словаре слабых паролей' if weak else 'совпадений в локальном словаре не найдено'}",
            f"Локальный словарь: {'подключён' if dictionary_available() else 'файл rockyou.txt не найден'}",
            f"Проверка HIBP: {breach['message']}",
            f"Паттерны: {', '.join(patterns_found) if patterns_found else 'известные паттерны не найдены'}",
            f"Энтропия: {entropy:.2f} бит",
            f"Оценка: {strength}",
            "",
            "Оценка времени перебора:",
        ]

        for scenario_key, seconds in brute_force.items():
            scenario_name = ATTACK_SCENARIOS[scenario_key][0]
            lines.append(f"  {scenario_name}: {format_time(seconds)}")

        self._set_result_text(result_widget, "\n".join(lines))

    def _set_result_text(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state="disabled")
