from django.db import models

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()
    mergable = models.BooleanField(default=False)
    merged_with = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='merged_tables')

    def merge_with(self, other_table):
        if self.mergable and other_table.mergable and not self.merged_with and not other_table.merged_with:
            self.merged_with = other_table
            other_table.merged_with = self
            self.save()
            other_table.save()
            return True
        return False

    def unmerge(self):
        if self.merged_with:
            other_table = self.merged_with
            self.merged_with = None
            other_table.merged_with = None
            self.save()
            other_table.save()
            return True
        return False

    def is_available(self):
        return self.merged_with is None

    def get_effective_capacity(self):
        if self.merged_with:
            return self.capacity + self.merged_with.capacity
        return self.capacity

    def can_accommodate(self, party_size):
        return party_size <= self.get_effective_capacity()

    def __str__(self):
        status = "Merged" if self.merged_with else "Available"
        return f"Table {self.id}: Capacity {self.get_effective_capacity()}, {status}, {'Mergable' if self.mergable else 'Not Mergable'}"

    class Meta:
        app_label = 'reservations'  # Replace with your app name if different