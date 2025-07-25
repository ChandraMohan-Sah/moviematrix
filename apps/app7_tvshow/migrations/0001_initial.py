# Generated by Django 5.2.3 on 2025-07-15 07:44

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app1_media_manger', '0001_initial'),
        ('app2_gener_platform', '0001_initial'),
        ('app3_cast', '0001_initial'),
        ('app4_creator', '0001_initial'),
        ('app5_writer', '0001_initial'),
        ('app8_lang_prod_company', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TvShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tvshow_created', models.DateTimeField(auto_now_add=True)),
                ('tvshow_updated', models.DateTimeField(auto_now=True)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_released_platform', to='app2_gener_platform.platform')),
                ('tvshow_cast', models.ManyToManyField(related_name='tvshow_cast', to='app3_cast.cast')),
                ('tvshow_creator', models.ManyToManyField(related_name='tvshow_creator', to='app4_creator.creator')),
                ('tvshow_genre', models.ManyToManyField(related_name='tvshow_genre', to='app2_gener_platform.genre')),
                ('tvshow_writer', models.ManyToManyField(related_name='tvshow_writer', to='app5_writer.writer')),
                ('tvshowmedia', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='app7_tvshow', to='app1_media_manger.tvshowmedia')),
            ],
        ),
        migrations.CreateModel(
            name='TvShowCoreDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_date', models.DateField()),
                ('country_of_origin', models.CharField(max_length=100)),
                ('also_known_as', models.CharField(blank=True, max_length=255)),
                ('filming_location', models.CharField(blank=True, max_length=255)),
                ('language', models.ManyToManyField(related_name='tvshow_language', to='app8_lang_prod_company.language')),
                ('production_companies', models.ManyToManyField(related_name='tvshow_prod_company', to='app8_lang_prod_company.productioncompany')),
                ('tvshow', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_core_detail', to='app7_tvshow.tvshow')),
            ],
        ),
        migrations.CreateModel(
            name='TvShowGeneralDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('is_original', models.BooleanField()),
                ('avg_rating', models.FloatField(default=0)),
                ('number_rating', models.IntegerField(default=0)),
                ('storyline', models.TextField()),
                ('tvshow', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_general_detail', to='app7_tvshow.tvshow')),
            ],
        ),
        migrations.CreateModel(
            name='TvShowRatingReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('review', models.CharField(blank=True, max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tvshow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_reviews', to='app7_tvshow.tvshow')),
                ('user_tvshow_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tvshow_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TvShowTechSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runtime', models.PositiveIntegerField(help_text='Runtime in minutes')),
                ('color', models.CharField(choices=[('color', 'Color'), ('bw', 'Black and White')], default='color', max_length=30)),
                ('sound_mix', models.CharField(choices=[('mono', 'Mono'), ('stereo', 'Stereo'), ('dolby_digital', 'Dolby Digital'), ('dts', 'DTS'), ('dolby_atmos', 'Dolby Atmos'), ('sdds', 'SDDS'), ('auro_3d', 'Auro 3D'), ('imax_6_track', 'IMAX 6-Track')], default='dolby_atmos', max_length=30)),
                ('tvshow', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_tech_specs', to='app7_tvshow.tvshow')),
            ],
        ),
        migrations.CreateModel(
            name='TvShowVotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike'), ('love', 'Love'), ('appreciate', 'Appreciate'), ('insightful', 'Insightful'), ('funny', 'Funny'), ('excited', 'Excited')], max_length=20)),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
                ('tvshow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_votes', to='app7_tvshow.tvshow')),
                ('user_vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_vote', 'tvshow')},
            },
        ),
        migrations.CreateModel(
            name='TvShowWatchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched_at', models.DateTimeField(auto_now_add=True)),
                ('duration_watched', models.PositiveIntegerField(blank=True, help_text='Duration watched in seconds', null=True)),
                ('is_completed', models.BooleanField(default=False, help_text='Whether the tvshow was fully watched')),
                ('tvshow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watch_history', to='app7_tvshow.tvshow')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_watch_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-watched_at'],
                'unique_together': {('user', 'tvshow', 'watched_at')},
            },
        ),
        migrations.CreateModel(
            name='UserTvShowViewed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('removed_at', models.DateTimeField(auto_now=True)),
                ('tvshow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_viewed_by', to='app7_tvshow.tvshow')),
                ('user_viewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_tvshow', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-viewed_at'],
                'unique_together': {('user_viewed', 'tvshow')},
            },
        ),
        migrations.CreateModel(
            name='UserTvShowWatchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('removed_at', models.DateTimeField(auto_now=True)),
                ('tvshow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_watchlisted_by', to='app7_tvshow.tvshow')),
                ('user_watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_watchlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-added_at'],
                'unique_together': {('user_watchlist', 'tvshow')},
            },
        ),
    ]
