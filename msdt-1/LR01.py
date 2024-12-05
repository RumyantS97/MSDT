import os
import pdb

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from attributes import models as attr_models
from attributes.models.photo import get_default_photo_url
from common.serializers import mixins


def image_exists(image) -> bool:
    return os.path.exists(image.path)


def to_representation_by_image_format(file) -> dict:
    res = {}
    if file.endswith('.webp'):
        res = {
            'webp'  : file,
            'other' : None
        }
    else:
        res = {
            'webp'  : None,
            'other' : file
        }
    return res


class ExtendedSerializer(serializers.Serializer):
    class Meta:
        abstract = True

    def to_representation(
            self, 
            instance
            ):
        data = super().to_representation(instance)
        for key in data:
            if data[key] == '':
                data[key] = None
        return data


class ExtendedModelSerializer(ExtendedSerializer, serializers.ModelSerializer):
    class Meta:
        abstract = True


# Тестовый сериализатор
class AttributeMixinSerializer(ExtendedSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        abstract = True


class RecursiveSerializer(serializers.Serializer):
    """
    Сериализатор который вызывает сам себя. Полезен для вывода вложенных объектов
    """

    class Meta:
        abstract = True

    def to_representation(
        self, 
        value
        ):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class PhotoSerialize(ExtendedModelSerializer):
    """
    Сериализатор для фотографий с полным выводом (ссылка на фото, формат фото и источник)
    """
    photo_url = 'photos'
    image = serializers.ImageField(
        default=f'/{photo_url}/404photo.webp'
    )
    is_represent_by_format = True

    class Meta:
        model = attr_models.Photo
        fields = (
            'image', 
            'source'
            )
        abstract = True

    def to_representation(
            self, 
            instance
            ):
        data = super().to_representation(instance)
        if self.is_represent_by_format:
            data['image'] = to_representation_by_image_format(instance.image.url)
        return data


class OrganizerSerializer(serializers.Serializer):
    """
    Шаблон сериализатора для организаторов с минимальной информацией (id и имя)
    """
    id = serializers.CharField(source='user.custom_id')
    name = serializers.CharField()
    url = serializers.URLField(source='site_url')

    class Meta:
        fields = (
            'id', 
            'name', 
            'url'
            )
        abstract = True


class SocialsSerializer(ExtendedSerializer):
    """
    Шаблон сериализатора для социальных сетей
    """
    vk = serializers.URLField(required=False)
    x_site = serializers.URLField(required=False)
    instagram = serializers.URLField(required=False)
    telegram = serializers.URLField(required=False)
    zen = serializers.URLField(required=False)
    youtube = serializers.URLField(required=False)
    rutube = serializers.URLField(required=False)
    facebook = serializers.URLField(required=False)

    class Meta:
        fields = (
            'vk', 
            'x_site', 
            'instagram', 
            'telegram', 
            'zen', 
            'youtube', 
            'rutube', 
            'facebook'
            )
        abstract = True

    def validate_vk(
        self, 
        value
        ):
        if (value and not 
            value.startswith('https://vk.com/')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://vk.com/'
                )
        return value

    def validate_x_site(
        self, 
        value
        ):
        if (value and not 
            value.startswith('https://x.com') and not
              value.startswith('https://twitter.com')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://x.com или https://twitter.com'
            )
        return value

    def validate_instagram(
        self, 
        value
        ):
        if (value and not
             value.startswith('https://instagram.com/')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://instagram.com/'
                )
        return value

    def validate_telegram(
        self, 
        value
        ):
        if (value and not
             value.startswith('https://t.me/')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://t.me/'
            )
        return value

    def validate_zen(
        self, 
        value
        ):
        if (value and not
             value.startswith('https://dzen.ru/') and
               value.startswith('https://zen.yandex.ru/')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://dzen.ru или https://zen.yandex.ru/'
                )
        return value

    def validate_youtube(
        self, 
        value
        ):
        if (value and not
             value.startswith('https://youtube.com/')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://youtube.com/'
                )
        return value

    def validate_rutube(
        self, 
        value
        ):
        if (value and not
             value.startswith('https://rutube.ru/')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://rutube.ru/'
                )
        return value

    def validate_facebook(
        self, 
        value
        ):
        if (value and not
             value.startswith('https://facebook.com/')):
            raise serializers.ValidationError(
                'Ссылка должна начинаться с https://facebook.com/'
                )
        return value



class TagsSerializer(serializers.Serializer):
    """
    Шаблон сериализатора для тегов
    """
    name = serializers.CharField()

    class Meta:
        abstract = True


class ContactSerializer(ExtendedSerializer):
    """
    Шаблон сериализатора для контактов
    """

    contact = serializers.SerializerMethodField(read_only=True)
    phone = PhoneNumberField(
        required=False, 
        error_messages={'invalid': 'Введите правильный номер телефона'}
        )
    email = serializers.EmailField(required=False)
    site = serializers.URLField(required=False,)

    class Meta:
        fields = (
            'contact', 
            'phone', 
            'email', 
            'site'
            )
        abstract = True

    def get_contact(
            self, 
            instance
            ):
        contact = self.get_contact_by_fields(instance)
        if contact:
            return contact
        return (instance.vk 
                or instance.x_site 
                or instance.instagram 
                or instance.telegram 
                or instance.zen 
                or instance.youtube 
                or instance.rutube 
                or instance.facebook)

    def get_contact_by_fields(
            self, 
            obj
            ):
        attrs = [
            'site', 
            'email', 
            'phone'
            ]
        for attr in attrs:
            if getattr(obj, attr):
                if attr == 'site':
                    return getattr(obj, attr)
                elif attr == 'email':
                    return f'mailto:{getattr(obj, attr)}'
                elif attr == 'phone':
                    return f'tel:{getattr(obj, attr)}'
        return None

    def to_representation(
            self, 
            instance
            ):
        if instance is None:
            return {
                'contact'   : None,
                'phone'     : None,
                'email'     : None,
                'site'      : None
            }
        data = super().to_representation(instance)
        return data




class PlaceSerializer(ExtendedSerializer):
    id = serializers.CharField(source='custom_id', read_only=True)
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(source='place_url', read_only=True)

    class Meta:
        fields = (
            'id', 
            'name', 
            'url'
            )


class AttributeSerializer(serializers.Serializer):
    """
    Шаблон сериализатора для атрибутов
    """
    name = serializers.CharField()

    class Meta:
        fields = ('name',)
        abstract = True


class SerializerWithPhoto(serializers.Serializer):
    photo_url = 'photos'
    photo = serializers.SerializerMethodField()
    is_source = False
    is_format = True

    def get_photo(
            self, 
            obj
            ):
        if (hasattr(obj, 'photo') and
             hasattr(obj.photo, 'image') and
               image_exists(obj.photo.image)):
            source = obj.photo.source if obj.photo.source != '' else None
            url = obj.photo.image.url
            # pdb.set_trace()
            data = self.photo_to_represent(
                url, 
                source
                )
        else:
            url = get_default_photo_url(self.photo_url)
            data = self.photo_to_represent(url)
        return data

    def photo_to_represent(
            self, 
            url, 
            source=None
            ) -> dict:
        data = {}
        if self.is_format:
            data['image'] = to_representation_by_image_format(url)
        else:
            data['image'] = url
        if self.is_source:
            data['source'] = source
        return data


class SerializerWithContacts(serializers.Serializer):
    contacts = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_contacts(
            self, 
            obj
            ):
        if (hasattr(obj, 'contacts') or not
             obj.contacts or
               obj.contacts.contacts_empty()):
            return {
                'contact'   : None,
                'phone'     : None,
                'email'     : None,
                'site'      : None
            }
        else:
            return ContactSerializer(obj.contacts).data
        
    def get_socials(
            self, 
            obj
            ):
        if (hasattr(obj, 'contacts') or not
             obj.contacts or
               obj.contacts.socials_empty()):
            return {
                'vk'        : None,
                'x_site'    : None,
                'instagram' : None,
                'telegram'  : None,
                'zen'       : None,
                'youtube'   : None,
                'rutube'    : None,
                'facebook'  : None
            }
        else:
            return SocialsSerializer(obj.contacts).data