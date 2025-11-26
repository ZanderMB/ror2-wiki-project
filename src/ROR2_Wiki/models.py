from django.db import models

# Create your models here.
class Monster(models.Model):
    MonsterImg = models.SlugField(max_length=500)
    MonsterName = models.SlugField(max_length=74, primary_key=True)
    MonsterHealth = models.SlugField(max_length=74)
    MonsterDamage = models.SlugField(max_length=74)
    MonsterHPRegen = models.SlugField(max_length=74)
    MonsterArmour = models.SlugField(max_length=74)
    MonsterSpeed = models.SlugField(max_length=74)
    Class = models.SlugField(max_length=74)
    MonsterType = models.SlugField(max_length=74)

class Item(models.Model):
    ItemImg = models.SlugField(max_length=500)
    ItemName = models.SlugField(max_length=124, primary_key=True)
    ItemDescription = models.SlugField(max_length=750)
    ItemStackType = models.SlugField(max_length=74)
    ItemTier = models.SlugField(max_length=74)
    ItemActPass = models.SlugField(max_length=74)
    Cooldown = models.SlugField(max_length=74)

class Survivor(models.Model):
    SurvivorImg = models.SlugField(max_length=500)
    SurvivorName = models.SlugField(max_length=74, primary_key=True)
    SurvivorHealth = models.SlugField(max_length=74)
    SurvivorDamage = models.SlugField(max_length=74)
    SurvivorHPRegen = models.SlugField(max_length=74)
    Class = models.SlugField(max_length=74)
    SurvivorArmour = models.SlugField(max_length=74)
    SurvivorSpeed = models.SlugField(max_length=74)
    SurvivorMass = models.SlugField(max_length=74)
    SurvivorDescription = models.SlugField(max_length=750)   

