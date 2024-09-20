from django.db import models

class MergedTable(models.Model):
    def __init__(self, table1, table2):
        self.table1 = table1
        self.table2 = table2
        self.id = f"{table1.id}{table2.id}"
        self.capacity = table1.capacity + table2.capacity

    def unmerge(self):
        self.table1.unmerge()
        self.table2.unmerge()

    def __str__(self):
        return f"Merged Table {self.id}: Capacity {self.capacity}, Composed of Tables {self.table1.id} and {self.table2.id}"