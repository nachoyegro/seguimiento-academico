# Generated by Django 2.2.13 on 2021-06-01 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('apellido', models.CharField(blank=True, max_length=255, null=True)),
                ('dni', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=128, null=True)),
                ('legajo', models.CharField(max_length=32)),
                ('es_regular', models.BooleanField(default=True)),
                ('sexo', models.CharField(blank=True, choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=2, null=True)),
                ('telefono', models.CharField(blank=True, max_length=32, null=True)),
                ('celular', models.CharField(blank=True, max_length=32, null=True)),
                ('tiene_beca', models.BooleanField(default=False)),
                ('tiene_tutor', models.BooleanField(default=False)),
                ('tiene_pc', models.BooleanField(default=False)),
                ('tiene_pendrive', models.BooleanField(default=False)),
                ('tiene_portatil', models.BooleanField(default=False)),
                ('comentario', models.CharField(blank=True, max_length=255, null=True)),
                ('observacion', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlumnoDeCarrera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promedio', models.CharField(blank=True, max_length=3, null=True)),
                ('coeficiente', models.CharField(blank=True, max_length=3, null=True)),
                ('fecha_inscripcion', models.DateField(blank=True, null=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=2)),
                ('fecha_creacion', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siglas', models.CharField(blank=True, max_length=32, null=True)),
                ('nombre', models.CharField(blank=True, max_length=128, null=True)),
                ('codigo', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carreras', models.ManyToManyField(to='core.Carrera')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Postulantes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateField()),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulantes', to='core.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='PlanDeEstudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('anio', models.IntegerField()),
                ('materias_necesarias', models.IntegerField(default=40)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Carrera')),
            ],
            options={
                'verbose_name_plural': 'Planes de estudio',
            },
        ),
        migrations.CreateModel(
            name='MateriaEnPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_en_plan', models.CharField(max_length=64)),
                ('nucleo', models.CharField(blank=True, choices=[('I', 'Introductoria'), ('B', 'Basica'), ('A', 'Avanzada'), ('C', 'Complementaria')], max_length=2, null=True)),
                ('creditos', models.IntegerField(blank=True, null=True)),
                ('codigo', models.CharField(blank=True, max_length=10, null=True)),
                ('orden_cuatrimestral', models.IntegerField(blank=True, null=True)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Area')),
                ('ciclo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Ciclo')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Materia')),
                ('obligatorias', models.ManyToManyField(blank=True, related_name='obligatoria_de', to='core.MateriaEnPlan')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.PlanDeEstudio')),
                ('recomendadas', models.ManyToManyField(blank=True, related_name='recomendada_de', to='core.MateriaEnPlan')),
            ],
            options={
                'verbose_name_plural': 'Materias de plan',
            },
        ),
        migrations.CreateModel(
            name='MateriaCursada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.CharField(blank=True, choices=[('A', 'A- Aprobado'), ('E', 'E- Pendiente de Aprobacion'), ('N', 'N- Reprobado'), ('P', 'P- Aprobado'), ('U', 'U- Ausente'), ('R', 'R- Reprobado'), ('V', 'V- Pendiente Virtual'), ('', 'Ausente de Examen')], max_length=2, null=True)),
                ('nota', models.CharField(blank=True, choices=[('PA', 'Pendiente de Aprobacion'), ('A', 'Aprobado'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=3, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('forma_aprobacion', models.CharField(blank=True, choices=[('EqE', 'Equivalencia equivalente'), ('PC', 'Promocion en otra carrera'), ('P', 'Promocion'), ('Eq', 'Equivalencia'), ('ExE', 'Examen equivalente'), ('Ex', 'Examen')], max_length=32, null=True)),
                ('acta_examen', models.CharField(blank=True, max_length=32, null=True)),
                ('acta_promocion', models.CharField(blank=True, max_length=32, null=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cursadas', to='core.Alumno')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cursadas', to='core.Carrera')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MateriaEnPlan')),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comision', models.CharField(blank=True, max_length=32, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='core.Alumno')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='core.Carrera')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Graduado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='egresos', to='core.AlumnoDeCarrera')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Carrera'),
        ),
        migrations.AddField(
            model_name='alumnodecarrera',
            name='carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Carrera'),
        ),
        migrations.AddField(
            model_name='alumnodecarrera',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.PlanDeEstudio'),
        ),
    ]
