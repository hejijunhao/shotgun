from django.db import models

class Table(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='tables')
    number = models.CharField(max_length=5)  # Use CharField to allow labels like 'A', 'B', etc.
    capacity = models.IntegerField()
    mergable = models.BooleanField(default=False)
    merged_with = models.ManyToManyField('self', blank=True, symmetrical=True)

    def merge_with(self, other_table):
        if self.mergable and other_table.mergable and not self.merged_with.exists():
            # Add both tables to each other's merged_with field
            self.merged_with.add(other_table)
            other_table.merged_with.add(self)
            self.save()
            other_table.save()
            return True
        return False

    def unmerge(self):
        # Unmerge all related tables
        if self.merged_with.exists():
            for table in self.merged_with.all():
                table.merged_with.remove(self)
            self.merged_with.clear()
            self.save()
            return True
        return False

    def get_effective_capacity(self):
        total_capacity = self.capacity
        if self.merged_with.exists():
            total_capacity += sum(table.capacity for table in self.merged_with.all())
        return total_capacity

    def can_accommodate(self, party_size):
        return party_size <= self.get_effective_capacity()

    def get_merged_identifier(self):
        # Create a unique identifier for merged tables by concatenating their numbers
        if self.merged_with.exists():
            merged_tables = [self.number] + [table.number for table in self.merged_with.all()]
            return 'Table ' + ''.join(sorted(merged_tables))
        return f"Table {self.number}"

    def __str__(self):
        status = "Merged" if self.merged_with.exists() else "Available"
        return f"{self.get_merged_identifier()}: Capacity {self.get_effective_capacity()}, {status}, {'Mergable' if self.mergable else 'Not Mergable'}"

    class Meta:
        unique_together = ['restaurant', 'number']
        ordering = ['number']
