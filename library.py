import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Union


class Book:

    
    def __init__(self, title: str, author: str, genre: str, year: int, description: str = ""):
        self.id = None  
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.description = description
        self.status = "не прочитана"  
        self.is_favorite = False  
        self.added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'year': self.year,
            'description': self.description,
            'status': self.status,
            'is_favorite': self.is_favorite,
            'added_date': self.added_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        book = cls(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            year=data['year'],
            description=data.get('description', '')
        )
        book.id = data.get('id')
        book.status = data.get('status', 'не прочитана')
        book.is_favorite = data.get('is_favorite', False)
        book.added_date = data.get('added_date', '')
        return book
    
    def __str__(self) -> str:
        favorite_mark = " *" if self.is_favorite else ""
        return f"[{self.id}] {self.title} - {self.author} ({self.year}){favorite_mark} - {self.status}"


class Library:
    
    def __init__(self, filename: str = "books.json"):
        self.filename = filename
        self.books: List[Book] = []
        self.next_id = 1
        self.load_from_file()
    
    def add_book(self, book: Book) -> int:
        book.id = self.next_id
        self.next_id += 1
        self.books.append(book)
        self.save_to_file()
        return book.id
    
    def get_all_books(self) -> List[Book]:
        return self.books
    
    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        for book in self.books:
            if book.id == book_id:
                return book
        return None
    
    def delete_book(self, book_id: int) -> bool:
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_to_file()
            return True
        return False
    
    def update_status(self, book_id: int, status: str) -> bool:
        book = self.find_book_by_id(book_id)
        if book:
            book.status = status
            self.save_to_file()
            return True
        return False
    
    def toggle_favorite(self, book_id: int) -> bool:
        book = self.find_book_by_id(book_id)
        if book:
            book.is_favorite = not book.is_favorite
            self.save_to_file()
            return True
        return False
    
    def get_favorites(self) -> List[Book]:
        return [book for book in self.books if book.is_favorite]
    
    def search_books(self, keyword: str) -> List[Book]:
        keyword = keyword.lower()
        results = []
        for book in self.books:
            if (keyword in book.title.lower() or 
                keyword in book.author.lower() or 
                keyword in book.description.lower()):
                results.append(book)
        return results
    
    def sort_books(self, key: str, reverse: bool = False) -> List[Book]:
        if key == 'title':
            return sorted(self.books, key=lambda x: x.title.lower(), reverse=reverse)
        elif key == 'author':
            return sorted(self.books, key=lambda x: x.author.lower(), reverse=reverse)
        elif key == 'year':
            return sorted(self.books, key=lambda x: x.year, reverse=reverse)
        else:
            return self.books
    
    def filter_by_genre(self, genre: str) -> List[Book]:
        return [book for book in self.books if book.genre.lower() == genre.lower()]
    
    def filter_by_status(self, status: str) -> List[Book]:
        return [book for book in self.books if book.status.lower() == status.lower()]
    
    def get_statistics(self) -> Dict:
        total = len(self.books)
        read = len([b for b in self.books if b.status == "прочитана"])
        unread = total - read
        favorites = len(self.get_favorites())
        
        # Жанры
        genres = {}
        for book in self.books:
            genres[book.genre] = genres.get(book.genre, 0) + 1
        
        return {
            'total': total,
            'read': read,
            'unread': unread,
            'favorites': favorites,
            'genres': genres
        }
    
    def save_to_file(self) -> None:
        data = {
            'next_id': self.next_id,
            'books': [book.to_dict() for book in self.books]
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")
    
    def load_from_file(self) -> None:
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.next_id = data.get('next_id', 1)
            self.books = [Book.from_dict(book_data) for book_data in data.get('books', [])]
        except Exception as e:
            print(f"Ошибка при загрузке из файла: {e}")
            self.books = []
            self.next_id = 1


class ConsoleInterface:
    
    def __init__(self):
        self.library = Library()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        print("\n" + "=" * 60)
        print(f" {title:^58}")
        print("=" * 60)
    
    def print_menu(self):
        self.print_header("T-БИБЛИОТЕКА - ГЛАВНОЕ МЕНЮ")
        print("\n УПРАВЛЕНИЕ КНИГАМИ:")
        print("  1. Добавить книгу")
        print("  2. Просмотреть все книги")
        print("  3. Найти книгу")
        print("  4. Удалить книгу")
        print("\n ИЗБРАННОЕ:")
        print("  5. Показать избранное")
        print("  6. Добавить/удалить из избранного")
        print("\n СТАТУС:")
        print("  7. Изменить статус книги")
        print("\n СТАТИСТИКА:")
        print("  8. Статистика библиотеки")
        print("\n СИСТЕМА:")
        print("  9. Сохранить данные")
        print("  0. Выход")
        print("\n" + "-" * 60)
    
    def get_user_choice(self, max_choice: int) -> int:
        while True:
            try:
                choice = int(input("Ваш выбор: "))
                if 0 <= choice <= max_choice:
                    return choice
                print(f"Пожалуйста, введите число от 0 до {max_choice}")
            except ValueError:
                print("Ошибка! Введите число.")
    
    def input_string(self, prompt: str, required: bool = True) -> str:
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            print("Это поле обязательно для заполнения!")
    
    def input_int(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        while True:
            try:
                value = int(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"Значение должно быть не меньше {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Значение должно быть не больше {max_val}")
                    continue
                return value
            except ValueError:
                print("Ошибка! Введите целое число.")
    
    def display_books(self, books: List[Book], title: str = "СПИСОК КНИГ"):
        self.print_header(title)
        
        if not books:
            print("\n Книги не найдены.")
            return
        
        print(f"\nНайдено книг: {len(books)}")
        print("-" * 80)
        print(f"{'ID':<4} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<12} {'Избр.'}")
        print("-" * 80)
        
        for book in books:
            fav = "*" if book.is_favorite else " "
            title_short = book.title[:28] + ".." if len(book.title) > 28 else book.title.ljust(30)
            author_short = book.author[:18] + ".." if len(book.author) > 18 else book.author.ljust(20)
            
            print(f"{book.id:<4} {title_short} {author_short} {book.year:<6} {book.status:<12} {fav}")
        
        print("-" * 80)
    
    def add_book_flow(self):
        self.print_header("ДОБАВЛЕНИЕ НОВОЙ КНИГИ")
        print("\nЗаполните информацию о книге:")
        
        title = self.input_string("Название: ")
        author = self.input_string("Автор: ")
        genre = self.input_string("Жанр: ")
        year = self.input_int("Год издания: ", min_val=-3000, max_val=datetime.now().year)
        description = self.input_string("Краткое описание (Enter чтобы пропустить): ", required=False)
        
        book = Book(title, author, genre, year, description)
        book_id = self.library.add_book(book)
        
        print(f"\n Книга успешно добавлена с ID: {book_id}")
        input("\nНажмите Enter чтобы продолжить...")
    
    def view_books_flow(self):
        while True:
            self.clear_screen()
            self.print_header("ПРОСМОТР КНИГ")
            
            print("\nПараметры отображения:")
            print("  Сортировка:")
            print("    1. По названию")
            print("    2. По автору")
            print("    3. По году издания")
            print("\n  Фильтрация:")
            print("    4. По жанру")
            print("    5. По статусу (прочитана/не прочитана)")
            print("    6. Сбросить фильтры")
            print("\n  0. Вернуться в главное меню")
            
            choice = self.get_user_choice(6)
            
            if choice == 0:
                return
            
            books = self.library.get_all_books()
            
            if choice == 1:
                books = self.library.sort_books('title')
                self.display_books(books, "КНИГИ (СОРТИРОВКА ПО НАЗВАНИЮ)")
            elif choice == 2:
                books = self.library.sort_books('author')
                self.display_books(books, "КНИГИ (СОРТИРОВКА ПО АВТОРУ)")
            elif choice == 3:
                books = self.library.sort_books('year')
                self.display_books(books, "КНИГИ (СОРТИРОВКА ПО ГОДУ)")
            elif choice == 4:
                genre = self.input_string("Введите жанр для фильтрации: ")
                books = self.library.filter_by_genre(genre)
                self.display_books(books, f"КНИГИ ЖАНРА '{genre.upper()}'")
            elif choice == 5:
                status = self.input_string("Введите статус (прочитана/не прочитана): ")
                books = self.library.filter_by_status(status)
                self.display_books(books, f"КНИГИ СО СТАТУСОМ '{status.upper()}'")
            elif choice == 6:
                self.display_books(books, "ВСЕ КНИГИ")
            
            if choice in [1, 2, 3, 4, 5, 6]:
                print("\n  Нажмите Enter чтобы увидеть больше опций...", end="")
                input()
    
    def search_flow(self):
        self.print_header("ПОИСК КНИГ")
        
        keyword = self.input_string("Введите ключевое слово для поиска: ")
        results = self.library.search_books(keyword)
        
        self.display_books(results, f"РЕЗУЛЬТАТЫ ПОИСКА: '{keyword}'")
        input("\nНажмите Enter чтобы продолжить...")
    
    def delete_book_flow(self):
        self.display_books(self.library.get_all_books(), "ВЫБЕРИТЕ КНИГУ ДЛЯ УДАЛЕНИЯ")
        
        if not self.library.get_all_books():
            input("\nНажмите Enter чтобы продолжить...")
            return
        
        try:
            book_id = self.input_int("\nВведите ID книги для удаления: ")
            

            book = self.library.find_book_by_id(book_id)
            if book:
                print(f"\nВы собираетесь удалить: {book}")
                confirm = input("Подтвердите удаление (да/нет): ").lower()
                
                if confirm in ['да', 'yes', 'y', 'д']:
                    if self.library.delete_book(book_id):
                        print(" Книга успешно удалена!")
                    else:
                        print(" Ошибка при удалении")
                else:
                    print("Удаление отменено")
            else:
                print(" Книга с таким ID не найдена")
        
        except Exception as e:
            print(f"Ошибка: {e}")
        
        input("\nНажмите Enter чтобы продолжить...")
    
    def show_favorites_flow(self):
        favorites = self.library.get_favorites()
        self.display_books(favorites, "ИЗБРАННЫЕ КНИГИ")
        input("\nНажмите Enter чтобы продолжить...")
    
    def toggle_favorite_flow(self):
        self.display_books(self.library.get_all_books(), "ВЫБЕРИТЕ КНИГУ")
        
        if not self.library.get_all_books():
            input("\nНажмите Enter чтобы продолжить...")
            return
        
        book_id = self.input_int("\nВведите ID книги: ")
        book = self.library.find_book_by_id(book_id)
        
        if book:
            new_status = not book.is_favorite
            self.library.toggle_favorite(book_id)
            status_text = "добавлена в" if new_status else "удалена из"
            print(f" Книга '{book.title}' {status_text} избранное!")
        else:
            print(" Книга не найдена")
        
        input("\nНажмите Enter чтобы продолжить...")
    
    def change_status_flow(self):
        self.display_books(self.library.get_all_books(), "ВЫБЕРИТЕ КНИГУ")
        
        if not self.library.get_all_books():
            input("\nНажмите Enter чтобы продолжить...")
            return
        
        book_id = self.input_int("\nВведите ID книги: ")
        book = self.library.find_book_by_id(book_id)
        
        if book:
            print(f"\nТекущий статус: {book.status}")
            print("Доступные статусы: прочитана / не прочитана")
            new_status = self.input_string("Введите новый статус: ")
            
            if new_status in ["прочитана", "не прочитана"]:
                self.library.update_status(book_id, new_status)
                print(f" Статус книги обновлён!")
            else:
                print(" Некорректный статус")
        else:
            print(" Книга не найдена")
        
        input("\nНажмите Enter чтобы продолжить...")
    
    def show_statistics_flow(self):
        stats = self.library.get_statistics()
        
        self.print_header("СТАТИСТИКА БИБЛИОТЕКИ")
        print(f"\n Общая статистика:")
        print(f"  Всего книг: {stats['total']}")
        print(f"  Прочитано: {stats['read']}")
        print(f"  Не прочитано: {stats['unread']}")
        print(f"  В избранном: {stats['favorites']}")
        
        if stats['genres']:
            print(f"\n Распределение по жанрам:")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
                print(f"  {genre}: {count} ({percentage:.1f}%)")
        
        input("\nНажмите Enter чтобы продолжить...")
    
    def save_data_flow(self):
        self.library.save_to_file()
        print(" Данные успешно сохранены в файл!")
        input("\nНажмите Enter чтобы продолжить...")
    
    def run(self):
        while True:
            self.clear_screen()
            self.print_menu()
            choice = self.get_user_choice(9)
            
            if choice == 0:
                self.print_header("ВЫХОД")
                print("\nСохраняем данные перед выходом...")
                self.library.save_to_file()
                print(" Данные сохранены. До свидания!")
                break
            elif choice == 1:
                self.add_book_flow()
            elif choice == 2:
                self.view_books_flow()
            elif choice == 3:
                self.search_flow()
            elif choice == 4:
                self.delete_book_flow()
            elif choice == 5:
                self.show_favorites_flow()
            elif choice == 6:
                self.toggle_favorite_flow()
            elif choice == 7:
                self.change_status_flow()
            elif choice == 8:
                self.show_statistics_flow()
            elif choice == 9:
                self.save_data_flow()


def main():
    print("Запуск T-Библиотеки...")
    
    if os.path.exists("books.json"):
        print("Найден файл с данными. Загружаем...")
    
    app = ConsoleInterface()
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n️ Программа прервана пользователем. Сохраняем данные...")
        app.library.save_to_file()
        print(" Данные сохранены. До свидания!")
    except Exception as e:
        print(f"\n Произошла ошибка: {e}")
        print("Попытка сохранить данные перед выходом...")
        try:
            app.library.save_to_file()
            print(" Данные сохранены")
        except:
            print(" Не удалось сохранить данные")
    
    print("\nПрограмма завершена.")


if __name__ == "__main__":
    main()
