# coding: utf-8

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Hidden
from crispy_forms.bootstrap import StrictButton
from zds.forum.models import Forum, Topic
from zds.utils.forms import CommonLayoutEditor, TagValidator
from django.utils.translation import ugettext_lazy as _


class TopicForm(forms.Form):
    title = forms.CharField(
        label=_('Titre'),
        max_length=Topic._meta.get_field('title').max_length,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Titre de mon sujet'),
                'required': 'required',
            }
        )
    )

    subtitle = forms.CharField(
        label=_('Sous-titre'),
        max_length=Topic._meta.get_field('subtitle').max_length,
        required=False,
    )

<<<<<<< 7b7a8ddbd9e3c810b7e62dac1bf9c9bfd6d3b642
=======
    section = forms.ModelChoiceField(
        label=_("Categorie"),
        queryset=Forum.objects.all(),
        widget=forms.Select(
            attrs={
                'required': 'required',
            }
        )
    )

>>>>>>> Suppression d'un print() et Modification de section dans TopicForm
    tags = forms.CharField(
        label=_(u'Tag(s) séparés par une virgule (exemple: python,django,web)'),
        max_length=64,
        required=False,
        widget=forms.TextInput(
            attrs={
                'data-autocomplete': '{ "type": "multiple", "fieldname": "title", "url": "/api/tags/?search=%s" }'
            }
        )
    )

    text = forms.CharField(
        label='Texte',
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Votre message au format Markdown.'),
                'required': 'required',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title', autocomplete='off'),
            Field('subtitle', autocomplete='off'),
            Field('tags'),
            CommonLayoutEditor(),
        )

    def clean(self):
        cleaned_data = super(TopicForm, self).clean()

        title = cleaned_data.get('title')
        section = cleaned_data.get('section')
        text = cleaned_data.get('text')
<<<<<<< 7b7a8ddbd9e3c810b7e62dac1bf9c9bfd6d3b642
        tags = cleaned_data.get('tags')

=======
        
>>>>>>> Suppression d'un print() et Modification de section dans TopicForm
        if title is not None:
            if not title.strip():
                self._errors['title'] = self.error_class(
                    [_(u'Le champ titre ne peut être vide')])
                if 'title' in cleaned_data:
                    del cleaned_data['title']
        if text is not None and not text.strip():
            self._errors['text'] = self.error_class(
                [_(u'Le champ text ne peut être vide')])
            if 'text' in cleaned_data:
                del cleaned_data['text']

        if text is not None and len(text) > settings.ZDS_APP['forum']['max_post_length']:
            self._errors['text'] = self.error_class(
                [_(u'Ce message est trop long, il ne doit pas dépasser {0} '
                   u'caractères').format(settings.ZDS_APP['forum']['max_post_length'])])

        validator = TagValidator()
        if not validator.validate_raw_string(tags):
            self._errors['tags'] = self.error_class(validator.errors)
        return cleaned_data


class PostForm(forms.Form):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Votre message au format Markdown.'),
                'required': 'required',
            }
        )
    )

    def __init__(self, topic, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            CommonLayoutEditor(),
            Hidden('last_post', '{{ last_post_pk }}'),
        )
        if topic.antispam(user):
            if 'text' not in self.initial:
                self.helper['text'].wrap(
                    Field,
                    placeholder=_(u'Vous venez de poster. Merci de patienter '
                                  u'au moins 15 minutes entre deux messages consécutifs '
                                  u'afin de limiter le flood.'),
                    disabled=True)
        elif topic.is_locked:
            if 'text' not in self.initial:
                self.helper['text'].wrap(
                    Field,
                    placeholder=_(u'Ce topic est verrouillé.'),
                    disabled=True
                )

    def clean(self):
        cleaned_data = super(PostForm, self).clean()

        text = cleaned_data.get('text')

        if text is None or not text.strip():
            self._errors['text'] = self.error_class(
                [_(u'Vous devez écrire une réponse !')])

        elif len(text) > settings.ZDS_APP['forum']['max_post_length']:
            self._errors['text'] = self.error_class(
                [_(u'Ce message est trop long, il ne doit pas dépasser {0} '
                   u'caractères').format(settings.ZDS_APP['forum']['max_post_length'])])

        return cleaned_data


class MoveTopicForm(forms.Form):

    forum = forms.ModelChoiceField(
        label=_("Forum"),
        queryset=Forum.objects.all(),
        required=True,
    )

    def __init__(self, topic, *args, **kwargs):
        super(MoveTopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('topic-edit')
        self.helper.form_class = 'modal modal-flex'
        self.helper.form_id = 'move-topic'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('forum'),
            Hidden('move', ''),
            Hidden('topic', topic.pk),
            StrictButton(_('Valider'), type='submit'),
        )
