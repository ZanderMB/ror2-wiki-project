from django.db import models

# Create your models here.
class Monster(models.Model):
    MonsterImg = models.CharField(max_length=500)
    MonsterName = models.CharField(max_length=74, primary_key=True)
    MonsterHealth = models.CharField(max_length=74)
    MonsterDamage = models.CharField(max_length=74)
    MonsterHPRegen = models.CharField(max_length=74)
    MonsterArmour = models.CharField(max_length=74)
    MonsterSpeed = models.CharField(max_length=74)
    Class = models.CharField(max_length=74)
    MonsterType = models.CharField(max_length=74)

class Item(models.Model):
    ItemImg = models.CharField(max_length=500)
    ItemName = models.CharField(max_length=124, primary_key=True)
    ItemDescription = models.CharField(max_length=750)
    ItemStackType = models.CharField(max_length=74)
    ItemTier = models.CharField(max_length=74)
    ItemActPass = models.CharField(max_length=74)
    Cooldown = models.CharField(max_length=74)

class Survivor(models.Model):
    SurvivorImg = models.CharField(max_length=500)
    SurvivorName = models.CharField(max_length=74, primary_key=True)
    SurvivorHealth = models.CharField(max_length=74)
    SurvivorDamage = models.CharField(max_length=74)
    SurvivorHPRegen = models.CharField(max_length=74)
    Class = models.CharField(max_length=74)
    SurvivorArmour = models.CharField(max_length=74)
    SurvivorSpeed = models.CharField(max_length=74)
    SurvivorMass = models.CharField(max_length=100)
    SurvivorDescription = models.CharField(max_length=750)

