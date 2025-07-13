# from django.contrib import admin
# from .models import MultyTest, MultyAnswer, TestResponse2, Tests
# from django.utils.translation import gettext_lazy as _
#
# # 🔹 Инлайн для ответов внутри вопроса
# class MultyAnswerInline(admin.TabularInline):
#     model = MultyTest.answers.through
#     extra = 2
#     verbose_name = _("Связь вопроса с ответами")
#     verbose_name_plural = _("Связи вопросов с ответами")
#
# # 🔹 Инлайн для вопросов внутри теста
# class MultyTestInline(admin.TabularInline):
#     model = Tests.tests.through
#     extra = 2
#     verbose_name = _("Связь теста с вопросами")
#     verbose_name_plural = _("Связи тестов с вопросами")
#
# # 🔹 Админка для тестов
# class TestsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)
#     inlines = [MultyTestInline]
#     filter_horizontal = ('tests',)
#     verbose_name = _("Тест-курс")
#     verbose_name_plural = _("Тест-курсы")
#
# # 🔹 Админка для вопросов
# class MultyTestAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'lesson')
#     list_filter = ('lesson',)
#     search_fields = ('name',)
#     inlines = [MultyAnswerInline]
#     filter_horizontal = ('answers',)
#     verbose_name = _("Вопрос")
#     verbose_name_plural = _("Вопросы")
#
# # 🔹 Админка для ответов
# class MultyAnswerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'placeholder', 'name')
#     search_fields = ('name', 'placeholder')
#     verbose_name = _("Ответ")
#     verbose_name_plural = _("Ответы")
#
# # 🔹 Админка для ответов студентов
# class TestResponse2Admin(admin.ModelAdmin):
#     list_display = ('id', 'student', 'test', 'multy_test', 'submitted_at')
#     list_filter = ('test', 'student')
#     search_fields = ('student__username', 'test__name')
#     verbose_name = _("Ответ на тест")
#     verbose_name_plural = _("Ответы на тесты")
#
# # ✅ Регистрация в нужном порядке
# admin.site.register(Tests, TestsAdmin)           # 1️⃣ Тест-курсы
# admin.site.register(MultyTest, MultyTestAdmin)   # 2️⃣ Вопросы
# admin.site.register(MultyAnswer, MultyAnswerAdmin) # 3️⃣ Ответы
# admin.site.register(TestResponse2, TestResponse2Admin) # 4️⃣ Ответы студентов
