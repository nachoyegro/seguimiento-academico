# Generated by Django 2.0.8 on 2018-08-29 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siglas', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MateriaAprobada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.CharField(choices=[('EQ', 'Equivalencia'), ('A', 'Aprobado'), ('D', 'Desaprobado'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='MateriaEnPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('tipo', models.CharField(choices=[('b', 'Basica'), ('a', 'Avanzada'), ('o', 'Optativa')], max_length=2)),
                ('creditos', models.IntegerField()),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('dni', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='PlanDeEstudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('materias', models.ManyToManyField(to='core.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=64)),
                ('comision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Comision')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Persona')),
            ],
        ),
        migrations.RemoveField(
            model_name='alumno',
            name='nombre',
        ),
        migrations.AddField(
            model_name='alumno',
            name='celular',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='comentario',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='cuatrimestre_inscripto',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='es_regular',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='legajo',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alumno',
            name='observacion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='sexo',
            field=models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alumno',
            name='telefono',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='tiene_beca',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alumno',
            name='tiene_pc',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alumno',
            name='tiene_pendrive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alumno',
            name='tiene_portatil',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alumno',
            name='tiene_tutor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='materiaaprobada',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Alumno'),
        ),
        migrations.AddField(
            model_name='materiaaprobada',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Materia'),
        ),
        migrations.AddField(
            model_name='inscripcion',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Alumno'),
        ),
        migrations.AddField(
            model_name='inscripcion',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Materia'),
        ),
        migrations.AddField(
            model_name='comision',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Materia'),
        ),
        migrations.AddField(
            model_name='carrera',
            name='planes',
            field=models.ManyToManyField(to='core.PlanDeEstudio'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='carreras',
            field=models.ManyToManyField(to='core.Carrera'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='persona',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.Persona'),
            preserve_default=False,
        ),
    ]