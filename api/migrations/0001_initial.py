# Generated by Django 2.1.2 on 2018-11-05 11:48

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=api.models.get_image_path)),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('about', models.TextField(default='', max_length=900)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_candidate', models.BooleanField(default=False)),
                ('is_company', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competence', models.CharField(max_length=120)),
                ('niveau', models.IntegerField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contrat', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=120)),
                ('document', models.FileField(db_index=True, upload_to=api.models.get_file_path)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('intitule', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=900, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('institute', models.CharField(max_length=120)),
                ('diplome', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Langue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('langue', models.CharField(max_length=120)),
                ('niveau', models.IntegerField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Metier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metier', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Offre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(default='', max_length=120)),
                ('description', models.TextField()),
                ('salaire', models.DecimalField(decimal_places=2, max_digits=12)),
                ('etat', models.CharField(default='active', max_length=50)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrat_offre', to='api.Contrat')),
                ('metier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metier_offre', to='api.Metier')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('number', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Secteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secteur', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Specialite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(default='Debutant', max_length=120)),
                ('metier', models.ManyToManyField(to='api.Metier')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birthdate', models.DateField(null=True)),
                ('etat_civil', models.CharField(max_length=80, null=True)),
                ('metier', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='metier_candidat', to='api.Specialite')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=120)),
                ('description', models.CharField(default='', max_length=800)),
                ('website', models.CharField(max_length=120, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='phone',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_number', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='metier',
            name='secteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Secteur'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Country'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='ville',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='residence', to='api.City'),
        ),
        migrations.AddField(
            model_name='offre',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_offre', to='api.Company'),
        ),
        migrations.AddField(
            model_name='langue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_langue', to='api.Candidate'),
        ),
        migrations.AddField(
            model_name='formation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_formation', to='api.Candidate'),
        ),
        migrations.AddField(
            model_name='experience',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_experience', to='api.Candidate'),
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_document', to='api.Candidate'),
        ),
        migrations.AddField(
            model_name='competence',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_competence', to='api.Candidate'),
        ),
    ]