from django.db import models

class BlockID(models.Model):
    b_id=models.CharField(max_length=1)
    long_name=models.CharField(max_length=8)

    def __str__(self):
        return self.long_name

class Person(models.Model):
    block = models.ForeignKey(BlockID)
    p_id=models.CharField(max_length=10,default="")
    f_name = models.CharField(max_length=15,default="")
    l_name=models.CharField(max_length=15,default="")

    def __str__(self):
        return self.f_name + ' ' + self.l_name

class ScoreKeeper(models.Model):
    username=models.CharField(max_length=10,default='Guest')
    active_score=models.IntegerField(default=0)
    high_score=models.IntegerField(default=0)