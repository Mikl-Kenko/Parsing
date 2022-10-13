from datetime import time

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
        '''Функция парсит альбомы с ресурса и сохраняет Альбомы по полученному user'''
        id = DataUser.objects.get(name=user.name)
        URL_TEMPLATE = f'https://jsonplaceholder.typicode.com/albums/?userId={id.id}'
        data = requests.get(URL_TEMPLATE)
        for album in data.json():
            user.albumuser_set.create(title=album['title'])


class PhotoAlbumUser(models.Model):
    album = models.ForeignKey(AlbumUser, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=150, blank=True, null=True)
    url = models.URLField('Ссылка')
    thumbnailUrl = models.URLField('Ссылка эскиза')

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return self.title

    @staticmethod
    def pars_photo_save(user):
        '''Функция парсит фото с ресурса и сохраняет в БД по полученному Альбому'''
        Albums_user = DataUser.objects.get(name=user.name).albumuser_set.all()
        for album in Albums_user:
            URL_TEMPLATE = f'https://jsonplaceholder.typicode.com/photos/?albumId={album.id}'
            data = requests.get(URL_TEMPLATE)
            photo_set = []
            for photo in data.json():
                photo_set.append(PhotoAlbumUser(album=album,title=photo['title'], url=photo['url'], thumbnailUrl=photo['thumbnailUrl']))
            PhotoAlbumUser.objects.bulk_create(photo_set)

