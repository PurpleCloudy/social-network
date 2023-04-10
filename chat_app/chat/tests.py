from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from django.urls import reverse

# Create your tests here.

# BASE SETTINGS

User = get_user_model()
c = Client()

class ChatTest(TestCase):
    
    def setUp(self):
        basic_user = User(username='basic', email='basic@basic.com')
        basic_user.set_password('basic')
        basic_user.save()
        self.basic_user = basic_user
        admin_user = User(username='admin', email='admin@admin.com')
        admin_user.set_password('admin')
        admin_user.save()
        self.admin_user = admin_user

    def test_chat_view_url(self):
        print('Тестирование модуля chat - Проверка urls.py для главной страницы [ ]')
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            get_request = self.client.get(reverse('index'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для главной страницы в urls.py, правильные значения: name="index"')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для стартовой страницы. Правильный путь - ""')
        print('Тестирование модуля chat - Проверка urls.py для главной страницы [x]')
        print('Тестирование модуля chat - Проверка шаблонов [ ]')
        template_names = []
        for t in get_request.templates:
            template_names.append(t.name)
        self.assertEqual('base.html' in template_names, True, msg='Нехватает шаблона base.html, для отображения основного контента')
        self.assertEqual('index.html' in template_names, True, msg='Нехватает шаблона index.html, для отображения основного контента')
        self.assertEqual('navbar.html' in template_names, True, msg='Нехватает шаблона navbar.html, для отображения основной навигационной панели')
        not_auth_login = 'login' in str(get_request.content)
        not_auth_register = 'registration' in str(get_request.content)
        self.assertEqual(not_auth_login, True, msg='Отсутствует ссылка на логин внутри навигационной панели. Используйте имя - login')
        self.assertEqual(not_auth_register, True, msg='Отсутствует ссылка на регистрацию внутри навигационной панели. Используйте имя - registration')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        get_request = self.client.get('')
        auth_account = 'profile' in str(get_request.content)
        auth_logout = 'logout' in str(get_request.content)
        self.assertEqual(auth_account, True, msg='Отсутствует ссылка на профиль для авторизированного пользователя внутри навигационной панели. Используйте имя - profile')
        self.assertEqual(auth_logout, True, msg='Отсутствует ссылка на логаут для авторизированного пользователя внутри навигационной панели. Используйте имя - logout')
        print('Тестирование модуля chat - Проверка шаблонов [x]')

    def test_chat_model(self):
        print('Тестирование модуля chat - Проверка модели [ ]')
        print('Тестирование модуля chat - Проверка импортирования модели для "Чата" [ ]')
        try:
            from .models import ChatModel
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования модели, используйте имя - ChatModel')
        print('Тестирование модуля chat - Проверка импортирования модели для "Чата" [x]')
        from django.db.models import ForeignKey, TextField, DateTimeField
        flag_user = False
        try:
            user_field = ChatModel._meta.get_field("user")
            check_user_field = isinstance(user_field, ForeignKey)
        except:
            flag_user = True
        self.assertTrue(not flag_user, msg='Отсутствует поле user для модели')
        flag_text = False
        try:
            text_field = ChatModel._meta.get_field("text")
            check_text_field = isinstance(text_field, TextField)
        except:
            flag_text = True
        self.assertTrue(not flag_text, msg='Отсутствует поле text для модели')
        flag_date = False
        try:
            date_field = ChatModel._meta.get_field("date")
            check_date_field = isinstance(date_field, DateTimeField)
        except:
            flag_date = True
        self.assertTrue(not flag_date, msg='Отсутствует поле date для модели')
        self.assertEqual(check_user_field, True, msg='Неправильно указан тип поля для user (используйте ForeignKey(User))')
        t = ChatModel._meta.get_field("user")
        auth_user = t.deconstruct()[-1].get('to', '')
        self.assertTrue(str(auth_user) == 'auth.user', msg='Не указана модель для пользователя User в поле user. Подробнее ищите в прошлых приложениях.')
        print('Тестирование модуля chat - Проверка модели [x]')
        self.assertEqual(check_text_field, True, msg='Неправильно указан тип поля для text (используйте TextField())')
        self.assertEqual(check_date_field, True, msg='Неправильно указан тип поля для date (используйте DateTimeField(auto_now_add=True))')

    def test_chat_form_and_context(self):
        print('Тестирование модуля chat - Проверка контекста в шаблоне [ ]')
        print('Тестирование модуля chat - Проверка формы [ ]')
        get_request = self.client.get('')
        error_msg = None
        try:
            get_request.context['form']
        except KeyError as k:
            error_msg = type(k)
        self.assertNotEqual(error_msg, KeyError, msg='Ошибка при получении контекста формы на главной странице, используйте имя - form, для контекста')
        input_content = 'type="submit"' in str(get_request.content)
        text_content = 'textarea' in str(get_request.content)
        action_content = 'action="/send/"' in str(get_request.content)
        self.assertEqual(text_content, True, msg='В шаблоне формы отсутствует поле для ввода текста (textarea). Для создания этого тега необходимо использовать виджет для CharField.')
        self.assertEqual(input_content, True, msg='В шаблоне формы отсутствует кнопка подтверждения ввода')
        self.assertEqual(action_content, True, msg='В шаблоне формы отсутствует или неправильно введен адрес для отправления запроса при обработке отправки сообщения. Используйте - /send/')
        print('Тестирование модуля chat - Проверка контекста в шаблоне [x]')

    def test_chat_send_message(self):
        from django.urls import reverse
        from .models import ChatModel
        print('Тестирование модуля chat - Проверка urls.py для отправления сообщений [ ]')
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            get_request = self.client.get(reverse('send-message'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для главной страницы в urls.py, правильные значения: name="send-message"')
        print('Тестирование модуля chat - Проверка urls.py для отправления сообщений [x]')
        print('Тестирование модуля chat - Проверка создания и чтения записей [ ]')
        get_request = self.client.get('/send/')
        self.assertRedirects(get_request, '/login/?next=/send/', status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при GET запросе не авторизированного пользователя на адрес /send/. Вы должны перенаправить пользователя на страницу с логином.', fetch_redirect_response=True)
        post_request = self.client.post('/send/')
        self.assertRedirects(post_request, '/login/?next=/send/', status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе не авторизированного пользователя на адрес /send/. Вы должны перенаправить пользователя на страницу с логином.', fetch_redirect_response=True)
        login_user = self.client.login(username='basic', password='basic')
        get_request_auth = self.client.get('/send/')
        from django.urls import reverse
        self.assertRedirects(get_request_auth, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при GET запросе авторизированного пользователя на адрес /send/. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        post_request_auth_no_data = self.client.post('/send/', {})
        self.assertRedirects(post_request_auth_no_data, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе авторизированного пользователя на адрес /send/ без отправления данных. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        post_request_auth_with_data = self.client.post('/send/', {'text': 'test'})
        self.assertRedirects(post_request_auth_with_data, reverse('index'), status_code=302, target_status_code=200, msg_prefix='Ошибка перенаправления при POST запросе авторизированного пользователя на адрес /send/ с отправленными данными. Вы должны перенаправить пользователя на главную страницу приложения.', fetch_redirect_response=True)
        obj = ChatModel.objects.all()
        self.assertEquals(len(obj), 1, msg='Ошибка создания записи в чат - Не удалось создать запись')
        from django.utils import timezone
        now = timezone.now()
        self.assertEquals(obj[0].user.username, 'basic', msg='Ошибка создания записи в чат - Неправильное сохранение в поле user')
        self.assertEquals(obj[0].text, 'test', msg='Ошибка создания записи в чат - Неправильное сохранение в поле text')
        self.assertEquals(obj[0].date.date(), now.date(), msg='Ошибка создания записи в чат - Неправильное сохранение в поле date')
        post_request_auth_with_data = self.client.post('/send/', {'text': 'test template render'})
        get_request_index = self.client.get(reverse('index'))
        text_content_with_data = 'test template render' in str(get_request_index.content)
        self.assertTrue(text_content_with_data, msg='Ошибка отображения записей в чат - Нет текста сообщения на главной странице')
        print('Тестирование модуля chat - Проверка создания и чтения записей [x]')
        print('Тестирование модуля chat - Все тесты пройдены успешно!')


class ProfileTest(TestCase):
    
    def setUp(self):
        basic_user = User(username='basic', email='basic@basic.com')
        basic_user.set_password('basic')
        basic_user.save()
        self.basic_user = basic_user

    def test_account_model(self):
        from django.db.models import OneToOneField
        print('Тестирование модуля accounts - Модель для пользователя [ ]')
        print('Тестирование модуля accounts - Проверка импортирования модели для "Пользователя" [ ]')
        try:
            from .models import UserProfile
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования модели, используйте имя - UserProfile')
        print('Тестирование модуля accounts - Проверка импортирования модели для "Пользователя" [x]')

        flag_user = False
        try:
            user_field = UserProfile._meta.get_field("profile")
            check_user_field = isinstance(user_field, OneToOneField)
        except:
            flag_user = True
        self.assertTrue(not flag_user, msg='Отсутствует поле profile для модели')
        t = UserProfile._meta.get_field("profile")
        auth_user = t.deconstruct()[-1].get('to', '')
        self.assertTrue(str(auth_user) == 'auth.user', msg='Не указана модель для пользователя User в поле profile. Подробнее ищите в прошлых приложениях.')
        user_exists = User.objects.filter(username='basic').exists()
        self.assertEqual(user_exists, True, msg='Ошибка в базовых настройках (системное сообщение)')
        user_profile = UserProfile(profile=self.basic_user)
        user_profile.save()
        self.assertEqual(user_profile.profile, self.basic_user, msg='Проверьте настройки accounts/models')
        o2o_f = UserProfile._meta.get_field("profile")
        check_o2o_f = isinstance(o2o_f, OneToOneField)
        self.assertEqual(check_o2o_f, True, msg='Неправильно указан тип поля для profile (используйте OneToOneField())')
        print('Тестирование модуля accounts - Модель для пользователя [x]')

    def test_account_registration_form(self):
        from .models import UserProfile

        print('Тестирование модуля accounts - Проверка формы для регистрации[ ]')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Регистрации" [ ]')
        try:
            from .forms import RegisterForm
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования формы, используйте имя - RegisterForm')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Регистрации" [x]')
        from django.forms import CharField, EmailField
        form_field_1 = RegisterForm.declared_fields.get('username', '')
        check_form_field_1 = isinstance(form_field_1, CharField)
        self.assertEqual(check_form_field_1, True, msg='Неправильно указан тип или название поля для username (используйте CharField())')
        form_field_2 = RegisterForm.declared_fields.get('email', '')
        check_form_field_2 = isinstance(form_field_2, EmailField)
        self.assertEqual(check_form_field_2, True, msg='Неправильно указан тип или название поля для email (используйте CharField())')
        form_field_3 = RegisterForm.declared_fields.get('password', '')
        check_form_field_3 = isinstance(form_field_3, CharField)
        self.assertEqual(check_form_field_3, True, msg='Неправильно указан тип или название поля для password (используйте CharField())')
        print('Тестирование модуля accounts - Проверка формы для регистрации[x]')
        print('Тестирование модуля accounts - Проверка urls.py для регистрации [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('registration'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для registration в urls.py, правильные значения: name="registration"')
        print('Тестирование модуля accounts - Проверка urls.py для регистрации [x]')
        print('Тестирование модуля accounts - Создание пользователя [ ]')
        get_request = self.client.get('/registration/')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для регистрации. Правильный путь - registration/')
        self.assertEqual(get_request.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для регистрации. Правильно: templates/accounts/...')
        get_request_form = ('<form' in str(get_request.content), '</form>' in str(get_request.content))
        self.assertEqual(False in get_request_form, False, msg='Ошибка при GET запросе, не отображается форма на шаблоне')
        post_request = self.client.post('/registration/', {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        })
        created_user = UserProfile.objects.filter(profile__username='test')
        self.assertEqual(len(created_user), 1, msg='Ошибка при создании UserProfile')
        created_user = created_user[0]
        self.assertTrue(not created_user.profile.is_staff, msg='Для созданного пользователя необходимо добавить, что он не является сотрудником (staff = False)')
        self.assertEqual(created_user.profile.username, 'test', msg='Ошибка при создании пользователя. Необходимые поля для формы: username, email, password')
        self.assertEqual(created_user.profile.email, 'test@test.com', msg='Ошибка при создании пользователя. Необходимые поля для формы: username, email, password')
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при успешной регистрации пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Создание пользователя [x]')

    def test_account_login_form(self):
        print('Тестирование модуля accounts - Проверка формы для логина [ ]')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Логина" [ ]')
        try:
            from .forms import LoginForm
            _form = True
        except:
            _form = False
        self.assertTrue(_form, msg='Ошибка импортирования формы, используйте имя - LoginForm')
        print('Тестирование модуля accounts - Проверка импортирования формы для "Логина" [x]')
        from django.forms import CharField, EmailField
        form_field_1 = LoginForm.declared_fields.get('username', '')
        check_form_field_1 = isinstance(form_field_1, CharField)
        self.assertEqual(check_form_field_1, True, msg='Неправильно указан тип или название поля для username (используйте CharField())')
        form_field_2 = LoginForm.declared_fields.get('password', '')
        check_form_field_2 = isinstance(form_field_2, CharField)
        self.assertEqual(check_form_field_2, True, msg='Неправильно указан тип или название поля для password (используйте CharField())')
        print('Тестирование модуля accounts - Проверка формы для логина [x]')
        print('Тестирование модуля accounts - Проверка urls.py для логина [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('login'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для login в urls.py, правильные значения: name="login"')
        print('Тестирование модуля accounts - Проверка urls.py для логина [x]')
        print('Тестирование модуля accounts - Логин пользователя [ ]')
        get_request = self.client.get('/login/')
        self.assertEqual(get_request.status_code, 200, msg='Неправильно указан url для логина. Правильный путь - login/')
        self.assertEqual(get_request.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для логина. Правильно: templates/accounts/...')

        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при успешном логине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')

        post_request = self.client.post('/login/', {
            'username': 'not exists',
            'password': 'not exists',
        })
        self.assertEqual(post_request.status_code, 302, msg='Ошибка при не успешном логине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Логин пользователя [x]')

    def test_account_logout_form(self):
        print('Тестирование модуля accounts - Проверка urls.py для логаута [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('logout'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для logout в urls.py, правильные значения: name="logout"')
        print('Тестирование модуля accounts - Проверка urls.py для логаута [x]')
        print('Тестирование модуля accounts - Логаут пользователя [ ]')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        sess_before = len(self.client.session.items())
        get_request = self.client.get('/logout/')
        sess_after = len(self.client.session.items())
        self.assertEquals(sess_before > sess_after and not sess_after, True, msg='Ошибка при логауте пользователя')

        self.assertEqual(get_request.status_code, 302, msg='Ошибка при разлогине пользователя. Необходимо перенаправить (используйте redirect) пользователя на главную страницу приложения')
        print('Тестирование модуля accounts - Логаут пользователя [x]')

    def test_account_profile_view(self):
        print('Тестирование модуля accounts - Проверка urls.py для профиля [ ]')
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        rev = False
        try:
            self.client.get(reverse('profile'))
        except NoReverseMatch:
            rev = True
        self.assertTrue(not rev, msg='Ошибка в параметре name для profile в urls.py, правильные значения: name="profile"')
        print('Тестирование модуля accounts - Проверка urls.py для профиля [x]')
        print('Тестирование модуля accounts - Аутентификация [ ]')
        get_request = self.client.get('/profile/')
        self.assertEqual(get_request.status_code, 302, msg='Ошибка при заходе на страницу профиля без логина пользователя')
        self.assertEqual(get_request.url, '/login/?next=/profile/', msg='Ошибка перенаправления неавторизированного пользователя в приложении, используйте ссылку на - /login/')
        post_request = self.client.post('/login/', {
            'username': 'basic',
            'password': 'basic',
        })
        get_request_auth = self.client.get('/profile/')
        self.assertEqual(get_request_auth.status_code, 200, msg='Ошибка захода на страницу профиля с авторизированным логином пользователя')
        self.assertEqual(get_request_auth.templates[0].name.count('accounts'), 1, msg='Неправильно указан путь до файла с HTML для профиля. Правильно: templates/accounts/...')
        error_msg = None
        try:
            get_request_auth.context['profile']
        except KeyError as k:
            error_msg = type(k)
        self.assertNotEqual(error_msg, KeyError, msg='Ошибка при получении контекста в профиле, используйте имя - profile, для контекста')
        print('Тестирование модуля accounts - Аутентификация [x]')

    def test_account_profile_display(self):
        print('Тестирование модуля accounts - Отображение данных в профиле [ ]')
        from chat.models import ChatModel
        objs = ChatModel.objects.bulk_create([ChatModel(user=self.basic_user, text=f'news - {i}') for i in range(113)])
        login_user = self.client.login(username='basic', password='basic')
        get_request_auth = self.client.get('/profile/')
        input_content = '113' in str(get_request_auth.content)
        self.assertTrue(input_content == True, msg='Ошибка отображения количества сообщений из чата в профиле. Вы должны вывести сообщения принадлежащие только текущему пользователю.')
        print('Тестирование модуля accounts - Отображение данных в профиле [x]')
        print('Тестирование модуля accounts - Все тесты пройдены успешно!')
        

