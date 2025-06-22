from django.contrib import admin
from django import forms
from itertools import chain
from django.contrib.contenttypes.models import ContentType

from .models import (
    MediaFile,
    MovieMedia,
    TVShowMedia,
    SeasonMedia,
    EpisodeMedia,
    CastMedia,
    CreatorMedia,
    WriterMedia,
)

# Admin form with combined dropdown for related object
class MediaFileAdminForm(forms.ModelForm):
    related_object = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = MediaFile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch all related model objects
        movie_qs = MovieMedia.objects.all()
        tv_qs = TVShowMedia.objects.all()
        cast_qs = CastMedia.objects.all()
        creator_qs = CreatorMedia.objects.all()
        writer_qs = WriterMedia.objects.all()
        season_qs = SeasonMedia.objects.select_related('tvshow').all()
        episode_qs = EpisodeMedia.objects.select_related('season__tvshow').all()

        # Combine all objects into a flat list of choices
        combined = list(chain(
            [(f"moviemedia-{m.pk}", f"🎬 Movie: {m.name}") for m in movie_qs],
            [(f"tvshowmedia-{t.pk}", f"📺 TV Show: {t.name}") for t in tv_qs],
            [(f"seasonmedia-{s.pk}", f"📂 {s.tvshow.name} - Season {s.season_number}") for s in season_qs],
            [(f"episodemedia-{e.pk}", f"🎞️ {e.season.tvshow.name} - S{e.season.season_number}E{e.episode_number}: {e.title}") for e in episode_qs],
            [(f"castmedia-{c.pk}", f"👤 Cast: {c.name}") for c in cast_qs],
            [(f"writermedia-{w.pk}", f"✍️ Writer: {w.name}") for w in writer_qs],
            [(f"creatormedia-{c.pk}", f"🎨 Creator: {c.name}") for c in creator_qs],
        ))

        # Set choices
        self.fields['related_object'].choices = [('', 'Select Related Object')] + combined

        # Pre-fill dropdown when editing existing entry
        if self.instance.pk:
            model_name = self.instance.content_type.model
            object_id = self.instance.object_id
            self.fields['related_object'].initial = f"{model_name}-{object_id}"



# Admin configuration for MediaFile
@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    form = MediaFileAdminForm
    exclude = ('object_id', 'content_type', 'related_object')
    list_display = ('id', 'media_type', 'file','cdn_url', 'content_type', 'object_id', 'uploaded_at')

    def save_model(self, request, obj, form, change):
        related_data = form.cleaned_data.get('related_object')
        if related_data:
            model_name, object_id = related_data.split('-')
            obj.content_type = ContentType.objects.get(model=model_name)
            obj.object_id = int(object_id)
        super().save_model(request, obj, form, change)


# Register all related media models
admin.site.register(MovieMedia)
admin.site.register(TVShowMedia)
admin.site.register(SeasonMedia)
admin.site.register(EpisodeMedia)
admin.site.register(CastMedia)
admin.site.register(CreatorMedia)
admin.site.register(WriterMedia)
