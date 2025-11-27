import pandas as pd
from django.core.management.base import BaseCommand
from ROR2_Wiki.models import Item, Monster, Survivor

class Command(BaseCommand):
    help = 'Import data from separate CSV files for Monsters, Items, and Survivors'

    def handle(self, *args, **kwargs): #Paths to my data filses
        monster_file_path = '/app/data-dump/monster-data.csv'
        item_file_path = '/app/data-dump/item-data.csv'
        survivor_file_path = '/app/data-dump/survivor-data.csv'

        # Import functions
        self.import_monsters(monster_file_path)
        self.import_items(item_file_path)
        self.import_survivors(survivor_file_path)

        self.stdout.write(self.style.SUCCESS('\nAll data has been successfully imported.'))

    def import_monsters(self, file_path):
        """Imports Monster data from a given CSV file."""
        try:
            df = pd.read_csv(file_path)
            self.stdout.write(self.style.HTTP_INFO(f'Starting monster import from {file_path}...'))

            for _, row in df.iterrows():
                #get_or_create does what it says on the lid, it either grabs something from the database, or creates it if it cannot find it.
                #The import_xxxxxxxx function iterate through the CSV file and dumb the row into the table, the get_or_create function will create or skip a row based on
                # wheter it can find or cannot find the data in the database.
                # Prevents duplicates withouth havin to use a entrypint.sh
                obj, created = Monster.objects.get_or_create(
                    MonsterName=row['MonsterName'],
                    defaults={
                        'MonsterImg': row['MonsterImg'],
                        'MonsterHealth': row['MonsterHealth'],
                        'MonsterDamage': row['MonsterDamage'],
                        'MonsterHPRegen': row['MonsterHPRegen'],
                        'MonsterArmour': row['MonsterArmour'],
                        'MonsterSpeed': row['MonsterSpeed'],
                        'Class': row['Class'],
                        'MonsterType': row['MonsterType'],
                    }
                )
                if created:
                    self.stdout.write(f'  + Created Monster: {obj.MonsterName}')
            
            self.stdout.write(self.style.SUCCESS('Monster import complete.\n'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}. Skipping monster import.'))

    def import_items(self, file_path):
        """Imports Item data from a given CSV file."""
        try:
            df = pd.read_csv(file_path)
            self.stdout.write(self.style.HTTP_INFO(f'Starting item import from {file_path}...'))

            for _, row in df.iterrows():
                obj, created = Item.objects.get_or_create(
                    ItemName=row['ItemName'],
                    defaults={
                        'ItemImg': row['ItemImg'],
                        'ItemDescription': row['ItemDescription'],
                        'ItemStackType': row['ItemStackType'],
                        'ItemTier': row['ItemTier'],
                        'ItemActPass': row['ItemActPass'],
                        'Cooldown': row['Cooldown'],
                    }
                )
                if created:
                    self.stdout.write(f'  + Created Item: {obj.ItemName}')
            
            self.stdout.write(self.style.SUCCESS('Item import complete.\n'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}. Skipping item import.'))
            
    def import_survivors(self, file_path):
        """Imports Survivor data from a given CSV file."""
        try:
            df = pd.read_csv(file_path)
            self.stdout.write(self.style.HTTP_INFO(f'Starting survivor import from {file_path}...'))

            for _, row in df.iterrows():
                obj, created = Survivor.objects.get_or_create(
                    SurvivorName=row['SurvivorName'],
                    defaults={
                        'SurvivorImg': row['SurvivorImg'],
                        'SurvivorHealth': row['SurvivorHealth'],
                        'SurvivorDamage': row['SurvivorDamage'],
                        'SurvivorHPRegen': row['SurvivorHPRegen'],
                        'Class': row['Class'],
                        'SurvivorArmour': row['SurvivorArmour'],
                        'SurvivorSpeed': row['SurvivorSpeed'],
                        'SurvivorMass': row['SurvivorMass'],
                        'SurvivorDescription': row['SurvivorDescription'],
                    }
                )
                if created:
                    self.stdout.write(f'  + Created Survivor: {obj.SurvivorName}')
            
            self.stdout.write(self.style.SUCCESS('Survivor import complete.\n'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}. Skipping survivor import.'))