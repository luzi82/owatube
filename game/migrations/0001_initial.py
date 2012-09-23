# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table('game_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('music_by', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('data_by', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('bgm', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('swf', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('state', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('successor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'], null=True)),
        ))
        db.send_create_signal('game', ['Game'])

        # Adding model 'GameDiff'
        db.create_table('game_gamediff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('ura', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('diff', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('star', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('game', ['GameDiff'])

        # Adding model 'GameComment'
        db.create_table('game_gamecomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('game', ['GameComment'])

        # Adding model 'ScoreReport'
        db.create_table('game_scorereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('diff', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('ura', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('score', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('r0', self.gf('django.db.models.fields.IntegerField')()),
            ('r1', self.gf('django.db.models.fields.IntegerField')()),
            ('r2', self.gf('django.db.models.fields.IntegerField')()),
            ('maxcombo', self.gf('django.db.models.fields.IntegerField')()),
            ('lenda', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('game', ['ScoreReport'])

        # Adding model 'ScoreReportBest'
        db.create_table('game_scorereportbest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.ScoreReport'])),
        ))
        db.send_create_signal('game', ['ScoreReportBest'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table('game_game')

        # Deleting model 'GameDiff'
        db.delete_table('game_gamediff')

        # Deleting model 'GameComment'
        db.delete_table('game_gamecomment')

        # Deleting model 'ScoreReport'
        db.delete_table('game_scorereport')

        # Deleting model 'ScoreReportBest'
        db.delete_table('game_scorereportbest')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'game.game': {
            'Meta': {'object_name': 'Game'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'bgm': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'data_by': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'music_by': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'state': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'successor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Game']", 'null': 'True'}),
            'swf': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'game.gamecomment': {
            'Meta': {'object_name': 'GameComment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'game.gamediff': {
            'Meta': {'object_name': 'GameDiff'},
            'diff': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'star': ('django.db.models.fields.IntegerField', [], {}),
            'ura': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'game.scorereport': {
            'Meta': {'object_name': 'ScoreReport'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'diff': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lenda': ('django.db.models.fields.IntegerField', [], {}),
            'maxcombo': ('django.db.models.fields.IntegerField', [], {}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'r0': ('django.db.models.fields.IntegerField', [], {}),
            'r1': ('django.db.models.fields.IntegerField', [], {}),
            'r2': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ura': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'game.scorereportbest': {
            'Meta': {'object_name': 'ScoreReportBest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.ScoreReport']"})
        }
    }

    complete_apps = ['game']