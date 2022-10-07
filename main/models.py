from django.db import models
import requests


class DataUser(models.Model):
    name = models.CharField('Имя', max_length=20)
    username = models.CharField('Имя пользователя', max_length=20, unique=True)
    phone = models.CharField('Телефон',max_length=25)
    address_city = models.CharField('Город', max_length=50)
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.name


class AlbumUser(models.Model):
    name = models.ForeignKey(DataUser, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return self.title

    @staticmethod
    def pars_album_save(user):
        '''Функция парсит альбомы с ресурса и сохраняет Альбомы по полученному юзеру'''
        id = DataUser.objects.get(name=user.name)
        print(user.name,'is id =', id.id)
        URL_TEMPLATE = 'https://jsonplaceholder.typicode.com/albums'
        data = requests.get(URL_TEMPLATE)
        for album in data.json():
            if album['userId'] == user.id:
                user.albumuser_set.create(title=album['title'])
