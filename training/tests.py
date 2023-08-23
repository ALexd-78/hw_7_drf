from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from training.models import Course, Lesson
from users.models import User



class CourseTestCase(APITestCase):
    """Тесты модели Course"""

    def setUp(self):
        pass
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@yandex.ru',
            first_name='Test',
            last_name='Test',
            is_staff=False,
            is_superuser=False
        )

        self.user.set_password('0000')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url_course = '/course/'

    def test_create_course(self):
        """Тест создания модели Course"""
        data = {
            'title': 'course_test',
            'description': 'test test'
        }
        response = self.client.post(
            self.url_course,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_course(self):
        """Тест деталей модели Course"""
        self.test_create_course()
        response = self.client.get(f'{self.url_course}2/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': 2, 'lesson_count': 0, 'lessons': [], 'title': 'course_test',
                          'preview': None, 'description': 'test test'})
#
    def test_list_course(self):
        """Тест листа модели Course"""
        self.test_create_course()
        response = self.client.get(self.url_course)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 1, 'next': None, 'previous': None, 'results': [
                             {'id': 3, 'lesson_count': 0, 'lessons': [], 'title': 'course_test',
                              'preview': None, 'description': 'test test'}]}
                         )


class LessonsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@yandex.ru',
            first_name='Test',
            last_name='Test',
            is_staff=True,
            is_superuser=False
        )

        self.user.set_password('0000')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url_lessons = '/lessons/'
        self.url_course = '/course/'

    def test_create_lessons(self):
        """Тест создания модели Lessons"""

        data = {
            'title': 'lesson_test',
            'description': 'test test'
        }
        response_course = self.client.post(self.url_course, data=data)

        response_lessons = self.client.post(f'{self.url_lessons}create/',
                                            {'course': 4, 'title': 'lesson_test', 'description': 'test test',
                                             'owner': 4, 'link_to_video': 'https://www.youtube.com/'})

        self.assertEqual(response_lessons.status_code, status.HTTP_201_CREATED)
        response_lessons_valid_link = self.client.post(f'{self.url_lessons}create/',
                                                       {'course': 4, 'title': 'lesson_test',
                                                        'description': 'test test',
                                                        'owner': 4, 'link_to_video': 'https://www.rutube.com/'})
        self.assertEqual(response_lessons_valid_link.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_lessons(self):
        """Тест объекта модели Lessons"""
        data = {
            'title': 'lesson_test',
            'description': 'test test'
        }
        response_course = self.client.post(self.url_course, data=data)

        response_lessons = self.client.post(f'{self.url_lessons}create/',
                                            {'course': 5, 'title': 'lessons_test', 'description': 'test test',
                                             'owner': 5, 'link_to_video': 'https://www.youtube.com/'})
        response = self.client.get(f'{self.url_lessons}2/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': 2, 'title': 'lessons_test', 'preview': None, 'description': 'test test',
                          'link_to_video': 'https://www.youtube.com/', 'course': 5})


class SubscribeTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@yandex.ru',
            first_name='Test',
            last_name='Test',
            is_staff=True,
            is_superuser=False
        )

        self.user.set_password('0000')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url_course = '/course/'
        self.url_subscribe = '/subscription/'

    def test_subscription_create(self):
        """Тест на создание Subscription"""

        data_course = {
            'title': 'course_test',
            'description': 'test test'
        }
        data_subscription = {
            'course': 6,
            'is_active': True,
            'version': 5
        }
        response_course = self.client.post(self.url_course, data=data_course)

        response_subscription = self.client.post(f'{self.url_subscribe}create/',
                                              data=data_subscription)
        # print(response_subscription.json())
        # print(response_course.json())

        self.assertEqual(response_subscription.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_subscription.json(),
                         {'id': 1, 'is_active': True, 'version': '5', 'owner': None, 'course': 6})

    def test_subscription_delete(self):
        """Тест на удаление subscription"""

        data_course = {
            'title': 'course_test',
            'description': 'test test'
        }
        data_subscription = {
            'course': 7,
            'is_active': True
        }
        response_course_create = self.client.post(self.url_course, data=data_course)

        response_subscribe_create = self.client.post(f'{self.url_subscribe}create/',
                                              data=data_subscription)
        response_subscription_delete = self.client.delete(f'{self.url_subscribe}delete/2/')
        self.assertEqual(response_subscription_delete.status_code, status.HTTP_204_NO_CONTENT)